# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests
from datetime import datetime, timedelta
#
#
class action_get_weather(Action):

     def name(self) -> Text:
         return "action_get_weather"
#
     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
         api_key = 'e7c0da0d1e27ebd35e173a262333b74f'
         loc = tracker.get_slot('location')
         forecastPeriod = tracker.get_slot('forecast_period')
         weatherType = tracker.get_slot('weather_type')

         response = ''
         today = datetime.now()
         tomorrow = str(today + timedelta(days=1))
         next2Day = str(today  + timedelta(days=2))
         print(tomorrow)
         print(next2Day)
         
         if not loc:
             response = "May i know for which location"
         else:
            dispatcher.utter_message(text=f'Do you mean {loc}, right?')
            #get coordinates
            coordinates = requests.get('http://api.openweathermap.org/geo/1.0/direct?q={}&limit=1&appid={}'.format(loc, api_key)).json()
            lat = round(coordinates[0]['lat'], 2)
            lon = round(coordinates[0]['lon'], 2)
            #get weather with coordinates
            if coordinates:
                weathers = requests.get('http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'.format(lat,lon, api_key)).json()
                current = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(loc, api_key)).json()
                country = weathers['city']['country']
                city = loc

                if weathers:
                    if forecastPeriod is None or forecastPeriod == 'today':
                    ##current
                        conditionCurrent = current['weather'][0]['main'    ]
                        temperature_cCurrent = round(current['main']['temp'] - 273.15, 2)
                        feelLike =  round(current['main']['feels_like'] - 273.15, 2)
                        humidityCurrent = current['main']['humidity']
                        wind_mphCurrent = current['wind']['speed']

                        if weatherType is None or weatherType == 'weather':
                            response = """It is currently {} in {} at the moment. The temperature is {} degrees in C, feel like {}, the humidity is {}% and the wind speed is {} mph.""".format(conditionCurrent, city, temperature_cCurrent, feelLike, humidityCurrent, wind_mphCurrent)
                        elif weatherType == 'temperature':
                            response = """The current temperature is {} degrees in C, feel like {}""".format(temperature_cCurrent, feelLike)
                        elif weatherType == 'humidity':
                            response = """The humidity now is {}%""".format(humidityCurrent)
                        elif weatherType == 'wind':
                            response =  """The wind today is {} mph with deg is {} and gust is {}""".format(wind_mphCurrent, current['wind']['deg'], current['wind']['gust'])
                    elif forecastPeriod == 'tomorrow':
                        ##tomorrow
                        tomorrows = [item for item in weathers['list'] if tomorrow[0:10] in item['dt_txt']]
                        morning = [item for item in tomorrows if item['dt_txt'][11:] == '09:00:00']
                        afternoon = [item for item in tomorrows if item['dt_txt'][11:] == '15:00:00']
                        evening = [item for item in tomorrows if item['dt_txt'][11:] == '21:00:00']
                        if weatherType is None or weatherType == 'weather':
                            response = """The weater tomorrow in {}: 
    - Morning will be {} with {}: temperature is {} degrees, the humidity is {}% and the wind speed is {} mph.
    - Afternoon will feel {} with {}: temperature is {} degrees, the humidity is {}% and the wind speed is {} mph.
    - Evening will like {} with {}: temperature is {} degrees, the humidity is {}% and the wind speed is {}mph.
    """.format(city, morning[0]['weather'][0]['main'], morning[0]['weather'][0]['description'], round(morning[0]['main']['temp'] - 273.15,2), morning[0]['main']['humidity'], morning[0]['wind']['speed'], afternoon[0]['weather'][0]['main'], afternoon[0]['weather'][0]['description'], round(afternoon[0]['main']['temp'] - 273.15,2), afternoon[0]['main']['humidity'], afternoon[0]['wind']['speed'], evening[0]['weather'][0]['main'], evening[0]['weather'][0]['description'], round(evening[0]['main']['temp'] - 273.15,2), evening[0]['main']['humidity'], evening[0]['wind']['speed'])
                        elif weatherType == 'temperature':
                            response = """The temperature in the next day morning is {} degrees in C, in afternoon is {} and in the evening is {}""".format(round(morning[0]['main']['temp'] - 273.15,2), round(afternoon[0]['main']['temp'] - 273.15,2), round(evening[0]['main']['temp'] - 273.15,2))
                        elif weatherType == 'humidity':
                            response = """The humidity tomorrow is {}% in morning, {}% in afternoon and the evening is {}%""".format(morning[0]['main']['humidity'], afternoon[0]['main']['humidity'], evening[0]['main']['humidity'])
                        elif weatherType == 'wind':
                            response =  """The wind today is {} mph with deg is {} and gust is {} in the morning, is {} mph with deg is {} and gust is {} in the afternoon and last {} mph with deg is {} and gust is {} in the evening""".format(morning[0]['wind']['speed'],  morning[0]['wind']['deg'], morning[0]['wind']['gust'], afternoon[0]['wind']['speed'], afternoon[0]['wind']['deg'], afternoon[0]['wind']['gust'], evening[0]['wind']['speed'], evening[0]['wind']['deg'], evening[0]['wind']['gust'])
                        
                    elif forecastPeriod == 'next 2 days':
                        ##next 2 days 
                        next2Days = [item for item in weathers['list'] if next2Day[0:10] in item['dt_txt']]
                        morning = [item for item in next2Days if item['dt_txt'][11:] == '09:00:00']
                        afternoon = [item for item in next2Days if item['dt_txt'][11:] == '15:00:00']
                        evening = [item for item in next2Days if item['dt_txt'][11:] == '21:00:00']

                        if weatherType is None or weatherType == 'weather':
                            response = """The weater next 2 days in {}: 
    - Morning will be {} with {}: temperature is {} degrees, the humidity is {}% and the wind speed is {} mph.
    - Afternoon will feel {} with {}: temperature is {} degrees, the humidity is {}% and the wind speed is {} mph.
    - Evening will like {} with {}: temperature is {} degrees, the humidity is {}% and the wind speed is {}mph.
    """.format(city, morning[0]['weather'][0]['main'], morning[0]['weather'][0]['description'], round(morning[0]['main']['temp'] - 273.15,2), morning[0]['main']['humidity'], morning[0]['wind']['speed'], afternoon[0]['weather'][0]['main'], afternoon[0]['weather'][0]['description'], round(afternoon[0]['main']['temp'] - 273.15,2), afternoon[0]['main']['humidity'], afternoon[0]['wind']['speed'], evening[0]['weather'][0]['main'], evening[0]['weather'][0]['description'], round(evening[0]['main']['temp'] - 273.15,2), evening[0]['main']['humidity'], evening[0]['wind']['speed'])
                        elif weatherType == 'temperature':
                            response = """The temperature in the next day after tomorrow morning is {} degrees in C, in afternoon is {} and in the evening is {}""".format(round(morning[0]['main']['temp'] - 273.15,2), round(afternoon[0]['main']['temp'] - 273.15,2), round(evening[0]['main']['temp'] - 273.15,2))
                        elif weatherType == 'humidity':
                            response = """The humidity next 2 days is {}% in morning, {}% in afternoon and the evening is {}%""".format(morning[0]['main']['humidity'], afternoon[0]['main']['humidity'], evening[0]['main']['humidity'])
                        elif weatherType == 'wind':
                            response =  """The wind next two days is {} mph with deg is {} and gust is {} in the morning, is {} mph with deg is {} and gust is {} in the afternoon and last {} mph with deg is {} and gust is {} in the evening""".format(morning[0]['wind']['speed'],  morning[0]['wind']['deg'], morning[0]['wind']['gust'], afternoon[0]['wind']['speed'], afternoon[0]['wind']['deg'], afternoon[0]['wind']['gust'], evening[0]['wind']['speed'], evening[0]['wind']['deg'], evening[0]['wind']['gust'])
                    else: 
                        response = """sorry, I can only forecast the weather within 2 days"""
                else:
                    response = """sorry, i can't get weather from OpenWeatherApi"""

            else:
                response = """sorry, i can't get coordinates from OpenWeatherApi"""
         
         dispatcher.utter_message(response)
         return [SlotSet('location', loc)]
