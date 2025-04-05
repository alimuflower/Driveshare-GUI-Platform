from abc import ABC, abstractmethod

class PricingStrategy(ABC):
    """
    Abstract base class for pricing strategies.
    Each subclass must implement the calculate_price method.
    """
    @abstractmethod
    def calculate_price(self, base_price, days, user):
        pass


class StandardPricing(PricingStrategy):
    """
    Default pricing: no discount.
    """
    def calculate_price(self, base_price, days, user):
        return base_price * days


class WeekendDiscountPricing(PricingStrategy):
    """
    Applies a 10% discount for weekend rentals.
    For demo purposes, applies to all rentals (not just actual weekends).
    """
    def calculate_price(self, base_price, days, user):
        return (base_price * days) * 0.90


class LoyaltyPricing(PricingStrategy):
    """
    Applies a 15% discount if the user has over 100 loyalty points.
    """
    def calculate_price(self, base_price, days, user):
        if hasattr(user, 'loyalty_points') and user.loyalty_points > 100:
            return (base_price * days) * 0.85
        return base_price * days


class FirstTimeRenterPricing(PricingStrategy):
    """
    Gives 10% discount to users renting for the first time.
    """
    def calculate_price(self, base_price, days, user):
        if hasattr(user, 'rental_history') and len(user.rental_history) == 0:
            return (base_price * days) * 0.90
        return base_price * days


class PromoCodePricing(PricingStrategy):
    """
    Gives a 10% discount if a valid promo code is provided.
    Only works for guests.
    """
    def __init__(self, code=None):
        self.code = code

    def calculate_price(self, base_price, days, user):
        valid_codes = ['firstride']
        if hasattr(user, 'role') and user.role == 'guest' and self.code in valid_codes:
            return (base_price * days) * 0.90
        return base_price * days



