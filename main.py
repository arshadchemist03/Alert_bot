import os
import time
import requests
from bs4 import BeautifulSoup
import telegram

# Load credentials from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MONITOR_URL = os.getenv("MONITOR_URL", "https://appointment.theitalyvisa.com/Global/Appointment/NewAppointment")

bot = telegram.Bot(token=BOT_TOKEN)

def get_page_snapshot():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(MONITOR_URL, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(strip=True)
    except Exception as e:
        print("Error fetching page:", e)
        return None

def main():
    print("Bot started...")
    last_snapshot = get_page_snapshot()

    while True:
        time.sleep(60)  # Check every 60 seconds
        current_snapshot = get_page_snapshot()
        if current_snapshot and current_snapshot != last_snapshot:
            bot.send_message(chat_id=CHAT_ID, text="⚠️ Visa appointment page has changed!")
            last_snapshot = current_snapshot
            print("Change detected and message sent.")

if __name__ == "__main__":
    main()
