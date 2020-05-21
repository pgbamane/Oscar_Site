from oscar.apps.offer.benefits import AbsoluteDiscountBenefit


class CustomAbsoluteDiscountPerProductBenefit(AbsoluteDiscountBenefit):
    """
    Core AbsoluteDiscountBenefit supports for Absolute discount on whole basket by the value of the benefit.
     E.g. if you have in the basket 3 items for €50 and €20 voucher,
      the basket total after discounts would be: 50 × 3 - 20 = 130
    Apply this class Absolute Discount per product, : (50 - 20) × 3 = 90.
    """

    def apply(self, basket, condition, offer, discount_amount=None,
              max_total_discount=None):
        line_tuples = self.get_applicable_lines(offer, basket)
        max_affected_items = self._effective_max_affected_items()
        num_affected_items = 0
        lines_to_discount = []

        for price, line in line_tuples:
            if num_affected_items >= max_affected_items:
                break

            qty = min(
                line.quantity_without_offer_discount(offer),
                max_affected_items - num_affected_items,
                line.quantity
            )
            lines_to_discount.append((line, price, qty))
            num_affected_items += qty

        discount_amount = self.value * num_affected_items
        return super().apply(
            basket, condition, offer, discount_amount=discount_amount, max_total_discount=max_total_discount
        )
