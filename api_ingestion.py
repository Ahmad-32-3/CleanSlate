"""
Step 1: API Ingestion
Fetches news articles from NewsData.io API
"""

import requests
from typing import Dict, Optional


def fetch_latest_news(
    api_key: str,
    query: Optional[str] = None,
    language: str = "en",
    country: Optional[str] = None,
    page: Optional[int] = None,
    full_content: Optional[int] = None
) -> Dict:
    """
    Fetch latest news articles from NewsData.io API.
    
    Args:
        api_key: NewsData.io API key
        query: Optional search term filter
        language: Language code (default: 'en')
        country: Optional country code filter
        page: Page number for pagination (optional, only include if > 1)
        full_content: Request full article text. Only set to 1 for paid plans.
                     Free tier cannot use this parameter at all (set to None).
    
    Returns:
        Dictionary containing API response with articles
    """
    url = "https://newsdata.io/api/1/latest"
    params = {
        "apikey": api_key,
        "language": language
    }
    
    if full_content == 1:
        params["full_content"] = full_content
    
    if page and page > 1:
        params["page"] = page
    
    if query:
        params["q"] = query
    if country:
        params["country"] = country
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching latest news: {str(e)}")


def search_news(
    api_key: str,
    keyword: str,
    language: str = "en"
) -> Dict:
    """
    Search news articles by keyword from NewsData.io API.
    
    Args:
        api_key: NewsData.io API key
        keyword: Search keyword
        language: Language code (default: 'en')
    
    Returns:
        Dictionary containing API response with articles
    """
    url = "https://newsdata.io/api/1/search"
    params = {
        "apikey": api_key,
        "q": keyword,
        "language": language
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error searching news: {str(e)}")


def fetch_sources(api_key: str) -> Dict:
    """
    Fetch available news sources from NewsData.io API.
    
    Args:
        api_key: NewsData.io API key
    
    Returns:
        Dictionary containing API response with sources
    """
    url = "https://newsdata.io/api/1/sources"
    params = {
        "apikey": api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching sources: {str(e)}")

