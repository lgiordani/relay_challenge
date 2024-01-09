import math
from typing import List

from .types import LineItemType


class EarningsStatement:
    diff_tolerance = 1e-6

    def __init__(
        self,
        line_items: List[LineItemType],
        line_items_subtotal: float,
        hours_worked: float,
        minimum_earnings: float,
        final_earnings: float,
    ):
        self.line_items = line_items
        self.line_items_subtotal = line_items_subtotal
        self.hours_worked = hours_worked
        self.minimum_earnings = minimum_earnings
        self.final_earnings = final_earnings

    def asdict(self):
        return {
            "line_items": self.line_items,
            "line_items_subtotal": self.line_items_subtotal,
            "hours_worked": self.hours_worked,
            "minimum_earnings": self.minimum_earnings,
            "final_earnings": self.final_earnings,
        }

    def __eq__(self, other):
        self_line_items = {i["name"]: i for i in self.line_items}
        other_line_items = {i["name"]: i for i in other.line_items}

        if self_line_items.keys() != other_line_items.keys():
            return False

        for key in self_line_items.keys():
            if not math.isclose(
                self_line_items[key]["rate"],
                other_line_items[key]["rate"],
                abs_tol=self.diff_tolerance,
            ):
                return False

            if not math.isclose(
                self_line_items[key]["total"],
                other_line_items[key]["total"],
                abs_tol=self.diff_tolerance,
            ):
                return False

        if not math.isclose(
            self.line_items_subtotal,
            other.line_items_subtotal,
            abs_tol=self.diff_tolerance,
        ):
            return False

        if not math.isclose(
            self.hours_worked, other.hours_worked, abs_tol=self.diff_tolerance
        ):
            return False

        if not math.isclose(
            self.minimum_earnings, other.minimum_earnings, abs_tol=self.diff_tolerance
        ):
            return False

        if not math.isclose(
            self.final_earnings, other.final_earnings, abs_tol=self.diff_tolerance
        ):
            return False

        return True

    def __repr__(self):
        return self.asdict().__repr__()
