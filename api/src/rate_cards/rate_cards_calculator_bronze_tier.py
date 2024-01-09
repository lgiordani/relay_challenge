from .rate_cards_calculator_tier import Tier


class BronzeTier(Tier):
    hourly_minimum = 14.50
    successful_rate = 0.459
    unsuccessful_rate = 0.229

    def _process_functions(self):
        functions = super()._process_functions()
        functions.extend([self._process_long_route_bonus, self._process_loyalty_bonus])

        return functions

    def _process_long_route_bonus(self):
        long_route_bonus = any(i > 30 for i in self.routes.values())
        long_route_bonus_quantity = 1 if long_route_bonus else 0
        long_route_bonus_rate = 10.0
        long_route_bonus_total = long_route_bonus_quantity * long_route_bonus_rate

        return {
            "name": "Long route bonus",
            "quantity": long_route_bonus_quantity,
            "rate": long_route_bonus_rate,
            "total": long_route_bonus_total,
        }

    def _process_loyalty_bonus(self):
        loyalty_bonus = len(self.routes.keys()) > 10
        loyalty_bonus_quantity = 1 if loyalty_bonus else 0
        loyalty_bonus_rate = 20.0
        loyalty_bonus_total = loyalty_bonus_quantity * loyalty_bonus_rate

        return {
            "name": "Loyalty bonus (routes)",
            "quantity": loyalty_bonus_quantity,
            "rate": loyalty_bonus_rate,
            "total": loyalty_bonus_total,
        }
