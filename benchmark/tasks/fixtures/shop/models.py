from dataclasses import dataclass, field


@dataclass
class Item:
    sku: str
    name: str
    price: float  # unit price in USD
    qty: int = 1


@dataclass
class Cart:
    items: list = field(default_factory=list)
    coupon: str | None = None
