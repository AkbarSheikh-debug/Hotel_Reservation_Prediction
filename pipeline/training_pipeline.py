from hotel_reservation.src.data_ingestion import DataIngestion
from hotel_reservation.src.data_preprocessing import DataProcessor
from hotel_reservation.src.model_training import ModelTraining
from hotel_reservation.utils.common_functions import read_yaml
from hotel_reservation.config.paths_config import CONFIG_PATH, TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH

def run_training_pipeline():
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
        raise RuntimeError(f"Training pipeline failed: {str(e)}")

if __name__ == "__main__":
    run_training_pipeline()