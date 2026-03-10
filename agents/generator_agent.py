import json
from models.schemas import IntakeData, VisionOutput, ListingDraft
from services.gemini_service import get_client


SYSTEM_PROMPT = """
You are an expert e-commerce copywriter.

Your task is to create:
1. A product title no more than 200 characters
2. Exactly 4 bullet points no more than 200 characters each, highlighting the key features of the product. Each bullet point should focus on a single feature and its benefit, without repeating the product name. 
3. A HTML description no more than 2000 characters, that is informative and easy to read, and includes the product name and key features in a natural way.

Rules:
- Each bullet point should start with a strong benefit statement, followed by a concise explanation of the feature that delivers that benefit.
- Each bullet point should start with an emoji. For example, if the product is a water bottle with a built-in filter, a bullet point could be:
"💧 Stay Hydrated Anywhere: Our water bottle features a built-in filter that removes impurities
- Be clear, fluent, and amazon-friendly
- Do not invent unsupported claims
- Do not use exaggerated marketing language
- Do not include any disclaimers or legal language
- Do not include any HTML tags in the title or bullet points
- Do not include the product name in the bullet points
- Do not use marketing language like "best", "top-rated", "high-quality", etc.
- Make the copy readable and useful
- Use the provided product name and features faithfully
- Output valid JSON only

Required JSON format:
{
  "title": "string",
  "bullet_points": ["string", "string", "string", "string"],
  "description": "string"
}
""".strip()

def generate_listing(intake: IntakeData, vision: VisionOutput) -> ListingDraft:
    client = get_client()

    user_prompt = f"""
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
""".strip()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{SYSTEM_PROMPT}\n\n{user_prompt}",
    )

    raw_text = response.text.strip()

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Model did not return valid JSON.\nRaw output:\n{raw_text}") from e

    draft = ListingDraft(**data)

    if len(draft.bullet_points) != 4:
        raise ValueError("Model did not return exactly 4 bullet points.")

    return draft