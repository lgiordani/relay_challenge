from collections import Counter

from .rate_cards_calculator_tier import Tier


class GoldTier(Tier):
    hourly_minimum = 15.0
    successful_rate = 0.511
    unsuccessful_rate = 0.126

    def _process_functions(self):
        functions = super()._process_functions()
        functions.extend([self._process_consistency_bonus])

        return functions

    def _process_consistency_bonus(self):
        success_rate = []
        for route in self.routes:
            successes = Counter(
                [i["success"] for i in self.activity_log if i["route_id"] == route]
            )
            successful_attempts = successes[True]
            unsuccessful_attempts = successes[False]
            total_attempts = successful_attempts + unsuccessful_attempts
            success_rate.append(successful_attempts / total_attempts)

        consistency_bonus = len(self.routes) > 1 and all(
            i > 0.965 for i in success_rate
        )
        consistency_bonus_quantity = 1 if consistency_bonus else 0
        consistency_bonus_rate = 32.0
        consistency_bonus_total = consistency_bonus_quantity * consistency_bonus_rate

        return {
            "name": "Consistency bonus",
            "quantity": consistency_bonus_quantity,
            "rate": consistency_bonus_rate,
            "total": consistency_bonus_total,
        }
