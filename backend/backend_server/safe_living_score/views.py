#from asyncio.windows_events import NULL
from math import exp, log
from typing import OrderedDict

from django.http import JsonResponse
import json
#import requests_cache
#requests_cache.install_cache(expire_after=-1) #NOTE Currently cache does not expire. 
from reviews.views import getReviewList


GEOCODING_KEY = json.load(open('./API_KEYS.json'))["geocoding"]
NATIONAL_POPULATION = 329484123

CRIME_TYPES = ["all", "violent_crime", "property_crime"]

codestoState = {
    "02": "AK",
    "01": "AL",
    "05": "AR",
    "60": "AS",
    "04": "AZ",
    "06": "CA",
    "08": "CO",
    "09": "CT",
    "11": "DC",
    "10": "DE",
    "12": "FL",
    "13": "GA",
    "66": "GU",
    "15": "HI",
    "19": "IA",
    "16": "ID",
    "17": "IL",
    "18": "IN",
    "20": "KS",
    "21": "KY",
    "22": "LA",
    "25": "MA",
    "24": "MD",
    "23": "ME",
    "26": "MI",
    "27": "MN",
    "29": "MO",
    "28": "MS",
    "30": "MT",
    "37": "NC",
    "38": "ND",
    "31": "NE",
    "33": "NH",
    "34": "NJ",
    "35": "NM",
    "32": "NV",
    "36": "NY",
    "39": "OH",
    "40": "OK",
    "41": "OR",
    "42": "PA",
    "72": "PR",
    "44": "RI",
    "45": "SC",
    "46": "SD",
    "47": "TN",
    "48": "TX",
    "49": "UT",
    "51": "VA",
    "78": "VI",
    "50": "VT",
    "53": "WA",
    "55": "WI",
    "54": "WV",
    "56": "WY"
}

stateCodes = {
    "AK": "02",
    "AL": "01",
    "AR": "05",
    "AS": "60",
    "AZ": "04",
    "CA": "06",
    "CO": "08",
    "CT": "09",
    "DC": "11",
    "DE": "10",
    "FL": "12",
    "GA": "13",
    "GU": "66",
    "HI": "15",
    "IA": "19",
    "ID": "16",
    "IL": "17",
    "IN": "18",
    "KS": "20",
    "KY": "21",
    "LA": "22",
    "MA": "25",
    "MD": "24",
    "ME": "23",
    "MI": "26",
    "MN": "27",
    "MO": "29",
    "MS": "28",
    "MT": "30",
    "NC": "37",
    "ND": "38",
    "NE": "31",
    "NH": "33",
    "NJ": "34",
    "NM": "35",
    "NV": "32",
    "NY": "36",
    "OH": "39",
    "OK": "40",
    "OR": "41",
    "PA": "42",
    "PR": "72",
    "RI": "44",
    "SC": "45",
    "SD": "46",
    "TN": "47",
    "TX": "48",
    "UT": "49",
    "VA": "51",
    "VI": "78",
    "VT": "50",
    "WA": "53",
    "WI": "55",
    "WV": "54",
    "WY": "56"
}

relevant_crimes = {
    'all': {
        "violent-crime", "property-crime"
    },
    'violent_crime': {
        "violent-crime"
    },
    'property_crime': {
        "property-crime"
    }
}

#Score types: safe_living_score, violent_crime_score, property_crime_score, crime_score

# Function to retrieve all of the safe living scores
def get_score(request, city, state):
    score_list = get_safe_living_score(city, state)
    score_list["city"] = city
    score_list["state"] = state
    return JsonResponse(score_list)

def get_score_dict(city, state):
    score_list = get_safe_living_score(city, state)
    score_list["city"] = city
    score_list["state"] = state
    return score_list




# Gets the crime score for a given city and state
# City should be the full city name, state should be the abbreviation (Ex: Tulsa, OK)
def get_legacy_crime_score(city, state,
POPULATION_DATA = json.load(open('./datasets/population_data_fixed.json')),
CRIME_DATA = json.load(open('./datasets/crime_data_sorted.json')),
CITY_ORI = json.load(open('./datasets/city_ori.json')),
PROJECTED_DATA = json.load(open('./datasets/ori_future_preds.json')),
normalize_scores = True
):
    crime_numbers = {"all": [], "violent_crime": [], "property_crime": []}
    projected_crime_numbers = {"all": [], "violent_crime": [], "property_crime": []}

    can_project = True

    if state in CITY_ORI:
        if city in CITY_ORI[state]:
            if CITY_ORI[state][city]:
                for agency in CITY_ORI[state][city]:
                    crime_count = get_crime_count(agency, state, CRIME_DATA)
                    projected_crime_count = get_projected_crime_count(agency, PROJECTED_DATA)
                    for crime_type in CRIME_TYPES:
                        crime_numbers[crime_type].append(int(crime_count[crime_type]))
                        if projected_crime_count["all"] == -1 or not can_project:
                            can_project = False
                        else:
                            projected_crime_numbers[crime_type].append(int(projected_crime_count[crime_type]))
            else:
                return {"all": -1, "violent_crime": -1, "property_crime": -1, "projected_all": -1, "projected_violent_crime": -1, "projected_property_crime": -1, "error_code": 3, "error_message": "No Agencies found for specified city."}
        else:
            return {"all": -1, "violent_crime": -1, "property_crime": -1, "projected_all": -1, "projected_violent_crime": -1, "projected_property_crime": -1, "error_code": 1, "error_message": "City not found."}
    else:
        return {"all": -1, "violent_crime": -1, "property_crime": -1, "projected_all": -1, "projected_violent_crime": -1, "projected_property_crime": -1, "error_code": 4, "error_message": "State not found."}

    num_crimes = {"all": 0, "violent_crime": 0, "property_crime": 0}
    num_projected_crimes = {"all": 0, "violent_crime": 0, "property_crime": 0}
    for type in CRIME_TYPES:
        for x in crime_numbers[type]:
            num_crimes[type] += x
        for y in projected_crime_numbers[type]:
            num_projected_crimes[type] += y
        if not can_project:
            num_projected_crimes[type] = -1

    if num_crimes["all"] < 100:
        return {"all": -1, "violent_crime": -1, "property_crime": -1, "projected_all": -1, "projected_violent_crime": -1, "projected_property_crime": -1, "error_code": 5, "error_message": "Less than 100 crimes reported. Data for this city is incomplete."}

    city_population = 0

    if city in POPULATION_DATA[state]:
        city_population = int(POPULATION_DATA[state][city]["Population"])
    else:
        city_name = city
        for suffix in [" city", " City", " village", " Village"]:
            if suffix in city_name: city_name = city_name[0:city_name.find(suffix)]
        if city_name in POPULATION_DATA[state]:
            city_population = int(POPULATION_DATA[state][city_name]["Population"])
        else:
            return {"all": -1, "violent_crime": -1, "property_crime": -1, "projected_all": -1, "projected_violent_crime": -1, "projected_property_crime": -1, "error_code": 6, "error_message": "City not found."}
    
    if city_population == 0:
        return {"all": -1, "violent_crime": -1, "property_crime": -1, "projected_all": -1, "projected_violent_crime": -1, "projected_property_crime": -1, "error_code": 6, "error_message": "City not found."}
    
    #print("HI")
    national_crimes = {"all": 7765143, "violent_crime": 1313105, "property_crime": 6452038}

    #print(f'(Number of crimes: {num_crimes["all"]} / City Pop: {city_population}) / (National crimes: {national_crimes["all"]} / National Pop: {NATIONAL_POPULATION})')
    score = {"all": 0, "violent_crime": 0, "property_crime": 0}
    for crime_type in CRIME_TYPES:
        score[crime_type] = (num_crimes[crime_type] / city_population) / (national_crimes[crime_type] / NATIONAL_POPULATION)
        score[f'projected_{crime_type}'] = (num_projected_crimes[crime_type] / city_population) / (national_crimes[crime_type] / NATIONAL_POPULATION)
    
    if normalize_scores:
        vcrime1 = 0.025
        vcrime2 = 8.36
        pcrime1 = 0.18
        pcrime2 = 4.54

        p_vcrime1 = 0.035
        p_vcrime2 = 1.53
        p_pcrime1 = 0.127
        p_pcrime2 = 4.40 # 3.087
    else:
        vcrime1 = 0
        vcrime2 = 1
        pcrime1 = 0
        pcrime2 = 1

        p_vcrime1 = 0
        p_vcrime2 = 1
        p_pcrime1 = 0
        p_pcrime2 = 1

    

    if normalize_scores:
        #Test normalization
        score["violent_crime"] = (score["violent_crime"] - vcrime1) / (vcrime2 - vcrime1) * 100
        score["property_crime"] = (score["property_crime"] - pcrime1) / (pcrime2 - pcrime1) * 100
        score["all"] = (score["violent_crime"] + score["property_crime"]) / 2
        score["violent_crime"] = round(score["violent_crime"])
        score["property_crime"]= round(score["property_crime"])
        score["all"] = round(score["all"])

    # Projected Crimes Normalization
    if can_project:
        if normalize_scores:
            score["projected_violent_crime"] = (score["projected_violent_crime"] - p_vcrime1) / (p_vcrime2 - p_vcrime1) * 100
            score["projected_property_crime"] = (score["projected_property_crime"] - p_pcrime1) / (p_pcrime2 - p_pcrime1) * 100
            score["projected_all"] = (score["projected_violent_crime"] + score["projected_property_crime"]) / 2
            score["projected_violent_crime"] = round(score["projected_violent_crime"])
            score["projected_property_crime"]= round(score["projected_property_crime"])
            score["projected_all"] = round(score["projected_all"])
    else:
        score["projected_violent_crime"] = -1
        score["projected_property_crime"] = -1
        score["projected_all"] = -1
        


    if normalize_scores:
        for crime_type in CRIME_TYPES:
            if score[crime_type] < 0 or score[crime_type] > 100:
                return {"all": -1, "violent_crime": -1, "property_crime": -1, "projected_all": -1, "projected_violent_crime": -1, "projected_property_crime": -1, "error_code": 2, "error_message": "Score is out of normal range."}

    score["error_code"] = 0
    score["error_message"] = ""

    return score

# Gets the safe living score for a given city and state.
def get_safe_living_score(city, state,
POPULATION_DATA = json.load(open('./datasets/population_data_fixed.json')),
CRIME_DATA = json.load(open('./datasets/crime_data_sorted.json')),
CITY_ORI = json.load(open('./datasets/city_ori.json')), include_reviews = True,
PROJECTED_DATA = json.load(open('./datasets/ori_future_preds.json')),
normalize_scores = True
):
    #print(f'Get safe living score for {city}, {state}')
    score = get_crime_score(city, state)
    if "error_code" in score and score["error_code"] != 0:
        score["safe-living-score"] = -1
        score["projected_score"] = -1
    else:
        score["error_code"] = 0
        score["error_message"] = ""
        score["safe-living-score"] = 100 - score["all"]
    if include_reviews and score["safe-living-score"] != -1:
        reviews = getReviewList(city, state)
        if reviews:
            ALPHA = 0.2 # Reviews make up a maximum of 20% of a score
            BETA = log(0.5) / 5 # 50% closer to maximum every 5 reviews
            count = len(reviews)
            avg = sum([r.get("rating") for r in reviews]) / count
            base_score = 100 - score["all"]
            base_projected_score = 100 - score["projected_all"]
            review_score = 25 * (avg - 1)
            review_weight = -ALPHA * (exp(BETA * count) - 1)
            score["safe-living-score"] = round(review_weight * review_score + (1-review_weight) * base_score)
            score["projected_score"] = round(review_weight * review_score + (1-review_weight) * base_projected_score)
    return score

def get_crime_score(city, state,
SCORES_DATASET = json.load(open("./datasets/scores.json")),
ERROR_CHECKING = json.load(open("./datasets/score_error_check.json"))):
    if state in ERROR_CHECKING:
        if city in ERROR_CHECKING[state]:
            if "error_code" not in ERROR_CHECKING[state][city]:
                print(f'{city},{state} PROBLEM')
            elif ERROR_CHECKING[state][city]["error_code"] != 0:
                return ERROR_CHECKING[state][city]
        else:
            return {"all": -1, "violent_crime": -1, "property_crime": -1, "projected_all": -1, "projected_violent_crime": -1, "projected_property_crime": -1, "error_code": 1, "error_message": "City not found."}
    else:
        return {"all": -1, "violent_crime": -1, "property_crime": -1, "projected_all": -1, "projected_violent_crime": -1, "projected_property_crime": -1, "error_code": 4, "error_message": "State not found."}

    if state in SCORES_DATASET:
        if city in SCORES_DATASET[state]:
            result = {}
            result["all"] = round(SCORES_DATASET[state][city]["all_crime_score"])
            result["property_crime"] = round(SCORES_DATASET[state][city]["property_crime_score"])
            result["violent_crime"] = round(SCORES_DATASET[state][city]["violent_crime_score"])
            result["safe-living-score"] = round(SCORES_DATASET[state][city]["safe-living-score"])

            if "all_crime_score_projected" in SCORES_DATASET[state][city]:
                result["projected_all"] = round(SCORES_DATASET[state][city]["all_crime_score_projected"])
                result["projected_property_crime"] = round(SCORES_DATASET[state][city]["property_crime_score_projected"])
                result["projected_violent_crime"] = round(SCORES_DATASET[state][city]["violent_crime_score_projected"])
                result["projected_score"] = round(SCORES_DATASET[state][city]["safe-living-score_projected"])
            else:
                result["projected_all"] = -1
                result["projected_property_crime"] = -1
                result["projected_violent_crime"] = -1
                result["projected_score"] = -1
            return result
        else:
            return {"all": -1, "violent_crime": -1, "property_crime": -1, "projected_all": -1, "projected_violent_crime": -1, "projected_property_crime": -1, "error_code": 1, "error_message": "City not found."}
    else:
        return {"all": -1, "violent_crime": -1, "property_crime": -1, "projected_all": -1, "projected_violent_crime": -1, "projected_property_crime": -1, "error_code": 4, "error_message": "State not found."}


# Gets the number of crimes for a certain ORI
def get_crime_count(ORI, state_abbr, CRIME_DATA = json.load(open('./datasets/crime_data_sorted.json'))):
    crime_list = {}
    for city_data in CRIME_DATA[state_abbr][ORI]["results"]:
        crime_list[city_data["offense"]] = city_data["actual"]
    num_crimes = {"all": 0, "violent_crime": 0, "property_crime": 0}
    for crime_type in CRIME_TYPES:
        for city_data in relevant_crimes[crime_type]:
            if(city_data in crime_list):
                num_crimes[crime_type] += int(crime_list[city_data])

    return num_crimes

# Gets the projected number of crimes for a certain ORI
def get_projected_crime_count(ORI, PROJECTED_DATA = json.load(open('./datasets/ori_future_preds.json'))):
    if ORI not in PROJECTED_DATA:
        return {
            "all": -1,
            "violent_crime": -1,
            "property_crime": -1
        }
    return {
        "all": PROJECTED_DATA[ORI][0] + PROJECTED_DATA[ORI][1],
        "violent_crime": PROJECTED_DATA[ORI][0],
        "property_crime": PROJECTED_DATA[ORI][1]
        }


# Gets the safe living score for a given city and state.
def get_safe_living_score_legacy(city, state,
POPULATION_DATA = json.load(open('./datasets/population_data_fixed.json')),
CRIME_DATA = json.load(open('./datasets/crime_data_sorted.json')),
CITY_ORI = json.load(open('./datasets/city_ori.json')), include_reviews = True,
PROJECTED_DATA = json.load(open('./datasets/ori_future_preds.json')),
normalize_results = False
):
    #print(f'Get safe living score for {city}, {state}')
    score = get_legacy_crime_score(city, state, POPULATION_DATA, CRIME_DATA, CITY_ORI, PROJECTED_DATA, normalize_results)
    
    if "error_code" in score and score["error_code"] != 0:
        score["safe-living-score"] = -1
        score["projected_score"] = -1
    else:
        score["error_code"] = 0
        score["error_message"] = ""
        score["safe-living-score"] = 100 - score["all"]
        if score["projected_all"] != -1:
            score["projected_score"] = 100 - score["projected_all"]
        else:
            score["projected_score"] = -1
    if include_reviews and score["safe-living-score"] != -1:
        reviews = getReviewList(city, state)
        if reviews:
            ALPHA = 0.2 # Reviews make up a maximum of 20% of a score
            BETA = log(0.5) / 5 # 50% closer to maximum every 5 reviews
            count = len(reviews)
            avg = sum([r.get("rating") for r in reviews]) / count
            base_score = 100 - score["all"]
            base_projected_score = 100 - score["projected_all"]
            review_score = 25 * (avg - 1)
            review_weight = -ALPHA * (exp(BETA * count) - 1)
            score["safe-living-score"] = round(review_weight * review_score + (1-review_weight) * base_score)
            score["projected_score"] = round(review_weight * review_score + (1-review_weight) * base_projected_score)
    return score