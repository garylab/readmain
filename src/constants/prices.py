from src.constants.config import FREE_PLAN_REQUEST_LIMIT

PRICES = [
    {
        "name": "Free",
        "market_price": 9.9,
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
        ],
        "stripe_price_id_single": "",
        "stripe_price_id_continuous": "",
        "highlight": 0
    },
    {
        "name": "Premium",
        "market_price": 29.9,
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

        ],
        "stripe_price_id_single": "price_1",
        "stripe_price_id_continuous": "price_2",
        "highlight": 1
    }
]
