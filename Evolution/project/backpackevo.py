import random

class BackPackProblemEvolutionSolve:
    """
    Решение проблемы об укладке рюкзака.

    Проблема: найти набор грузов, который имеет наибольшую суммарную ценность так,
    чтобы его суммарный объем и масса не превосходили ограничение рюкзака.

    Индивид - список булевых значений, в котором 1 означает, что i-й груз кладется в рюкзак,
    а 0 - нет, где i - номер элемента типа Bool
    """
    POPULATION_SIZE = 200
    GENERATION_COUNT = 500
    CROSSOVER_CHANCE = 0.5

    class Individual:
        def __init__(self) -> None:
            super().__init__()
            self.values = list()
            self.cost = float()
            self.isOld = bool()

    def __init__(self, backpack:dict) -> None:
        super().__init__()
        self._backpack = backpack
        self._itemCount = len(self._backpack["data"])
        self._population = list()
        self._bestIndividual = self.Individual()

    @classmethod
    def solve(cls, backpack:dict) -> dict:
        """
        Решить задачу укладки рюкзака для данных backpack:
            * weight - вместимость рюкзака по массе
            * capacity - вместимость рюкзака по объему
            * data - список вещей:
                * mass - масса вещи
                * volume - объем вещи
                * cost - ценность вещи

        :param backpack:
        :return: словарь, в котором есть значения массы, объема, стоимости и номера предметов, которые нужно положить в рюкзак (смотреть _parseIndividual)
        """
        return cls(backpack)._solveProblem()

    def _solveProblem(self) -> dict:
        bestIndividual = self._execute()
        result = self._parseIndividual(bestIndividual)
        return result

    def _execute(self) -> Individual:
        """
        Запуск алгоритма. Эволюция поколений.
        Оценка результата - наступила сходимость, если функция приспособленности лучшей
        особи в популяциях отличается не более, чем на 10%, или прошло 500 поколений

        :return: лучший индивид в последнем поколении
        """
        self._population = self._initPopulation()

        self._bestIndividual.cost = -1
        for generation in range(0,self.GENERATION_COUNT):
            self._globalCrossover()
            self._mutate()
            self._selection()
            pastBestIndividual = self._bestIndividual
            self._bestIndividual = self._getNBest(1)[0]
            #if (min(pastBestIndividual.cost, self._bestIndividual.cost)/
            #        max(pastBestIndividual.cost, self._bestIndividual.cost) > 0.9):
            #    break
            # 10% отличия - плохая идея, так как рост неравномерный и в некоторых поколениях его не будет

        return self._bestIndividual

    def _initPopulation(self) -> list:
        """
        Инициализация популяции

        :return: список индивидов
        """
        population = list()
        for indnum in range(0, self.POPULATION_SIZE):
            individual = self._generateIndividual()
            population.append(individual)
        return population

    def _generateIndividual(self) -> Individual:
        """
        Генерация индивида - случайная генерация

        :return: структура со списком из случайных значений 0-1
        """
        individual = self.Individual()
        for i in range(0, self._itemCount):
            randVal = random.randint(0,1)
            individual.values.append(randVal)
        individual.cost = self._getIndividualCost(individual)
        individual.isOld = True
        return individual

    def _getIndividualCost(self, individual:Individual) -> float:
        """
        Подсчет ценности.
        Если превышен вес или объем, ценность сходит на нет (равна 0)
        :param individual:
        :return: float - ценность индивида
        """
        items = self._backpack["data"]
        totalMass = 0.0
        totalVolume = 0.0
        totalCost = 0.0
        for index, value in enumerate(individual.values):
            if (value==1):
                totalMass += items[index]["mass"]
                totalVolume += items[index]["volume"]
                totalCost += items[index]["cost"]
        if (totalVolume > self._backpack["capacity"] or totalMass > self._backpack["weight"]):
            return 0.0
        return totalCost

    def _globalCrossover(self) -> None:
        """
        Скрещивание особей популяции экземпляра - каждая особь скрещивается 1 раз за 1 поколение

        :return: добавление потомков к популяции
        """
        population = self._selectionForCrossover()
        offspring = list()
        for index in range(0,len(population)-1,2):
            parent1 = population[index]
            parent2 = population[index+1]
            children = self._crossover(parent1, parent2)
            offspring.append(children[0])
            offspring.append(children[1])

        self._population.extend(offspring)

    def _selectionForCrossover(self) -> list:
        """
        Отбор особей для скрещивания - выбор каждой особи пропорционально приспособленности (рулетка)

        :return: список особей для скрещивания
        """
        totalCost = self._getPopulationTotalCost()
        populationCrossover = list()
        for index, individual in enumerate(self._population):
            probability = individual.cost/totalCost
            roulette = random.random()
            if (probability <= roulette):
                populationCrossover.append(individual)
        return populationCrossover

    def _getPopulationTotalCost(self) -> float:
        """
        Расчет общей стоимости (приспособленности) индивидов

        :return: сумма значений приспособленности
        """
        cost = 0.0
        for index, individual in enumerate(self._population):
            cost += individual.cost
        return cost

    def _crossover(self, parent1:Individual, parent2:Individual) -> tuple:
        """
        Скрещивание особей - 1 пара дает 2 потомка, метод - однородный (каждый бит от случайно выбранного родителя)

        :param parent1:
        :param parent2:
        :return: кортеж 2х элементов - потомков родителей
        """
        child1 = self.Individual()
        child2 = self.Individual()
        for index, (value1, value2) in enumerate(zip(parent1.values, parent2.values)):
            roulette = random.random()
            if (self.CROSSOVER_CHANCE <= roulette):
                child1.values.insert(index,value1)
                child2.values.insert(index,value2)
            else:
                child1.values.insert(index,value2)
                child2.values.insert(index,value1)
        child1.cost = self._getIndividualCost(child1)
        child1.isOld = False
        child2.cost = self._getIndividualCost(child2)
        child2.isOld = False
        return child1, child2

    def _mutate(self) -> None:
        """
        Мутация - инвертирование всех битов у 1 особи

        :return: изменение (мутация) особи из популяции
        """
        indexOfLastInduvudual = len(self._population) - 1
        randomIndex = random.randint(0, indexOfLastInduvudual)
        individual = self._population.pop(randomIndex)

        for index, value in enumerate(individual.values):
            individual.values[index] = 1 if value==0 else 0
        individual.cost = self._getIndividualCost(individual)

    def _selection(self) -> None:
        """
        Формирование новой популяции (количество особей - константа)
        метод - «штраф» за «старость» -20% функции приспособленности, выбор лучших

        :return: в популяции остаются только POPULATION_SIZE лучших индивидов
        """
        map(self._penalty, enumerate(self._population))
        self._population = self._getNBest(self.POPULATION_SIZE)

    def _penalty(self, individual:Individual):
        """
        «штраф» -20% функции приспособленности

        :param individual:
        :return: индивид с уменьшенной ценностью
        """
        if (individual.isOld):
            individual.cost *= 0.8
        return individual

    def _parseIndividual(self, individual:Individual) -> dict:
        """
        Перевод данных индивида в читаемый вид - словарь вида:
            * value - суммарная ценность вещей в рюкзаке
            * weight - вес вещей в рюкзаке
            * volume - объем, занимаемый вещами
            * items - список номеров вещей, что лежат в рюкзаке

        :param individual:
        :return:
        """
        totalMass = 0.0
        totalVolume = 0.0
        totalCost = 0.0
        totalItems = list()
        for index, value in enumerate(individual.values):
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

    def _getNBest(self, n:int) -> list:
        """
        Возвращает n лучших особей
        :param n:
        :return: список особей
        """
        population = self._population
        population.sort(key=lambda x: x.cost, reverse=True)
        return population[0:n]
