from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from database import add_user, get_balance

TOKEN = "8674292035:AAHRlHUZlQJZHFcPuFwWQ8borwZbFzmzeaA"

keyboard = [
    ["🎮 شروع دوئل", "💰 موجودی"],
    ["👥 دعوت دوستان", "🪙 خرید سکه"],
    ["💸 برداشت وجه"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    add_user(user_id)

    await update.message.reply_text(
        "🎮 به ربات سنگ کاغذ قیچی خوش اومدی!",
        reply_markup=reply_markup
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if text == "💰 موجودی":
        balance = get_balance(user_id)
        await update.message.reply_text(f"💰 موجودی شما: {balance} سکه")

    elif text == "🪙 خرید سکه":
        await update.message.reply_text("🪙 بخش خرید سکه به‌زودی آماده می‌شود.")

    elif text == "💸 برداشت وجه":
        await update.message.reply_text("💸 بخش برداشت به‌زودی آماده می‌شود.")

    elif text == "👥 دعوت دوستان":
        await update.message.reply_text("👥 لینک دعوت به‌زودی اضافه می‌شود.")

    elif text == "🎮 شروع دوئل":
        await update.message.reply_text("🎮 بخش دوئل در مرحله بعد ساخته می‌شود.")


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buttons))

app.run_polling()
