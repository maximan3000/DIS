import json

from Evolution.project.util import parseInput
from Evolution.project.deapusage import BackPackProblemDeap


dataFile = "../data/7.txt"
backpack = parseInput(dataFile)
cargoCount = len(backpack["data"])

problemDeapSolution = BackPackProblemDeap.solve(backpack=backpack)

result = {
    "1": problemDeapSolution,
    "2": {}
}
with open('../result.json', 'w') as outfile:
    json.dump(obj=result, fp=outfile, indent=4)