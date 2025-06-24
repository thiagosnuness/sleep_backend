import sys
import os
import pytest
import pandas as pd
from sklearn.metrics import accuracy_score

# Add project root to sys.path to allow import of app and models
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))

from app import app
from api import db
from api.model.prediction_record import PredictionRecord
from api.model.predictor import load_model_and_scaler

# To run: pytest -v tests/test_api.py


@pytest.fixture
def client():
    """
    Configures the test client for the Flask application.
    Enables test mode and yields a test client for making requests.
    """
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.init_app(app)
        db.create_all()
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_input_data():
    """
    Provides sample input data for sleep prediction.

    Returns:
        dict: A dictionary containing realistic user input values.
    """
    return {
        "name": "Test User",
        "age": 30,
        "heart_rate": 70,
        "stress_level": 3,
        "physical_activity_level": 4,
        "sleep_duration": 7.0
    }


def test_predict_sleep_quality(client, sample_input_data):
    """
    Tests the /predict endpoint using sample input data.
    Verifies:
        - Status code is 200.
        - The prediction is present and valid (0 or 1).
        - The prediction is stored in the SQLite database.

    Note:
        The database must already exist. Run the app once before testing.
    """
    # Send the prediction request
    response = client.post(
        "/predict",
        data=sample_input_data,
        content_type="application/x-www-form-urlencoded"
    )

    assert response.status_code == 200

    result = response.get_json()
    assert "prediction" in result
    assert isinstance(result["prediction"], int)
    assert result["prediction"] in [0, 1]

    with app.app_context():
        # Ensure the record was saved to the database
        record = PredictionRecord.query.filter_by(
            name=sample_input_data["name"]).first()
        assert record is not None
        assert record.prediction_result == result["prediction"]


def test_model_accuracy_threshold():
    """
    Ensure that the sleep prediction model meets the minimum accuracy threshold

    This test loads a small labeled test dataset and calculates the accuracy.
    The test fails if the accuracy is below the defined threshold.
    """
    # Load test data (X and y) from CSV
    df = pd.read_csv("machine_learning/test_data.csv")
    X = df.drop(columns=["label"])
    y_true = df["label"]

    model, scaler = load_model_and_scaler()
    X_scaled = scaler.transform(X)
    y_pred = model.predict(X_scaled)

    accuracy = accuracy_score(y_true, y_pred)
    print(f"\nModel accuracy: {accuracy:.2f}")

    # Define the minimum acceptable performance
    threshold = 0.80
    assert accuracy >= threshold, (
        f"Model accuracy {accuracy:.2f} is below threshold {threshold}"
    )
