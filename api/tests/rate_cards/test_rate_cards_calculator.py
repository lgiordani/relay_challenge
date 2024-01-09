import pytest

from src.rate_cards.rate_cards_calculator import RateCardsCalculator, WrongTierName


def test_unknown_tier():
    with pytest.raises(WrongTierName):
        RateCardsCalculator("does-not-exist")
