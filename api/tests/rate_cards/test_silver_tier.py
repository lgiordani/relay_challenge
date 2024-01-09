from src.entities.earnings_statement import EarningsStatement
from src.rate_cards.rate_cards_calculator import RateCardsCalculator


def test_silver_tier_single_successful_attempt():
    activity_log = [
        {
            "route_id": "RT5QHQ6M3A937H",
            "attempt_date_time": "2023-12-18T08:33:18.588934+00:00",
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
                "rate": 0.65,
                "total": 0.65,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 0,
                "rate": 0.0,
                "total": 0,
            },
            {
                "name": "Loyalty bonus (attempts)",
                "quantity": 0,
                "rate": 19.0,
                "total": 0,
            },
            {
                "name": "Quality bonus",
                "quantity": 0,
                "rate": 25.0,
                "total": 0,
            },
        ],
        line_items_subtotal=0.65,
        hours_worked=0,
        minimum_earnings=0,
        final_earnings=0.65,
    )

    assert earnings_statement == expected_statement


def test_silver_tier_multiple_successful_attempts():
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

    rcc = RateCardsCalculator("silver")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 2,
                "rate": 0.65,
                "total": 1.3,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 0,
                "rate": 0.0,
                "total": 0,
            },
            {
                "name": "Loyalty bonus (attempts)",
                "quantity": 0,
                "rate": 19.0,
                "total": 0,
            },
            {
                "name": "Quality bonus",
                "quantity": 0,
                "rate": 25.0,
                "total": 0,
            },
        ],
        line_items_subtotal=1.3,
        hours_worked=0.03333333,
        minimum_earnings=0.449999995,  # This is 13.50*0.03333333
        final_earnings=1.3,
    )

    assert earnings_statement == expected_statement


def test_silver_tier_single_unsuccessful_attempt():
    activity_log = [
        {
            "route_id": "AAAA",
            "attempt_date_time": "2023-12-18T08:33:18.588934+00:00",
            "success": False,
        }
    ]

    rcc = RateCardsCalculator("silver")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 0,
                "rate": 0.65,
                "total": 0,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 1,
                "rate": 0.0,
                "total": 0.0,
            },
            {
                "name": "Loyalty bonus (attempts)",
                "quantity": 0,
                "rate": 19.0,
                "total": 0,
            },
            {
                "name": "Quality bonus",
                "quantity": 0,
                "rate": 25.0,
                "total": 0,
            },
        ],
        line_items_subtotal=0.0,
        hours_worked=0,
        minimum_earnings=0,
        final_earnings=0.0,
    )

    assert earnings_statement == expected_statement


def test_silver_tier_multiple_unsuccessful_attempts():
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

    rcc = RateCardsCalculator("silver")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 0,
                "rate": 0.65,
                "total": 0,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 2,
                "rate": 0.0,
                "total": 0.0,
            },
            {
                "name": "Loyalty bonus (attempts)",
                "quantity": 0,
                "rate": 19.0,
                "total": 0,
            },
            {
                "name": "Quality bonus",
                "quantity": 0,
                "rate": 25.0,
                "total": 0,
            },
        ],
        line_items_subtotal=0.0,
        hours_worked=0.03333333,
        minimum_earnings=0.449999995,  # This is 13.50*0.03333333
        final_earnings=0.449999995,
    )

    assert earnings_statement == expected_statement


def test_silver_tier_multiple_routes():
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

    rcc = RateCardsCalculator("silver")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 4,
                "rate": 0.65,
                "total": 2.6,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 0,
                "rate": 0.0,
                "total": 0.0,
            },
            {
                "name": "Loyalty bonus (attempts)",
                "quantity": 0,
                "rate": 19.0,
                "total": 0,
            },
            {
                "name": "Quality bonus",
                "quantity": 0,
                "rate": 25.0,
                "total": 0,
            },
        ],
        line_items_subtotal=2.6,
        hours_worked=0.0666666666,
        minimum_earnings=0.8999999991,  # This is 13.50*0.06666666
        final_earnings=2.6,
    )

    assert earnings_statement == expected_statement


def test_silver_tier_loyalty_bonus():
    activity_log = []
    for i in range(151):
        activity_log.append(
            {
                "route_id": f"AAAA{i:02}",
                "attempt_date_time": "2023-12-18T08:00:18.588934+00:00",
                "success": True,
            }
        )

        activity_log.append(
            {
                "route_id": f"BBBB{i:02}",
                "attempt_date_time": "2023-12-18T08:00:18.588934+00:00",
                "success": False,
            }
        )

    rcc = RateCardsCalculator("silver")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 151,
                "rate": 0.65,
                "total": 98.15,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 151,
                "rate": 0.0,
                "total": 0,
            },
            {
                "name": "Loyalty bonus (attempts)",
                "quantity": 1,
                "rate": 19.0,
                "total": 19.0,
            },
            {
                "name": "Quality bonus",
                "quantity": 0,
                "rate": 25.0,
                "total": 0,
            },
        ],
        line_items_subtotal=117.15,
        hours_worked=0,
        minimum_earnings=0,
        final_earnings=117.15,
    )

    assert earnings_statement == expected_statement


def test_silver_tier_quality_bonus():
    activity_log = []
    for i in range(40):
        activity_log.append(
            {
                "route_id": f"AAAA{i:02}",
                "attempt_date_time": "2023-12-18T08:00:18.588934+00:00",
                "success": True,
            }
        )

    activity_log.append(
        {
            "route_id": "BBBB",
            "attempt_date_time": "2023-12-18T08:00:18.588934+00:00",
            "success": False,
        }
    )

    rcc = RateCardsCalculator("silver")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 40,
                "rate": 0.65,
                "total": 26.0,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 1,
                "rate": 0.0,
                "total": 0,
            },
            {
                "name": "Loyalty bonus (attempts)",
                "quantity": 0,
                "rate": 19.0,
                "total": 0.0,
            },
            {
                "name": "Quality bonus",
                "quantity": 1,
                "rate": 25.0,
                "total": 25.0,
            },
        ],
        line_items_subtotal=51.0,
        hours_worked=0,
        minimum_earnings=0,
        final_earnings=51.0,
    )

    assert earnings_statement == expected_statement
