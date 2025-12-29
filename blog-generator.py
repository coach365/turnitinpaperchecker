#!/usr/bin/env python3
import os
import json
import re
from datetime import datetime
from groq import Groq

# ===== CONFIGURATION =====
WEBSITE_URL = "https://coach365.github.io/turnitinpaperchecker/"
EMAIL = "shivansh.assignment365@gmail.com"
WHATSAPP = "+91-8168706565"

# ===== LOAD EXISTING BLOGS =====
def load_blogs():
    try:
        with open('blogs-data.js', 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'const allBlogs = (\[.*?\]);', content, re.DOTALL)
            if match:
                return json.loads(match.group(1))
    except:
        pass
    return []

# ===== LOAD KEYWORDS =====
def load_keywords():
    try:
        with open('keywords.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('queue', [])
    except:
        pass
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
    used = set()
    for blog in blogs:
        title = blog.get('title', '').lower()
        for kw in keywords:
            if kw.lower() in title:
                used.add(kw)
    
    for kw in keywords:
        if kw not in used:
            return kw
    
    return keywords[0] if keywords else "plagiarism checker India"

# ===== GENERATE PROMPT =====
def create_prompt(keyword, existing_titles):
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

3. IMAGE URL from Unsplash (direct .jpg link)

4. META DESCRIPTION (150-155 chars, include keyword)

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

---IMAGE---
https://images.unsplash.com/photo-xxxxx

---META---
[meta description]

---END---"""

# ===== CALL GROQ AI =====
def generate_blog(keyword, existing_titles):
    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        print("❌ GROQ_API_KEY not found")
        return None
    
    client = Groq(api_key=api_key)
    prompt = create_prompt(keyword, existing_titles)
    
    print(f"🤖 Generating blog for keyword: {keyword}")
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert SEO blogger."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=4000
    )
    
    return response.choices[0].message.content

# ===== PARSE AI RESPONSE =====
def parse_response(text):
    data = {}
    
    title_match = re.search(r'---TITLE---\s*(.+?)\s*---CONTENT---', text, re.DOTALL)
    if title_match:
        data['title'] = title_match.group(1).strip()
    
    content_match = re.search(r'---CONTENT---\s*(.+?)\s*---IMAGE---', text, re.DOTALL)
    if content_match:
        data['content'] = content_match.group(1).strip()
    
    image_match = re.search(r'---IMAGE---\s*(.+?)\s*---META---', text, re.DOTALL)
    if image_match:
        data['image'] = image_match.group(1).strip()
    
    meta_match = re.search(r'---META---\s*(.+?)\s*---END---', text, re.DOTALL)
    if meta_match:
        data['meta'] = meta_match.group(1).strip()
    
    return data

# ===== CREATE SLUG =====
def make_slug(title):
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    return slug.strip('-')[:60]

# ===== UPDATE BLOGS FILE =====
def save_blog(blog_data):
    blogs = load_blogs()
    
    new_id = max([b.get('id', 0) for b in blogs], default=0) + 1
    
    new_blog = {
        'id': new_id,
        'title': blog_data['title'],
        'slug': make_slug(blog_data['title']),
        'content': blog_data['content'],
        'excerpt': blog_data['content'][:200].replace('<h2>', '').replace('</h2>', '').replace('<p>', '').replace('</p>', '').strip() + '...',
        'image': blog_data.get('image', 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8'),
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
    return new_id

# ===== MAIN =====
def main():
    print("="*60)
    print("🚀 AUTO BLOG GENERATOR - TurnitinPaperChecker")
    print("="*60)
    
    blogs = load_blogs()
    print(f"📚 Existing blogs: {len(blogs)}")
    
    keywords = load_keywords()
    print(f"🔑 Keywords loaded: {len(keywords)}")
    
    keyword = get_next_keyword(blogs, keywords)
    print(f"🎯 Target keyword: {keyword}")
    
    existing_titles = [b['title'] for b in blogs]
    
    ai_response = generate_blog(keyword, existing_titles)
    
    if not ai_response:
        print("❌ Failed to generate blog")
        return
    
    blog_data = parse_response(ai_response)
    
    if not all(k in blog_data for k in ['title', 'content']):
        print("❌ Invalid AI response")
        return
    
    print(f"📝 Title: {blog_data['title']}")
    print(f"📊 Length: {len(blog_data['content'])} chars")
    
    blog_id = save_blog(blog_data)
    
    print("="*60)
    print("✅ SUCCESS! Blog published")
    print(f"📌 ID: {blog_id}")
    print(f"📌 Title: {blog_data['title']}")
    print("="*60)

if __name__ == "__main__":
    main()
