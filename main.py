import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

# Gemini Client Setup (Using new google-genai library)
gemini_client = genai.Client(api_key=os.environ.get("AQ.Ab8RN6KQYH9Ro967rLCuTCxUCEcPzrvYnWvIzImb-AJf32hhBQ"))

# Flask Server (Keep-alive for Render)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Telegram Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Namaste! Mai aapka Gemini AI Bot hoon. Koi bhi sawal poochhein.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_text
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def main():
    # Start Keep-alive Web Server
    Thread(target=run_flask, daemon=True).start()

    # Start Telegram Bot
    token = os.environ.get("8665661554:AAGdOngXiHmSmXc-fMpkQn4d5qzAujAJPIw")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set!")
        return

    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main() 
