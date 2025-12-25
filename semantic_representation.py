"""
Step 5: Semantic Representation
Generates embeddings for article text using sentence transformers
"""

import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer


def load_embedding_model(model_name: str = "sentence-transformers/all-mpnet-base-v2") -> SentenceTransformer:
    """
    Load a sentence transformer model for generating embeddings.
    
    Args:
        model_name: Name of the model to load
    
    Returns:
        Loaded SentenceTransformer model
    """
    try:
        model = SentenceTransformer(model_name)
        return model
    except Exception as e:
        raise Exception(f"Error loading embedding model {model_name}: {str(e)}")


def generate_embeddings(texts: List[str], model: SentenceTransformer) -> np.ndarray:
    """
    Generate embeddings for a list of texts.
    
    Args:
        texts: List of text strings to embed
        model: Loaded SentenceTransformer model
    
    Returns:
        NumPy array of shape (n_texts, embedding_dim) containing embeddings
    """
    try:
        embeddings = model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True,
            batch_size=32
        )
        return embeddings
    except Exception as e:
        raise Exception(f"Error generating embeddings: {str(e)}")


def process_articles_embeddings(articles: List[str], model: SentenceTransformer) -> np.ndarray:
    """
    Generate embeddings for all article texts.
    
    Args:
        articles: List of article text strings
        model: Loaded SentenceTransformer model
    
    Returns:
        NumPy array of shape (n_articles, embedding_dim) containing embeddings
    """
    return generate_embeddings(articles, model)

