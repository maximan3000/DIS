import json

from RecSys.project.sugrate import UserSuggestingRate
from RecSys.project.util import parseCsv

rateFile = "../data/data.csv"
weeklyFile = "../data/context_day.csv"
placeFile = "../data/context_place.csv"

usersRates = parseCsv(rateFile, int)
usersDaysOfWeek = parseCsv(weeklyFile, str)
usersPlaces = parseCsv(placeFile, str)

myName = "User 1"
userSuggestion = UserSuggestingRate(myName=myName, usersRates=usersRates, usersDaysOfWeek=usersDaysOfWeek, usersPlaces=usersPlaces)
result = {
    "User": myName,
    "Rates forecast": userSuggestion.suggestRates(),
    "Film recommendation": "Movie " + str(userSuggestion.recommend())
}
with open('../'+myName+'.json', 'w') as outfile:
    json.dump(obj=result, fp=outfile, indent=4)