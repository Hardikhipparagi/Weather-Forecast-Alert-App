import requests
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt

CITIES = {
    "Pune": (18.52, 73.85),
    "Mumbai": (19.07, 72.87),
    "Delhi": (28.61, 77.21),
    "Bangalore": (12.97, 77.59),
    "Hyderabad": (17.38, 78.48)
}

load_dotenv()

API_KEY = os.getenv("API_KEY")

def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,relativehumidity_2m,precipitation&timezone=auto"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print("Error:", e)
        return None

def analyze_weather(data):
    alerts = []
    records = []

    hourly = data["hourly"]

    times = hourly["time"]
    temps = hourly["temperature_2m"]
    humidity = hourly["relativehumidity_2m"]
    rain = hourly["precipitation"]

    for i in range(len(times)):
        record = {
            "datetime": times[i],
            "temp": temps[i],
            "humidity": humidity[i],
            "rain": rain[i]
        }
        records.append(record)

        # 🔥 Alert Logic
        if temps[i] > 35:
            alerts.append(f"🔥 High Temperature at {times[i]}")

        if humidity[i] > 80:
            alerts.append(f"💧 High Humidity at {times[i]}")

        if rain[i] > 0:
            alerts.append(f"🌧️ Rain Alert at {times[i]}")

    return records, alerts

def save_report(records):
    df = pd.DataFrame(records)
    filename = f"reports/weather_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    df.to_csv(filename, index=False)
    print(f"📁 Report saved: {filename}")

def plot_weather(records):
    temps = [r["temp"] for r in records[:24]]
    times = [r["datetime"] for r in records[:24]]

    plt.figure()
    plt.plot(times, temps)
    plt.xticks(rotation=45)
    plt.title("Temperature Forecast")
    plt.tight_layout()
    plt.savefig("outputs/temp_plot.png")
    plt.show()    

def main():
    print("🌍 Select a City:\n")
    
    city_list = list(CITIES.keys())
    
    for i, city in enumerate(city_list, 1):
        print(f"{i}. {city}")
    
    choices = input("Enter city numbers OR names (comma separated): ").split(",")

    for ch in choices:
        ch = ch.strip().title()

        # If user entered number
        if ch.isdigit():
            index = int(ch) - 1
            if 0 <= index < len(city_list):
                selected_city = city_list[index]
            else:
                print(f"❌ Invalid city number: {ch}")
                continue

        # If user entered name
        else:
            if ch in CITIES:
                selected_city = ch
            else:
                print(f"❌ Invalid city: {ch}")
                continue

        lat, lon = CITIES[selected_city]

        print(f"\n📍 {selected_city}")

        data = get_weather(lat, lon)
        records, alerts = analyze_weather(data)

        save_report(records)
        plot_weather(records)

if __name__ == "__main__":
    main()
       