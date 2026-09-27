import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils import Bunch


def run_classification_pipeline():
    print("Attempting to load California housing dataset...")

    try:
        # Fetch raw numpy arrays (works on all scikit-learn versions)
        raw_data: Bunch = fetch_california_housing()
        X = pd.DataFrame(raw_data.data, columns=raw_data.feature_names)
        y = pd.Series(raw_data.target, name="MedHouseVal")
        print("Dataset successfully downloaded/loaded from cache.")

    except Exception as e:
        print(f"\n[Notice] Could not download dataset online ({type(e).__name__}).")
        print(
            "Generating a synthetic local dataset so you can run the code offline...\n"
        )

        # Create a realistic offline dummy dataset matching the real structure
        np.random.seed(42)
        n_samples = 500
        feature_names = [
            "MedInc",
            "HouseAge",
            "AveRooms",
            "AveBedrms",
            "Population",
            "AveOccup",
            "Latitude",
            "Longitude",
        ]

        dummy_data = np.random.randn(n_samples, len(feature_names))
        X = pd.DataFrame(dummy_data, columns=feature_names)
        # Generate a target variable linearly dependent on MedInc with some noise
        y = 2.0 + 0.4 * X["MedInc"] + np.random.normal(0, 0.5, n_samples)

    # Convert the regression target into a binary classification problem:
    # 1 if the house price is above the median, 0 otherwise
    y = (y > y.median()).astype(int)

    # 2. Partition into training (80%) and testing (20%) datasets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 3. Scale features so the model converges and weights are comparable
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # 4. Initialize and train the Logistic Regression model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    print("Model training complete.\n")

    # 5. Generate predictions on the test partition
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    # 6. Extract and display model parameters (Weights)
    print("--- MODEL INTERPRETATION ---")
    print(f"Baseline Log-Odds (Intercept): {model.intercept_[0]:.4f}")
    coefficients = pd.DataFrame(
        {"Feature": X.columns, "Weight (Coefficient)": model.coef_[0]}
    )
    print(coefficients.to_string(index=False))
    print("\n")

    # 7. Quantify prediction accuracy metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_pred_proba)
    conf_matrix = confusion_matrix(y_test, y_pred)

    print("--- PERFORMANCE EVALUATION ---")
    print(f"Accuracy:                    {accuracy:.4f}")
    print(f"Precision:                   {precision:.4f}")
    print(f"Recall (Sensitivity):        {recall:.4f}")
    print(f"F1 Score:                    {f1:.4f}")
    print(f"ROC-AUC Score:               {auc:.4f}")
    print("Confusion Matrix ([[TN, FP], [FN, TP]]):")
    print(conf_matrix)


if __name__ == "__main__":
    run_classification_pipeline()
