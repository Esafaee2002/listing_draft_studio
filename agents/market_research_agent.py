import json

from models.schemas import (
    IntakeData,
    VisionOutput,
    AmazonSearchOutput,
    AmazonExtractionOutput,
    MarketResearchOutput,
)
from services.gemini_service import get_client
from services.json_utils import clean_json_text
from services.amazon_research_service import (
    search_amazon_candidates,
    extract_listing_data,
)


SYSTEM_PROMPT = """
You are a market research agent for e-commerce listing optimization.

You will receive:
1. Product information from the user
2. A visual description of the product
3. Candidate competitor listings
4. Extracted listing details from those competitors

Your task:
- Identify the most useful recurring keywords
- Identify common feature patterns
- Summarize listing style patterns in the market
- Identify the most relevant competitor titles

Rules:
- Focus on useful, relevant, non-spammy language
- Avoid suggesting misleading or unsupported claims
- Return valid JSON only

Required JSON format:
{
  "top_keywords": ["string", "string"],
  "common_features": ["string", "string"],
  "market_style_notes": ["string", "string"],
  "most_relevant_titles": ["string", "string"]
}
""".strip()


def run_market_research(
    intake: IntakeData,
    vision: VisionOutput,
) -> MarketResearchOutput:
    search_output: AmazonSearchOutput = search_amazon_candidates(
        product_name=intake.product_name,
        key_features=intake.key_features,
        visual_description=vision.visual_description,
    )

    extraction_output: AmazonExtractionOutput = extract_listing_data(search_output)

    client = get_client()

    competitor_text = []
    for i, listing in enumerate(extraction_output.listings, start=1):
        bullets = "\n".join(f"- {b}" for b in listing.bullet_points)
        competitor_text.append(
            f"""
Listing {i}
Title: {listing.title}
Brand: {listing.brand}
Bullet Points:
{bullets}
Description:
{listing.description}
""".strip()
        )

    prompt = f"""
User product name:
{intake.product_name}

User key features:
1. {intake.key_features[0]}
2. {intake.key_features[1]}
3. {intake.key_features[2]}
4. {intake.key_features[3]}

Vision output:
{vision.visual_description}

Observed attributes:
{", ".join(vision.observed_attributes) if vision.observed_attributes else "None"}

Search query used:
{search_output.search_query}

Candidate titles:
{chr(10).join(f"- {c.title}" for c in search_output.candidates)}

Extracted competitor listing details:
{chr(10).join(competitor_text)}
""".strip()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{SYSTEM_PROMPT}\n\n{prompt}",
    )

    raw_text = response.text.strip()
    cleaned_text = clean_json_text(raw_text)

    try:
        data = json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Market research agent did not return valid JSON.\nRaw output:\n{raw_text}"
        ) from e

    return MarketResearchOutput(**data)