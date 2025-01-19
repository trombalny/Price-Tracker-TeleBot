#TOP SHITCODE :)

import telebot
import requests
import time
import matplotlib.pyplot as plt

BOT_TOKEN = "72345133708:AAEucJ40Hzh3uinfdsg32Of29A3hofdamwjdf8"
API_URL = "https://api.dexscreener.com/token-pairs/v1/ton/EQD0KpcRMh-sKO2z5-vOjgvFjTT58tO-2Nmvxqg5ocFQFtWz" #FPIBANK 
CHANNEL = -1002293098732
filename = "cost.txt"

bot = telebot.TeleBot(BOT_TOKEN)

def add_to_file(cost):
    with open(filename, 'a') as file:
        file.write(cost + '\n')
    create_chart()

def read_from_file():
    with open(filename, 'r') as file:
        costs = [line.strip() for line in file.readlines()]
    return costs

def fetch_token_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                price_usd = data[0]["priceUsd"]
                add_to_file(str(price_usd))
            else:
                print("Unexpected data format received.")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}. URL: {API_URL}")
    except Exception as e:
        print(f"Error fetching data from {API_URL}: {e}")

def create_chart():
    data = read_from_file()
    if data:
        data = [float(value) for value in data]
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('#111111')
        ax.set_facecolor('#111111')
        ax.plot(data, color='white', linewidth=3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        last_value = data[-1]
        ax.text(0.02, 0.95, f"{last_value:.6f} $", transform=ax.transAxes, color='white', fontsize=25, fontweight='bold', fontfamily='Arial')
        plt.tight_layout()
        plt.savefig('FPIBANK.jpg', facecolor=fig.get_facecolor(), edgecolor='none')
        with open("FPIBANK.jpg", "rb") as image:
            bot.send_photo(chat_id=CHANNEL, photo=image, caption=f"<b>1 FPIBANK = {data[-1]} USD</b>\n\n#FPIBANK #BANKFPI #toncoin #TON #tonprice #bitcoin", parse_mode="html")
        plt.close(fig)

if __name__ == "__main__":
    while True:
        fetch_token_data()
        time.sleep(59)
