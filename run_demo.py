from agents.intake_agent import collect_user_input
from agents.vision_agent import analyze_image
from agents.generator_agent import generate_listing
from agents.reviewer_agent import review_listing


def main():
    print("Listing Draft Studio starting...\n")

    intake = collect_user_input()
    vision = analyze_image(intake)
    draft = generate_listing(intake, vision)
    reviewed = review_listing(intake, draft)

    print("\n=== VISION OUTPUT ===\n")
    print(f"Visual description:\n{vision.visual_description}\n")

    print("Observed attributes:")
    for i, attr in enumerate(vision.observed_attributes, start=1):
        print(f"{i}. {attr}")

    print("\n=== GENERATED DRAFT ===\n")
    print(f"TITLE:\n{draft.title}\n")

    print("BULLET POINTS:")
    for i, bullet in enumerate(draft.bullet_points, start=1):
        print(f"{i}. {bullet}")

    print(f"\nDESCRIPTION:\n{draft.description}\n")

    print("\n=== REVIEW ISSUES FOUND ===\n")
    for i, issue in enumerate(reviewed.issues_found, start=1):
        print(f"{i}. {issue}")

    print("\n=== IMPROVED FINAL LISTING ===\n")
    print(f"TITLE:\n{reviewed.improved_title}\n")

    print("BULLET POINTS:")
    for i, bullet in enumerate(reviewed.improved_bullet_points, start=1):
        print(f"{i}. {bullet}")

    print(f"\nDESCRIPTION:\n{reviewed.improved_description}\n")


if __name__ == "__main__":
    main()