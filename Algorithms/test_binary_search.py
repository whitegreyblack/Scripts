import unittest
from binary_search import binary_search
class TestBinarySearch(unittest.TestCase):
    def setUp(self):
        self.array = [x for x in range(10)]
    
    def test_search(self):
        self.assertEqual(binary_search(self.array, 10), -1)
        self.assertEqual(binary_search(self.array, 8), 8)
        self.assertEqual(binary_search(self.array, 2), 2)

if __name__ == "__main__":
    unittest.main()
