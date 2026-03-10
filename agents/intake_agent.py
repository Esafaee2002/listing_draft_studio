from models.schemas import IntakeData


def collect_user_input() -> IntakeData:
    print("\n=== Intake Agent ===")
    product_name = input("What is the product? ").strip()

    features = []
    for i in range(1, 5):
        feature = input(f"Enter key feature {i}: ").strip()
        features.append(feature)

    image_input = input(
        "Enter image path(s), separated by commas (or leave blank): "
    ).strip()

    image_paths = []
    if image_input:
        image_paths = [p.strip() for p in image_input.split(",") if p.strip()]

    return IntakeData(
        product_name=product_name,
        key_features=features,
        image_paths=image_paths,
    )