import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from hotel_reservation.src.logger import get_logger
from hotel_reservation.src.custom_exception import CustomException
from hotel_reservation.utils.common_functions import read_yaml, load_data

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)
        os.makedirs(self.processed_dir, exist_ok=True)

    def preprocess_data(self, df):
        try:
            logger.info("Starting data preprocessing")
            
            # Drop unnecessary columns
            df = df.drop(columns=['Unnamed: 0', 'Booking_ID'], errors='ignore')
            df = df.drop_duplicates()
            
            # Handle categorical columns
            cat_cols = self.config["data_processing"]["categorical_columns"]
            label_encoder = LabelEncoder()
            mappings = {}
            
            for col in cat_cols:
                if col in df.columns:
                    df[col] = label_encoder.fit_transform(df[col])
                    mappings[col] = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
            
            # Handle numerical columns
            num_cols = self.config["data_processing"]["numerical_columns"]
            skew_threshold = self.config["data_processing"]["skewness_threshold"]
            
            for col in num_cols:
                if col in df.columns and abs(df[col].skew()) > skew_threshold:
                    df[col] = np.log1p(df[col])
            
            return df
            
        except Exception as e:
            logger.error(f"Preprocessing error: {str(e)}")
            raise CustomException("Data preprocessing failed", e)

    def balance_data(self, df, is_train=True):
        try:
            if not is_train:
                return df
                
            logger.info("Balancing imbalanced data")
            X = df.drop(columns='booking_status')
            y = df["booking_status"]
            
            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X, y)
            
            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df["booking_status"] = y_resampled
            
            return balanced_df
            
        except Exception as e:
            logger.error(f"Balancing error: {str(e)}")
            raise CustomException("Data balancing failed", e)

    def select_features(self, df):
        try:
            logger.info("Selecting important features")
            
            X = df.drop(columns='booking_status')
            y = df["booking_status"]
            
            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)
            
            importance_df = pd.DataFrame({
                'feature': X.columns,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            num_features = self.config["data_processing"]["no_of_features"]
            selected_features = importance_df['feature'].head(num_features).tolist()
            
            return df[selected_features + ['booking_status']]
            
        except Exception as e:
            logger.error(f"Feature selection error: {str(e)}")
            raise CustomException("Feature selection failed", e)

    def process(self):
        try:
            logger.info("Starting data processing pipeline")
            
            # Load data
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)
            
            # Preprocess
            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)
            
            # Balance only training data
            train_df = self.balance_data(train_df, is_train=True)
            
            # Feature selection
            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]
            
            # Save processed data
            train_df.to_csv(os.path.join(self.processed_dir, "processed_train.csv"), index=False)
            test_df.to_csv(os.path.join(self.processed_dir, "processed_test.csv"), index=False)
            
            logger.info("Data processing completed successfully")
            
        except Exception as e:
            logger.error(f"Processing pipeline failed: {str(e)}")
            raise CustomException("Data processing pipeline failed", e)