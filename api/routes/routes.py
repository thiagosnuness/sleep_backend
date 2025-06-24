from flask_openapi3 import Tag
from flask import jsonify
from datetime import datetime, timezone

from app import app
from api import db
from api.schemas.input_schema import SleepInputSchema
from api.schemas.delete_schema import DeletePredictionByIDSchema
from api.schemas.error_schema import ValidationErrorSchema
from api.model.predictor import load_model_and_scaler, predict_quality
from api.model.prediction_record import PredictionRecord

# Load model and scaler once
model, scaler = load_model_and_scaler()

# Define tag for grouping in Swagger
sleep_tag = Tag(
    name="SleepCheck",
    description="Operations related to predicting sleep disorders."
)


@app.post(
    "/predict",
    tags=[sleep_tag],
    summary="Predict Sleep Disorder",
    description=(
        "This endpoint receives input data such as age, heart rate, stress, "
        "physical activity, and sleep duration to predict the likelihood of "
        "a sleep disorder. Returns 1 for 'Disorder' and 0 for 'No Disorder'."
    ),
    responses={
        200: {
            "description": "Prediction successfully computed.",
            "content": {
                "application/json": {
                    "schema": SleepInputSchema.model_json_schema()
                }
            }
        },
        422: {
            "description": "Unprocessable Entity",
            "content": {
                "application/json": {
                    "schema": ValidationErrorSchema.model_json_schema()
                }
            },
        }
    }
)
def predict(form: SleepInputSchema):
    """
    Predicts sleep disorder based on input features.

    Parameters:
        body (SleepInput): Input payload containing age, heart rate,
        stress level, physical activity level, and sleep duration.

    Returns:
        JSON response with the prediction result:
        - 1: Sleep Disorder
        - 0: No Disorder
    """
    prediction = predict_quality(model, scaler, form)

    # Save record in SQLite database
    new_record = PredictionRecord(
        name=form.name,
        age=form.age,
        heart_rate=form.heart_rate,
        stress_level=form.stress_level,
        physical_activity_level=form.physical_activity_level,
        sleep_duration=form.sleep_duration,
        prediction_result=prediction,
        timestamp=datetime.now(timezone.utc)
    )
    db.session.add(new_record)
    db.session.commit()

    return jsonify({"prediction": prediction})


@app.get(
    "/records",
    tags=[sleep_tag],
    summary="List Prediction Records",
    description="Retrieves all prediction records stored in the database.",
    responses={
        200: {
            "description": "List of prediction records.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "name": "Alice",
                            "age": 30,
                            "heart_rate": 75,
                            "stress_level": 3,
                            "physical_activity_level": 40,
                            "sleep_duration": 7.5,
                            "prediction": 0,
                            "created_at": "2024-06-23 22:18:00"
                        }
                    ]
                }
            }
        }
    }
)
def list_records():
    """
    Returns all prediction records saved in the database.
    """
    records = PredictionRecord.query.all()
    return jsonify([record.to_dict() for record in records])


@app.delete(
    "/prediction",
    tags=[sleep_tag],
    summary="Delete prediction record",
    description="Removes a specific prediction record by ID.",
    responses={
        "200": {
            "description": "Prediction record successfully removed.",
            "content": {
                "application/json": {
                    "schema": DeletePredictionByIDSchema.model_json_schema()
                }
            },
        },
        "404": {
            "description": "Prediction not found",
            "content": {
                "application/json": {
                    "schema": ValidationErrorSchema.model_json_schema()
                }
            },
        },
        "422": {
            "description": "Unprocessable Entity",
            "content": {
                "application/json": {
                    "schema": ValidationErrorSchema.model_json_schema()
                }
            },
        },
    },
)
def delete_prediction(query: DeletePredictionByIDSchema):
    """
    Removes a specific prediction record by ID.

    Returns a success message if the record was removed.
    """
    record_id = query.id
    record = db.session.get(PredictionRecord, record_id)
    if not record:
        return (
            jsonify(
                {
                    "loc": ["id"],
                    "msg": "Prediction record not found",
                    "type_": "not_found_error",
                }
            ),
            404,
        )

    db.session.delete(record)
    db.session.commit()

    return jsonify({"message": "Prediction record removed successfully"}), 200
