import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ============================================================
# CONFIGURATION
# ============================================================

DATASET_FILE = "training_data.csv"
MODEL_FILE = "hostel_recommender.pkl"


# ============================================================
# LOAD DATASET
# ============================================================

print("=" * 60)
print("HOSTEL RECOMMENDATION ML MODEL TRAINING")
print("=" * 60)

print()
print("Loading dataset...")

df = pd.read_csv(DATASET_FILE)

print(
    f"Dataset shape: {df.shape}"
)

print(
    f"Total samples: {len(df)}"
)


# ============================================================
# CHECK DATASET
# ============================================================

print()
print("Checking dataset...")

print(
    f"Missing values: {df.isnull().sum().sum()}"
)

if df.isnull().sum().sum() > 0:

    print(
        "ERROR: Dataset contains missing values."
    )

    exit()


# ============================================================
# FEATURES AND TARGET
# ============================================================

FEATURE_COLUMNS = [
    "user_budget",
    "hostel_rent",
    "rent_difference",
    "budget_ratio",
    "location_score",
    "room_score",
    "facility_score",
    "availability_score",
    "available_rooms",
    "wifi_required",
    "mess_required",
    "heating_required",
    "bathroom_required",
    "hostel_has_wifi",
    "hostel_has_mess",
    "hostel_has_heating",
    "hostel_has_bathroom",
]

TARGET_COLUMN = "target_score"


X = df[FEATURE_COLUMNS]

y = df[TARGET_COLUMN]


print()
print(
    f"Input features: {len(FEATURE_COLUMNS)}"
)

print(
    f"Target: {TARGET_COLUMN}"
)


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

print()
print("Splitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


print(
    f"Training samples: {len(X_train)}"
)

print(
    f"Testing samples : {len(X_test)}"
)


# ============================================================
# CREATE RANDOM FOREST MODEL
# ============================================================

print()
print("Creating Random Forest model...")

model = RandomForestRegressor(
    n_estimators=300,
    max_depth=12,
    min_samples_split=4,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)


# ============================================================
# TRAIN MODEL
# ============================================================

print()
print("Training model...")
print("Please wait...")

model.fit(
    X_train,
    y_train
)

print(
    "Model training completed."
)


# ============================================================
# PREDICTION
# ============================================================

print()
print("Evaluating model...")

y_pred = model.predict(
    X_test
)


# ============================================================
# EVALUATION METRICS
# ============================================================

mae = mean_absolute_error(
    y_test,
    y_pred
)

mse = mean_squared_error(
    y_test,
    y_pred
)

rmse = mse ** 0.5

r2 = r2_score(
    y_test,
    y_pred
)


print()
print("=" * 60)
print("MODEL EVALUATION")
print("=" * 60)

print(
    f"MAE  : {mae:.4f}"
)

print(
    f"MSE  : {mse:.4f}"
)

print(
    f"RMSE : {rmse:.4f}"
)

print(
    f"R²   : {r2:.4f}"
)


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

print()
print("=" * 60)
print("FEATURE IMPORTANCE")
print("=" * 60)

feature_importance = pd.DataFrame({
    "feature": FEATURE_COLUMNS,
    "importance": model.feature_importances_
})

feature_importance = (
    feature_importance
    .sort_values(
        by="importance",
        ascending=False
    )
)


for _, row in feature_importance.iterrows():

    print(
        f"{row['feature']:25s}"
        f" : {row['importance']:.4f}"
    )


# ============================================================
# SAVE MODEL
# ============================================================

print()
print("Saving trained model...")

model_package = {
    "model": model,
    "features": FEATURE_COLUMNS,
    "target": TARGET_COLUMN
}

joblib.dump(
    model_package,
    MODEL_FILE
)


print(
    f"Model saved to: {MODEL_FILE}"
)


# ============================================================
# SAMPLE PREDICTIONS
# ============================================================

print()
print("=" * 60)
print("SAMPLE PREDICTIONS")
print("=" * 60)

comparison = pd.DataFrame({
    "Actual": y_test.values[:10],
    "Predicted": y_pred[:10]
})

comparison["Difference"] = (
    comparison["Actual"]
    -
    comparison["Predicted"]
)

print(
    comparison.round(2).to_string(
        index=False
    )
)


# ============================================================
# FINAL STATUS
# ============================================================

print()
print("=" * 60)
print("ML MODEL TRAINING COMPLETE")
print("=" * 60)

print(
    f"Training samples : {len(X_train)}"
)

print(
    f"Testing samples  : {len(X_test)}"
)

print(
    f"Features         : {len(FEATURE_COLUMNS)}"
)

print(
    f"R² Score         : {r2:.4f}"
)

print(
    f"RMSE             : {rmse:.4f}"
)

print(
    f"Saved model      : {MODEL_FILE}"
)

print()
print("Ready for Flask integration.")