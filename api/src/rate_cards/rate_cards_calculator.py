from .rate_cards_calculator_bronze_tier import BronzeTier
from .rate_cards_calculator_silver_tier import SilverTier
from .rate_cards_calculator_gold_tier import GoldTier


class WrongTierName(ValueError):
    """The given tier name is not valid"""


class RateCardsCalculator:
    tiers = {
        "bronze": BronzeTier,
        "silver": SilverTier,
        "gold": GoldTier,
    }

    def __init__(self, tier):
        try:
            self._class = self.tiers[tier]
        except KeyError as exc:
            raise WrongTierName from exc

    def process(self, activity_log):
        return self._class(activity_log).process()
