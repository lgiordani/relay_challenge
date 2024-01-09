from src.entities.earnings_statement import EarningsStatement
from src.rate_cards.rate_cards_calculator import RateCardsCalculator


def test_gold_tier_single_successful_attempt():
    activity_log = [
        {
            "route_id": "RT5QHQ6M3A937H",
            "attempt_date_time": "2023-12-18T08:33:18.588934+00:00",
            "success": True,
        }
    ]

    rcc = RateCardsCalculator("gold")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 1,
                "rate": 0.511,
                "total": 0.511,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 0,
                "rate": 0.126,
                "total": 0,
            },
            {
                "name": "Consistency bonus",
                "quantity": 0,
                "rate": 32.0,
                "total": 0,
            },
        ],
        line_items_subtotal=0.511,
        hours_worked=0,
        minimum_earnings=0,
        final_earnings=0.511,
    )

    assert earnings_statement == expected_statement


def test_gold_tier_multiple_successful_attempts():
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

    rcc = RateCardsCalculator("gold")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 2,
                "rate": 0.511,
                "total": 1.022,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 0,
                "rate": 0.126,
                "total": 0,
            },
            {
                "name": "Consistency bonus",
                "quantity": 0,
                "rate": 32.0,
                "total": 0,
            },
        ],
        line_items_subtotal=1.022,
        hours_worked=0.03333333,
        minimum_earnings=0.499999999,  # This is 15.0*0.03333333
        final_earnings=1.022,
    )

    assert earnings_statement == expected_statement


def test_gold_tier_single_unsuccessful_attempt():
    activity_log = [
        {
            "route_id": "AAAA",
            "attempt_date_time": "2023-12-18T08:33:18.588934+00:00",
            "success": False,
        }
    ]

    rcc = RateCardsCalculator("gold")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 0,
                "rate": 0.511,
                "total": 0,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 1,
                "rate": 0.126,
                "total": 0.126,
            },
            {
                "name": "Consistency bonus",
                "quantity": 0,
                "rate": 32.0,
                "total": 0,
            },
        ],
        line_items_subtotal=0.126,
        hours_worked=0,
        minimum_earnings=0,
        final_earnings=0.126,
    )

    assert earnings_statement == expected_statement


def test_gold_tier_multiple_unsuccessful_attempts():
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

    rcc = RateCardsCalculator("gold")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 0,
                "rate": 0.511,
                "total": 0,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 2,
                "rate": 0.126,
                "total": 0.252,
            },
            {
                "name": "Consistency bonus",
                "quantity": 0,
                "rate": 32.0,
                "total": 0,
            },
        ],
        line_items_subtotal=0.252,
        hours_worked=0.03333333,
        minimum_earnings=0.49999999,  # This is 15.0*0.03333333
        final_earnings=0.499999999,
    )

    assert earnings_statement == expected_statement


def test_gold_tier_multiple_routes():
    activity_log = [
        {
            "route_id": "AAAA",
            "attempt_date_time": "2023-12-18T08:33:18.588934+00:00",
            "success": True,
        },
        {
            "route_id": "AAAA",
            "attempt_date_time": "2023-12-18T08:35:18.588934+00:00",
            "success": False,
        },
        {
            "route_id": "BBBB",
            "attempt_date_time": "2023-12-18T08:33:18.588934+00:00",
            "success": True,
        },
        {
            "route_id": "BBBB",
            "attempt_date_time": "2023-12-18T08:35:18.588934+00:00",
            "success": False,
        },
    ]

    rcc = RateCardsCalculator("gold")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 2,
                "rate": 0.511,
                "total": 1.022,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 2,
                "rate": 0.126,
                "total": 0.252,
            },
            {
                "name": "Consistency bonus",
                "quantity": 0,
                "rate": 32.0,
                "total": 0,
            },
        ],
        line_items_subtotal=1.274,
        hours_worked=0.0666666666,
        minimum_earnings=0.999999999,  # This is 15.0*0.06666666
        final_earnings=1.274,
    )

    assert earnings_statement == expected_statement


def test_gold_tier_consistency_bonus():
    activity_log = [
        {
            "route_id": "AAAA",
            "attempt_date_time": "2023-12-18T08:00:18.588934+00:00",
            "success": True,
        },
        {
            "route_id": "BBBB",
            "attempt_date_time": "2023-12-18T08:00:18.588934+00:00",
            "success": True,
        },
    ]

    rcc = RateCardsCalculator("gold")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 2,
                "rate": 0.511,
                "total": 1.022,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 0,
                "rate": 0.126,
                "total": 0,
            },
            {
                "name": "Consistency bonus",
                "quantity": 1,
                "rate": 32.0,
                "total": 32.0,
            },
        ],
        line_items_subtotal=33.022,
        hours_worked=0,
        minimum_earnings=0,
        final_earnings=33.022,
    )

    assert earnings_statement == expected_statement
