import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    try:
        # Geocoding - buscar latitude e longitude automaticamente
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()

        if not geo_data:
            return f"Não consegui encontrar a cidade '{city}'."

        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]
        city_name = geo_data[0]["name"]
        country = geo_data[0]["country"]

        # Buscar o clima pela latitude/longitude
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=pt_br"
        weather_response = requests.get(weather_url)
        data = weather_response.json()

        # Tratar retorno e formatar resposta
        descricao = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        sensacao = data["main"]["feels_like"]

        return f"Clima em {city_name} ({country}): {descricao}, {round(temp)}ºC (sensação {round(sensacao)}ºC)"

    except Exception as e:
        print(f"Erro em get_weather: {e}")
        return "Erro ao buscar o clima, tente novamente."
