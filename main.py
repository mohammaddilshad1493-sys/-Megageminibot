import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Gemini Client Setup
gemini_client = genai.Client(api_key=os.environ.get("AQ.Ab8RN6KQYH9Ro967rLCuTCxUCEcPzrvYnWvIzImb-AJf32hhBQ"))

# Flask Server (Hosting ko active rakhne ke liye)
app = Flask(__render__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# Telegram Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Namaste! Main Gemini AI Bot hoon. Mujhse koi bhi sawal poochhein.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_text
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("Kuchh error aaya, kripya dubara try karein.")

def main():
    # Keep-alive web server start karein
    Thread(target=run_flask).start()

    # Telegram Bot start karein
    token = os.environ.get("8665661554:AAGdOngXiHmSmXc-fMpkQn4d5qzAujAJPIw")
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
