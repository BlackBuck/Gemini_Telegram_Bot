from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import logging
import google.generativeai as genai
import os

#get the api tokens
api_token = os.environ.get("TELEGRAM_BOT_TOKEN")
gemini_api = os.environ['GOOGLE_API_TOKEN']

#configure the gemini api
genai.configure(api_key=gemini_api)
model = genai.GenerativeModel("gemini-pro")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

#start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(text="Hello I am the AI assistant bot built with gemini. Please enter your query in the message box.", chat_id=update.effective_chat.id)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    res = model.generate_content(update.message.text)
    await context.bot.send_message(text=res.text, chat_id=update.effective_chat.id)

async def say_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.split(" ")[1]
    await context.bot.send_message(text="Hello " + name, chat_id=update.effective_chat.id)

if __name__ == '__main__':
    application = ApplicationBuilder().token(api_token).build()

    #for the start command
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    #for the non-command messages
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)

    #start pollling
    application.run_polling()