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

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
         api_key = 'e7c0da0d1e27ebd35e173a262333b74f'
         loc = tracker.get_slot('location')
         forecastPeriod = tracker.get_slot('forecast_period')
         weatherType = tracker.get_slot('weather_type')
         guess = tracker.get_slot('guess')
         
         response = ''
         today = datetime.now()
         tomorrow = str(today + timedelta(days=1))
         next2Day = str(today  + timedelta(days=2))
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
                        conditionDesc = current['weather'][0]['description'    ]
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
                        elif weatherType == 'sunny':
                            if conditionCurrent == 'Rain':
                                response = f"""No, today is not sunny, it {conditionDesc}"""
                            if conditionDesc == 'clear sky':
                                response = """Yes, the weather today is sunny, you should use suncreen if you want to go out 😉"""
                            elif conditionDesc == 'few clouds' or conditionDesc =='scattered clouds':
                                response = """Hmmm, it's not exactly sunny today, maybe a little because there are scattered clouds today 😉"""
                            else:
                                response = f"""No, today is not sunny, it {conditionDesc}"""
                        elif weatherType == 'rain':
                            if conditionCurrent == 'Rain':
                                if conditionDesc ==  'light rain':
                                    response = """Yes, The weather today is rain but it is light rain, you may be bring umbrella ☔"""
                                elif conditionDesc == 'moderate rain':
                                    response = """Yes, The weather today is rain with moderate rain, you should bring a raincoat and move carefully if you go out 😭"""
                                else:
                                    response = """Yes, The weather today is rain, you should bring a raincoat and move carefully if you go out 😭"""
                            elif conditionCurrent == "Clouds":
                                if conditionDesc == 'broken clouds' or conditionDesc == 'overcast clouds':
                                    response = f"""Today's weather is likely to be rainy with {conditionDesc}, you should bring umbrella"""
                                else:
                                    response = f"""No, today is not rain, it is {conditionDesc}"""   
                            else:
                                response = f"""No, today is not rain, it is {conditionDesc}"""   
                    elif forecastPeriod == 'tomorrow':
                        ##tomorrow
                        tomorrows = [item for item in weathers['list'] if tomorrow[0:10] in item['dt_txt']]
                        morning = [item for item in tomorrows if item['dt_txt'][11:] == '09:00:00']
                        afternoon = [item for item in tomorrows if item['dt_txt'][11:] == '15:00:00']
                        evening = [item for item in tomorrows if item['dt_txt'][11:] == '21:00:00']
                        conditionCurrent =  afternoon[0]['weather'][0]['main']
                        conditionDesc =  afternoon[0]['weather'][0]['description']
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
                            response =  """The wind tomorrow is {} mph with deg is {} and gust is {} in the morning, is {} mph with deg is {} and gust is {} in the afternoon and the last: {} mph with deg is {} and gust is {} in the evening""".format(morning[0]['wind']['speed'],  morning[0]['wind']['deg'], morning[0]['wind']['gust'], afternoon[0]['wind']['speed'], afternoon[0]['wind']['deg'], afternoon[0]['wind']['gust'], evening[0]['wind']['speed'], evening[0]['wind']['deg'], evening[0]['wind']['gust'])
                        elif weatherType == 'sunny':
                            if conditionCurrent == 'Rain':
                                response = f"""No, tomorrow is not sunny, it {conditionDesc}"""
                            if conditionDesc == 'clear sky':
                                response = """Yes, the weather tomorrow is sunny, you should use suncreen if you want to go out 😉"""
                            elif conditionDesc == 'few clouds' or conditionDesc =='scattered clouds':
                                response = """Hmmm, it's not exactly sunny tomorrow, maybe a little because there are scattered clouds 😉"""
                            else:
                                response = f"""No, the next day is not sunny, it {conditionDesc}"""
                        elif weatherType == 'rain':
                            if conditionCurrent == 'Rain':
                                if conditionDesc ==  'light rain':
                                    response = """Yes, The weather tomorrow is rain but it is light rain, you may be bring umbrella ☔"""
                                elif conditionDesc == 'moderate rain':
                                    response = """Yes, The weather next day is rain with moderate rain, you should bring a raincoat and move carefully if you go out 😭"""
                                else:
                                    response = """Yes, The weather tomorrow is rain, you should bring a raincoat and move carefully if you go out 😭"""
                            elif conditionCurrent == "Clouds":
                                if conditionDesc == 'broken clouds' or conditionDesc == 'overcast clouds':
                                    response = f"""Tomorrow's weather is likely to be rainy with {conditionDesc}, you should bring umbrella"""
                                else:
                                    response = f"""No, the next day is not rain, it is {conditionDesc}"""   
                            else:
                                response = f"""No, the next day is not rain, it is {conditionDesc}"""
                             
                    elif forecastPeriod == 'next 2 days':
                        tomorrows = [item for item in weathers['list'] if tomorrow[0:10] in item['dt_txt']]
                        afternoonTomorrow = [item for item in tomorrows if item['dt_txt'][11:] == '15:00:00']
                        conditionTomor = afternoonTomorrow[0]['weather'][0]['main']
                        conditionTomorDesc = afternoonTomorrow[0]['weather'][0]['description']
                        ##next 2 days 
                        next2Days = [item for item in weathers['list'] if next2Day[0:10] in item['dt_txt']]
                        morning = [item for item in next2Days if item['dt_txt'][11:] == '09:00:00']
                        afternoon = [item for item in next2Days if item['dt_txt'][11:] == '15:00:00']
                        evening = [item for item in next2Days if item['dt_txt'][11:] == '21:00:00']
                        conditionCurrent =  afternoon[0]['weather'][0]['main']
                        conditionDesc =  afternoon[0]['weather'][0]['description']


                        if guess == '' or guess is None:
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
                                response =  """The wind next two days is {} mph with deg is {} and gust is {} in the morning, is {} mph with deg is {} and gust is {} in the afternoon and the last: {} mph with deg is {} and gust is {} in the evening""".format(morning[0]['wind']['speed'],  morning[0]['wind']['deg'], morning[0]['wind']['gust'], afternoon[0]['wind']['speed'], afternoon[0]['wind']['deg'], afternoon[0]['wind']['gust'], evening[0]['wind']['speed'], evening[0]['wind']['deg'], evening[0]['wind']['gust'])
                            elif weatherType == 'sunny':
                                if conditionCurrent == 'Rain':
                                    response = f"""No, the next 2 days is not sunny, it {conditionDesc}"""
                                if conditionDesc == 'clear sky':
                                    response = """Yes, the weather the next 2 days is sunny, you should use suncreen if you want to go out 😉"""
                                elif conditionDesc == 'few clouds' or conditionDesc =='scattered clouds':
                                    response = """Hmmm, it's not exactly sunny the next 2 days, It's not really sunny the next 2 days, maybe a little because there are scattered clouds the next 2 days 😉"""
                                else:
                                    response = f"""No, the next 2 days is not sunny, it {conditionDesc}"""
                            elif weatherType == 'rain':
                                if conditionCurrent == 'Rain':
                                    if conditionDesc ==  'light rain':
                                        response = """Yes, The weather the day after tomorrow is rain but it is light rain, you may be bring umbrella ☔"""
                                    elif conditionDesc == 'moderate rain':
                                        response = """Yes, The weather the next 2 days is rain with moderate rain, you should bring a raincoat and move carefully if you go out 😭"""
                                    else:
                                        response = """Yes, The weather the next 2 days is rain, you should bring a raincoat and move carefully if you go out 😭"""
                                elif conditionCurrent == "Clouds":
                                    if conditionDesc == 'broken clouds' or conditionDesc == 'overcast clouds':
                                        response = f"""the next 2 days's weather is likely to be rainy with {conditionDesc}, you should bring umbrella"""
                                    else:
                                        response = f"""No, the day after tomorrow is not rain, it is {conditionDesc}"""   
                                else:
                                    response = f"""No, the next day after tomorrow is not rain, it is {conditionDesc}"""
              
                        else:
                            if weatherType == 'rain':
                                if conditionTomor == 'Rain':
                                    response = f"""It's will be rain tomorrow ({afternoonTomorrow[0]['dt_txt'][0:10]}), you may be bring umbrella ☔"""
                                elif conditionCurrent == 'Rain':
                                    response = f"""It's will be rain in next 2 days({afternoon[0]['dt_txt'][0:10]}), you may be bring umbrella ☔"""
                                elif conditionCurrent == 'Rain' and conditionTomor == 'Rain':
                                    response = f"""It's will be rain both 2 days), you may be bring umbrella ☔"""
                                else:
                                    response = """There will be no rain in the next 2 days, rest assured! 😉"""
                                    SlotSet('guess', None)
                            elif weatherType == 'sunny':
                                if conditionTomor == 'Clear' or conditionTomorDesc == 'few clouds' or conditionTomorDesc =='scattered clouds':
                                    response = f"""It's will be sunny tomorrow ({afternoonTomorrow[0]['dt_txt'][0:10]}), you should be use sunscreen"""
                                elif conditionCurrent == 'Clear' or conditionDesc == 'few clouds' or conditionDesc =='scattered clouds':
                                    response = f"""It's will have sunny in next 2 days({afternoon[0]['dt_txt'][0:10]}), you should be use sunscreen"""
                                elif (conditionTomor == 'Clear' or conditionTomorDesc == 'few clouds' or conditionTomorDesc =='scattered clouds') and conditionCurrent == 'Clear' or conditionDesc == 'few clouds' or conditionDesc =='scattered clouds':
                                    response = f"""It's will be sunny all, rest assured 😉"""
                                else:
                                    response = """There will be no sun both days, rest assured! 😉"""
                                    
                            
                    else: 
                        response = """sorry, I can only forecast the weather within 2 days"""
                
                else:
                    response = """sorry, i can't get weather from OpenWeatherApi"""

            else:
                response = """sorry, i can't get coordinates from OpenWeatherApi"""
         
         dispatcher.utter_message(response)
         
         return [SlotSet('location', loc), SlotSet('guess', None)]
