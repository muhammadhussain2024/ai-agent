import requests

def get_weather(city):
    """Fetch live weather using OpenWeather API."""
    api_key_weather = "YOUR_OPENWEATHER_API_KEY"  # Replace with your key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key_weather}&units=metric"
    response = requests.get(url).json()

    if response.get("main"):
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        return f"🌤️ Weather in {city}: {temp}°C, {desc}"
    return "⚠️ Sorry, I couldn't fetch the weather."
