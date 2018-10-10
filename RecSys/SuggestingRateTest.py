import numpy
import unittest
from unittest import TestCase

from RecSys.SuggestingRate import SuggestingRate


class SuggestingRateTest(unittest.TestCase):
    userSuggestion = None

    def setUp(self):
        self.userSuggestion = SuggestingRate("User 1")

    def test_shouldGetCorrectUserRatesForUser1(self):
        real = self.userSuggestion._SuggestingRate__getUserRates()
        expected = [-1, 4, 1, 5, -1, -1, -1, 1, 3, -1, 5, 5, 1, 3, 3, 3, -1, 4, 2, 2, 2, 4, -1, -1, 3, 4, -1, 2, 4, 1]
        self.assertEqual(real, expected)

    def test_shouldCorrectSymmetryWithUser1AndUser2(self):
        data = [4, 5, 2, 3, 3, 4, -1, 5, 3, 2, 2, -1, 5, 5, 4, 1, -1, 2, 4, 5, -1, 2, -1, 3, 1, 5, -1, 5, 2, 2]
        real = self.userSuggestion._SuggestingRate__findSymmetry(data)
        """
        User 1, -1, 4, 1, 5, -1, -1, -1, 1, 3, -1, 5, 5, 1, 3, 3, 3, -1, 4, 2, 2, 2, 4, -1, -1, 3, 4, -1, 2, 4, 1
        User 2, 4, 5, 2, 3, 3, 4, -1, 5, 3, 2, 2, -1, 5, 5, 4, 1, -1, 2, 4, 5, -1, 2, -1, 3, 1, 5, -1, 5, 2, 2
        """
        expected = 173.0 / ( numpy.sqrt(191.0) * numpy.sqrt(251.0))
        self.assertEqual(real, expected)

    def test_shouldGetAverageRateForUser1(self):
        data = [-1, 4, 1, 5, -1, -1, -1, 1, 3, -1, 5, 5, 1, 3, 3, 3, -1, 4, 2, 2, 2, 4, -1, -1, 3, 4, -1, 2, 4, 1]
        real = self.userSuggestion._SuggestingRate__getAverageRate(data)
        real = numpy.round(real, 3)
        expected = 2.952
        self.assertEqual(real, expected)

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
        self.assertEqual(real, expected)


if __name__ == '__main__':
    unittest.main()
