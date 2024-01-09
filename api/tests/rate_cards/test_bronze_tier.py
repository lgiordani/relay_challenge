from src.entities.earnings_statement import EarningsStatement
from src.rate_cards.rate_cards_calculator import RateCardsCalculator


def test_bronze_tier_single_successful_attempt():
    activity_log = [
        {
            "route_id": "AAAA",
            "attempt_date_time": "2023-12-18T08:33:18.588934+00:00",
            "success": True,
        }
    ]

    rcc = RateCardsCalculator("bronze")

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


def test_bronze_tier_multiple_successful_attempts():
    activity_log = [
        {
            "route_id": "AAAA",
            "attempt_date_time": "2023-12-18T08:33:18.588934+00:00",
            "success": True,
        },
        {
            "route_id": "AAAA",
            "attempt_date_time": "2023-12-18T08:35:18.588934+00:00",
            "success": True,
        },
    ]

    rcc = RateCardsCalculator("bronze")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 2,
                "rate": 0.459,
                "total": 0.918,
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
        line_items_subtotal=0.918,
        hours_worked=0.03333333,
        minimum_earnings=0.483333285,  # This is 14.50*0.03333333
        final_earnings=0.918,
    )

    assert earnings_statement == expected_statement


def test_bronze_tier_single_unsuccessful_attempt():
    activity_log = [
        {
            "route_id": "AAAA",
            "attempt_date_time": "2023-12-18T08:33:18.588934+00:00",
            "success": False,
        }
    ]

    rcc = RateCardsCalculator("bronze")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 0,
                "rate": 0.459,
                "total": 0,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 1,
                "rate": 0.229,
                "total": 0.229,
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
        line_items_subtotal=0.229,
        hours_worked=0,
        minimum_earnings=0,
        final_earnings=0.229,
    )

    assert earnings_statement == expected_statement


def test_bronze_tier_multiple_unsuccessful_attempts():
    activity_log = [
        {
            "route_id": "AAAA",
            "attempt_date_time": "2023-12-18T08:33:18.588934+00:00",
            "success": False,
        },
        {
            "route_id": "AAAA",
            "attempt_date_time": "2023-12-18T08:35:18.588934+00:00",
            "success": False,
        },
    ]

    rcc = RateCardsCalculator("bronze")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 0,
                "rate": 0.459,
                "total": 0,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 2,
                "rate": 0.229,
                "total": 0.458,
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
        line_items_subtotal=0.458,
        hours_worked=0.03333333,
        minimum_earnings=0.483333285,  # This is 14.50*0.03333333
        final_earnings=0.483333285,
    )

    assert earnings_statement == expected_statement


def test_bronze_tier_multiple_routes():
    activity_log = [
        {
            "route_id": "AAAA",
            "attempt_date_time": "2023-12-18T08:33:18.588934+00:00",
            "success": True,
        },
        {
            "route_id": "AAAA",
            "attempt_date_time": "2023-12-18T08:35:18.588934+00:00",
            "success": True,
        },
        {
            "route_id": "BBBB",
            "attempt_date_time": "2023-12-18T08:33:18.588934+00:00",
            "success": True,
        },
        {
            "route_id": "BBBB",
            "attempt_date_time": "2023-12-18T08:35:18.588934+00:00",
            "success": True,
        },
    ]

    rcc = RateCardsCalculator("bronze")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 4,
                "rate": 0.459,
                "total": 1.836,
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
        line_items_subtotal=1.836,
        hours_worked=0.0666666666,
        minimum_earnings=0.9666666656999999,  # This is 14.50*0.06666666
        final_earnings=1.836,
    )

    assert earnings_statement == expected_statement


def test_bronze_tier_long_route_bonus():
    activity_log = []
    for i in range(31):
        activity_log.append(
            {
                "route_id": "AAAA",
                "attempt_date_time": f"2023-12-18T08:{i:02}:18.588934+00:00",
                "success": True,
            }
        )

    rcc = RateCardsCalculator("bronze")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 31,
                "rate": 0.459,
                "total": 14.229,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 0,
                "rate": 0.229,
                "total": 0,
            },
            {
                "name": "Long route bonus",
                "quantity": 1,
                "rate": 10.0,
                "total": 10.0,
            },
            {
                "name": "Loyalty bonus (routes)",
                "quantity": 0,
                "rate": 20.0,
                "total": 0,
            },
        ],
        line_items_subtotal=24.229,
        hours_worked=0.5,
        minimum_earnings=7.25,  # This is 14.50*0.5
        final_earnings=24.229,
    )

    assert earnings_statement == expected_statement


def test_bronze_tier_loyalty_bonus():
    activity_log = []
    for i in range(11):
        activity_log.append(
            {
                "route_id": f"AAAA{i:02}",
                "attempt_date_time": "2023-12-18T08:00:18.588934+00:00",
                "success": True,
            }
        )

    rcc = RateCardsCalculator("bronze")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 11,
                "rate": 0.459,
                "total": 5.049,
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
                "quantity": 1,
                "rate": 20.0,
                "total": 20.0,
            },
        ],
        line_items_subtotal=25.049,
        hours_worked=0,
        minimum_earnings=0,  # This is 14.50*0
        final_earnings=25.049,
    )

    assert earnings_statement == expected_statement
