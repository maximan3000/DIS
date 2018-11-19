import random
from deap import creator, base, tools, algorithms

class BackPackProblemDeap:
    """
    Решение проблемы сб укладке рюкзака.

    Проблема: найти набор грузов, который имеет наибольшую суммарную ценность так,
    чтобы его суммарный объем и масса не превосходили ограничение рюкзака.

    Для генетического алгоритма используется библиотека deap (https://github.com/DEAP/deap)

    Алгоритм основан на примере, данном в репозитории deap, который решает проблему Max One Problem
    (https://github.com/Oddsor/EvolAlgo/wiki/Max-One-Problem)
    """
    START_POPULATION_SIZE = 300
    GENERATION_COUNT = 100
    CROSSOVER_CHANCE = 0.5
    MUTATE_CHANCE = 0.1
    MUTATE_INVERT_VALUE_CHANCE = 0.05

    def __init__(self, backpack:dict) -> None:
        self._backpack = backpack
        self._itemCount = len(self._backpack["data"])
        self._toolbox = base.Toolbox()

        self._initFitness()
        self._initPopulation()
        self._initEvolutionFunctions()
        super().__init__()

    @classmethod
    def solve(cls, backpack:dict) -> dict:
        return cls(backpack)._solveProblem()

    def _solveProblem(self) -> dict:
        bestIndividual = self._execute()
        result = self._parseIndividual(bestIndividual)
        return result

    def _execute(self) -> list:
        """
        Запуск алгоритма.

        Потомок offspring - с вероятностью cxpb 2 подряд идущих в списке индивида скрещиваются
        и их дети заменяют родителей, а с вероятностью mutpb после процесса скрещивания каждый индивид мутирует.

        Далее рассчитывается ценность каждого потомка и рассчитанные ценности
        заполняют поля ценности (values) в соответствующих индивидах.

        Затем отбор нового поколения.
        В конце - выбор лучшего
        :return:
        """
        population = self._toolbox.population(n=self.START_POPULATION_SIZE)
        for gen in range(self.GENERATION_COUNT):
            offspring = algorithms.varAnd(population, self._toolbox, cxpb=self.CROSSOVER_CHANCE, mutpb=self.MUTATE_CHANCE)
            fits = self._toolbox.map(self._toolbox.evaluate, offspring)
            for fit, ind in zip(fits, offspring):
                ind.fitness.values = fit
            population = self._toolbox.select(offspring, k=len(population))
        top1 = tools.selBest(population, k=1)
        return top1[0]

    def _parseIndividual(self, individual:list) -> dict:
        """
        Перевод данных индивида в читаемый вид
        :return:
        """
        totalMass = 0.0
        totalVolume = 0.0
        totalCost = 0.0
        totalItems = list()
        for index, value in enumerate(individual):
            items = self._backpack["data"]
            if (value == 1):
                totalMass += items[index]["mass"]
                totalVolume += items[index]["volume"]
                totalCost += items[index]["cost"]
                totalItems.append(index+1)

        result = dict()
        result["value"] = totalCost
        result["weight"] = totalMass
        result["volume"] = totalVolume
        result["items"] = totalItems
        return result

    def _initFitness(self) -> None:
        """
        Создание классов для работы.
        FitnessMax - класс для проверки пригодности индивида - операции сравнения по ценности.
        Individual - индивид: список булевых значений, в котором 1 означает, что i-й груз кладется в рюкзак,
        а 0 - нет, где i - номер элемента типа Bool
        :return:
        """
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

    def _initPopulation(self) -> None:
        """
        Создание популяции, где individual - список случайных 1-0, а population - список individual
        :return:
        """
        self._toolbox.register("attr_bool", random.randint, 0, 1)
        self._toolbox.register("individual", tools.initRepeat, creator.Individual, self._toolbox.attr_bool, n=self._itemCount)
        self._toolbox.register("population", tools.initRepeat, list, self._toolbox.individual)

    def _initEvolutionFunctions(self) -> None:
        """
        evaluate - функция отбора (возвращает ценность, которая умножается на вес weight
        в fitness - функции и результат затем сравнивается с результатами других индивидов)

        mate - скрещивание по алгоритму Two-point crossover
        (https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)#Two-point_and_k-point_crossover)

        mutate - мутация - с вероятностью indpb каждое значение в списке индивида инвертируется

        select - новое поколение - выбирается 3 случайных индивида и из них выбирается лучший
        и так повторяется k раз
        :return:
        """
        self._toolbox.register("evaluate", self._evalOneMax)
        self._toolbox.register("mate", tools.cxTwoPoint)
        self._toolbox.register("mutate", tools.mutFlipBit, indpb=self.MUTATE_INVERT_VALUE_CHANCE)
        self._toolbox.register("select", tools.selTournament, tournsize=3)

    def _evalOneMax(self, individual) -> tuple:
        """
        Подсчет ценности.
        Если превышен вес или объем, ценность сходит на нет (равна 0)
        :param individual:
        :return: tuple with max cost
        """
        items = self._backpack["data"]
        totalMass = 0.0
        totalVolume = 0.0
        totalCost = 0.0
        for index, value in enumerate(individual):
            if (value==1):
                totalMass += items[index]["mass"]
                totalVolume += items[index]["volume"]
                totalCost += items[index]["cost"]
        if (totalVolume > self._backpack["capacity"] or totalMass > self._backpack["weight"]):
            return 0.0,
        return totalCost,
