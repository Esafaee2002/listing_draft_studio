import json
import mimetypes
from pathlib import Path

from google.genai import types

from models.schemas import IntakeData, VisionOutput
from services.gemini_service import get_client


SYSTEM_PROMPT = """
You are a product image analyst for e-commerce listings.

Your task is to examine the provided product image and produce:
1. A clear visual description of the product
2. A list of observed attributes visible in the image

Rules:
- Only describe what is actually visible or strongly inferable from the image
- Do not invent specifications, certifications, dimensions, or materials unless clearly visible
- Be objective and concise
- Output valid JSON only

Required JSON format:
{
  "visual_description": "string",
  "observed_attributes": ["string", "string", "string"]
}
""".strip()


def clean_json_text(raw_text: str) -> str:
    """
    Remove common markdown code fences around JSON responses.
    """
    text = raw_text.strip()

    if text.startswith("```json"):
        text = text[len("```json"):].strip()
    elif text.startswith("```"):
        text = text[len("```"):].strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    return text


def analyze_image(intake: IntakeData) -> VisionOutput:
    if not intake.image_paths:
        return VisionOutput(
            visual_description="No product image was provided.",
            observed_attributes=[],
        )

    first_image = Path(intake.image_paths[0])

    if not first_image.exists():
        raise FileNotFoundError(f"Image not found: {first_image}")

    client = get_client()
    image_bytes = first_image.read_bytes()

    mime_type, _ = mimetypes.guess_type(first_image.name)
    if mime_type is None:
        mime_type = "application/octet-stream"

    prompt = f"""
Product name:
{intake.product_name}

User-provided key features:
1. {intake.key_features[0]}
2. {intake.key_features[1]}
3. {intake.key_features[2]}
4. {intake.key_features[3]}

Analyze the product image objectively.
""".strip()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            SYSTEM_PROMPT,
            prompt,
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type,
            ),
        ],
    )

    raw_text = response.text.strip()
    cleaned_text = clean_json_text(raw_text)

    try:
        data = json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Vision agent did not return valid JSON.\nRaw output:\n{raw_text}"
        ) from e

    return VisionOutput(**data)