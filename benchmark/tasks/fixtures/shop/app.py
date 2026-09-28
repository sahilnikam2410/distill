from cart import subtotal, total
from models import Cart, Item
from utils import fmt_money


def checkout(items, coupon=None):
    cart = Cart(items=[Item(**i) for i in items], coupon=coupon)
    return {
        "subtotal": fmt_money(subtotal(cart)),
        "total": fmt_money(total(cart)),
    }


if __name__ == "__main__":
    print(checkout([{"sku": "A1", "name": "Mug", "price": 12.5, "qty": 2}], coupon="SAVE10"))
