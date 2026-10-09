import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.utils import Bunch


def run_housing_pipeline():
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

    # 2. Partition into training (80%) and testing (20%) datasets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 3. Initialize and train the Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    print("Model training complete.\n")

    # 4. Generate predictions on the test partition
    y_pred = model.predict(X_test)

    # 5. Extract and display model parameters (Weights)
    print("--- MODEL INTERPRETATION ---")
    print(f"Base Baseline Price (Intercept): {model.intercept_:.4f}")
    coefficients = pd.DataFrame(
        {"Feature": X.columns, "Weight (Coefficient)": model.coef_}
    )
    print(coefficients.to_string(index=False))
    print("\n")

    # 6. Quantify prediction accuracy metrics
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print("--- PERFORMANCE EVALUATION ---")
    print(f"Mean Absolute Error (MAE):     ${mae * 100000:,.2f}")
    print(f"Root Mean Squared Error (RMSE): ${rmse * 100000:,.2f}")
    print(f"R² Score (Variance Explained):  {r2:.4f}")


if __name__ == "__main__":
    run_housing_pipeline()
