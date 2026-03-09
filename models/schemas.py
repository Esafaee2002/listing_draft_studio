from pydantic import BaseModel, Field
from typing import List


class IntakeData(BaseModel):
    product_name: str = Field(..., min_length=1)
    key_features: List[str] = Field(..., min_length=4, max_length=4)


class ListingDraft(BaseModel):
    title: str
    bullet_points: List[str]
    description: str