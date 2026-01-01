#!/usr/bin/env python3
"""
ENHANCED Auto Blog Generator for TurnitinPaperChecker
Generates UNIQUE, RANDOMIZED, SEO-optimized blog posts using Groq AI
With 5 different templates, varied structures, and creative content
"""

import os
import json
import re
import requests
import random
from datetime import datetime
from groq import Groq

# ===== CONFIGURATION =====
WEBSITE_URL = "https://www.turnitinpaperchecker.com/"
WEBSITE_HOST = "www.turnitinpaperchecker.com"
EMAIL = "shivansh.assignment365@gmail.com"
WHATSAPP = "+91-8168706565"

# ===== BLOG TEMPLATES =====
TEMPLATES = [
    {
        "name": "How-To Guide",
        "title_format": "How to {action}: {subtitle}",
        "sections": [
            "Quick Overview",
            "Why This Matters",
            "What You'll Need",
            "Step-by-Step Process",
            "Common Mistakes to Avoid",
            "Pro Tips from Experts",
            "Real-World Examples",
            "Conclusion and Next Steps"
        ]
    },
    {
        "name": "Listicle",
        "title_format": "{number} {adjective} Ways to {achieve_goal}",
        "sections": [
            "Introduction",
            "Method #{n}: {title}",  # Repeated dynamically
            "Which Approach Works Best?",
            "Implementation Timeline",
            "Final Recommendations"
        ]
    },
    {
        "name": "Problem-Solution",
        "title_format": "{problem}? Here's the Complete Solution",
        "sections": [
            "Understanding the Problem",
            "Why This Happens in Indian Universities",
            "The Real Impact on Students",
            "The Comprehensive Solution",
            "Step-by-Step Implementation",
            "Success Stories from DU, JNU, IIT",
            "Key Takeaways"
        ]
    },
    {
        "name": "Comparison Guide",
        "title_format": "{option_a} vs {option_b}: Complete 2025 Guide",
        "sections": [
            "Overview of Both Options",
            "Feature-by-Feature Comparison",
            "Pros and Cons Analysis",
            "Price and Value Comparison",
            "Best Use Cases for Each",
            "Expert Recommendations",
            "Final Verdict"
        ]
    },
    {
        "name": "Ultimate Guide",
        "title_format": "The Ultimate Guide to {topic} in 2025",
        "sections": [
            "What is {topic}?",
            "Historical Background",
            "Current Landscape in India",
            "Latest Statistics and Trends",
            "Expert Insights",
            "Future Predictions",
            "Essential Resources",
            "Conclusion"
        ]
    }
]

# Randomization elements
ADJECTIVES = ["Proven", "Effective", "Essential", "Powerful", "Smart", "Quick", "Simple", "Advanced"]
NUMBERS = ["5", "7", "10", "12", "15"]
UNIVERSITIES = ["Delhi University", "JNU", "IIT Delhi", "IIT Bombay", "Mumbai University", "Pune University"]

# ===== LOAD FUNCTIONS =====
def load_blogs():
    """Load existing blogs"""
    try:
        with open('blogs-data.js', 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'const allBlogs = (\[.*?\]);', content, re.DOTALL)
            if match:
                return json.loads(match.group(1))
    except Exception as e:
        print(f"⚠️ Error loading blogs: {e}")
    return []

def load_keywords():
    """Load keywords"""
    try:
        with open('keywords.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('queue', [])
    except:
        return [
            "how to reduce turnitin similarity score",
            "turnitin alternative India",
            "plagiarism checker Rs 200",
            "AI content detection students"
        ]

def get_next_keyword(blogs, keywords):
    """Get unused keyword"""
    used = set()
    for blog in blogs:
        title = blog.get('title', '').lower()
        for kw in keywords:
            if kw.lower() in title:
                used.add(kw)
    
    for kw in keywords:
        if kw not in used:
            return kw
    
    return random.choice(keywords)

# ===== IMAGE FUNCTIONS =====
def get_image_from_unsplash(keyword):
    """Fetch from Unsplash"""
    api_key = os.environ.get('UNSPLASH_ACCESS_KEY')
    if not api_key:
        return None
    
    try:
        search_terms = ' '.join(keyword.split()[:3] + ['student', 'education'])
        print(f"🔍 Searching Unsplash: {search_terms}")
        
        response = requests.get(
            "https://api.unsplash.com/search/photos",
            headers={"Authorization": f"Client-ID {api_key}"},
            params={"query": search_terms, "per_page": 5, "orientation": "landscape"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                return data['results'][0]['urls']['regular']
    except Exception as e:
        print(f"⚠️ Unsplash error: {e}")
    
    return None

def get_image_from_pexels(keyword):
    """Fetch from Pexels"""
    api_key = os.environ.get('PEXELS_API_KEY')
    if not api_key:
        return None
    
    try:
        search_terms = ' '.join(keyword.split()[:3] + ['student'])
        print(f"🔍 Searching Pexels: {search_terms}")
        
        response = requests.get(
            "https://api.pexels.com/v1/search",
            headers={"Authorization": api_key},
            params={"query": search_terms, "per_page": 5, "orientation": "landscape"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('photos'):
                return data['photos'][0]['src']['large']
    except Exception as e:
        print(f"⚠️ Pexels error: {e}")
    
    return None

def get_relevant_image(keyword):
    """Get image with fallback"""
    image = get_image_from_unsplash(keyword)
    if image:
        return image
    
    print("📸 Trying Pexels...")
    image = get_image_from_pexels(keyword)
    if image:
        return image
    
    print("📸 Using default")
    return "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800"

# ===== RANDOMIZED PROMPT GENERATION =====
def create_randomized_prompt(keyword, existing_titles):
    """Create completely randomized, unique prompt"""
    
    # Select random template
    template = random.choice(TEMPLATES)
    
    # Generate random backlink positions
    total_sections = len(template['sections'])
    backlink_positions = random.sample(range(2, total_sections - 1), min(3, total_sections - 3))
    
    # Create unique structure instructions
    structure_variation = random.choice([
        "Use short paragraphs (2-3 sentences each)",
        "Include bullet points in 2-3 sections",
        "Add numbered lists where appropriate",
        "Mix paragraphs with lists for variety"
    ])
    
    # Random university mentions
    unis = random.sample(UNIVERSITIES, 2)
    
    prompt = f"""Write a comprehensive, UNIQUE blog post for TurnitinPaperChecker.

CRITICAL: This must be COMPLETELY DIFFERENT from any previous posts. Use creative, unpredictable structure and content.

SERVICE INFO:
- Plagiarism & AI detection service in India
- Price: Rs 200 single, Rs 300 combined
- Delivery: 6-12 hours via WhatsApp
- Contact: {EMAIL}, {WHATSAPP}
- Website: {WEBSITE_URL}

TARGET KEYWORD: "{keyword}"

TEMPLATE: {template['name']}

EXISTING TITLES (NEVER repeat these patterns):
{chr(10).join('- ' + t for t in existing_titles[-10:])}

WRITE A COMPLETELY UNIQUE POST:

1. TITLE (50-60 characters with keyword):
   Format: {template.get('title_format', 'Creative title with keyword')}
   
2. CONTENT (1500-2000 words):

{chr(10).join(f'   <h2>{section}</h2>' for section in template['sections'][:8])}

CRITICAL REQUIREMENTS:
- {structure_variation}
- Mention {unis[0]} and {unis[1]} with SPECIFIC examples
- Include 2-3 statistics with fake but realistic numbers
- Add personal student story/example in one section
- Vary sentence length (mix short and long)
- Use transition words naturally
- NO generic phrases like "In today's digital age"

BACKLINK PLACEMENT (must include ALL 3 naturally):
- Section {backlink_positions[0]}: Link to <a href="{WEBSITE_URL}">TurnitinPaperChecker</a>
- Section {backlink_positions[1]}: Link to <a href="{WEBSITE_URL}#services">plagiarism detection services</a>
- Section {backlink_positions[2]}: Link to <a href="{WEBSITE_URL}#pricing">affordable pricing at Rs 200</a>

WRITING STYLE:
- Conversational yet professional
- Use "you" to address reader
- Include rhetorical questions
- Add specific, actionable advice
- NO clichés or overused phrases

CONCLUSION:
End with: "Ready to check your document? Get started for just Rs 200 at <a href='{WEBSITE_URL}'>TurnitinPaperChecker</a>"

3. META DESCRIPTION (150-155 chars with keyword)

FORMAT OUTPUT EXACTLY:

---TITLE---
[unique title here]

---CONTENT---
<h2>Section 1</h2>
<p>Content...</p>

[continue all sections]

---META---
[meta description]

---END---"""

    return prompt

# ===== GROQ AI GENERATION =====
def generate_blog(keyword, existing_titles):
    """Generate with randomized prompt"""
    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        print("❌ GROQ_API_KEY not found")
        return None
    
    client = Groq(api_key=api_key)
    prompt = create_randomized_prompt(keyword, existing_titles)
    
    print(f"🤖 Generating UNIQUE blog for: {keyword}")
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert SEO blogger who creates UNIQUE, engaging content. Never use templates - every post must be completely different in structure and style."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,  # Higher for more creativity
            max_tokens=5000
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"❌ Groq error: {e}")
        return None

# ===== PARSING =====
def parse_response(text):
    """Parse AI response"""
    data = {}
    
    title_match = re.search(r'---TITLE---\s*(.+?)\s*---CONTENT---', text, re.DOTALL)
    if title_match:
        data['title'] = title_match.group(1).strip()
    
    content_match = re.search(r'---CONTENT---\s*(.+?)\s*---META---', text, re.DOTALL)
    if content_match:
        data['content'] = content_match.group(1).strip()
    
    meta_match = re.search(r'---META---\s*(.+?)\s*---END---', text, re.DOTALL)
    if meta_match:
        data['meta'] = meta_match.group(1).strip()
    
    return data

def make_slug(title):
    """Create URL slug"""
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    return slug.strip('-')[:60]

# ===== SITEMAP & INDEXING =====
def update_sitemap(blogs):
    """Update sitemap.xml"""
    try:
        sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        sitemap += '  <url>\n'
        sitemap += f'    <loc>{WEBSITE_URL}</loc>\n'
        sitemap += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
        sitemap += '    <changefreq>daily</changefreq>\n'
        sitemap += '    <priority>1.0</priority>\n'
        sitemap += '  </url>\n'
        
        sitemap += '  <url>\n'
        sitemap += f'    <loc>{WEBSITE_URL}blog.html</loc>\n'
        sitemap += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
        sitemap += '    <changefreq>daily</changefreq>\n'
        sitemap += '    <priority>0.9</priority>\n'
        sitemap += '  </url>\n'
        
        for blog in blogs:
            try:
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
        
        print(f"✅ Sitemap updated: {len(blogs)} posts")
        return True
    except Exception as e:
        print(f"⚠️ Sitemap error: {e}")
        return False

def ping_google_sitemap():
    """Ping Google"""
    try:
        response = requests.get(
            f"https://www.google.com/ping?sitemap={WEBSITE_URL}sitemap.xml",
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Google pinged")
            return True
    except Exception as e:
        print(f"⚠️ Google ping error: {e}")
    return False

def notify_indexnow(blog_url):
    """Notify IndexNow"""
    api_key = os.environ.get('INDEXNOW_API_KEY')
    if not api_key:
        return False
    
    try:
        payload = {
            "host": WEBSITE_HOST,
            "key": api_key,
            "keyLocation": f"{WEBSITE_URL}{api_key}.txt",
            "urlList": [blog_url]
        }
        
        print(f"📡 IndexNow: {blog_url}")
        
        response = requests.post(
            "https://api.indexnow.org/indexnow",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ IndexNow sent")
            return True
    except Exception as e:
        print(f"⚠️ IndexNow error: {e}")
    return False

# ===== SAVE BLOG =====
def save_blog(blog_data, keyword):
    """Save blog"""
    blogs = load_blogs()
    new_id = max([b.get('id', 0) for b in blogs], default=0) + 1
    
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
    
    js_content = f"""// Auto-generated blog data
// Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

const allBlogs = {json.dumps(blogs, indent=2, ensure_ascii=False)};
"""
    
    with open('blogs-data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"✅ Blog #{new_id} saved: {blog_data['title']}")
    
    update_sitemap(blogs)
    ping_google_sitemap()
    
    blog_url = f"{WEBSITE_URL}blog-post.html?id={new_id}"
    notify_indexnow(blog_url)
    
    return new_id

# ===== MAIN =====
def main():
    """Main execution"""
    print("="*60)
    print("🚀 ENHANCED RANDOMIZED BLOG GENERATOR")
    print("="*60)
    
    blogs = load_blogs()
    print(f"📚 Existing: {len(blogs)} blogs")
    
    keywords = load_keywords()
    print(f"🔑 Keywords: {len(keywords)}")
    
    keyword = get_next_keyword(blogs, keywords)
    print(f"🎯 Target: {keyword}")
    
    existing_titles = [b['title'] for b in blogs]
    
    ai_response = generate_blog(keyword, existing_titles)
    
    if not ai_response:
        print("❌ Generation failed")
        return
    
    blog_data = parse_response(ai_response)
    
    if not all(k in blog_data for k in ['title', 'content']):
        print("❌ Invalid response")
        return
    
    print(f"📝 Title: {blog_data['title']}")
    print(f"📊 Length: {len(blog_data['content'])} chars")
    
    blog_id = save_blog(blog_data, keyword)
    
    print("="*60)
    print("✅ SUCCESS!")
    print(f"📌 ID: {blog_id}")
    print(f"📌 Title: {blog_data['title']}")
    print("="*60)

if __name__ == "__main__":
    main()
