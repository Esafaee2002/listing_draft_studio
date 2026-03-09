from agents.intake_agent import collect_user_input
from agents.generator_agent import generate_listing


def main():
    print("Listing Draft Studio starting...\n")

    intake = collect_user_input()
    draft = generate_listing(intake)

    print("\n=== Final Listing Draft ===\n")
    print(f"TITLE:\n{draft.title}\n")

    print("BULLET POINTS:")
    for i, bullet in enumerate(draft.bullet_points, start=1):
        print(f"{i}. {bullet}")

    print(f"\nDESCRIPTION:\n{draft.description}\n")


if __name__ == "__main__":
    main()