import unittest

from app.links.link_generation import generateCompletelyRandomShortID


class MyTestCase(unittest.TestCase):
    def test_completely_random_generation(self):
        length = 10
        short_id = generateCompletelyRandomShortID(length)
        self.assertEqual(length, len(short_id))


if __name__ == '__main__':
    unittest.main()
