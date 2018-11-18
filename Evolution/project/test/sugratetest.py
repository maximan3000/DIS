import unittest

import numpy
from unittest import TestCase
from RecSys.project.sugrate import UserSuggestingRate
from RecSys.project.util import parseCsv


class UserSuggestingRateTest(unittest.TestCase):
    myName = "User 1"
    userSuggestion = None

    def setUp(self):
        usersRates = parseCsv("data.csv", int)
        usersDaysOfWeek = parseCsv("context_day.csv", str)
        usersPlaces = parseCsv("context_place.csv", str)
        self.userSuggestion = UserSuggestingRate(myName=self.myName,
                                                 usersRates=usersRates,
                                                 usersDaysOfWeek=usersDaysOfWeek,
                                                 usersPlaces=usersPlaces)

    def test_shouldCorrectSymmetryWithUser1AndUser2(self):
        expected = 173.0 / ( numpy.sqrt(191.0) * numpy.sqrt(251.0))

        user1Rates = self.userSuggestion.usersRates["User 1"]
        user2Rates = self.userSuggestion.usersRates["User 2"]
        actual = UserSuggestingRate.findSymmetry(user1Rates, user2Rates)

        self.assertEqual(actual, expected)

    def test_shouldGetAverageRateForUser1(self):
        expected = 2.952

        user1Rates = self.userSuggestion.usersRates["User 1"]
        actual = UserSuggestingRate.getAverageRate(user1Rates)
        actual = numpy.round(actual, 3)

        self.assertEqual(actual, expected)

    def test_allSuggestionRatesForUser1ShouldBeCorrect(self):
        expected = {"Movie 0": 3.126,
                    "Movie 4": 2.933,
                    "Movie 5": 2.411,
                    "Movie 6": 3.949,
                    "Movie 9": 2.668,
                    "Movie 16": 1.305,
                    "Movie 22": 2.666,
                    "Movie 23": 3.289,
                    "Movie 26": 2.69
                    }

        actual = self.userSuggestion.suggestRates()

        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()

