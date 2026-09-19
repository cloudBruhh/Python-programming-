import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.utils import Bunch


def load_housing_data():
    print("Attempting to load California housing dataset...")

    try:
        # Fetch raw numpy arrays (works on all scikit-learn versions)
        raw_data: Bunch = fetch_california_housing()
        X = pd.DataFrame(raw_data.data, columns=raw_data.feature_names)
        y = pd.Series(raw_data.target, name="MedHouseVal")
        print("Dataset successfully downloaded/loaded from cache.\n")

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

    return X, y


def run_decision_tree_regressor(X, y):
    print("=== DECISION TREE REGRESSOR (predict price) ===\n")

    # 1. Partition into training (80%) and testing (20%) datasets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 2. Initialize and train the Decision Tree Regression model
    model = DecisionTreeRegressor(max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    print("Model training complete.\n")

    # 3. Generate predictions on the test partition
    y_pred = model.predict(X_test)

    # 4. Extract and display feature importance scores
    print("--- MODEL INTERPRETATION ---")
    print(f"Tree Depth: {model.get_depth()}, Leaves: {model.get_n_leaves()}")
    importances = pd.DataFrame(
        {"Feature": X.columns, "Importance": model.feature_importances_}
    ).sort_values("Importance", ascending=False)
    print(importances.to_string(index=False))
    print("\n")

    # 5. Quantify prediction accuracy metrics
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print("--- PERFORMANCE EVALUATION ---")
    print(f"Mean Absolute Error (MAE):     ${mae * 100000:,.2f}")
    print(f"Root Mean Squared Error (RMSE): ${rmse * 100000:,.2f}")
    print(f"R² Score (Variance Explained):  {r2:.4f}")
    print("\n")


def run_decision_tree_classifier(X, y):
    print("=== DECISION TREE CLASSIFIER (predict above/below median price) ===\n")

    # 1. Convert the regression target into a binary classification problem:
    #    1 if the house price is above the median, 0 otherwise
    y_binary = (y > y.median()).astype(int)

    # 2. Partition into training (80%) and testing (20%) datasets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_binary, test_size=0.2, random_state=42, stratify=y_binary
    )

    # 3. Initialize and train the Decision Tree Classification model
    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    print("Model training complete.\n")

    # 4. Generate predictions on the test partition
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    # 5. Extract and display feature importance scores
    print("--- MODEL INTERPRETATION ---")
    print(f"Tree Depth: {model.get_depth()}, Leaves: {model.get_n_leaves()}")
    importances = pd.DataFrame(
        {"Feature": X.columns, "Importance": model.feature_importances_}
    ).sort_values("Importance", ascending=False)
    print(importances.to_string(index=False))
    print("\n")

    # 6. Quantify prediction accuracy metrics
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


def run_pipeline():
    X, y = load_housing_data()
    run_decision_tree_regressor(X, y)
    run_decision_tree_classifier(X, y)


if __name__ == "__main__":
    run_pipeline()
