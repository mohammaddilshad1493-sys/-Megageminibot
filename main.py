import os
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

# Gemini Client Setup (New google-genai library)
gemini_client = genai.Client(api_key=os.environ.get("sk-rb-koEySh6OTr37-uOBXQGmqXe4AtmKjxsFtp0bC413cy1MBU6wsPhIEbKBM7X0B"))

# Flask Server (Keep-alive for Render web service)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Helper: Telegram ke 4096 character limit ko handle karne ke liye
async def send_long_message(message, text: str):
    max_length = 4000  # Safe limit
    for i in range(0, len(text), max_length):
        await message.reply_text(text[i:i + max_length])

# Telegram Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Namaste! Mai aapka Gemini AI Bot hoon. Koi bhi sawal poochhein.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text
    chat_id = update.effective_chat.id

    # User ko 'typing...' indicator dikhayein
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        # gemini_client.aio use karein taaki event loop block na ho
        response = await gemini_client.aio.models.generate_content(
            model="gemini-2.0-flash",  # ya 'gemini-1.5-flash'
            contents=user_text
        )

        reply_content = response.text or "Maaf kijiye, koi response generate nahi ho paya."
        await send_long_message(update.message, reply_content)

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def main():
    token = os.environ.get("8665661554:AAGdOngXiHmSmXc-fMpkQn4d5qzAujAJPIw")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set!")
        return

    # Background Flask thread start karein
    Thread(target=run_flask, daemon=True).start()

    # Telegram Bot setup
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot polling started...")
    application.run_polling()

if __name__ == '__main__':
    main()
