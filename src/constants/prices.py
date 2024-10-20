from src.constants.config import FREE_PLAN_REQUEST_LIMIT, STRIPE_PREMIUM_ID, STRIPE_PREMIUM_PLUS_ID

PRICES = [
    {
        "id": 1,
        "name": "Free",
        "description": "Free forever",
        "stripe_price_id": "",
        "stripe_price_mode": "",
        "highlight": 0,
        "selling_price": 0,
        "expand_months": 'month',
        "features": [
            {"count": " × Unlimited", "title": "Book reading"},
            {"count": " × Unlimited", "title": "News reading"},
            {"count": " × Unlimited", "title": "Book vocabulary viewing"},
            {"count": " × Unlimited", "title": "News vocabulary viewing"},
            {"count": " × Unlimited", "title": "Preferences saving"},
            {"count": " × Unlimited", "title": "Word Saving"},
            {"count": " × Unlimited", "title": "Sentence Saving"},
            {"count": " × Unlimited", "title": "Word translation"},
            {"count": " × Unlimited", "title": "Word Audio Playing"},

            {"count": f" × {FREE_PLAN_REQUEST_LIMIT} shared", "title": "Sentence translation"},
            {"count": f" × {FREE_PLAN_REQUEST_LIMIT} shared", "title": "Sentence Audio Playing"},

            {"count": " × 0", "title": "Vocabulary Exporting"},
            {"count": " × 0", "title": "Sentence Exporting"},
        ]
    },
    {
        "id": 2,
        "name": "Premium Plus",
        "description": "Unlimited access continuously, can be canceled at any time",
        "stripe_price_id": STRIPE_PREMIUM_PLUS_ID,
        "stripe_price_mode": "subscription",
        "highlight": 1,
        "selling_price": 19.9,
        "expand_months": 'month',
        "features": [
            {"count": " × Unlimited", "title": "Book reading"},
            {"count": " × Unlimited", "title": "News reading"},
            {"count": " × Unlimited", "title": "Book vocabulary viewing"},
            {"count": " × Unlimited", "title": "News vocabulary viewing"},
            {"count": " × Unlimited", "title": "Preferences saving"},
            {"count": " × Unlimited", "title": "Word Saving"},
            {"count": " × Unlimited", "title": "Sentence Saving"},
            {"count": " × Unlimited", "title": "Word translation"},
            {"count": " × Unlimited", "title": "Word Audio Playing"},

            {"count": " × Unlimited", "title": "Sentence translation"},
            {"count": " × Unlimited", "title": "Sentence Audio Playing"},

            {"count": " × Unlimited", "title": "Vocabulary Exporting"},
            {"count": " × Unlimited", "title": "Sentence Exporting"},

        ]
    },
    {
        "id": 3,
        "name": "Premium",
        "description": "Unlimited access in 1 month",
        "stripe_price_id": STRIPE_PREMIUM_ID,
        "strip_price_mode": "payment",
        "highlight": 0,
        "selling_price": 24.9,
        "expand_months": 'month',
        "features": [
            {"count": " × Unlimited", "title": "Book reading"},
            {"count": " × Unlimited", "title": "News reading"},
            {"count": " × Unlimited", "title": "Book vocabulary viewing"},
            {"count": " × Unlimited", "title": "News vocabulary viewing"},
            {"count": " × Unlimited", "title": "Preferences saving"},
            {"count": " × Unlimited", "title": "Word Saving"},
            {"count": " × Unlimited", "title": "Sentence Saving"},
            {"count": " × Unlimited", "title": "Word translation"},
            {"count": " × Unlimited", "title": "Word Audio Playing"},

            {"count": " × Unlimited", "title": "Sentence translation"},
            {"count": " × Unlimited", "title": "Sentence Audio Playing"},

            {"count": " × Unlimited", "title": "Vocabulary Exporting"},
            {"count": " × Unlimited", "title": "Sentence Exporting"},
        ]
    }
]

STRIPE_PRICE_MAP = {price["id"]: price for price in PRICES}