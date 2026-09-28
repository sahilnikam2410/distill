# Coupon code -> percent off
COUPONS = {
    "SAVE10": 10,
    "SAVE25": 25,
    "HALF": 50,
}


def percent_for(code):
    if code is None:
        return 0
    return COUPONS.get(code.upper(), 0)
