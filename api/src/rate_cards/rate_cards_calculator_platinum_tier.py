from collections import Counter

from .rate_cards_calculator_tier import Tier


class PlatinumTier(Tier):
    hourly_minimum = 15.25
    successful_rate = 0.667
    unsuccessful_rate = 0.155

    def _process_functions(self):
        functions = super()._process_functions()
        functions.extend(
            [
                self._process_long_route_bonus,
                self._process_loyalty_bonus_attempts,
                self._process_consistency_bonus,
            ]
        )

        return functions

    def _process_long_route_bonus(self):
        long_route_bonus = any(i > 30 for i in self.routes.values())
        long_route_bonus_quantity = 1 if long_route_bonus else 0
        long_route_bonus_rate = 12.0
        long_route_bonus_total = long_route_bonus_quantity * long_route_bonus_rate

        return {
            "name": "Long route bonus",
            "quantity": long_route_bonus_quantity,
            "rate": long_route_bonus_rate,
            "total": long_route_bonus_total,
        }

    def _process_loyalty_bonus_attempts(self):
        loyalty_bonus = self.successful_attempts > 150
        loyalty_bonus_quantity = 1 if loyalty_bonus else 0
        loyalty_bonus_rate = 18.0
        loyalty_bonus_total = loyalty_bonus_quantity * loyalty_bonus_rate

        return {
            "name": "Loyalty bonus (attempts)",
            "quantity": loyalty_bonus_quantity,
            "rate": loyalty_bonus_rate,
            "total": loyalty_bonus_total,
        }

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
        consistency_bonus_rate = 34.50
        consistency_bonus_total = consistency_bonus_quantity * consistency_bonus_rate

        return {
            "name": "Consistency bonus",
            "quantity": consistency_bonus_quantity,
            "rate": consistency_bonus_rate,
            "total": consistency_bonus_total,
        }
