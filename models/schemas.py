from pydantic import BaseModel, Field
from typing import List, Optional


class IntakeData(BaseModel):
    product_name: str = Field(..., min_length=1)
    key_features: List[str] = Field(..., min_length=4, max_length=4)
    image_paths: List[str] = Field(default_factory=list)


class VisionOutput(BaseModel):
    visual_description: str
    observed_attributes: List[str]


class AmazonCandidate(BaseModel):
    title: str
    url: Optional[str] = None
    snippet: Optional[str] = None


class AmazonSearchOutput(BaseModel):
    search_query: str
    candidates: List[AmazonCandidate]


class ExtractedAmazonListing(BaseModel):
    title: str
    bullet_points: List[str]
    description: str
    brand: Optional[str] = None


class AmazonExtractionOutput(BaseModel):
    listings: List[ExtractedAmazonListing]


class MarketResearchOutput(BaseModel):
    top_keywords: List[str]
    common_features: List[str]
    market_style_notes: List[str]
    most_relevant_titles: List[str]


class ListingDraft(BaseModel):
    title: str
    bullet_points: List[str]
    description: str


class ReviewOutput(BaseModel):
    issues_found: List[str]
    improved_title: str
    improved_bullet_points: List[str]
    improved_description: str