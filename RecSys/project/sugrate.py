import numpy

class UserSuggestingRate:
    """
    Класс для рекомендационной системы. Строится на основании данных конкретного пользователя
    """

    # Коллаборативая фильтрация: user-based, метод kNN
    kNN = int()

    __myName = str()
    __myRates = list()
    __myAverageRate = float()

    usersRates = dict()
    usersDaysOfWeek = dict()
    usersPlaces = dict()

    __symmetries = dict()

    def suggestRates(self) -> dict:
        """
        Найти прогноз оценки пользователя для всех фильмов, которые он не оценил
        """
        suggest = dict()
        for filmNumber in range(len(self.__myRates)):
            filmRate = self.__myRates[filmNumber]
            if filmRate == -1:
                suggest["Movie " + str(filmNumber)] = self.suggestRate(filmNumber)
        return suggest

    def suggestRate(self, filmNumber: int) -> float:
        """
        Найти прогноз оценки пользователя для фильма номер filmNumber (нумерация с 0)
        Рассчитывается по формуле в задании
        """
        topSum = 0.0
        downSum = 0.0
        nClosestUsers = self.__getNclosestUsers(self.kNN, filmNumber)
        for userName, userRates in self.usersRates.items():
            if userName in nClosestUsers:
                avgRate = UserSuggestingRate.getAverageRate(userRates)
                rate = userRates[filmNumber]
                a = self.__symmetries[userName] * (rate - avgRate)
                topSum += a
                b = numpy.abs(self.__symmetries[userName])
                downSum += b
        suggest = self.__myAverageRate + (topSum / downSum)
        return numpy.round(suggest, 3)

    def recommend(self):
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
        filmRecommendations = dict()

        for userName, userRates in self.usersRates.items():
            if userName != self.__myName:
                for filmNumber in range(len(userRates)):
                    if self.verifyFilmConditions(userName, filmNumber):
                        recommendationCost = self.__symmetries[userName] * userRates[filmNumber]
                        if filmNumber not in filmRecommendations.keys() or filmRecommendations[filmNumber] < recommendationCost:
                            filmRecommendations[filmNumber] = recommendationCost

        sortedRecommendations = list(filmRecommendations.items())
        sortedRecommendations.sort(key=lambda entry: entry[1], reverse=True)
        return sortedRecommendations[0][0]

    def verifyFilmConditions(self, userName, filmNumber):
        """
        Проверка удовлетворения фильмом условиям в алгоритме выше
        """
        didMeWatch = (self.__myRates[filmNumber] == -1)
        didUserWatchAtWeekend = (self.usersDaysOfWeek[userName][filmNumber].strip() == "Sat") or \
                                (self.usersDaysOfWeek[userName][filmNumber].strip() == "Sun")
        didUserWatchAtHome = (self.usersPlaces[userName][filmNumber].strip() == "h")

        if didMeWatch and didUserWatchAtHome and didUserWatchAtWeekend:
            return True
        else:
            return False

    @staticmethod
    def getAverageRate(filmRates: list) -> float:
        """
        Найти среднюю оценку
        """
        avg = 0.0
        count = 0
        for filmRate in filmRates:
            if -1 != filmRate:
                avg += filmRate
                count += 1
        return avg / count

    @staticmethod
    def findSymmetry(filmRates1: list, filmRates2: list) -> float:
        """
        Найти сходство пользователя с тем, у кого оценки = filmRates

        sim(U,V) = sum(i=1..m; U[i]*V[i]) / ( sqrt sum(i=1..m; U[i]^2]) * sqrt sum(i=1..m; V[i]^2) )
        где V - текущий пользователь
        """
        sumUV = 0
        sumU2 = 0
        sumV2 = 0
        for i in range(len(filmRates1)):
            rate1 = filmRates1[i]
            rate2 = filmRates2[i]
            if rate1 != -1 and rate2 != -1:
                sumUV += rate1 * rate2
                sumU2 += rate1 * rate1
                sumV2 += rate2 * rate2
        symmetry = sumUV / (numpy.sqrt(sumV2) * numpy.sqrt(sumU2))
        return symmetry

    def __init__(self, myName: str, usersRates: dict, usersDaysOfWeek: dict, usersPlaces: dict, kNN: int = 7) -> None:
        super().__init__()
        self.__myName = myName
        self.kNN = kNN

        self.usersRates = usersRates
        self.usersDaysOfWeek = usersDaysOfWeek
        self.usersPlaces = usersPlaces

        self.__myRates = self.__getUserRates()
        self.__symmetries = self.__getSymmetries()
        self.__myAverageRate = self.getAverageRate(self.__myRates)

    def __getUserRates(self) -> list:
        """
        Получить список оценок фильмов для нашего пользователя
        """
        selfUserRates = list()
        for userName, userRates in self.usersRates.items():
            if userName == self.__myName:
                selfUserRates = userRates
                break

        return selfUserRates

    def __getSymmetries(self) -> dict:
        """
        Заполнить self.__symmetries - данные сходства пользователя со всеми остальными пользователями
        """
        symmetries = dict()

        for userName, userRates in self.usersRates.items():
            if userName != self.__myName:
                symmetries[userName] = self.findSymmetry(self.__myRates, userRates)
        return symmetries

    def __getNclosestUsers(self, n: int, filmNumber: int) -> list:
        """
        Получить не более n пользователей, которые наиболее схожи с нашим пользователем, в убывающем порядке сходства
        """
        symmetriesEntries = list(self.__symmetries.items())
        symmetriesEntries.sort(key=lambda entry: entry[1], reverse=True)

        symmetriesUsers = list()
        i = 0
        while i < n:
            userName = symmetriesEntries[i][0]
            rates = self.usersRates[userName]
            if (rates[filmNumber] != -1):
                symmetriesUsers.append(userName)
            i += 1

        return symmetriesUsers
