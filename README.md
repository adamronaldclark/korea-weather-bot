# Korea Weather Bot

Simple web scraper I wrote to get the 5 day weather forecast (including the API) while I was in Korea.

## Setup

This script is set up to use Gmail to mail a list of recipients the 5 day weather forecast after it runs.

You need to create and populate "app-user.txt", "app-pw.txt", and "emails.txt" before running.

app-user.txt contains your gmail account (the account you are sending from)

app-pw.txt contains the gmail app password for the account listed in app-user.txt

Link to create Google app passwords: https://knowledge.workspace.google.com/kb/how-to-create-app-passwords-000009237

emails.txt contains the list of emails (one per line) that you want the forecast emailed to

## Install Dependencies
pip install -r requirements.txt

## Run

python korea-weather-bot.py