"""
    SeasonalCustomer.py
    Subclass that overrides discount_rate() based on the customer's preferred season.
"""

from __future__ import annotations
import datetime as dt
from Customer import Customer

class SeasonalCustomer(Customer):
    def __init__(
        self,
        customer_id: str,
        name: str,
        email: str,
        season: str,
        total_spent: float = 0.0,
        visits: int = 0,
    ):
        super().__init__(customer_id, name, email, total_spent=total_spent, visits=visits)
        self.season = season  # route through setter

    @property
    def season(self) -> str:
        return self.__season

    @season.setter
    def season(self, value: str) -> None:
        value = (value or "").strip().title()
        allowed = {"Winter", "Spring", "Summer", "Fall"}
        if value not in allowed:
            raise ValueError(f"season must be one of {sorted(allowed)}")
        self.__season = value

    def discount_rate(self, on_date: dt.date | None = None) -> float:
        on_date = on_date or dt.date.today()
        month = on_date.month

        season_months = {
            "Winter": {12, 1, 2},
            "Spring": {3, 4, 5},
            "Summer": {6, 7, 8},
            "Fall":   {9, 10, 11},
        }

        return 0.10 if month in season_months[self.season] else 0.0
