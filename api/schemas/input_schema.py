from pydantic import BaseModel, Field, ConfigDict


class SleepInputSchema(BaseModel):
    """
    Input schema for predicting sleep disorder based on health and
    lifestyle attributes.

    Attributes:
        name (str): User's name (max length 100 characters).
        age (int): Age of the individual in years (0 to 120).
        heart_rate (int): Resting heart rate in bpm (30 to 220).
        stress_level (int): Stress level on a scale of 0 to 10.
        physical_activity_level (int): Physical activity on a scale of 0 to 100
        sleep_duration (float): Number of hours slept per night (0.0 to 24.0).
    """
    name: str = Field(
        ...,
        max_length=100,
        description="User's name"
    )
    age: int = Field(
        ge=0,
        le=120,
        description="Age in years",
    )
    heart_rate: int = Field(
        ge=30,
        le=220,
        description="Average resting heart rate (in bpm)",
    )
    stress_level: int = Field(
        ge=0,
        le=10,
        description="Stress level (scale 0 to 10)",
    )
    physical_activity_level: int = Field(
        ge=0,
        le=100,
        description="Physical activity level (scale 0 to 100)",
    )
    sleep_duration: float = Field(
        ge=0.0,
        le=24.0,
        description="Sleep duration in hours",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Alice",
                "age": 28,
                "heart_rate": 85,
                "stress_level": 9,
                "physical_activity_level": 45,
                "sleep_duration": 6.0,
            }
        }
    )
