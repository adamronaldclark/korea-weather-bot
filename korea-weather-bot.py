# Imports
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

# Variables
URL = "https://www.iqair.com/south-korea/gyeonggi-do/pyeongtaek"
today = datetime.today()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}

# Open the file in read mode
with open('emails.txt', 'r') as file:
    # Read all lines from the file
    email_list = file.readlines()

# Strip any leading/trailing whitespace characters (like newline characters)
email_list = [email.strip() for email in email_list]

# Open the file in read mode
with open('app-pw.txt', 'r') as file:
    # Read the password from the file
    app_password = file.read().strip()
    
    # Open the file in read mode
with open('app-user.txt', 'r') as file:
    # Read the password from the file
    app_user = file.read().strip()

# Functions
def get_fahrenheit(celsius):
    fahrenheit = (celsius * 1.8) + 32
    return round(fahrenheit, 2)

def get_miles(kilometers):
    conversion_factor = 0.621371
    miles = kilometers * conversion_factor
    return round(miles, 2)

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())

# Scrape forecast data
response = requests.get(URL, headers=headers)
if response.status_code != 200:
    print(f"Error: {response.status_code}")
    exit()
else:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

# Extract forecast data
forecast_data = []
for i in range(1, 6):
    forecast_date = today + timedelta(days=i)
    forecast_day = forecast_date.strftime('%A, %b %d')
    
    forecast_row = soup.find('td', string=forecast_day).find_parent('tr')
    aqi_div = forecast_row.find('div', class_='pollutant-level-wrapper')
    aqi_value = aqi_div.find('b').text.strip()
    aqi_status = forecast_row.find('strong').string.strip()
    weather_icon = forecast_row.find('img', class_='forecast-weather_icon')
    if "rain" in weather_icon:
        rain = "Yes"
    else:
        rain = "No"
    max_temp = get_fahrenheit(float(forecast_row.find('span', class_='forecast-temperature_max').text.strip()[:2]))
    min_temp = get_fahrenheit(float(forecast_row.find('span', class_='forecast-temperature_min').text.strip()[:2]))
    wind_speed = get_miles(float(forecast_row.find('span', class_='forecast-wind_text').text.strip()[:-4]))
    
    forecast_data.append({
        'date': forecast_day,
        'aqi_value': aqi_value,
        'aqi_status': aqi_status,
        'rain': rain,
        'max_temp': max_temp,
        'min_temp': min_temp,
        'wind_speed': wind_speed
    })

# Add forecast data to email body
email_body = "Good Afternoon!\n\nHere is your 5 day forecast for Pyeontaek, South Korea:\n\n"
for forecast in forecast_data:
    email_body += f"Date: {forecast['date']}\n"
    email_body += f"AQI: {forecast['aqi_value']} ({forecast['aqi_status']})\n"
    email_body += f"Rain: {forecast['rain']}\n"
    email_body += f"Temperature (min/max): {forecast['max_temp']} / {forecast['min_temp']} fahrenheit\n"
    email_body += f"Wind Speed: {forecast['wind_speed']} mph\n"
    email_body += "\n"
    
subject = "Pyeontaek, South Korea - 5 Day Weather Forecast"
body = email_body
sender = app_user
recipients = email_list
password = app_password

send_email(subject, body, sender, recipients, password)