from pydantic import BaseModel, Field, ConfigDict


class DeletePredictionByIDSchema(BaseModel):
    """
    Schema for deleting a prediction record by ID.

    Attributes:
        id (int): Unique ID of the prediction record to delete.
    """

    id: int = Field(
        ...,
        gt=0,
        description="Unique ID of the prediction record to delete"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"message": "Item removed successfully"}
        }
    )
