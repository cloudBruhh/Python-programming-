import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import (
    GradientBoostingClassifier,
    GradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression, LogisticRegression
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
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.utils import Bunch


def load_housing_data():
    print("Attempting to load California housing dataset...")

    try:
        raw_data: Bunch = fetch_california_housing()
        X = pd.DataFrame(raw_data.data, columns=raw_data.feature_names)
        y = pd.Series(raw_data.target, name="MedHouseVal")
        print("Dataset successfully downloaded/loaded from cache.\n")

    except Exception as e:
        print(f"\n[Notice] Could not download dataset online ({type(e).__name__}).")
        print(
            "Generating a synthetic local dataset so you can run the code offline...\n"
        )

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
        y = 2.0 + 0.4 * X["MedInc"] + np.random.normal(0, 0.5, n_samples)

    return X, y


def evaluate_regression(model, X_train, X_test, y_train, y_test, name, example):
    print(f"=== {name} (REG - {example}) ===\n")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("--- PERFORMANCE EVALUATION ---")
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    print(f"Mean Absolute Error (MAE):     ${mae * 100000:,.2f}")
    print(f"Root Mean Squared Error (RMSE): ${rmse * 100000:,.2f}")
    print(f"R² Score (Variance Explained):  {r2:.4f}\n")
    return r2


def evaluate_classification(model, X_train, X_test, y_train, y_test, name, example):
    print(f"=== {name} (CLASS - {example}) ===\n")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    print("--- PERFORMANCE EVALUATION ---")
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_pred_proba)
    conf_matrix = confusion_matrix(y_test, y_pred)
    print(f"Accuracy:                    {accuracy:.4f}")
    print(f"Precision:                   {precision:.4f}")
    print(f"Recall (Sensitivity):        {recall:.4f}")
    print(f"F1 Score:                    {f1:.4f}")
    print(f"ROC-AUC Score:               {auc:.4f}")
    print("Confusion Matrix ([[TN, FP], [FN, TP]]):")
    print(conf_matrix)
    print("\n")
    return accuracy


def run_pipeline():
    X, y = load_housing_data()

    # 1. Split regression target once
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 2. Build binary classification target (above/below median price)
    y_bin = (y > y.median()).astype(int)
    X_train_b, X_test_b, y_train_b, y_test_b = train_test_split(
        X, y_bin, test_size=0.2, random_state=42, stratify=y_bin
    )

    # 3. Scale features (required by LR, SVM, KNN, Neural Nets)
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)
    X_train_bs = scaler.fit_transform(X_train_b)
    X_test_bs = scaler.transform(X_test_b)

    print(
        "\n##################### REGRESSION (predict house price) #####################\n"
    )

    regression_results = {
        "Linear Regression": (
            LinearRegression(),
            X_train,
            X_test,
            "House price",
        ),
        "Decision Tree": (
            DecisionTreeRegressor(max_depth=5, random_state=42),
            X_train,
            X_test,
            "Churn prediction",
        ),
        "Random Forest": (
            RandomForestRegressor(n_estimators=100, random_state=42),
            X_train,
            X_test,
            "House price (ensemble)",
        ),
        "Gradient Boosting": (
            GradientBoostingRegressor(random_state=42),
            X_train,
            X_test,
            "Search ranking",
        ),
        "Neural Network (MLP)": (
            MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=1000, random_state=42),
            X_train_s,
            X_test_s,
            "Face recognition",
        ),
        "SVM (SVR)": (
            SVR(),
            X_train_s,
            X_test_s,
            "House price",
        ),
        "KNN": (
            KNeighborsRegressor(n_neighbors=5),
            X_train_s,
            X_test_s,
            "Fruit recognition",
        ),
    }

    for name, (model, X_tr, X_te, example) in regression_results.items():
        regression_results[name] = evaluate_regression(
            model, X_tr, X_te, y_train, y_test, name, example
        )

    print(
        "\n##################### CLASSIFICATION (above/below median price) #####################\n"
    )

    classification_results = {
        "Logistic Regression": (
            LogisticRegression(max_iter=1000),
            X_train_bs,
            X_test_bs,
            "Spam detection",
        ),
        "Decision Tree": (
            DecisionTreeClassifier(max_depth=5, random_state=42),
            X_train_b,
            X_test_b,
            "Churn prediction",
        ),
        "SVM (SVC)": (
            CalibratedClassifierCV(SVC(), ensemble=False),
            X_train_bs,
            X_test_bs,
            "Cat vs dog",
        ),
        "KNN": (
            KNeighborsClassifier(n_neighbors=5),
            X_train_bs,
            X_test_bs,
            "Fruit recognition",
        ),
        "Naive Bayes": (
            GaussianNB(),
            X_train_bs,
            X_test_bs,
            "Sentiment analysis",
        ),
        "Random Forest": (
            RandomForestClassifier(n_estimators=100, random_state=42),
            X_train_b,
            X_test_b,
            "Titanic survival",
        ),
        "Gradient Boosting": (
            GradientBoostingClassifier(random_state=42),
            X_train_b,
            X_test_b,
            "Search ranking",
        ),
        "Neural Network (MLP)": (
            MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=1000, random_state=42),
            X_train_bs,
            X_test_bs,
            "Face recognition",
        ),
    }

    classification_results = {
        name: evaluate_classification(
            model, X_tr, X_te, y_train_b, y_test_b, name, example
        )
        for name, (model, X_tr, X_te, example) in classification_results.items()
    }

    print("\n##################### SUMMARY #####################\n")
    print("--- REGRESSION (R², higher is better) ---")
    for name, r2 in sorted(
        regression_results.items(), key=lambda kv: kv[1], reverse=True
    ):
        print(f"  {name:<24} R² = {r2:.4f}")

    print("\n--- CLASSIFICATION (Accuracy, higher is better) ---")
    for name, acc in sorted(
        classification_results.items(), key=lambda kv: kv[1], reverse=True
    ):
        print(f"  {name:<24} Acc = {acc:.4f}")


if __name__ == "__main__":
    run_pipeline()
