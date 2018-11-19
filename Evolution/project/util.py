import csv

def parseInput(fileName: str) -> dict:
    result = dict()
    result["data"] = list()

    with open(file=fileName, encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=" ")
        fileLines = list(reader)
        globalParameters = fileLines.pop(0)
        result["weight"] = float(globalParameters[0])
        result["capacity"] = float(globalParameters[1])

    for line in fileLines:
        values = dict()
        values["mass"] = float(line[0])
        values["volume"] = float(line[1])
        values["cost"] = float(line[2])

        result["data"].append(values)

    return result
