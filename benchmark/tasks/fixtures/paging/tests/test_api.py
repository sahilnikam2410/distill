import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import list_items  # noqa: E402


class ListItemsTest(unittest.TestCase):
    def test_first_page(self):
        res = list_items(1)
        self.assertEqual(res["items"], [f"item-{i}" for i in range(1, 11)])

    def test_last_page_is_partial(self):
        res = list_items(3)
        self.assertEqual(res["total_pages"], 3)
        self.assertEqual(res["items"], [f"item-{i}" for i in range(21, 26)])

    def test_exact_multiple(self):
        self.assertEqual(list_items(1, size=5)["total_pages"], 5)

    def test_out_of_range(self):
        with self.assertRaises(ValueError):
            list_items(4)


if __name__ == "__main__":
    unittest.main()
