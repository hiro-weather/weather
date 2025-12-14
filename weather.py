import requests
from datetime import datetime, date

BASE_DIR = "/Users/hiro/weather/"

ICS_FILE = BASE_DIR + "weather.ics"

def fetch_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 35.6895,
        "longitude": 139.6917,
        "hourly": "temperature_2m,precipitation",
        "timezone": "Asia/Tokyo"
    }
    return requests.get(url, params=params).json()

def main():
    data = fetch_weather()

    temp = data["hourly"]["temperature_2m"][0]
    rain = data["hourly"]["precipitation"][0]

    today = date.today().strftime("%Y%m%d")
    now = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    ics = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//hiro-weather//Weather//
BEGIN:VEVENT
UID:weather-{today}@hiro-weather
DTSTAMP:{now}
DTSTART;VALUE=DATE:{today}
DTEND;VALUE=DATE:{today}
SUMMARY:気温: {temp}°C, 降水量: {rain}mm
END:VEVENT
END:VCALENDAR
"""

    with open(ICS_FILE, "w", encoding="utf-8") as f:
        f.write(ics)

if __name__ == "__main__":
    main()
