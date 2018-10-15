import unittest
from Category import Category
from Line import Line


class CategoryPrint(unittest.TestCase):
    def test(self):
        cat = Category("cat")
        l1 = Line("Date", "01/01/18")
        l2 = Line("OS", "Linux")
        self.assertEqual(len(l1), 15)
        self.assertEqual(len(l2), 10)
        cat.add_line(l1)
        cat.add_line(l2)
        self.assertEqual(len(cat), 15)
