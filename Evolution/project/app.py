import json

from Evolution.project.util import parseInput
from Evolution.project.deapusage import BackPackProblemDeap
from Evolution.project.backpackevo import BackPackProblemEvolutionSolve


dataFile = "../data/7.txt"
backpack = parseInput(dataFile)
cargoCount = len(backpack["data"])

deapSolution = BackPackProblemDeap.solve(backpack=backpack)
mySolution = BackPackProblemEvolutionSolve.solve(backpack=backpack)

result = {
    "1": deapSolution,
    "2": mySolution
}
with open('../result.json', 'w') as outfile:
    json.dump(obj=result, fp=outfile, indent=4)