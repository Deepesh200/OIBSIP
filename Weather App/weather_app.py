import tkinter as tk
from tkinter import messagebox
import requests
import geocoder
from datetime import datetime
from PIL import Image, ImageTk
from io import BytesIO

# -----------------------------
# Configuration
# -----------------------------
API_KEY = "YOUR_API_KEY"  # 🔴 Replace with your OpenWeatherMap API Key
BASE_URL = "https://api.openweathermap.org/data/2.5/"

# -----------------------------
# Helper Functions
# -----------------------------
def get_device_location():
    """Get user's city using IP address."""
    try:
        g = geocoder.ip('me')
        return g.city or "Delhi"
    except:
        return "Delhi"

def get_weather_data(city):
    """Fetch current and forecast weather data."""
    try:
        weather_url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(weather_url)
        data = response.json()
        if data.get("cod") != 200:
            raise Exception(data.get("message", "Error fetching weather data"))

        lat, lon = data["coord"]["lat"], data["coord"]["lon"]

        forecast_url = f"{BASE_URL}forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        forecast_data = requests.get(forecast_url).json()
        return data, forecast_data
    except Exception as e:
        raise Exception(f"City not found: {city} ({str(e)})")

def update_weather(city=None):
    """Update UI with weather data."""
    city = city or city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name!")
        return

    try:
        loading_label.config(text="Loading...")
        root.update_idletasks()

        weather_data, forecast_data = get_weather_data(city)
        city_name = weather_data["name"]
        country = weather_data["sys"]["country"]
        temp = weather_data["main"]["temp"]
        feels_like = weather_data["main"]["feels_like"]
        humidity = weather_data["main"]["humidity"]
        pressure = weather_data["main"]["pressure"]
        wind_speed = weather_data["wind"]["speed"]
        description = weather_data["weather"][0]["description"].capitalize()
        icon_code = weather_data["weather"][0]["icon"]

        city_label.config(text=f"{city_name}, {country}")
        temp_label.config(text=f"{temp:.1f}°C")
        desc_label.config(text=description)
        details_label.config(
            text=f"Feels like: {feels_like}°C | Humidity: {humidity}% | Wind: {wind_speed} m/s | Pressure: {pressure} hPa"
        )

        # Weather Icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_img = Image.open(BytesIO(requests.get(icon_url).content))
        icon_photo = ImageTk.PhotoImage(icon_img)
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo

        # Forecast
        forecast_text = ""
        for i in range(0, 40, 8):  # Every 8 entries ~ 1 per day
            f = forecast_data["list"][i]
            date_txt = datetime.fromtimestamp(f["dt"]).strftime("%a %d %b")
            temp_day = f["main"]["temp"]
            desc = f["weather"][0]["description"].capitalize()
            forecast_text += f"{date_txt}: {temp_day:.1f}°C, {desc}\n"
        forecast_label.config(text=forecast_text)

        loading_label.config(text="")
    except Exception as e:
        loading_label.config(text="")
        messagebox.showerror("Error", str(e))

def show_device_weather():
    """Fetch and show weather of current location."""
    city = get_device_location()
    update_weather(city)

# -----------------------------
# GUI Setup
# -----------------------------
root = tk.Tk()
root.title("Advanced Weather App")
root.geometry("600x600")
root.configure(bg="#1E213A")

title_label = tk.Label(root, text="Weather Forecast", font=("Arial", 22, "bold"), bg="#1E213A", fg="white")
title_label.pack(pady=10)

frame = tk.Frame(root, bg="#1E213A")
frame.pack(pady=5)

city_entry = tk.Entry(frame, font=("Arial", 14), width=25)
city_entry.grid(row=0, column=0, padx=10)

search_button = tk.Button(frame, text="Search", font=("Arial", 12, "bold"), bg="#6C63FF", fg="white", command=lambda: update_weather())
search_button.grid(row=0, column=1)

detect_button = tk.Button(frame, text="Use My Location", font=("Arial", 10), bg="#FFB74D", fg="black", command=show_device_weather)
detect_button.grid(row=0, column=2, padx=10)

loading_label = tk.Label(root, text="", font=("Arial", 12), bg="#1E213A", fg="white")
loading_label.pack()

city_label = tk.Label(root, text="", font=("Arial", 18, "bold"), bg="#1E213A", fg="#FFD700")
city_label.pack()

icon_label = tk.Label(root, bg="#1E213A")
icon_label.pack(pady=5)

temp_label = tk.Label(root, text="", font=("Arial", 40, "bold"), bg="#1E213A", fg="white")
temp_label.pack()

desc_label = tk.Label(root, text="", font=("Arial", 14), bg="#1E213A", fg="#D3D3D3")
desc_label.pack()

details_label = tk.Label(root, text="", font=("Arial", 12), bg="#1E213A", fg="#A9A9A9")
details_label.pack(pady=5)

separator = tk.Label(root, text="------------------------------", bg="#1E213A", fg="#444")
separator.pack(pady=5)

forecast_title = tk.Label(root, text="5-Day Forecast", font=("Arial", 16, "bold"), bg="#1E213A", fg="white")
forecast_title.pack(pady=5)

forecast_label = tk.Label(root, text="", justify="left", font=("Arial", 12), bg="#1E213A", fg="#D3D3D3")
forecast_label.pack()

# -----------------------------
# Auto-load weather
# -----------------------------
root.after(1000, show_device_weather)
root.mainloop()
