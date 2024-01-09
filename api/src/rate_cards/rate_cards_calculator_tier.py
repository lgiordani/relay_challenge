from typing import List
from collections import Counter

from src.entities.types import LineItemType
from src.entities.earnings_statement import EarningsStatement


class Tier:
    successful_rate: float = 0
    unsuccessful_rate: float = 0
    hourly_minimum: float = 0

    def __init__(self, activity_log):
        self.activity_log = activity_log
        self.routes = Counter([i["route_id"] for i in activity_log])

        successes = Counter([i["success"] for i in self.activity_log])
        self.successful_attempts = successes[True]
        self.unsuccessful_attempts = successes[False]

    def _process_functions(self):
        return [self._process_successful_attempts, self._process_unsuccessful_attempts]

    def _process_line_items(self):
        line_items: List[LineItemType] = []

        for func in self._process_functions():
            line_items.append(func())

        return line_items

    def _process_successful_attempts(self):
        successful_total = self.successful_attempts * self.successful_rate
        return {
            "name": "Per successful attempt",
            "quantity": self.successful_attempts,
            "rate": self.successful_rate,
            "total": successful_total,
        }

    def _process_unsuccessful_attempts(self):
        unsuccessful_total = self.unsuccessful_attempts * self.unsuccessful_rate
        return {
            "name": "Per unsuccessful attempt",
            "quantity": self.unsuccessful_attempts,
            "rate": self.unsuccessful_rate,
            "total": unsuccessful_total,
        }

    def process(self):
        line_items = self._process_line_items()

        route_hours = []
        for route in self.routes:
            times = [
                i["attempt_date_time"]
                for i in self.activity_log
                if i["route_id"] == route
            ]
            delta = max(times) - min(times)

            route_hours.append(delta.total_seconds() / 3600)

        line_items_subtotal = sum(i["total"] for i in line_items)

        hours_worked = sum(route_hours)
        minimum_earnings = self.hourly_minimum * hours_worked

        final_earnings = max(minimum_earnings, line_items_subtotal)

        return EarningsStatement(
            line_items=line_items,
            line_items_subtotal=line_items_subtotal,
            hours_worked=hours_worked,
            minimum_earnings=minimum_earnings,
            final_earnings=final_earnings,
        )
