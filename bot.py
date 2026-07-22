from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

TOKEN = "8674292035:AAFl58vbAHReyPMQqWe8X5_44ceFJyRn8ws"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "ربات سنگ کاغذ قیچی آماده است!\n\n"
        "برای شروع بازی بزن:\n"
        "/game"
    )


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🪨 سنگ", callback_data="سنگ"),
            InlineKeyboardButton("📄 کاغذ", callback_data="کاغذ"),
            InlineKeyboardButton("✂️ قیچی", callback_data="قیچی")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "یکی را انتخاب کن:",
        reply_markup=reply_markup
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        f"انتخاب تو: {query.data}"
    )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("game", game))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
