import csv
import numpy
import json
from RecSys.Consts import Paths

"""
Класс для рекомендационной системы. Строится на основании данных конкретного пользователя
"""


class SuggestingRate:
    # Коллаборативая фильтрация: user-based, метод kNN
    kNN = 7

    __userName = str()
    __userRates = list()
    __userAverageRate = 0.0

    """
    Не хочется держать внутри экземпляра, но лучше пока не придумал
    """
    __allUserRates = list()
    __allUserDaysOfWeek = list()
    __allUserPlaces = list()

    __symmetries = dict()
    __nClosestUsers = list()

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

    """
    Найти прогноз оценки пользователя для фильма номер filmIndex (нумерация с 1)
    Рассчитывается по формуле в задании
    """
    def suggestRate(self, filmIndex: int) -> float:
        topSum = 0.0
        downSum = 0.0
        for user in self.__allUserRates:
            userName = user[0]
            if userName in self.__nClosestUsers:
                rates = user[1:len(user)]
                avgRate = self.__getAverageRate(rates)
                topSum += self.__symmetries[userName] * (int(user[filmIndex]) - avgRate)
                downSum += numpy.abs(self.__symmetries[userName])

        suggest = self.__userAverageRate + topSum / downSum
        return numpy.round(suggest, 2)

    """
    Алгоритм рекомендации:

    Идем по всем пользователям и ищем у них фильм, который:
    1) не смотрел наш пользователь
    2) был просмотрен в sat или sun (на выходных)
    3) был просмотрен дома

    Если такой фильм найден, то метрика сходства умножается на оценку пользователя об этом фильме ( sim * rate )
    полученное число - ценность рекомендации данного фильма - добавляется в dict (мапу). Если в мапе уже была рекомендация
    данного фильма, но с меньшей ценностью, то она заменяется

    В конце полученную мапу приводим к списку и сортируем по убыванию ценности. 

    Далее рекомендуем фильм, который имеет наибольшую ценность     
    """
    def recommend(self):
        filmRecommendations = dict()
        size = len(self.__allUserRates)
        rowLength = len(self.__allUserRates[0])

        for rowNumber in range(size):
            userName = self.__allUserRates[rowNumber][0]
            if userName != self.__userName:
                for filmNumber in range(1, rowLength):
                    if self.__verifyConditions(rowNumber, filmNumber):
                        recommendationCost = self.__symmetries[userName] * int(self.__allUserRates[rowNumber][filmNumber])
                        if filmNumber not in filmRecommendations.keys() or filmRecommendations[filmNumber] < recommendationCost:
                            filmRecommendations[filmNumber] = recommendationCost

        sortedRecommendations = list(filmRecommendations.items())
        sortedRecommendations.sort(key=lambda entry: entry[1], reverse=True)
        return sortedRecommendations[0][0]

    """
    Проверка удовлетворения фильмом условиям в алгоритме выше
    """
    def __verifyConditions(self, rowNumber, filmNumber):
        userDidntSee = self.__userRates[filmNumber - 1] == -1
        hasWatchedOnWeekend = self.__allUserDaysOfWeek[rowNumber][filmNumber].strip() == "Sat" or \
                              self.__allUserDaysOfWeek[rowNumber][filmNumber].strip() == "Sun"
        hasWatchedAtHome = self.__allUserPlaces[rowNumber][filmNumber].strip() == "h"

        if userDidntSee and hasWatchedAtHome and hasWatchedOnWeekend:
            return True
        else:
            return False

    def __init__(self, user: str) -> None:
        super().__init__()
        self.__userName = user

        self.__allUserRates = self.__parseCsv(Paths.rateFile)
        self.__allUserDaysOfWeek = self.__parseCsv(Paths.weeklyFile)
        self.__allUserPlaces = self.__parseCsv(Paths.placeFile)

        self.__userRates = self.__getUserRates()
        self.__symmetries = self.__getSymmetries()
        self.__userAverageRate = self.__getAverageRate(self.__userRates)
        self.__nClosestUsers = self.__getNclosestUsers(self.kNN)

    """
    Заполнить self.__userRates - все оценки пользователя для текущего экземпляра
    """
    def __parseCsv(self, fileName: str) -> list:
        parsed = list()
        with open(fileName, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            parsed = list(reader)
        return parsed

    """
    Получить список оценок фильмов для нашего пользователя
    """
    def __getUserRates(self) -> list:
        selfUserRates = list()
        for userRates in self.__allUserRates:
            userName = userRates[0]
            if userName == self.__userName:
                selfUserRates = userRates[1:len(userRates)]
                break

        for i in range(len(selfUserRates)):
            selfUserRates[i] = int(selfUserRates[i])

        return selfUserRates

    """
    Заполнить self.__symmetries - данные сходства пользователя со всеми остальными пользователями
    """
    def __getSymmetries(self) -> dict:
        symmetries = dict()

        for user in self.__allUserRates:
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


userSuggestion = SuggestingRate("User 1")
result = {
    "user": 1,
    "1 (rate forecasts)": userSuggestion.suggestRates(),
    "2 (film recommendation)": "Movie " + str(userSuggestion.recommend())
}
with open('user1.json', 'w') as outfile:
    json.dump(obj=result, fp=outfile, indent=4)
