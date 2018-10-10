import unittest
from unittest import TestCase

from RecSys.SuggestingRate import SuggestingRate


class SuggestingRateTest(unittest.TestCase):
    userSuggestion = None

    def setUp(self):
        self.userSuggestion = SuggestingRate("User 1")

    def test_allSuggestionRatesForUser1ShouldBeCorrect(self):
        expected = {"Movie 1": 3.2,
                    "Movie 5": 3.17,
                    "Movie 6": 2.36,
                    "Movie 7": 3.95,
                    "Movie 10": 2.67,
                    "Movie 17": 1.35,
                    "Movie 23": 2.67,
                    "Movie 24": 3.08,
                    "Movie 27": 2.4}
        real = self.userSuggestion.suggestRates()
        self.assertEqual(expected, real)


if __name__ == '__main__':
    unittest.main()
