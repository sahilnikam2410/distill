import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cart import total  # noqa: E402
from models import Cart, Item  # noqa: E402


class TotalTest(unittest.TestCase):
    def test_no_coupon(self):
        c = Cart(items=[Item("A", "Mug", 10.0, 2)])
        self.assertEqual(total(c), 21.60)

    def test_coupon_taxes_discounted_amount(self):
        c = Cart(items=[Item("A", "Mug", 100.0, 1)], coupon="SAVE25")
        self.assertEqual(total(c), 81.00)

    def test_lowercase_coupon(self):
        c = Cart(items=[Item("A", "Mug", 50.0, 2)], coupon="half")
        self.assertEqual(total(c), 54.00)


if __name__ == "__main__":
    unittest.main()
