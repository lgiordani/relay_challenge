from .rate_cards_calculator_tier import Tier


class SilverTier(Tier):
    hourly_minimum = 13.50
    successful_rate = 0.65
    unsuccessful_rate = 0.0

    def _process_functions(self):
        functions = super()._process_functions()
        functions.extend([self._process_quality_bonus, self._process_loyalty_bonus])

        return functions

    def _process_quality_bonus(self):
        total_attempts = self.successful_attempts + self.unsuccessful_attempts
        success_rate = self.successful_attempts / total_attempts

        quality_bonus = total_attempts >= 20 and success_rate >= 0.97
        quality_bonus_quantity = 1 if quality_bonus else 0
        quality_bonus_rate = 25.0
        quality_bonus_total = quality_bonus_quantity * quality_bonus_rate

        return {
            "name": "Quality bonus",
            "quantity": quality_bonus_quantity,
            "rate": quality_bonus_rate,
            "total": quality_bonus_total,
        }

    def _process_loyalty_bonus(self):
        loyalty_bonus = self.successful_attempts > 150
        loyalty_bonus_quantity = 1 if loyalty_bonus else 0
        loyalty_bonus_rate = 19.0
        loyalty_bonus_total = loyalty_bonus_quantity * loyalty_bonus_rate

        return {
            "name": "Loyalty bonus (attempts)",
            "quantity": loyalty_bonus_quantity,
            "rate": loyalty_bonus_rate,
            "total": loyalty_bonus_total,
        }
