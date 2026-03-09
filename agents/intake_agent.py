from models.schemas import IntakeData


def collect_user_input() -> IntakeData:
    print("\n=== Intake Agent ===")
    product_name = input("What is the product? ").strip()

    features = []
    for i in range(1, 5):
        feature = input(f"Enter key feature {i}: ").strip()
        features.append(feature)

    return IntakeData(
        product_name=product_name,
        key_features=features,
    )