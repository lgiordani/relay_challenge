from unittest import mock

from src.entities.earnings_statement import EarningsStatement
from src.use_cases import error_codes
from src.use_cases.calculate_earnings import (
    build_calculate_earnings_request,
    calculate_earnings_use_case,
)


@mock.patch("src.use_cases.calculate_earnings.RateCardsCalculator")
def test_calculate_earnings(mock_rcc, test_activity_log):
    statement = EarningsStatement([], 0, 0, 0, 0)
    mock_rcc().process.return_value = statement

    request = build_calculate_earnings_request("bronze", test_activity_log)

    response = calculate_earnings_use_case(request)

    assert bool(response) is True
    assert response.value == statement.asdict()
    mock_rcc.assert_called_with("bronze")
    mock_rcc().process.assert_called_with(test_activity_log)


@mock.patch("src.use_cases.calculate_earnings.RateCardsCalculator")
def test_calculate_earnings_calculator_error(mock_rcc, test_activity_log):
    mock_rcc().process.side_effect = Exception

    request = build_calculate_earnings_request("bronze", test_activity_log)

    response = calculate_earnings_use_case(request)

    assert bool(response) is False
    assert response.error_code == error_codes.UNKNOWN_ERROR
