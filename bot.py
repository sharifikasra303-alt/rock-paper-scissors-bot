from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "توکن_ربات_اینجا"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋 ربات سنگ کاغذ قیچی آماده است!")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()
