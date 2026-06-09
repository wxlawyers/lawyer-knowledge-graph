#!/usr/bin/env python3
"""Convert HTML article to WeChat-safe plain text.

Usage: python3 html-to-plaintext.py input.html output.txt

Converts HTML to plain text with:
- 【】 for headings and bold text
- Empty lines for paragraph separation
- Strips all HTML tags and base64 images
- Converts HTML entities
"""
import sys
import re

def html_to_plaintext(html: str) -> str:
    text = html
    # Remove head, style, script
    text = re.sub(r'<head>.*?</head>', '', text, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    # Remove comments and images (including base64)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'<img[^>]*>', '', text)
    # Convert headings to 【】
    text = re.sub(r'<h[12][^>]*>(.*?)</h[12]>', r'\n【\1】\n', text)
    # Convert bold to 【】
    text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'【\1】', text)
    # Remove all remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Convert HTML entities
    entities = {'&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&#x27;': "'", '&nbsp;': ' '}
    for k, v in entities.items():
        text = text.replace(k, v)
    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} input.html output.txt")
        sys.exit(1)
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        html = f.read()
    plaintext = html_to_plaintext(html)
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        f.write(plaintext)
    print(f"✅ Converted {len(html)} chars HTML → {len(plaintext)} chars plaintext")
    print(f"   Output: {sys.argv[2]}")
