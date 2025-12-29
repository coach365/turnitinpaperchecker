#!/usr/bin/env python3
"""
Auto Blog Generator for TurnitinPaperChecker
Generates SEO-optimized blog posts using Groq AI
With Unsplash/Pexels image integration and IndexNow auto-indexing
"""

import os
import json
import re
import requests
from datetime import datetime
from groq import Groq

# ===== CONFIGURATION =====
WEBSITE_URL = "https://coach365.github.io/turnitinpaperchecker/"
WEBSITE_HOST = "coach365.github.io"
EMAIL = "shivansh.assignment365@gmail.com"
WHATSAPP = "+91-8168706565"

# ===== LOAD EXISTING BLOGS =====
def load_blogs():
    """Load existing blogs from blogs-data.js"""
    try:
        with open('blogs-data.js', 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'const allBlogs = (\[.*?\]);', content, re.DOTALL)
            if match:
                return json.loads(match.group(1))
    except Exception as e:
        print(f"⚠️ Error loading blogs: {e}")
    return []

# ===== LOAD KEYWORDS =====
def load_keywords():
    """Load keyword list from keywords.json"""
    try:
        with open('keywords.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('queue', [])
    except Exception as e:
        print(f"⚠️ Error loading keywords: {e}")
    
    # Default keywords if file doesn't exist
    return [
        "how to reduce turnitin similarity score",
        "turnitin alternative India affordable",
        "plagiarism checker Rs 200 India",
        "AI content detection for students",
        "avoid plagiarism academic writing",
        "paraphrasing techniques students",
        "citation styles guide APA MLA",
        "turnitin percentage meaning",
        "check plagiarism before submission",
        "plagiarism report sample India"
    ]

# ===== GET NEXT KEYWORD =====
def get_next_keyword(blogs, keywords):
    """Get next keyword that hasn't been used"""
    used = set()
    for blog in blogs:
        title = blog.get('title', '').lower()
        for kw in keywords:
            if kw.lower() in title:
                used.add(kw)
    
    # Return first unused keyword
    for kw in keywords:
        if kw not in used:
            return kw
    
    # If all used, return first one (will create variation)
    return keywords[0] if keywords else "plagiarism checker India"

# ===== EXTRACT KEYWORDS FROM TEXT =====
def extract_keywords(text):
    """Extract meaningful keywords from text for image search"""
    # Remove common words
    stop_words = {'how', 'to', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'for', 'with', 'about', 'as', 'by', 'is', 'was', 'are', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'can'}
    
    # Extract words
    words = re.findall(r'\b[a-z]+\b', text.lower())
    
    # Filter out stop words and short words
    keywords = [w for w in words if w not in stop_words and len(w) > 3]
    
    # Return top 3 keywords
    return keywords[:3]

# ===== GET IMAGE FROM UNSPLASH =====
def get_image_from_unsplash(keyword):
    """Fetch relevant image from Unsplash API"""
    api_key = os.environ.get('UNSPLASH_ACCESS_KEY')
    if not api_key:
        print("⚠️ Unsplash API key not found")
        return None
    
    try:
        # Extract keywords for search
        search_terms = extract_keywords(keyword)
        search_query = ' '.join(search_terms + ['student', 'education', 'academic'])
        
        print(f"🔍 Searching Unsplash for: {search_query}")
        
        # Call Unsplash API
        url = "https://api.unsplash.com/search/photos"
        headers = {"Authorization": f"Client-ID {api_key}"}
        params = {
            "query": search_query,
            "per_page": 5,
            "orientation": "landscape"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('results') and len(data['results']) > 0:
                image_url = data['results'][0]['urls']['regular']
                print(f"✅ Found Unsplash image: {image_url[:60]}...")
                return image_url
            else:
                print("⚠️ No Unsplash results found")
        else:
            print(f"⚠️ Unsplash API error: {response.status_code}")
    
    except Exception as e:
        print(f"⚠️ Unsplash error: {e}")
    
    return None

# ===== GET IMAGE FROM PEXELS (FALLBACK) =====
def get_image_from_pexels(keyword):
    """Fetch relevant image from Pexels API as fallback"""
    api_key = os.environ.get('PEXELS_API_KEY')
    if not api_key:
        print("⚠️ Pexels API key not found")
        return None
    
    try:
        # Extract keywords for search
        search_terms = extract_keywords(keyword)
        search_query = ' '.join(search_terms + ['student', 'education'])
        
        print(f"🔍 Searching Pexels for: {search_query}")
        
        # Call Pexels API
        url = "https://api.pexels.com/v1/search"
        headers = {"Authorization": api_key}
        params = {
            "query": search_query,
            "per_page": 5,
            "orientation": "landscape"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('photos') and len(data['photos']) > 0:
                image_url = data['photos'][0]['src']['large']
                print(f"✅ Found Pexels image: {image_url[:60]}...")
                return image_url
            else:
                print("⚠️ No Pexels results found")
        else:
            print(f"⚠️ Pexels API error: {response.status_code}")
    
    except Exception as e:
        print(f"⚠️ Pexels error: {e}")
    
    return None

# ===== GET RELEVANT IMAGE (WITH FALLBACKS) =====
def get_relevant_image(keyword):
    """Get relevant image with fallback chain: Unsplash → Pexels → Default"""
    
    # Try Unsplash first
    image_url = get_image_from_unsplash(keyword)
    if image_url:
        return image_url
    
    # Try Pexels as fallback
    print("📸 Trying Pexels as fallback...")
    image_url = get_image_from_pexels(keyword)
    if image_url:
        return image_url
    
    # Use default image as last resort
    print("📸 Using default image")
    return "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800"

# ===== GENERATE PROMPT =====
def create_prompt(keyword, existing_titles):
    """Create detailed prompt for AI"""
    return f"""Write a comprehensive SEO blog post for TurnitinPaperChecker (plagiarism detection service in India).

SERVICE INFO:
- Plagiarism & AI detection service
- Price: Rs 200 single check, Rs 150 combined
- Delivery: 6-12 hours via WhatsApp
- Contact: {EMAIL}, {WHATSAPP}
- Website: {WEBSITE_URL}

TARGET KEYWORD: "{keyword}"

EXISTING TITLES (don't repeat):
{chr(10).join('- ' + t for t in existing_titles[-5:])}

WRITE:

1. TITLE (50-60 characters, must include keyword):
   Example: "How to Reduce Turnitin Similarity Score: 10 Proven Methods"

2. CONTENT (1500-2000 words):
   
   - Introduction (150 words)
   - 5-7 main sections with H2 headings
   - Each section 200-300 words
   - Use simple language (Grade 8-10)
   - Include examples from Indian universities (DU, JNU, IIT)
   - Mention TurnitinPaperChecker naturally 2-3 times
   
   MUST INCLUDE these 3 backlinks in content:
   - <a href="{WEBSITE_URL}">TurnitinPaperChecker</a>
   - <a href="{WEBSITE_URL}#services">plagiarism detection services</a>
   - <a href="{WEBSITE_URL}#pricing">affordable pricing at Rs 200</a>
   
   - End with: "Ready to check your document? Get started for just Rs 200 at <a href='{WEBSITE_URL}'>TurnitinPaperChecker</a>"

3. META DESCRIPTION (150-155 chars, include keyword)

FORMAT OUTPUT EXACTLY:

---TITLE---
[title here]

---CONTENT---
<h2>Introduction</h2>
<p>First paragraph...</p>
<p>Second paragraph...</p>

<h2>Section 1 Title</h2>
<p>Content...</p>

<h2>Section 2 Title</h2>
<p>Content...</p>

[continue 5-7 sections]

<h2>Conclusion</h2>
<p>Summary...</p>
<p>Ready to check your document? Get started for just Rs 200 at <a href='{WEBSITE_URL}'>TurnitinPaperChecker</a></p>

---META---
[meta description]

---END---"""

# ===== CALL GROQ AI =====
def generate_blog(keyword, existing_titles):
    """Generate blog using Groq AI"""
    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        print("❌ GROQ_API_KEY not found")
        return None
    
    client = Groq(api_key=api_key)
    prompt = create_prompt(keyword, existing_titles)
    
    print(f"🤖 Generating blog for keyword: {keyword}")
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert SEO blogger specializing in academic services."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"❌ Groq AI error: {e}")
        return None

# ===== PARSE AI RESPONSE =====
def parse_response(text):
    """Parse AI response to extract components"""
    data = {}
    
    # Extract title
    title_match = re.search(r'---TITLE---\s*(.+?)\s*---CONTENT---', text, re.DOTALL)
    if title_match:
        data['title'] = title_match.group(1).strip()
    
    # Extract content
    content_match = re.search(r'---CONTENT---\s*(.+?)\s*---META---', text, re.DOTALL)
    if content_match:
        data['content'] = content_match.group(1).strip()
    
    # Extract meta description
    meta_match = re.search(r'---META---\s*(.+?)\s*---END---', text, re.DOTALL)
    if meta_match:
        data['meta'] = meta_match.group(1).strip()
    
    return data

# ===== CREATE SLUG =====
def make_slug(title):
    """Create URL-friendly slug"""
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    return slug.strip('-')[:60]

# ===== UPDATE SITEMAP =====
def update_sitemap(blogs):
    """Update sitemap.xml with all blog URLs"""
    try:
        sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        # Homepage
        sitemap += '  <url>\n'
        sitemap += f'    <loc>{WEBSITE_URL}</loc>\n'
        sitemap += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
        sitemap += '    <changefreq>daily</changefreq>\n'
        sitemap += '    <priority>1.0</priority>\n'
        sitemap += '  </url>\n'
        
        # Blog page
        sitemap += '  <url>\n'
        sitemap += f'    <loc>{WEBSITE_URL}blog.html</loc>\n'
        sitemap += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
        sitemap += '    <changefreq>daily</changefreq>\n'
        sitemap += '    <priority>0.9</priority>\n'
        sitemap += '  </url>\n'
        
        # All blog posts
        for blog in blogs:
            try:
                # Parse date
                blog_date = datetime.strptime(blog['date'], '%B %d, %Y').strftime('%Y-%m-%d')
            except:
                blog_date = datetime.now().strftime('%Y-%m-%d')
            
            sitemap += '  <url>\n'
            sitemap += f'    <loc>{WEBSITE_URL}blog-post.html?id={blog["id"]}</loc>\n'
            sitemap += f'    <lastmod>{blog_date}</lastmod>\n'
            sitemap += '    <changefreq>monthly</changefreq>\n'
            sitemap += '    <priority>0.8</priority>\n'
            sitemap += '  </url>\n'
        
        sitemap += '</urlset>'
        
        with open('sitemap.xml', 'w', encoding='utf-8') as f:
            f.write(sitemap)
        
        print(f"✅ Sitemap updated with {len(blogs)} blog posts")
        return True
    
    except Exception as e:
        print(f"⚠️ Sitemap update error: {e}")
        return False

# ===== PING GOOGLE SITEMAP =====
def ping_google_sitemap():
    """Notify Google of sitemap update"""
    try:
        sitemap_url = f"{WEBSITE_URL}sitemap.xml"
        ping_url = f"https://www.google.com/ping?sitemap={sitemap_url}"
        
        response = requests.get(ping_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Google sitemap pinged successfully")
            return True
        else:
            print(f"⚠️ Google ping returned: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"⚠️ Google ping error: {e}")
        return False

# ===== NOTIFY INDEXNOW =====
def notify_indexnow(blog_url):
    """Notify search engines via IndexNow API"""
    api_key = os.environ.get('INDEXNOW_API_KEY')
    if not api_key:
        print("⚠️ IndexNow API key not found")
        return False
    
    try:
        payload = {
            "host": WEBSITE_HOST,
            "key": api_key,
            "keyLocation": f"{WEBSITE_URL}{api_key}.txt",
            "urlList": [blog_url]
        }
        
        print(f"📡 Notifying IndexNow for: {blog_url}")
        
        response = requests.post(
            "https://api.indexnow.org/indexnow",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ IndexNow notification sent (Google, Bing, Yandex)")
            return True
        else:
            print(f"⚠️ IndexNow returned: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"⚠️ IndexNow error: {e}")
        return False

# ===== SAVE BLOG =====
def save_blog(blog_data, keyword):
    """Save blog to blogs-data.js"""
    blogs = load_blogs()
    
    new_id = max([b.get('id', 0) for b in blogs], default=0) + 1
    
    # Get relevant image
    image_url = get_relevant_image(keyword)
    
    new_blog = {
        'id': new_id,
        'title': blog_data['title'],
        'slug': make_slug(blog_data['title']),
        'content': blog_data['content'],
        'excerpt': blog_data['content'][:200].replace('<h2>', '').replace('</h2>', '').replace('<p>', '').replace('</p>', '').strip() + '...',
        'image': image_url,
        'meta': blog_data.get('meta', ''),
        'date': datetime.now().strftime('%B %d, %Y'),
        'author': 'TurnitinPaperChecker Team',
        'readTime': max(3, len(blog_data['content'].split()) // 200)
    }
    
    blogs.append(new_blog)
    
    # Write to blogs-data.js
    js_content = f"""// Auto-generated blog data
// Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

const allBlogs = {json.dumps(blogs, indent=2, ensure_ascii=False)};
"""
    
    with open('blogs-data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"✅ Blog #{new_id} saved: {blog_data['title']}")
    
    # Update sitemap
    update_sitemap(blogs)
    
    # Ping Google
    ping_google_sitemap()
    
    # Notify IndexNow
    blog_url = f"{WEBSITE_URL}blog-post.html?id={new_id}"
    notify_indexnow(blog_url)
    
    return new_id

# ===== MAIN =====
def main():
    """Main execution function"""
    print("="*60)
    print("🚀 AUTO BLOG GENERATOR - TurnitinPaperChecker")
    print("="*60)
    
    # Load existing data
    blogs = load_blogs()
    print(f"📚 Existing blogs: {len(blogs)}")
    
    keywords = load_keywords()
    print(f"🔑 Keywords loaded: {len(keywords)}")
    
    # Get next keyword
    keyword = get_next_keyword(blogs, keywords)
    print(f"🎯 Target keyword: {keyword}")
    
    existing_titles = [b['title'] for b in blogs]
    
    # Generate blog with AI
    ai_response = generate_blog(keyword, existing_titles)
    
    if not ai_response:
        print("❌ Failed to generate blog")
        return
    
    # Parse response
    blog_data = parse_response(ai_response)
    
    if not all(k in blog_data for k in ['title', 'content']):
        print("❌ Invalid AI response - missing required fields")
        return
    
    print(f"📝 Title: {blog_data['title']}")
    print(f"📊 Content length: {len(blog_data['content'])} characters")
    
    # Save blog
    blog_id = save_blog(blog_data, keyword)
    
    print("="*60)
    print("✅ SUCCESS! Blog published")
    print(f"📌 ID: {blog_id}")
    print(f"📌 Title: {blog_data['title']}")
    print(f"📌 Keyword: {keyword}")
    print("="*60)

if __name__ == "__main__":
    main()
