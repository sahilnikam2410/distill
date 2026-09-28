from coupons import percent_for
from utils import money

TAX_RATE = 0.08


def subtotal(cart):
    return sum(i.price * i.qty for i in cart.items)


def discount(cart):
    pct = percent_for(cart.coupon)
    return subtotal(cart) * pct / 100


def total(cart):
    """Subtotal minus coupon discount, plus tax on the discounted amount."""
    sub = subtotal(cart)
    disc = discount(cart)
    taxed = sub * (1 + TAX_RATE)
    return money(taxed - disc)
