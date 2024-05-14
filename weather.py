import requests
# import datetime as dt
from sshhhh import WEATHER_API_KEY

BASE_URL = "http://api.weatherapi.com/v1/current.json?key="

def weather(loc):
    URL = BASE_URL + WEATHER_API_KEY + "&q=" + loc + "&aqi=yes"
    response = requests.get(URL).json()
    if 'error' in response.keys():
        return f"Weather confidential and can't be disclosed!"
    # we can even use the dictionary of the .json file we requested i.e "response"
    data = {"temperature" : response["current"]["temp_c"],
        "sky" :  response["current"]["condition"]["text"],
        "region" : response["location"]["region"],
        "country" : response["location"]["country"],
        "localTime" : response["location"]["localtime"].split()[1],
        'localDate' : response["location"]["localtime"].split()[0],
        "windSpeed" : response["current"]["wind_kph"], # wind speed in Kmph
        "humidity" : response["current"]["humidity"],
        "airQualityGbDefraIndex" : response["current"]["air_quality"]["gb-defra-index"]}

    # gb defra index: refer https://uk-air.defra.gov.uk/air-pollution/daqi
    air_quality_risk = "LOW" if 1<=data["airQualityGbDefraIndex"]<=5 else ("MODERATE" if 4<=data["airQualityGbDefraIndex"]<=6 else ("HIGH" if 7<=data["airQualityGbDefraIndex"]<=9 else "VERY HIGH"))
    # adding the variable to the dictionary
    # data["air_quality_risk"] = air_quality_risk

    weather_para = f"""Weather details of {loc.capitalize()}, {data['region']}, {data['country']}:
-> The local time is {data['localTime']} and the date is {data['localDate']}
-> The sky is {data['sky']}
-> The temperature is {data['temperature']} Celcius
-> Wind is running at {data["windSpeed"]} Kmph
-> Humidity is {data["humidity"]}
-> Air quality risk is {air_quality_risk}
    """

    return weather_para
    # return what_to_return(data, air_quality_risk, loc, parameter)

def what_to_return(data, air_quality_risk, loc, parameter):

    weather_para =  f"""Weather details of {loc.capitalize()}, {data['region']}, {data['country']}:
-> The local time is {data['localTime']} and the date is {data['localDate']}
-> The sky is {data['sky']}
-> The temperature is {data['temperature']} Celcius
-> Wind is running at {data["windSpeed"]} Kmph
-> Humidity is {data["humidity"]}
-> Air quality risk is {air_quality_risk}
"""

    # can be merged with the data dictionary in the weather() program
    weather_parameters = {"weather" : weather_para,
                  'temperature' : f'The temperature in {loc.capitalize()} is {data["temperature"]} Celcius',
                  'sky' : f"The sky in {loc.capitalize()} is {data['sky']}",
                  'region' : f"{loc.capitalize()} is in {data['region'].capitalize()} region",
                  'country' : f"{loc.capitalize()} is in {data['country'].capitalize()}",
                  'local_Time' : f"The local time in {loc.capitalize()} is {data['localTime']}",
                  'time' : f"The local time in {loc.capitalize()} is {data['localTime']}",
                  'local_Date' : f"The local date in {loc.capitalize()} is {data['localDate']}",
                  'date' : f"The local date in {loc.capitalize()} is {data['localDate']}",
                  'wind_Speed' : f"Wind speeds in {loc.capitalize()} is {data['windSpeed']}",
                  'humidity' : f"Humidity in {loc.capitalize()} is {data['humidity']}",
                  'air_Quality' : f"Air pollution in {loc.capitalize()} is {air_quality_risk.capitalize()}"}

    return weather_parameters[parameter]