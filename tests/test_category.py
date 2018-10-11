import unittest
import Category


class CategoryTest(unittest.TestCase):
    def test(self):
        cat = Category.Category("cat")
        cat.add_line("test")
        self.assertEqual(len(cat), 5)
