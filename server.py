from flask import Flask
import threading
import requests
from bs4 import BeautifulSoup
import telebot
import time

TOKEN = '7747545992:AAFBiSvgsCKYfGQ2b9LnC6UD0OFBHE0CY48'
CHAT_ID = '6249436686'
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return 'Ahly Tickets Bot is running on Railway!'

last_detected_match = None

def check_tickets():
    url = 'https://www.tazkarti.com/'
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        all_text = soup.get_text().lower()
        keywords = ['ahly', 'sundowns', 'al ahly', 'mameloid sundowns']

        for kw1 in keywords:
            for kw2 in keywords:
                if kw1 != kw2 and kw1 in all_text and kw2 in all_text:
                    return f'{kw1} vs {kw2}'
        return None
    except Exception as e:
        print(f'Error during ticket check: {e}')
        return None

def bot_loop():
    global last_detected_match
    while True:
        try:
            match = check_tickets()
            if match:
                if match != last_detected_match:
                    for _ in range(15):
                        bot.send_message(CHAT_ID, f'احجز بسرعة التذاكر نزلت: {match}')
                        time.sleep(2)
                    last_detected_match = match
            else:
                bot.send_message(CHAT_ID, 'لا، مفيش تذاكر نزلت لسه')
        except Exception as e:
            print(f"Error in loop: {e}")
        time.sleep(600)

threading.Thread(target=bot_loop).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
