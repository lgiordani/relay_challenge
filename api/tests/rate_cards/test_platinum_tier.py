from src.entities.earnings_statement import EarningsStatement
from src.rate_cards.rate_cards_calculator import RateCardsCalculator


def test_platinum_tier_single_successful_attempt():
    activity_log = [
        {
            "route_id": "AAAA",
            "attempt_date_time": "2023-12-18T08:33:18.588934+00:00",
            "success": True,
        }
    ]

    rcc = RateCardsCalculator("platinum")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 1,
                "rate": 0.667,
                "total": 0.667,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 0,
                "rate": 0.155,
                "total": 0,
            },
            {
                "name": "Long route bonus",
                "quantity": 0,
                "rate": 12.0,
                "total": 0,
            },
            {
                "name": "Loyalty bonus (attempts)",
                "quantity": 0,
                "rate": 18.0,
                "total": 0,
            },
            {
                "name": "Consistency bonus",
                "quantity": 0,
                "rate": 34.5,
                "total": 0,
            },
        ],
        line_items_subtotal=0.667,
        hours_worked=0,
        minimum_earnings=0,
        final_earnings=0.667,
    )

    assert earnings_statement == expected_statement


def test_platinum_tier_multiple_successful_attempts():
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
    ]

    rcc = RateCardsCalculator("platinum")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 1,
                "rate": 0.667,
                "total": 0.667,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 1,
                "rate": 0.155,
                "total": 0.155,
            },
            {
                "name": "Long route bonus",
                "quantity": 0,
                "rate": 12.0,
                "total": 0,
            },
            {
                "name": "Loyalty bonus (attempts)",
                "quantity": 0,
                "rate": 18.0,
                "total": 0,
            },
            {
                "name": "Consistency bonus",
                "quantity": 0,
                "rate": 34.5,
                "total": 0,
            },
        ],
        line_items_subtotal=0.822,
        hours_worked=0.03333333,
        minimum_earnings=0.5083333328249999,  # This is 15.25*0.03333333
        final_earnings=0.822,
    )

    assert earnings_statement == expected_statement


def test_platinum_tier_single_unsuccessful_attempt():
    activity_log = [
        {
            "route_id": "AAAA",
            "attempt_date_time": "2023-12-18T08:33:18.588934+00:00",
            "success": False,
        }
    ]

    rcc = RateCardsCalculator("platinum")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 0,
                "rate": 0.667,
                "total": 0,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 1,
                "rate": 0.155,
                "total": 0.155,
            },
            {
                "name": "Long route bonus",
                "quantity": 0,
                "rate": 12.0,
                "total": 0,
            },
            {
                "name": "Loyalty bonus (attempts)",
                "quantity": 0,
                "rate": 18.0,
                "total": 0,
            },
            {
                "name": "Consistency bonus",
                "quantity": 0,
                "rate": 34.5,
                "total": 0,
            },
        ],
        line_items_subtotal=0.155,
        hours_worked=0,
        minimum_earnings=0,
        final_earnings=0.155,
    )

    assert earnings_statement == expected_statement


def test_platinum_tier_multiple_unsuccessful_attempts():
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

    rcc = RateCardsCalculator("platinum")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 0,
                "rate": 0.667,
                "total": 0,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 2,
                "rate": 0.155,
                "total": 0.310,
            },
            {
                "name": "Long route bonus",
                "quantity": 0,
                "rate": 12.0,
                "total": 0,
            },
            {
                "name": "Loyalty bonus (attempts)",
                "quantity": 0,
                "rate": 18.0,
                "total": 0,
            },
            {
                "name": "Consistency bonus",
                "quantity": 0,
                "rate": 34.5,
                "total": 0,
            },
        ],
        line_items_subtotal=0.310,
        hours_worked=0.03333333,
        minimum_earnings=0.5083333328249999,  # This is 15.25*0.03333333
        final_earnings=0.5083333328249999,
    )

    assert earnings_statement == expected_statement


def test_platinum_tier_long_route_bonus():
    activity_log = []
    for i in range(16):
        activity_log.append(
            {
                "route_id": "AAAA",
                "attempt_date_time": f"2023-12-18T08:{i:02}:18.588934+00:00",
                "success": True,
            }
        )

    for i in range(15):
        activity_log.append(
            {
                "route_id": "AAAA",
                "attempt_date_time": f"2023-12-18T08:{i:02}:18.588934+00:00",
                "success": False,
            }
        )

    rcc = RateCardsCalculator("platinum")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 16,
                "rate": 0.667,
                "total": 10.672,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 15,
                "rate": 0.155,
                "total": 2.325,
            },
            {
                "name": "Long route bonus",
                "quantity": 1,
                "rate": 12.0,
                "total": 12,
            },
            {
                "name": "Loyalty bonus (attempts)",
                "quantity": 0,
                "rate": 18.0,
                "total": 0,
            },
            {
                "name": "Consistency bonus",
                "quantity": 0,
                "rate": 34.5,
                "total": 0,
            },
        ],
        line_items_subtotal=24.997,
        hours_worked=0.25,
        minimum_earnings=3.8125,  # This is 15.25*0.25
        final_earnings=24.997,
    )

    assert earnings_statement == expected_statement


def test_platinum_tier_loyalty_bonus_attempts():
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

    rcc = RateCardsCalculator("platinum")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 151,
                "rate": 0.667,
                "total": 100.717,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 151,
                "rate": 0.155,
                "total": 23.405,
            },
            {
                "name": "Long route bonus",
                "quantity": 0,
                "rate": 12.0,
                "total": 0,
            },
            {
                "name": "Loyalty bonus (attempts)",
                "quantity": 1,
                "rate": 18.0,
                "total": 18.0,
            },
            {
                "name": "Consistency bonus",
                "quantity": 0,
                "rate": 34.5,
                "total": 0,
            },
        ],
        line_items_subtotal=142.122,
        hours_worked=0,
        minimum_earnings=0,
        final_earnings=142.122,
    )

    assert earnings_statement == expected_statement


def test_platinum_tier_consistency_bonus_attempts():
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

    rcc = RateCardsCalculator("platinum")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 2,
                "rate": 0.667,
                "total": 1.334,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 0,
                "rate": 0.155,
                "total": 0,
            },
            {
                "name": "Long route bonus",
                "quantity": 0,
                "rate": 12.0,
                "total": 0,
            },
            {
                "name": "Loyalty bonus (attempts)",
                "quantity": 0,
                "rate": 18.0,
                "total": 0,
            },
            {
                "name": "Consistency bonus",
                "quantity": 1,
                "rate": 34.5,
                "total": 34.5,
            },
        ],
        line_items_subtotal=35.834,
        hours_worked=0,
        minimum_earnings=0,
        final_earnings=35.834,
    )

    assert earnings_statement == expected_statement


def test_platinum_tier_provided_example():
    activity_log = [
        {
            "route_id": "RT5QHQ6M3A937H",
            "attempt_date_time": "2023-12-18T08:33:18.588934+00:00",
            "success": True,
        },
        {
            "route_id": "RT5QHQ6M3A937H",
            "attempt_date_time": "2023-12-18T08:37:11.897203+00:00",
            "success": True,
        },
        {
            "route_id": "RT5QHQ6M3A937H",
            "attempt_date_time": "2023-12-18T08:39:10.938613+00:00",
            "success": True,
        },
        {
            "route_id": "RT5QHQ6M3A937H",
            "attempt_date_time": "2023-12-18T08:43:14.747595+00:00",
            "success": False,
        },
        {
            "route_id": "RT5QHQ6M3A937H",
            "attempt_date_time": "2023-12-18T08:45:45.375317+00:00",
            "success": True,
        },
        {
            "route_id": "RT5QHQ6M3A937H",
            "attempt_date_time": "2023-12-18T08:45:58.396736+00:00",
            "success": True,
        },
    ]

    rcc = RateCardsCalculator("platinum")

    earnings_statement = rcc.process(activity_log)

    expected_statement = EarningsStatement(
        line_items=[
            {
                "name": "Per successful attempt",
                "quantity": 5,
                "rate": 0.667,
                "total": 3.335,
            },
            {
                "name": "Per unsuccessful attempt",
                "quantity": 1,
                "rate": 0.155,
                "total": 0.155,
            },
            {"name": "Long route bonus", "quantity": 0, "rate": 12.0, "total": 0.0},
            {
                "name": "Loyalty bonus (attempts)",
                "quantity": 0,
                "rate": 18.0,
                "total": 0.0,
            },
            {"name": "Consistency bonus", "quantity": 0, "rate": 34.5, "total": 0.0},
        ],
        line_items_subtotal=3.4899999999999998,
        hours_worked=0.2110577227777778,
        minimum_earnings=3.218630272361111,
        final_earnings=3.4899999999999998,
    )

    assert earnings_statement == expected_statement
