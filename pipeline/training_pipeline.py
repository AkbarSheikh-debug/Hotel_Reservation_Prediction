import sys
import os
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTraining
from utils.common_functions import read_yaml
from config.paths_config import (
    CONFIG_PATH,
    TRAIN_FILE_PATH,
    TEST_FILE_PATH,
    PROCESSED_DIR,
    PROCESSED_TRAIN_DATA_PATH,
    PROCESSED_TEST_DATA_PATH,
    MODEL_OUTPUT_PATH
)

def main():
    try:
        # 1. Data Ingestion
        data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
        data_ingestion.run()

        # 2. Data Processing
        processor = DataProcessor(
            train_path=TRAIN_FILE_PATH,
            test_path=TEST_FILE_PATH,
            processed_dir=PROCESSED_DIR,
            config_path=CONFIG_PATH
        )
        processor.process()

        # 3. Model Training
        trainer = ModelTraining(
            train_path=PROCESSED_TRAIN_DATA_PATH,
            test_path=PROCESSED_TEST_DATA_PATH,
            model_output_path=MODEL_OUTPUT_PATH
        )
        trainer.run()
        
    except Exception as e:
        print(f"Training pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()