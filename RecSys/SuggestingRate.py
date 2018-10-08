import csv
import numpy
from RecSys.Consts import Paths

"""
Класс для рекомендационной системы
"""
class SuggestingRate :

    __symmetries = dict()
    __userName = str()
    __userRates = []

    def __init__(self, user: str) -> None:
        super().__init__()
        self.__userName = user
        self.__fillUserRates()
        self.__computeSymmetries()

    def __fillUserRates(self):
        with open(Paths.rateFile, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for user in reader:
                userName = user[0]
                if userName == self.__userName:
                    filmRates = user[1:user.__len__()]
                    for filmRate in filmRates:
                        self.__userRates.append( int(filmRate) )

    def __computeSymmetries(self):
        with open(Paths.rateFile, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for user in reader:
                userName = user[0]
                if userName and userName!=self.__userName:
                    filmRates = user[1:user.__len__()]
                    self.__symmetries[userName] = self.__findSymmetry( filmRates )

    def __findSymmetry(self, filmRates: list) -> float:
        """
        sim(U,V) = sum(i=1..m; U[i]*V[i]) / ( sqrt sum(i=1..m; U[i]^2]) * sqrt sum(i=1..m; V[i]^2) )
        где V - текущий пользователь
        """
        sumUV = 0
        sumU2 = 0
        sumV2 = 0
        for i in range(0, filmRates.__len__()):
            filmRate = int(filmRates[i])
            ourRate = self.__userRates[i]
            if filmRate != -1 and ourRate != -1:
                sumUV += filmRate * ourRate
                sumU2 += filmRate * filmRate
                sumV2 += ourRate * ourRate
        return sumUV / (numpy.sqrt(sumU2) * numpy.sqrt(sumV2))

    def suggestRates(self) -> None :
        return


suggestion = SuggestingRate("User 1")
print("lol")