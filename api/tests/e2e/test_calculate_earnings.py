import json
from http import HTTPStatus

import pytest

from tests.e2e.request import request

pytestmark = pytest.mark.e2e

provided_activity_log_json = """
[
    {
        "route_id": "RT5QHQ6M3A937H",
        "attempt_date_time": "2023-12-18T08:33:18.588934+00:00",
        "success": true
    },
    {
        "route_id": "RT5QHQ6M3A937H",
        "attempt_date_time": "2023-12-18T08:37:11.897203+00:00",
        "success": true
    },
    {
        "route_id": "RT5QHQ6M3A937H",
        "attempt_date_time": "2023-12-18T08:39:10.938613+00:00",
        "success": true
    },
    {
        "route_id": "RT5QHQ6M3A937H",
        "attempt_date_time": "2023-12-18T08:43:14.747595+00:00",
        "success": false
    },
    {
        "route_id": "RT5QHQ6M3A937H",
        "attempt_date_time": "2023-12-18T08:45:45.375317+00:00",
        "success": true
    },
    {
        "route_id": "RT5QHQ6M3A937H",
        "attempt_date_time": "2023-12-18T08:45:58.396736+00:00",
        "success": true
    }
]
"""

provided_earnings_json = """
{
    "line_items": [
        {
            "name": "Per successful attempt",
            "quantity": 5,
            "rate": 0.667,
            "total": 3.335
        },
        {
            "name": "Per unsuccessful attempt",
            "quantity": 1,
            "rate": 0.155,
            "total": 0.155
        },
        {
            "name": "Long route bonus",
            "quantity": 0,
            "rate": 12.0,
            "total": 0.0
        },
        {
            "name": "Loyalty bonus (attempts)",
            "quantity": 0,
            "rate": 18.0,
            "total": 0.0
        },
        {
            "name": "Consistency bonus",
            "quantity": 0,
            "rate": 34.5,
            "total": 0.0
        }
    ],
    "line_items_subtotal": 3.4899999999999998,
    "hours_worked": 0.2110577227777778,
    "minimum_earnings": 3.218630272361111,
    "final_earnings": 3.4899999999999998
}
"""


def test_e2e_calculate_earnings():
    response = request(
        "POST", "/earnings/platinum", json=json.loads(provided_activity_log_json)
    )
    assert response["status_code"] == HTTPStatus.CREATED
    assert response["json"] == json.loads(provided_earnings_json)
