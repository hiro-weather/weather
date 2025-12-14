import requests
import json
import traceback
from datetime import datetime, timedelta

# 保存先ディレクトリ（絶対パス）
BASE_DIR = "/Users/hiro/iCloudWeather/"

# ログファイル
LOG_FILE = BASE_DIR + "weather.log"
ERROR_LOG_FILE = BASE_DIR + "weather_error.log"
ICS_FILE = BASE_DIR + "weather.ics"


def log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {message}\n")


def log_error(message):
    with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] ERROR: {message}\n")


def fetch_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 35.6895,   # Tokyo
        "longitude": 139.6917,
        "hourly": "temperature_2m,precipitation",
        "timezone": "Asia/Tokyo"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def create_ics(weather_data):
    now = datetime.now()
    event_time = now.strftime("%Y%m%dT%H%M%S")

    temp = weather_data["hourly"]["temperature_2m"][0]
    rain = weather_data["hourly"]["precipitation"][0]

    summary = f"気温: {temp}°C, 降水量: {rain}mm"

    ics = (
        "BEGIN:VCALENDAR\n"
        "VERSION:2.0\n"
        "BEGIN:VEVENT\n"
        f"DTSTAMP:{event_time}\n"
        f"SUMMARY:{summary}\n"
        "END:VEVENT\n"
        "END:VCALENDAR\n"
    )

    with open(ICS_FILE, "w", encoding="utf-8") as f:
        f.write(ics)


def main():
    try:
        log("天気データ取得開始")
        weather = fetch_weather()
        create_ics(weather)
        log(f"weather.ics を保存しました → {ICS_FILE}")
    except Exception as e:
        log_error(str(e))
        log_error(traceback.format_exc())


if __name__ == "__main__":
    main()


