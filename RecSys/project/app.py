import json

from RecSys.project.sugrate import UserSuggestingRate
from RecSys.project.util import parseCsv
from RecSys.project.util import getDirectorAwardsFromFilmName

rateFile = "../data/data.csv"
weeklyFile = "../data/context_day.csv"
placeFile = "../data/context_place.csv"

usersRates = parseCsv(rateFile, int)
usersDaysOfWeek = parseCsv(weeklyFile, str)
usersPlaces = parseCsv(placeFile, str)

myName = "User 5"
userSuggestion = UserSuggestingRate(myName=myName, usersRates=usersRates, usersDaysOfWeek=usersDaysOfWeek, usersPlaces=usersPlaces)
filmIndexRec = userSuggestion.recommend()
filmNumberRec = "Movie " + str(filmIndexRec+1)


filmNames = parseCsv(fileName="../data/Movie_names.csv", valueType=str, skipFirstLine=False)

filmNameRec = ""
directorInfo = ""
if filmNumberRec in filmNames.keys():
    filmNameRec = filmNames[filmNumberRec][0].strip()
    directorInfo = getDirectorAwardsFromFilmName(filmNameRec)

result = {
    "User": myName,
    "Rates forecast": userSuggestion.suggestRates(),
    "Film recommendation": filmNumberRec,
    "Film name": filmNameRec,
    "Director name": directorInfo["name"],
    "Director awards": directorInfo["awards"]
}
with open('../'+myName+'.json', 'w') as outfile:
    json.dump(obj=result, fp=outfile, indent=4)