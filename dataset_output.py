"""
Step 6: Dataset Output
Creates final dataset combining articles, features, and embeddings
"""

import os
import pandas as pd
import numpy as np


def create_final_dataset(
    articles_df: pd.DataFrame,
    embeddings: np.ndarray,
    output_path: str,
    format: str = "parquet"
) -> str:
    """
    Create final dataset combining articles DataFrame with embeddings.
    
    Args:
        articles_df: DataFrame with articles and features
        embeddings: NumPy array of embeddings (n_articles, embedding_dim)
        output_path: Path where the dataset should be saved
        format: Output format - 'parquet', 'csv', or 'jsonl'
    
    Returns:
        Path to the saved dataset file
    """
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    final_df = articles_df.copy()
    final_df['embedding'] = embeddings.tolist()
    
    try:
        if format.lower() == 'parquet':
            if not output_path.endswith('.parquet'):
                output_path = output_path + '.parquet'
            final_df.to_parquet(output_path, index=False, engine='pyarrow')
        
        elif format.lower() == 'csv':
            if not output_path.endswith('.csv'):
                output_path = output_path + '.csv'
            final_df_csv = final_df.copy()
            final_df_csv['embedding'] = final_df_csv['embedding'].apply(str)
            final_df_csv.to_csv(output_path, index=False, encoding='utf-8')
        
        elif format.lower() == 'jsonl':
            if not output_path.endswith('.jsonl'):
                output_path = output_path + '.jsonl'
            final_df.to_json(output_path, orient='records', lines=True, force_ascii=False)
        
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'parquet', 'csv', or 'jsonl'")
        
        return output_path
    
    except Exception as e:
        raise Exception(f"Error saving dataset to {output_path}: {str(e)}")

