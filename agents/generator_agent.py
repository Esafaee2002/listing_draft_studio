import json

from models.schemas import IntakeData, VisionOutput, MarketResearchOutput, ListingDraft
from services.gemini_service import get_client
from services.json_utils import clean_json_text


SYSTEM_PROMPT = """
You are an expert e-commerce copywriter.

Create:
1. A product title
2. Exactly 4 bullet points
3. A product description

Use:
- user-provided product information
- visual product understanding
- market research insights

Rules:
- Be clear, fluent, and marketplace-friendly
- Do not invent unsupported claims
- Avoid keyword stuffing
- Use useful market language naturally
- Return valid JSON only

Required JSON format:
{
  "title": "string",
  "bullet_points": ["string", "string", "string", "string"],
  "description": "string"
}
""".strip()


def generate_listing(
    intake: IntakeData,
    vision: VisionOutput,
    research: MarketResearchOutput,
) -> ListingDraft:
    client = get_client()

    prompt = f"""
Product name:
{intake.product_name}

Key features:
1. {intake.key_features[0]}
2. {intake.key_features[1]}
3. {intake.key_features[2]}
4. {intake.key_features[3]}

Visual description:
{vision.visual_description}

Observed attributes:
{", ".join(vision.observed_attributes) if vision.observed_attributes else "None"}

Market research keywords:
{", ".join(research.top_keywords)}

Common feature patterns:
{", ".join(research.common_features)}

Market style notes:
{", ".join(research.market_style_notes)}

Relevant competitor titles:
{chr(10).join(f"- {title}" for title in research.most_relevant_titles)}
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
        raise ValueError(f"Generator did not return valid JSON.\nRaw output:\n{raw_text}") from e

    draft = ListingDraft(**data)

    if len(draft.bullet_points) != 4:
        raise ValueError("Generator did not return exactly 4 bullet points.")

    return draft