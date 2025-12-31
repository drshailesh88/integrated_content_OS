"""
Email Sender Module
Sends HTML digest emails via Gmail SMTP.
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from typing import Dict, List, Optional
import os
import re
import sys
sys.path.insert(0, '..')
from config import GMAIL_USER, GMAIL_APP_PASSWORD, DEFAULT_RECIPIENT_EMAIL


def load_template() -> str:
    """Load the email HTML template."""
    template_path = os.path.join(
        os.path.dirname(__file__), 
        '..', 
        'templates', 
        'email_template.html'
    )
    try:
        with open(template_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        # Fallback minimal template
        return """
        <!DOCTYPE html>
        <html>
        <body style="font-family: Georgia, serif; max-width: 700px; margin: 0 auto; padding: 20px;">
        <h1>Dr. Shailesh Singh's Medical Insights</h1>
        <p>{{date}}</p>
        {{b2c_articles_html}}
        {{b2b_articles_html}}
        </body>
        </html>
        """


def format_article_html(article: Dict, article_type: str) -> str:
    """
    Format a single article as HTML.
    
    Args:
        article: Article dictionary with generated_content
        article_type: 'b2c' or 'b2b'
        
    Returns:
        HTML string for the article
    """
    content = article.get('generated_content', '')
    if not content:
        return ""
    
    # Convert paragraphs
    paragraphs = content.split('\n\n')
    content_html = ''.join(f'<p>{p.strip()}</p>' for p in paragraphs if p.strip())
    
    # Build article HTML
    return f"""
    <div class="article {article_type}">
        <h3><a href="{article.get('url', '#')}">{article.get('title', 'Untitled')}</a></h3>
        <div class="meta">{article.get('journal', '')} | {article.get('pub_date', '')}</div>
        <div class="text">{content_html}</div>
    </div>
    """


def build_email_html(b2c_articles: List[Dict], b2b_articles: List[Dict]) -> str:
    """
    Build the complete email HTML from articles.
    
    Args:
        b2c_articles: List of B2C articles with generated content
        b2b_articles: List of B2B articles with generated content
        
    Returns:
        Complete HTML email string
    """
    template = load_template()
    
    # Format date
    date_str = datetime.now().strftime('%B %d, %Y')
    
    # Build article HTML blocks
    b2c_html = ''.join(format_article_html(a, 'b2c') for a in b2c_articles if a.get('generated_content'))
    b2b_html = ''.join(format_article_html(a, 'b2b') for a in b2b_articles if a.get('generated_content'))
    
    # Count articles with content
    b2c_count = sum(1 for a in b2c_articles if a.get('generated_content'))
    b2b_count = sum(1 for a in b2b_articles if a.get('generated_content'))
    
    # Replace template variables
    html = template
    html = html.replace('{{date}}', date_str)
    html = html.replace('{{b2c_count}}', str(b2c_count))
    html = html.replace('{{b2b_count}}', str(b2b_count))
    html = html.replace('{{b2c_articles_html}}', b2c_html)
    html = html.replace('{{b2b_articles_html}}', b2b_html)
    
    # Handle conditional sections (simple implementation)
    if b2c_count > 0:
        html = re.sub(r'\{\{#if b2c_articles\}\}', '', html)
        html = re.sub(r'\{\{/if\}\}', '', html)
    else:
        html = re.sub(r'\{\{#if b2c_articles\}\}.*?\{\{/if\}\}', '', html, flags=re.DOTALL)
    
    if b2b_count > 0:
        html = re.sub(r'\{\{#if b2b_articles\}\}', '', html)
        html = re.sub(r'\{\{/if\}\}', '', html)
    else:
        html = re.sub(r'\{\{#if b2b_articles\}\}.*?\{\{/if\}\}', '', html, flags=re.DOTALL)
    
    # Handle empty state
    if b2c_count == 0 and b2b_count == 0:
        html = re.sub(r'\{\{#if no_articles\}\}', '', html)
    else:
        html = re.sub(r'\{\{#if no_articles\}\}.*?\{\{/if\}\}', '', html, flags=re.DOTALL)
    
    return html


def send_email(
    html_content: str,
    subject: str,
    to_email: str = None,
    from_email: str = None
) -> bool:
    """
    Send an HTML email via Gmail SMTP.
    
    Args:
        html_content: HTML email content
        subject: Email subject line
        to_email: Recipient email (uses default if not provided)
        from_email: Sender email (uses config if not provided)
        
    Returns:
        True if sent successfully, False otherwise
    """
    if not GMAIL_APP_PASSWORD:
        print("  ⚠ GMAIL_APP_PASSWORD not set - skipping email")
        return False
    
    to_email = to_email or DEFAULT_RECIPIENT_EMAIL
    from_email = from_email or GMAIL_USER
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        
        # Attach HTML content
        msg.attach(MIMEText(html_content, 'html'))
        
        # Send via Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(from_email, to_email, msg.as_string())
        
        print(f"  ✓ Email sent to {to_email}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("  ✗ Email authentication failed - check GMAIL_APP_PASSWORD")
        return False
    except Exception as e:
        print(f"  ✗ Email error: {e}")
        return False


def send_digest_email(
    triaged_articles: Dict[str, list],
    to_email: str = None
) -> bool:
    """
    Send the full digest email.
    
    Args:
        triaged_articles: Dictionary with 'b2c', 'b2b' article lists
        to_email: Recipient email
        
    Returns:
        True if sent successfully
    """
    print(f"\n📧 Preparing email digest...")
    print("-" * 40)
    
    b2c_articles = triaged_articles.get('b2c', [])
    b2b_articles = triaged_articles.get('b2b', [])
    
    # Build HTML
    html = build_email_html(b2c_articles, b2b_articles)
    
    # Count articles
    b2c_count = sum(1 for a in b2c_articles if a.get('generated_content'))
    b2b_count = sum(1 for a in b2b_articles if a.get('generated_content'))
    
    if b2c_count == 0 and b2b_count == 0:
        print("  ○ No articles to send")
        return False
    
    # Build subject
    date_str = datetime.now().strftime('%b %d')
    subject = f"Medical Insights - {date_str} | {b2c_count} Public + {b2b_count} Clinical"
    
    # Send
    result = send_email(html, subject, to_email)
    
    print("-" * 40)
    return result


if __name__ == "__main__":
    # Test with sample data
    test_articles = {
        'b2c': [{
            'title': 'Test B2C Article',
            'journal': 'NEJM',
            'pub_date': '2024-12-18',
            'url': 'https://example.com',
            'generated_content': 'This is a test B2C article content.\n\nSecond paragraph here.'
        }],
        'b2b': [{
            'title': 'Test B2B Article',
            'journal': 'JACC',
            'pub_date': '2024-12-18',
            'url': 'https://example.com',
            'generated_content': 'This is a test B2B article for interventional cardiologists.\n\nWhat I\'m taking to the cath lab: Test insights.'
        }]
    }
    
    # Test HTML generation
    html = build_email_html(test_articles['b2c'], test_articles['b2b'])
    print(f"Generated HTML length: {len(html)} characters")
    
    # Save test HTML
    with open('test_email.html', 'w') as f:
        f.write(html)
    print("Saved test email to test_email.html")
