import tkinter as tk
from tkinter import messagebox
import requests                 #for HTTP requests
from PIL import Image, ImageTk  #for processing and displaying images
import ttkbootstrap

#function to get weather information from OpenWeatherMap API
def get_weather(city):
    API_key = "PUT YOUR API KEY HERE GENERATED FROM OPEN WEATHER MAP WEBSITE"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code==404:
        messagebox.showerror("Error","City not found")
        return None
    
    weather=res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.25
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']

    #Get the icon URL and return all the weather info
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, city, country)

#function to search weather for a city
def search():
    city = city_name.get()
    result = get_weather(city)
    if result is None:
        return
    #If the city is found
    icon_url, temperature, description, city, country = result
    location_label.configure(text=f"{city}, {country}")

    #Get the weather icon image from the url and update the icon label
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    #update the temperature and description labels
    temperature_label.configure(text=f"Temperature: {temperature:.2f}C")
    description_label.configure(text=f"Description: {description}")

root = ttkbootstrap.Window(themename='morph')
root.title("Weather Report App")
root.geometry("400x400")

#enter city name
city_name = ttkbootstrap.Entry(root, font="Helvetica, 18")
city_name.pack(pady=10)

#search button
search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning")
search_button.pack(pady=10)

#city/country name
location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack(pady=20)

#weather icon
icon_label = tk.Label(root)
icon_label.pack()

#temperature
temperature_label = tk.Label(root, font="Helvetica, 20")
temperature_label.pack()

#weather description
description_label = tk.Label(root, font="Helvetica, 20")
description_label.pack()

root.mainloop()
