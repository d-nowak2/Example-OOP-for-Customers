"""
    Customer.py
    Parent class demonstrating encapsulation with private fields (double underscore),
    plus a shared method that relies on an overridable rule method.
"""

from __future__ import annotations
import datetime as dt


class Customer:
    """
    Encapsulation note:
    - We store state in private fields like __name, __email, etc.
    - We expose controlled access via @property getters/setters (validation lives there).
    """

    def __init__(self, customer_id: str, name: str, email: str, total_spent: float = 0.0, visits: int = 0):
        self.__customer_id = (customer_id or "").strip()
        if not self.__customer_id:
            raise ValueError("customer_id is required")

        # Route through setters for validation:
        self.name = name
        self.email = email
        self.total_spent = total_spent
        self.visits = visits

    # --- Read-only ID ---
    @property
    def customer_id(self) -> str:
        return self.__customer_id

    # --- Encapsulated fields ---
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        value = (value or "").strip()
        if len(value) < 2:
            raise ValueError("name must be at least 2 characters")
        self.__name = value

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str) -> None:
        value = (value or "").strip()
        if "@" not in value or "." not in value:
            raise ValueError("email must look like an email address")
        self.__email = value

    @property
    def total_spent(self) -> float:
        return self.__total_spent

    @total_spent.setter
    def total_spent(self, value: float) -> None:
        value = float(value)
        if value < 0:
            raise ValueError("total_spent cannot be negative")
        self.__total_spent = value

    @property
    def visits(self) -> int:
        return self.__visits

    @visits.setter
    def visits(self, value: int) -> None:
        value = int(value)
        if value < 0:
            raise ValueError("visits cannot be negative")
        self.__visits = value

    # --- Shared behavior for ALL customers ---
    def record_purchase(self, amount: float) -> None:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("purchase amount must be > 0")
        self.total_spent += amount
        self.visits += 1

    # --- Overridable rule method ---
    def discount_rate(self, on_date: dt.date | None = None) -> float:
        """
        Subclasses override this to change discount logic.
        Default: 0% discount.
        """
        return 0.0

    # --- Method used by everyone, but behavior depends on overridden rule ---
    def final_price(self, subtotal: float, on_date: dt.date | None = None) -> float:
        subtotal = float(subtotal)
        if subtotal < 0:
            raise ValueError("subtotal cannot be negative")
        rate = self.discount_rate(on_date=on_date)
        return round(subtotal * (1.0 - rate), 2)

    def summary(self) -> str:
        return (
            f"{self.customer_id}: {self.name} ({self.__class__.__name__}) "
            f"| visits={self.visits} | total_spent=${self.total_spent:.2f}"
        )
