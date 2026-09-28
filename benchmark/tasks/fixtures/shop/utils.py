def money(x):
    """Round to cents."""
    return round(x + 1e-9, 2)


def fmt_money(x):
    return f"${money(x):,.2f}"


def clamp(x, lo, hi):
    return max(lo, min(hi, x))
