"""
Step 4: Structured Feature Extraction
Extracts structured features from cleaned articles
"""

import re
from datetime import datetime
from typing import List, Dict
from urllib.parse import urlparse
import pandas as pd


def extract_features(article: Dict) -> Dict:
    """
    Extract structured features from a cleaned article.
    
    Args:
        article: Cleaned article dictionary
    
    Returns:
        Dictionary with extracted features
    """
    cleaned_text = article.get('body_text', article.get('cleaned_text', ''))
    
    tokens = cleaned_text.split()
    token_count = len(tokens)
    
    sentences = re.split(r'[.!?]+', cleaned_text)
    sentence_count = len([s for s in sentences if s.strip()])
    
    pub_datetime = article.get('pub_datetime')
    if pub_datetime is None:
        pub_date = article.get('pub_date')
        if pub_date:
            try:
                if isinstance(pub_date, str):
                    try:
                        pub_datetime = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                    except:
                        for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d']:
                            try:
                                pub_datetime = datetime.strptime(pub_date, fmt)
                                break
                            except:
                                continue
                elif isinstance(pub_date, datetime):
                    pub_datetime = pub_date
            except:
                pub_datetime = None
    elif isinstance(pub_datetime, (int, float)):
        pub_datetime = datetime.fromtimestamp(pub_datetime)
    
    url = article.get('url', '')
    domain = ''
    if url:
        try:
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path.split('/')[0] if parsed.path else ''
        except:
            domain = ''
    
    source = article.get('source', '')
    
    category = article.get('category', [])
    if isinstance(category, list):
        category_tag = category[0] if category else ''
    else:
        category_tag = str(category) if category else ''
    
    features = {
        'token_count': token_count,
        'sentence_count': sentence_count,
        'pub_datetime': pub_datetime,
        'source_category': source,
        'domain': domain,
        'category_tag': category_tag
    }
    
    return features


def create_features_dataframe(cleaned_articles: List[Dict]) -> pd.DataFrame:
    """
    Create a pandas DataFrame with articles and their extracted features.
    
    Args:
        cleaned_articles: List of cleaned article dictionaries
    
    Returns:
        Pandas DataFrame with articles and features
    """
    rows = []
    
    for idx, article in enumerate(cleaned_articles):
        features = extract_features(article)
        
        article_id = article.get('article_id', f"article_{idx + 1:04d}")
        body_text = article.get('body_text', article.get('cleaned_text', ''))
        
        row = {
            'article_id': article_id,
            'title': article.get('title', ''),
            'description': article.get('description', ''),
            'cleaned_text': body_text,
            'source': article.get('source', ''),
            'url': article.get('url', ''),
            'pub_date': article.get('pub_date', ''),
            'category': article.get('category', []),
            'token_count': features['token_count'],
            'sentence_count': features['sentence_count'],
            'pub_datetime': features['pub_datetime'],
            'domain': features['domain'],
            'category_tag': features['category_tag']
        }
        
        if 'character_count' in article:
            row['character_count'] = article['character_count']
        if 'token_count' in article:
            row['token_count'] = article['token_count']
        if 'sentence_count' in article:
            row['sentence_count'] = article['sentence_count']
        rows.append(row)
    
    df = pd.DataFrame(rows)
    return df

