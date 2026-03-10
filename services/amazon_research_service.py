from models.schemas import (
    AmazonCandidate,
    AmazonSearchOutput,
    AmazonExtractionOutput,
    ExtractedAmazonListing,
)


def search_amazon_candidates(
    product_name: str,
    key_features: list[str],
    visual_description: str,
) -> AmazonSearchOutput:
    query = f"{product_name} {' '.join(key_features[:2])}".strip()

    candidates = [
        AmazonCandidate(
            title=f"{product_name} Portable Travel Version",
            url="https://example.com/product1",
            snippet="Compact portable version for daily and travel use.",
        ),
        AmazonCandidate(
            title=f"{product_name} Lightweight Foldable Design",
            url="https://example.com/product2",
            snippet="Lightweight and easy to carry with practical use case.",
        ),
        AmazonCandidate(
            title=f"{product_name} Waterproof Compact Mat",
            url="https://example.com/product3",
            snippet="Compact product with water-resistant construction.",
        ),
    ]

    return AmazonSearchOutput(
        search_query=query,
        candidates=candidates,
    )


def extract_listing_data(
    search_output: AmazonSearchOutput,
) -> AmazonExtractionOutput:
    listings = []

    for candidate in search_output.candidates:
        listings.append(
            ExtractedAmazonListing(
                title=candidate.title,
                bullet_points=[
                    "Portable and easy to carry",
                    "Lightweight design for convenience",
                    "Suitable for travel and daily use",
                    "Compact construction for simple storage",
                ],
                description=(
                    "This product is designed for portability, convenience, "
                    "and practical everyday use."
                ),
                brand="Generic",
            )
        )

    return AmazonExtractionOutput(listings=listings)