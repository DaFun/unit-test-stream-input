import unittest
from median import Median

class MedianTestCase(unittest.TestCase):
    def setUp(self):
        self.median = Median()

    def test_add_num(self):
        self.assertEqual(self.median.get_num(), 0)
        self.median.add_num(1)
        self.assertEqual(self.median.get_num(), 1)
        self.median.add_num(2)
        self.assertEqual(self.median.get_num(), 2)

    def test_get_median(self):
        self.median.add_num(1)
        self.assertEqual(self.median.get_median(), 1)
        self.median.add_num(2)
        self.assertEqual(self.median.get_median(), 2)
        self.median.add_num(3)
        self.assertEqual(self.median.get_median(), 2)

    def test_get_total(self):
        self.median.add_num(1)
        self.assertEqual(self.median.get_total(), 1)
        self.median.add_num(2)
        self.assertEqual(self.median.get_total(), 3)
        self.median.add_num(3)
        self.assertEqual(self.median.get_total(), 6)

    def test_overflow(self):
        self.median.add_num(9223372036854775807)
        self.median.add_num(1)
        self.assertEqual(self.median.get_num(), 2)
        self.assertEqual(self.median.get_total(), 9223372036854775808)
        self.assertEqual(self.median.get_median(), 4611686018427387904)

    def test_negative_num(self):
        self.median.add_num(-62)
        self.assertEqual(self.median.get_median(), -62)
        self.median.add_num(-63)
        self.assertEqual(self.median.get_median(), -63)
        # if all negative


if __name__ == '__main__':
    unittest.main()