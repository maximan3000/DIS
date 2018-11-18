import json
import random

from Evolution.project.util import parseInput
# Для генетического алгоритма используется библиотека deap (https://github.com/DEAP/deap)
from deap import creator, base, tools, algorithms

# Алгоритм основан на примере, данном в репозитории deap, который решает проблему Max One Problem (https://github.com/Oddsor/EvolAlgo/wiki/Max-One-Problem)

dataFile = "../data/7.txt"
backpack = parseInput(dataFile)
cargoCount = len(backpack["data"])

# Фитнесс - класс (класс для проверки пригодности индивида - операции сравнения по ценности)
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
# То, что считаем индивидом - последовательность (список) булевых значений,
# в которой 1 означает, что i-й груз кладется в рюкзак, а 0 - нет,
# где i - номер элемента типа Bool
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Создание популяции, где individual - список случайных 1-0, а population - список individual
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=cargoCount)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMax(individual):
    # Подсчет ценности.
    # Если превышен вес или объем, ценность сходит на нет (равна 0)
    cargo = backpack["data"]
    totalMass = 0.0
    totalVolume = 0.0
    totalCost = 0.0
    for index, value in enumerate(individual):
        if (value==1):
            totalMass += cargo[index]["mass"]
            totalVolume += cargo[index]["volume"]
            totalCost += cargo[index]["cost"]
    if (totalVolume > backpack["capacity"] or totalMass > backpack["weight"]):
        return 0.0,
    return totalCost,

# evaluate - функция отбора (возвращает ценность, которая умножается на вес weight
# в fitness - функции и результат затем сравнивается с результатами других индивидов)
# evaluate - скрещивание по алгоритму Two-point crossover
# (https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)#Two-point_and_k-point_crossover)
# mutate - мутация - с вероятностью indpb каждое значение в списке индивида инвертируется
# select - новое поколение - выбирается 3 случайных индивида и из них выбирается лучший
# и так повторяется k раз
toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

population = toolbox.population(n=300)

# запуск алгоритма - эволюция NGEN поколений
NGEN=40
for gen in range(NGEN):
    # потомки - с вероятностью cxpb 2 подряд идущих в списке индивида скрещиваются
    # и их дети заменяют родителей, а с вероятностью mutpb после процесса скрещивания
    # каждый индивид мутирует
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
    # рассчитывается ценность каждого потомка
    fits = toolbox.map(toolbox.evaluate, offspring)
    # рассчитанные ценности заполняют поля ценности в соответствующих индивидах
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
    # отбор нового поколения
    population = toolbox.select(offspring, k=len(population))

# k лучших индивидов в последнем поколении
top10 = tools.selBest(population, k=10)
print(*top10, sep ="\n")
print("\n")

for indexValues, values in enumerate(top10):
    totalMass = 0.0
    totalVolume = 0.0
    totalCost = 0.0
    for index, value in enumerate(values):
        cargo = backpack["data"]
        if (value == 1):
            totalMass += cargo[index]["mass"]
            totalVolume += cargo[index]["volume"]
            totalCost += cargo[index]["cost"]
    print(f"mass = {totalMass}; volume = {totalVolume}; cost = {totalCost} \n")