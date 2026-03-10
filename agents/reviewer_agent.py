import json
from models.schemas import IntakeData, ListingDraft, ReviewOutput
from services.gemini_service import get_client
from services.json_utils import clean_json_text

SYSTEM_PROMPT = """
You are a senior e-commerce listing editor.

Your task is to review and improve a draft product listing.

You must:
1. Identify issues in the draft
2. Improve fluency, clarity, and natural wording
3. Remove repetition or weak phrasing
4. Avoid unsupported claims
5. Keep the copy marketplace-friendly
6. Return exactly 4 bullet points
7. Preserve the product's actual meaning and features

Do not add made-up specifications, certifications, or guarantees.

Output valid JSON only in this format:
{
  "issues_found": ["string", "string"],
  "improved_title": "string",
  "improved_bullet_points": ["string", "string", "string", "string"],
  "improved_description": "string"
}
""".strip()


def review_listing(intake: IntakeData, draft: ListingDraft) -> ReviewOutput:
    client = get_client()

    user_prompt = f"""
Original product name:
{intake.product_name}

Key features:
1. {intake.key_features[0]}
2. {intake.key_features[1]}
3. {intake.key_features[2]}
4. {intake.key_features[3]}

Draft title:
{draft.title}

Draft bullet points:
1. {draft.bullet_points[0]}
2. {draft.bullet_points[1]}
3. {draft.bullet_points[2]}
4. {draft.bullet_points[3]}

Draft description:
{draft.description}
""".strip()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{SYSTEM_PROMPT}\n\n{user_prompt}",
    )

    raw_text = response.text.strip()
    cleaned_text = clean_json_text(raw_text)

    try:
        data = json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Reviewer did not return valid JSON.\nRaw output:\n{raw_text}"
        ) from e
    reviewed = ReviewOutput(**data)

    if len(reviewed.improved_bullet_points) != 4:
        raise ValueError("Reviewer did not return exactly 4 bullet points.")

    return reviewed