import csv
import numpy
from RecSys.Consts import Paths

"""
Класс для рекомендационной системы. Строится на основании данных конкретного пользователя
"""


class SuggestingRate:
    # Коллаборативая фильтрация: user-based, метод kNN
    kNN = 7

    __symmetries = dict()
    __userName = str()
    __userRates = list()
    __userAverageRate = 0.0
    __nClosestUsers = list()

    def __init__(self, user: str) -> None:
        super().__init__()
        self.__userName = user
        self.__userRates = self.__getUserRates()
        self.__symmetries = self.__getSymmetries()
        self.__userAverageRate = self.__getAverageRate(self.__userRates)
        self.__nClosestUsers = self.__getNclosestUsers(self.kNN)

    """
    Заполнить self.__userRates - все оценки пользователя для текущего экземпляра
    """

    def __getUserRates(self) -> list:
        userRates = list()
        with open(Paths.rateFile, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for user in reader:
                userName = user[0]
                if userName == self.__userName:
                    userRates = user[1:len(user)]
        for i in range(len(userRates)):
            userRates[i] = int(userRates[i])
        return userRates

    """
    Заполнить self.__symmetries - данные сходства пользователя со всеми остальными пользователями
    """

    def __getSymmetries(self) -> dict:
        symmetries = dict()
        with open(Paths.rateFile, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for user in reader:
                userName = user[0]
                if userName and userName != self.__userName:
                    filmRates = user[1:len(user)]
                    symmetries[userName] = self.__findSymmetry(filmRates)
        return symmetries

    """
    Найти сходство пользователя с тем, у кого оценки = filmRates
    """

    def __findSymmetry(self, filmRates: list) -> float:
        """
        sim(U,V) = sum(i=1..m; U[i]*V[i]) / ( sqrt sum(i=1..m; U[i]^2]) * sqrt sum(i=1..m; V[i]^2) )
        где V - текущий пользователь
        """
        sumUV = 0
        sumU2 = 0
        sumV2 = 0
        for i in range(len(filmRates)):
            filmRate = int(filmRates[i])
            ourRate = self.__userRates[i]
            if filmRate != -1 and ourRate != -1:
                sumUV += filmRate * ourRate
                sumU2 += filmRate * filmRate
                sumV2 += ourRate * ourRate
        symmetry = sumUV / (numpy.sqrt(sumV2) * numpy.sqrt(sumU2))
        return symmetry

    """
    Найти среднюю оценку
    """

    def __getAverageRate(self, filmRates: list) -> float:
        avg = 0.0
        count = 0
        for filmRate in filmRates:
            rate = int(filmRate)
            if -1 != rate:
                avg += rate
                count += 1
        return avg / count

    """
    Получить n пользователей, которые наиболее схожи с нашим пользователем, в убывающем порядке сходства
    """

    def __getNclosestUsers(self, n: int) -> list:
        symmetriesEntries = list(self.__symmetries.items())
        symmetriesEntries.sort(key=lambda entry: entry[1], reverse=True)

        symmetriesUsers = list()
        for i in range(n):
            symmetriesUsers.append(symmetriesEntries[i][0])
        return symmetriesUsers

    """
    Найти прогноз оценки пользователя для фильма номер filmIndex (нумерация с 1)
    Рассчитывается по формуле в задании
    """

    def suggestRate(self, filmIndex: int) -> float:
        topSum = 0.0
        downSum = 0.0
        with open(Paths.rateFile, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for user in reader:
                userName = user[0]
                if userName in self.__nClosestUsers:
                    rates = user[1:len(user)]
                    avgRate = self.__getAverageRate(rates)
                    topSum += self.__symmetries[userName] * (int(user[filmIndex]) - avgRate)
                    downSum += numpy.abs(self.__symmetries[userName])
        suggest = self.__userAverageRate + topSum / downSum
        return numpy.round(suggest, 2)

    """
    Найти прогноз оценки пользователя для всех фильмов, которые он не оценил
    """

    def suggestRates(self) -> dict:
        suggest = dict()
        for index in range(len(self.__userRates)):
            filmRate = self.__userRates[index]
            filmNumber = index + 1
            if int(filmRate) == -1:
                suggest["Movie " + str(filmNumber)] = self.suggestRate(filmNumber)
        return suggest


userSuggestion = SuggestingRate("User 1")
suggest = userSuggestion.suggestRates()
print(suggest)
