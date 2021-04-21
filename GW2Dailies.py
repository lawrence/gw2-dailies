import json
import requests

# Returns an API url with a list of all wanted achievementIDs
def getIDs(time,eventType):

    # Some spicy defensive programming:
    allowedTime = ["now","tom"]
    if time not in allowedTime:
        print("Invalid time (first arg)/n")
        return

    allowedEvents = ["pve","pvp","wvw","fractals"]
    if eventType not in allowedEvents:
        print("Invalid event (second arg)/n")
        return

    # Depending on what you give into the time, you can get the fractals for today or tomorrow":
    if time == "now":
        dailiesResponse = requests.get("https://api.guildwars2.com/v2/achievements/daily")
    if time == "tom":
        dailiesResponse = requests.get("https://api.guildwars2.com/v2/achievements/daily/tomorrow")

    # Retrieves the request and pipes it as json:
    dailiesResponse = dailiesResponse.json()

    # Retrieves all the achievement IDs for event:
    achievoIDs = ""
    for event in dailiesResponse[eventType]:
        achievoIDs += str(event["id"]) + ","

    # Trailing "," from loop above:
    achievoList = "https://api.guildwars2.com/v2/achievements?ids="+achievoIDs[0:-1]
    return achievoList

# Returns an array of arrays w/ http status_code:
    # [0] = status_code
    # [1] = (A): fractal recs (scale: name)
    # [2] = (A): fractal dailies (t1-4)

def getFractals(fractalsURL,which):
    # Retrieves the URL request and pipes it as json:
    fractalsResponse = requests.get(fractalsURL)
    fractalsResponseJSON = fractalsResponse.json()

    fractalDailies = []
    fractalRecs = []

    # The return array that is an array of the arrays for dailies and recs
    fractalEvents = []
    fractalEvents.append(fractalsResponse.status_code)

    for fractals in fractalsResponseJSON:
        if which == "both":
            if "Daily Recommended" in fractals["name"]:
                fractalRecs.append(fractals["name"][32:])

            if "Daily Tier 4" in fractals["name"]:
                fractalDailies.append(fractals["name"][13:])

        if which == "dailies":
            if "Daily Tier 4" in fractals["name"]:
                fractalDailies.append(fractals["name"][13:])

        if which == "recs":
            if "Daily Recommended" in fractals["name"]:
                fractalRecs.append(fractals["name"][32:])

    # Naming the scales:
    if which == "recs" or which == "both":
        namedScales = getScales(fractalRecs)
        fractalEvents.append(namedScales)

    if which == "dailies" or which == "both":
        fractalEvents.append(fractalDailies)

    # Index 0: http status_code (for debugging)
    # (WHEN which == BOTH)
        # Index 1: fractal recs
        # Index 2: fractal dailies

    return fractalEvents

# Returns an array w/ http status_code in index 0 and the rest as names or descriptions of other dailies besides fractals
def getEvents(gw2URL,descriptor):
    # Some more defensive programming:
    allowedDesc = ["name","requirement"]
    if descriptor not in allowedDesc:
        print("Invalid descriptor (arg 2)\n")
        return

    # Retrieves the URL request and pipes it as json:
    eventsResponse = requests.get(gw2URL)
    eventsResponseJSON = eventsResponse.json()

    # Array of names or requirements of dailies (Index 0 is http status code):
    dailies = []
    dailies.append(eventsResponse.status_code)

    for event in eventsResponseJSON:
        dailies.append(event[descriptor])

    return dailies

# Dictionary object containing all scales (only used in getScales()):
scalesDict = {
    "1": "Volcanic",
    "2": "Uncategorized",
    "3": "Snowblind",
    "4": "Urban Battleground",
    "5": "Swampland",
    "6": "Cliffside",
    "7": "Aquatic Ruins",
    "8": "Underground Facility",
    "9": "Molten Furnace",
    "10": "Molten Boss",
    "11": "Deepstone",
    "12": "Siren's Reef",
    "13": "Chaos Isles",
    "14": "Aetherblade",
    "15": "Thaumanova Reactor",
    "16": "Twilight Oasis",
    "17": "Swampland",
    "18": "Captain Mai Trin Boss",
    "19": "Volcanic",
    "20": "Solid Ocean",
    "21": "Cliffside",
    "22": "Molten Furnace",
    "23": "Nightmare",
    "24": "Shattered Observatory",
    "25": "Sunqua Peak",
    "26": "Aquatic Ruins",
    "27": "Snowblind",
    "28": "Volcanic",
    "29": "Underground Facility",
    "30": "Chaos Isles",
    "31": "Urban Battleground",
    "32": "Swampland",
    "33": "Deepstone",
    "34": "Thaumanova Reactor",
    "35": "Solid Ocean",
    "36": "Uncategorized",
    "37": "Siren's Reef",
    "38": "Chaos Isles",
    "39": "Molten Furnace",
    "40": "Molten Boss",
    "41": "Twilight Oasis",
    "42": "Captain Mai Trin Boss",
    "43": "Thaumanova Reactor",
    "44": "Uncategorized",
    "45": "Solid Ocean",
    "46": "Aetherblade",
    "47": "Cliffside",
    "48": "Nightmare",
    "49": "Shattered Observatory",
    "50": "Sunqua Peak",
    "51": "Snowblind",
    "52": "Volcanic",
    "53": "Underground Facility",
    "54": "Siren's Reef",
    "55": "Thaumanova Reactor",
    "56": "Swampland",
    "57": "Urban Battleground",
    "58": "Molten Furnace",
    "59": "Twilight Oasis",
    "60": "Solid Ocean",
    "61": "Aquatic Ruins",
    "62": "Uncategorized",
    "63": "Chaos Isles",
    "64": "Thaumanova Reactor",
    "65": "Aetherblade",
    "66": "Urban Battleground",
    "67": "Deepstone",
    "68": "Snowblind",
    "69": "Cliffside",
    "70": "Molten Boss",
    "71": "Aetherblade",
    "72": "Captain Mai Trin Boss",
    "73": "Nightmare",
    "74": "Shattered Observatory",
    "75": "Sunqua Peak",
    "76": "Aquatic Ruins",
    "77": "Swampland",
    "78": "Siren's Reef",
    "79": "Uncategorized",
    "80": "Solid Ocean",
    "81": "Underground Facility",
    "82": "Thaumanova Reactor",
    "83": "Molten Furnace",
    "84": "Deepstone",
    "85": "Urban Battleground",
    "86": "Snowblind",
    "87": "Twilight Oasis",
    "88": "Chaos Isles",
    "89": "Swampland",
    "90": "Molten Boss",
    "91": "Uncategorized",
    "92": "Volcanic",
    "93": "Snowblind",
    "94": "Cliffside",
    "95": "Captain Mai Trin Boss",
    "96": "Aetherblade",
    "97": "Chaos Isles",
    "98": "Nightmare",
    "99": "Shattered Observatory",
    "100": "Sunqua Peak",
}

# Returns a new array of scales with their respective scale names (only used in getFractals())
def getScales(scales):
    newScales = []
    # Looks up scale numbers in scaleDict and finds the correct fractal:
    for scale in scales:
        newScales.append(str(scale)+": " + scalesDict[scale])

    return newScales

# getIDs(time,eventType): [now,tom] , [pve,pvp,wvw,fractals]
# getEvents(gw2URL, descriptor): [url from getIDs()] , [name,requirement]
# getFractals(fractalsURL): [url from getIDs]
# getScales(scales): [list of scales from getFractals[2]]

today_fractals = getFractals(getIDs("now","fractals"),"both")
tom_fractals = getFractals(getIDs("tom","fractals"),"both")

print("\n Today's RECs:\n =============")
for d in today_fractals[1]:
    print("\t"+d)

print("\n Today's Dailies:\n ================")
for d in today_fractals[2]:
    print("\t"+d)

print("\n\n Tommorrow's RECs:\n =============")
for t in tom_fractals[1]:
    print("\t"+t)

print("\n Tommorrow's Dailies:\n ================")
for t in tom_fractals[2]:
    print("\t"+t)

input('\n Press ENTER to exit')
