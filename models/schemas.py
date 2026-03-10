from pydantic import BaseModel, Field
from typing import List


class IntakeData(BaseModel):
    product_name: str = Field(..., min_length=1)
    key_features: List[str] = Field(..., min_length=4, max_length=4)
    image_paths: List[str] = Field(default_factory=list)


class VisionOutput(BaseModel):
    visual_description: str
    observed_attributes: List[str]


class ListingDraft(BaseModel):
    title: str
    bullet_points: List[str]
    description: str


class ReviewOutput(BaseModel):
    issues_found: List[str]
    improved_title: str
    improved_bullet_points: List[str]
    improved_description: str