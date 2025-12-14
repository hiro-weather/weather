from pathlib import Path
import requests
from datetime import datetime, timedelta, date

BASE_DIR = Path(__file__).parent
ICS_FILE = BASE_DIR / "weather.ics"


LAT = 35.6895
LON = 139.6917


def fetch_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LAT,
        "longitude": LON,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode",
        "timezone": "Asia/Tokyo"
    }

    headers = {
        "User-Agent": "hiro-weather/1.0"
    }

    r = requests.get(url, params=params, headers=headers, timeout=20)

    if r.status_code != 200 or not r.text.strip():
        raise RuntimeError(f"Weather API error: {r.status_code}")

    return r.json()

def weather_icon(code):
    if code == 0:
        return "☀️"
    elif code in (1, 2):
        return "🌤️"
    elif code == 3:
        return "☁️"
    elif code in (45, 48):
        return "🌫️"
    elif code in (51, 53, 55, 61, 63, 65):
        return "☔"
    elif code in (71, 73, 75):
        return "❄️"
    elif code in (95, 96, 99):
        return "⛈️"
    else:
        return "🌡️"

def create_ics(data):
    today = date.today()
    now = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    daily = data["daily"]
    t_max_list = daily["temperature_2m_max"]
    t_min_list = daily["temperature_2m_min"]
    rain_list = daily["precipitation_sum"]
    weather_codes = daily["weathercode"]

    events = []

    for i in range(7):
        d = today + timedelta(days=i)
        d_start = d.strftime("%Y%m%d")
        d_end = (d + timedelta(days=1)).strftime("%Y%m%d")

        t_max = t_max_list[i]
        t_min = t_min_list[i]
        rain = rain_list[i]
        icon = weather_icon(weather_codes[i])

        summary = f"{icon} {t_max}° / {t_min}°  {rain}mm"
        description = (
            f"最高気温: {t_max}°C\\n"
            f"最低気温: {t_min}°C\\n"
            f"降水量: {rain}mm"
        )

        events.append(f"""BEGIN:VEVENT
UID:weather-{d_start}@hiro-weather
DTSTAMP:{now}
DTSTART;VALUE=DATE:{d_start}
DTEND;VALUE=DATE:{d_end}
SUMMARY:{summary}
DESCRIPTION:{description}
END:VEVENT
""")

    ics_text = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//hiro-weather//Weather//
CALSCALE:GREGORIAN
{''.join(events)}
END:VCALENDAR
"""

    with open(ICS_FILE, "w", encoding="utf-8") as f:
        f.write(ics_text)




def main():
    try:
        data = fetch_weather()
        create_ics(data)
    except Exception as e:
        print("❌ 天気取得失敗:", e)

if __name__ == "__main__":
    main()

