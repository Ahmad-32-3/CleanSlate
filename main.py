"""
Main Orchestrator Script
Coordinates all pipeline steps sequentially
"""

import logging
import os
from datetime import datetime
import config
import api_ingestion
import raw_storage
import cleaning
import feature_extraction
import semantic_representation
import dataset_output


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    """
    Main pipeline orchestrator function.
    Executes all steps sequentially.
    """
    logger.info("=" * 60)
    logger.info("Starting News Data Pipeline")
    logger.info("=" * 60)
    
    try:
        logger.info("\n[Step 1] Fetching news from API...")
        try:
            raw_data = api_ingestion.fetch_latest_news(
                api_key=config.API_KEY,
                language=config.DEFAULT_LANGUAGE
            )
            logger.info(f"Successfully fetched {len(raw_data.get('results', []))} articles")
        except Exception as e:
            logger.error(f"Error in Step 1: {str(e)}")
            raise
        
        logger.info("\n[Step 2] Saving raw JSON response...")
        try:
            raw_file_path = raw_storage.save_raw_response(
                data=raw_data,
                output_dir=config.RAW_DATA_DIR
            )
            logger.info(f"Raw data saved to: {raw_file_path}")
        except Exception as e:
            logger.error(f"Error in Step 2: {str(e)}")
            raise
        
        logger.info("\n[Step 3] Cleaning and normalizing articles...")
        try:
            raw_articles = raw_data.get('results', [])
            cleaned_articles = cleaning.process_articles(
                raw_articles,
                normalize_numbers_flag=config.NORMALIZE_NUMBERS,
                min_length=config.MIN_ARTICLE_LENGTH,
                max_length=config.MAX_ARTICLE_LENGTH
            )
            logger.info(f"Cleaned {len(cleaned_articles)} articles (removed {len(raw_articles) - len(cleaned_articles)} invalid/duplicate articles)")
            
            cleaned_file_path = cleaning.save_cleaned_articles(
                cleaned_articles,
                output_dir=config.CLEANED_DATA_DIR
            )
            logger.info(f"Cleaned articles saved to: {cleaned_file_path}")
        except Exception as e:
            logger.error(f"Error in Step 3: {str(e)}")
            raise
        
        if not cleaned_articles:
            logger.warning("No cleaned articles to process. Exiting pipeline.")
            return
        
        logger.info("\n[Step 4] Extracting structured features...")
        try:
            articles_df = feature_extraction.create_features_dataframe(cleaned_articles)
            logger.info(f"Created DataFrame with {len(articles_df)} articles and {len(articles_df.columns)} columns")
        except Exception as e:
            logger.error(f"Error in Step 4: {str(e)}")
            raise
        
        logger.info("\n[Step 5] Generating embeddings...")
        try:
            model = semantic_representation.load_embedding_model(config.EMBEDDING_MODEL)
            logger.info(f"Loaded embedding model: {config.EMBEDDING_MODEL}")
            
            article_texts = articles_df['cleaned_text'].tolist()
            embeddings = semantic_representation.process_articles_embeddings(article_texts, model)
            logger.info(f"Generated embeddings with shape: {embeddings.shape}")
        except Exception as e:
            logger.error(f"Error in Step 5: {str(e)}")
            raise
        
        logger.info("\n[Step 6] Creating final dataset...")
        try:
            date_str = datetime.now().strftime("%Y%m%d")
            
            counter = 1
            while True:
                output_filename = f"data_{date_str}_{counter:02d}"
                output_path = os.path.join(config.OUTPUT_DATA_DIR, output_filename)
                if not any(os.path.exists(f"{output_path}.{ext}") for ext in ['parquet', 'csv', 'jsonl']):
                    break
                counter += 1
            
            final_path = dataset_output.create_final_dataset(
                articles_df=articles_df,
                embeddings=embeddings,
                output_path=output_path,
                format=config.DEFAULT_OUTPUT_FORMAT
            )
            logger.info(f"Final dataset saved to: {final_path}")
        except Exception as e:
            logger.error(f"Error in Step 6: {str(e)}")
            raise
        
        logger.info("\n" + "=" * 60)
        logger.info("Pipeline completed successfully!")
        logger.info(f"Processed {len(cleaned_articles)} articles")
        logger.info(f"Final dataset: {final_path}")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"\nPipeline failed with error: {str(e)}")
        raise


if __name__ == "__main__":
    main()

