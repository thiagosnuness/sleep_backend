from datetime import datetime, timezone
from api import db


class PredictionRecord(db.Model):
    """
    Stores a record of a user's sleep disorder prediction.
    """

    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    heart_rate = db.Column(db.Integer, nullable=False)
    stress_level = db.Column(db.Integer, nullable=False)
    physical_activity_level = db.Column(db.Integer, nullable=False)
    sleep_duration = db.Column(db.Float, nullable=False)
    prediction_result = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.now(timezone.utc), nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "heart_rate": self.heart_rate,
            "stress_level": self.stress_level,
            "physical_activity_level": self.physical_activity_level,
            "sleep_duration": self.sleep_duration,
            "prediction_result": self.prediction_result,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }
