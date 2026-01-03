import requests
import json
from datetime import datetime
import os

# ===== CONFIGURATION =====
BREVO_API_KEY = 'xsmtpsib-c52b1a5897d4fb061380796be4d038b8a805669a60f495eaa7a730cbe70fe992-WtaOMsBPAtQPCnwn'  # You'll get this from Brevo dashboard
FROM_EMAIL = 'shivansh.assignment365@gmail.com'
FROM_NAME = 'TurnitinPaperChecker'
SUBSCRIBERS_FILE = 'newsletter-subscribers.json'
BLOGS_FILE = 'blogs-data.js'
SENT_BLOGS_FILE = 'sent-blogs.json'

# ===== LOAD SUBSCRIBERS =====
def load_subscribers():
    try:
        with open(SUBSCRIBERS_FILE, 'r') as f:
            data = json.load(f)
            return data.get('subscribers', [])
    except:
        return []

# ===== LOAD LATEST BLOG =====
def load_latest_blog():
    try:
        with open(BLOGS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract the allBlogs array
            start = content.find('const allBlogs = [')
            end = content.find('];', start) + 2
            blogs_str = content[start:end]
            # Remove the const declaration
            blogs_str = blogs_str.replace('const allBlogs = ', '')
            # Parse JSON
            blogs = json.loads(blogs_str)
            return blogs[0] if blogs else None  # Return most recent blog
    except Exception as e:
        print(f"Error loading blogs: {e}")
        return None

# ===== CHECK IF BLOG WAS SENT =====
def check_if_sent(blog_id):
    try:
        with open(SENT_BLOGS_FILE, 'r') as f:
            sent = json.load(f)
            return blog_id in sent
    except:
        return False

# ===== MARK BLOG AS SENT =====
def mark_as_sent(blog_id):
    try:
        with open(SENT_BLOGS_FILE, 'r') as f:
            sent = json.load(f)
    except:
        sent = []
    
    sent.append(blog_id)
    
    with open(SENT_BLOGS_FILE, 'w') as f:
        json.dump(sent, f)

# ===== SEND EMAIL VIA BREVO =====
def send_blog_email(blog, subscribers):
    if not subscribers:
        print("No subscribers found.")
        return
    
    # Create HTML email
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #0a5d8c 0%, #0a9cfc 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: white; padding: 30px; border: 1px solid #ddd; }}
            .footer {{ background: #f8f9fa; padding: 20px; text-align: center; border-radius: 0 0 10px 10px; }}
            .btn {{ background: #0a5d8c; color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; display: inline-block; margin: 20px 0; }}
            img {{ max-width: 100%; border-radius: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📝 New Blog Post from TurnitinPaperChecker!</h1>
            </div>
            <div class="content">
                <h2>{blog['title']}</h2>
                <p><strong>Published:</strong> {blog['date']} | <strong>Read Time:</strong> {blog['readTime']} minutes</p>
                <img src="{blog['image']}" alt="{blog['title']}">
                <p>{blog['excerpt']}</p>
                <a href="https://www.turnitinpaperchecker.com/blog-post.html?id={blog['id']}" class="btn">Read Full Article →</a>
            </div>
            <div class="footer">
                <p>You're receiving this because you subscribed to TurnitinPaperChecker updates.</p>
                <p><small>TurnitinPaperChecker | Professional Plagiarism & AI Detection</small></p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Prepare recipients
    to_emails = [{"email": sub} for sub in subscribers]
    
    # Send via Brevo API
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "sender": {
            "name": FROM_NAME,
            "email": FROM_EMAIL
        },
        "to": to_emails,
        "subject": f"📚 New Post: {blog['title']}",
        "htmlContent": html_content
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            print(f"✅ Email sent successfully to {len(subscribers)} subscribers!")
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

# ===== MAIN FUNCTION =====
def main():
    print("🚀 Starting blog email sender...")
    
    # Load latest blog
    latest_blog = load_latest_blog()
    if not latest_blog:
        print("❌ No blogs found in blogs-data.js")
        return
    
    print(f"📝 Latest blog: {latest_blog['title']}")
    
    # Check if already sent
    if check_if_sent(latest_blog['id']):
        print(f"✅ Blog {latest_blog['id']} already sent. Skipping.")
        return
    
    # Load subscribers
    subscribers = load_subscribers()
    if not subscribers:
        print("❌ No subscribers found in newsletter-subscribers.json")
        return
    
    print(f"👥 Found {len(subscribers)} subscribers")
    
    # Send email
    if send_blog_email(latest_blog, subscribers):
        mark_as_sent(latest_blog['id'])
        print(f"✅ Successfully sent blog {latest_blog['id']} to {len(subscribers)} subscribers!")
    else:
        print("❌ Failed to send emails")

if __name__ == '__main__':
    main()
