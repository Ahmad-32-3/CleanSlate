"""
Step 3: Cleaning & Normalization
Comprehensive 8-step cleaning process for news articles
"""

import re
import html
import json
import os
import string
import unicodedata
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urlparse


def validate_and_enforce_schema(article: Dict, article_idx: int = 0) -> Optional[Dict]:
    """
    Step 1: Field Validation & Schema Enforcement
    
    Verify required fields exist, coerce types, fill missing values.
    
    Args:
        article: Raw article dictionary from API
        article_idx: Index for generating article_id if missing
    
    Returns:
        Validated article dictionary with enforced schema or None if invalid
    """
    try:
        article_id = article.get('article_id') or f"article_{article_idx:04d}"
        
        title = article.get('title') or article.get('headline', '')
        title = str(title).strip() if title else None
        
        description = article.get('description', '') or ''
        content = article.get('content', '') or ''
        if content and 'ONLY AVAILABLE' in content.upper():
            content = ''
        
        body_text_parts = [title or '', description, content]
        body_text = ' '.join([part for part in body_text_parts if part and part.strip()])
        
        source = article.get('source_name') or article.get('source_id', '') or ''
        source = str(source).strip()
        
        url = article.get('link') or article.get('url', '') or ''
        url = str(url).strip()
        domain = ''
        if url:
            try:
                parsed = urlparse(url)
                domain = parsed.netloc or ''
            except:
                domain = ''
        
        category = article.get('category', [])
        if not isinstance(category, list):
            category = [category] if category else []
        category = [str(c).strip() for c in category if c]
        
        pub_date = article.get('pubDate') or article.get('pub_date', '')
        pub_datetime = None
        if pub_date:
            try:
                if isinstance(pub_date, str):
                    try:
                        dt = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                    except:
                        for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d']:
                            try:
                                dt = datetime.strptime(pub_date, fmt)
                                break
                            except:
                                continue
                        else:
                            dt = None
                    if dt:
                        pub_datetime = int(dt.timestamp())
                elif isinstance(pub_date, (int, float)):
                    pub_datetime = int(pub_date)
            except:
                pub_datetime = None
        
        if not body_text or len(body_text.strip()) < 10:
            return None
        
        validated = {
            'article_id': str(article_id),
            'title': title,
            'body_text': body_text,
            'source': source,
            'domain': domain,
            'category': category,
            'pub_datetime': pub_datetime,
            'url': url
        }
        
        return validated
    except Exception as e:
        return None


def sanitize_text(text: str) -> str:
    """
    Step 2: Raw Text Sanitation (Hard Cleaning)
    
    Strip HTML, decode entities, remove URLs, normalize whitespace.
    
    Args:
        text: Raw text content
    
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    text = html.unescape(text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text, flags=re.IGNORECASE)
    text = ''.join(char for char in text if char in string.printable or char.isspace())
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'([!?.]){2,}', r'\1', text)
    
    return text.strip()


def normalize_unicode_and_case(text: str) -> str:
    """
    Step 3: Unicode + Casing Normalization
    
    Normalize unicode, convert to lowercase, normalize quotes.
    
    Args:
        text: Text to normalize
    
    Returns:
        Normalized text
    """
    if not text:
        return ""
    
    text = unicodedata.normalize('NFKC', text)
    text = text.lower()
    text = text.replace(''', "'").replace(''', "'")
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace('—', '-').replace('–', '-')
    
    return text


def normalize_sentence_boundaries(text: str) -> str:
    """
    Step 4: Sentence Boundary Normalization
    
    Ensure proper sentence structure, remove orphaned punctuation.
    
    Args:
        text: Text to normalize
    
    Returns:
        Text with normalized sentence boundaries
    """
    if not text:
        return ""
    
    text = re.sub(r'\.\s{2,}', '. ', text)
    text = re.sub(r'!\s{2,}', '! ', text)
    text = re.sub(r'\?\s{2,}', '? ', text)
    text = re.sub(r'\s+([.,!?;:])+\s+', ' ', text)
    text = re.sub(r'^\s*([.,!?;:])+\s+', '', text)
    text = re.sub(r'([.!?])([a-z])', r'\1 \2', text)
    
    return text.strip()


def normalize_numbers(text: str, enabled: bool = False) -> str:
    """
    Step 5: Optional Numeric Normalization
    
    Replace standalone numbers with <NUM> token if enabled.
    
    Args:
        text: Text to process
        enabled: Whether to normalize numbers
    
    Returns:
        Text with normalized numbers (if enabled)
    """
    if not enabled or not text:
        return text
    
    text = re.sub(r'\b\d+\b', '<NUM>', text)
    
    return text


def perform_linguistic_checks(article: Dict, min_length: int = 50, max_length: int = 100000) -> Optional[Dict]:
    """
    Step 6: Lightweight Linguistic Checks
    
    Detect language (optional), validate length, flag issues.
    
    Args:
        article: Article dictionary
        min_length: Minimum character count
        max_length: Maximum character count
    
    Returns:
        Article with linguistic metadata or None if invalid
    """
    body_text = article.get('body_text', '')
    
    if not body_text:
        return None
    
    char_count = len(body_text)
    
    if char_count < min_length:
        return None
    
    if char_count > max_length:
        article['_flags'] = article.get('_flags', []) + ['extremely_long']
    
    if char_count < 100:
        article['_flags'] = article.get('_flags', []) + ['very_short']
    
    return article


def add_derived_statistics(article: Dict) -> Dict:
    """
    Step 7: Derived Statistics
    
    Calculate and attach character_count, token_count, sentence_count.
    
    Args:
        article: Article dictionary
    
    Returns:
        Article with statistics added
    """
    body_text = article.get('body_text', '')
    
    character_count = len(body_text)
    tokens = body_text.split()
    token_count = len(tokens)
    sentences = re.split(r'[.!?]+', body_text)
    sentence_count = len([s for s in sentences if s.strip()])
    
    article['character_count'] = character_count
    article['token_count'] = token_count
    article['sentence_count'] = sentence_count
    
    return article


def process_articles(raw_articles: List[Dict], normalize_numbers_flag: bool = False, 
                     min_length: int = 50, max_length: int = 100000) -> List[Dict]:
    """
    Process and clean all articles through the 8-step cleaning process.
    
    Args:
        raw_articles: List of raw article dictionaries from API
        normalize_numbers_flag: Whether to normalize numbers
        min_length: Minimum article length
        max_length: Maximum article length
    
    Returns:
        List of cleaned and normalized article dictionaries
    """
    cleaned_articles = []
    
    for idx, article in enumerate(raw_articles):
        validated = validate_and_enforce_schema(article, idx)
        if not validated:
            continue
        
        body_text = validated.get('body_text', '')
        title = validated.get('title', '') or ''
        
        body_text = sanitize_text(body_text)
        if title:
            title = sanitize_text(title)
            validated['title'] = title
        
        validated['body_text'] = body_text
        
        body_text = normalize_unicode_and_case(body_text)
        if title:
            title = normalize_unicode_and_case(title)
            validated['title'] = title
        validated['body_text'] = body_text
        
        body_text = normalize_sentence_boundaries(body_text)
        validated['body_text'] = body_text
        
        body_text = normalize_numbers(body_text, normalize_numbers_flag)
        validated['body_text'] = body_text
        
        checked = perform_linguistic_checks(validated, min_length, max_length)
        if not checked:
            continue
        
        with_stats = add_derived_statistics(checked)
        cleaned_articles.append(with_stats)
    
    return cleaned_articles


def save_cleaned_articles(cleaned_articles: List[Dict], output_dir: str = "data/cleaned") -> str:
    """
    Step 8: Output Cleaned JSON
    
    Save cleaned articles to JSON file with timestamp.
    
    Args:
        cleaned_articles: List of cleaned article dictionaries
        output_dir: Directory to save the file
    
    Returns:
        Path to the saved file
    """
    os.makedirs(output_dir, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y%m%d")
    
    counter = 1
    while True:
        filename = f"clean_{date_str}_{counter:02d}.json"
        file_path = os.path.join(output_dir, filename)
        if not os.path.exists(file_path):
            break
        counter += 1
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(cleaned_articles, f, indent=2, ensure_ascii=False)
        return file_path
    except IOError as e:
        raise Exception(f"Error saving cleaned articles to {file_path}: {str(e)}")
