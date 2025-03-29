import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

class DiseasePrediction:
    def __init__(self):
        # Load dataset once (DO NOT DROP DUPLICATES)
        file_path = "C:\\Users\\USER\\Downloads\\symtoms_df.csv"
        df = pd.read_csv(file_path)
        df.drop(columns=["Symptom_4", "Unnamed: 0"], inplace=True)

        # Fix spacing issues in symptoms
        for col in ["Symptom_1", "Symptom_2", "Symptom_3"]:
            df[col] = df[col].str.strip()

        # One-Hot Encode symptoms
        symptom_columns = ["Symptom_1", "Symptom_2", "Symptom_3"]
        target_column = "Disease"

        self.onehot_encoders = {}
        encoded_dfs = []
        for col in symptom_columns:
            ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
            encoded_values = ohe.fit_transform(df[[col]])  # Train on FULL dataset
            encoded_df = pd.DataFrame(encoded_values, columns=[f"{col}_{v}" for v in ohe.categories_[0]])
            encoded_dfs.append(encoded_df)
            self.onehot_encoders[col] = ohe  # Save encoder for later predictions

        # ✅ Combine encoded features with original dataset
        df_encoded = pd.concat([df] + encoded_dfs, axis=1).drop(columns=symptom_columns)

        # ✅ Label Encode the target (disease)
        self.le_disease = LabelEncoder()
        df_encoded[target_column] = self.le_disease.fit_transform(df_encoded[target_column])

        # ✅ Split data into features (X) and target (y)
        X = df_encoded.drop(columns=[target_column])
        y = df_encoded[target_column]

        # ✅ Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # ✅ Save feature names for input validation
        self.feature_names = list(X_train.columns)

        # ✅ Train a Random Forest Model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

    def predict_disease(self, symptom1, symptom2, symptom3):
        # Encode input symptoms
        def encode_symptom(col, value):
            if value in self.onehot_encoders[col].categories_[0]:
                return self.onehot_encoders[col].transform([[value]]).flatten()
            else:
                return np.zeros((len(self.onehot_encoders[col].categories_[0]),))  # Zero vector for unknown symptoms

        user_encoded = np.concatenate([
            encode_symptom("Symptom_1", symptom1),
            encode_symptom("Symptom_2", symptom2),
            encode_symptom("Symptom_3", symptom3)
        ]).reshape(1, -1)

        # Convert to DataFrame and ensure feature names match
        user_df = pd.DataFrame(user_encoded, columns=self.feature_names).reindex(columns=self.feature_names, fill_value=0)

        # Make prediction
        predicted_class = self.model.predict(user_df)[0]

        # Handle unknown predictions
        if predicted_class >= len(self.le_disease.classes_):
            return "Unknown Disease"

        predicted_disease = self.le_disease.inverse_transform([predicted_class])[0]

        return predicted_disease
