import pickle
import pandas as pd


def load_model_and_scaler():
    """
    Loads the pre-trained sleep disorder prediction model and the scaler
    from pickle files.

    Returns:
        tuple: A tuple containing the loaded model and the scaler.
               - model: A scikit-learn SVC model trained on sleep data.
               - scaler: A fitted StandardScaler used for input normalization.
    """
    with open("machine_learning/sleep_model.pkl", "rb") as f_model, \
         open("machine_learning/sleep_scaler.pkl", "rb") as f_scaler:
        model = pickle.load(f_model)
        scaler = pickle.load(f_scaler)
    return model, scaler


def predict_quality(model, scaler, input_data):
    """
    Predicts sleep disorder status based on input features.

    Args:
        model: Trained classification model (e.g., sklearn.svm.SVC).
        scaler: Pre-fitted scaler for input normalization(e.g., StandardScaler)
        input_data: An instance of SleepInput schema containing the features:
                    - age
                    - heart_rate
                    - stress_level
                    - physical_activity_level
                    - sleep_duration

    Returns:
        int: Prediction result (0 = No Disorder, 1 = Disorder)
    """
    # Prepare input data
    features = pd.DataFrame([{
        "Age": input_data.age,
        "Heart Rate": input_data.heart_rate,
        "Stress Level": input_data.stress_level,
        "Physical Activity Level": input_data.physical_activity_level,
        "Sleep Duration": input_data.sleep_duration
    }])

    # Apply scaling and predict using the trained model
    scaled = scaler.transform(features)
    prediction = model.predict(scaled)[0]

    return int(prediction)
