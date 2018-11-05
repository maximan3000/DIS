import csv

def parseCsv(fileName: str, valueType: type) -> dict:
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        fileLines = list(reader)

    result = dict()
    for line in fileLines:
        values = list()
        for value in line[1:len(line)]:
            values.append(valueType(value))
        result[line[0]] = values

    return result