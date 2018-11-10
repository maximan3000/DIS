import csv
from SPARQLWrapper import SPARQLWrapper, JSON

def getDirectorAwardsFromFilmName(filmName: str) -> dict:
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery("""SELECT ?directorLabel ?awardLabel
    WHERE {
      ?film wdt:P31 wd:Q11424.
      ?film wdt:P1476 ?title.
      """ + f"""FILTER regex(?title, "^{filmName}"). """ + """
      ?film wdt:P57 ?director.
      ?director wdt:P166 ?award.

      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    """)
    sparql.setReturnFormat(JSON)
    queryResults = sparql.query().convert()["results"]["bindings"]

    results = dict()
    results["name"] = queryResults[0]["directorLabel"]["value"]
    results["awards"] = list()

    for award in queryResults:
        results["awards"].append(award["awardLabel"]["value"])

    return results

def parseCsv(fileName: str, valueType: type, skipFirstLine: bool = True ) -> dict:
    result = dict()

    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile)
        if (skipFirstLine):
            next(reader)
        fileLines = list(reader)

    for line in fileLines:
        values = list()
        for value in line[1:len(line)]:
            values.append(valueType(value))
        result[line[0]] = values

    return result