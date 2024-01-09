from datetime import datetime

from src.entities.earnings_statement import EarningsStatement
from src.rate_cards.rate_cards_calculator import RateCardsCalculator, WrongTierName


def test_silver_tier_single_successful_attempt():
    activity_log = [
        {
            "route_id": "RT5QHQ6M3A937H",
            "attempt_date_time": datetime.fromisoformat(
                "2023-12-18T08:33:18.588934+00:00"
            ),
            "success": True,
        }
    ]

    rcc = RateCardsCalculator("silver")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 1,
                "rate": 0.459,
                "total": 0.459,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 0,
                "rate": 0.229,
                "total": 0,
            },
            {
                "name": "Long route bonus",
                "quantity": 0,
                "rate": 10.0,
                "total": 0,
            },
            {
                "name": "Loyalty bonus (routes)",
                "quantity": 0,
                "rate": 20.0,
                "total": 0,
            },
        ],
        line_items_subtotal=0.459,
        hours_worked=0,
        minimum_earnings=0,
        final_earnings=0.459,
    )

    assert earnings_statement == expected_statement
