from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8674292035:AAHRlHUZlQJZHFcPuFwWQ8borwZbFzmzeaA"

keyboard = [
    ["🎮 شروع دوئل", "💰 موجودی"],
    ["👥 دعوت دوستان", "🪙 خرید سکه"],
    ["💸 برداشت وجه"]
]

reply_markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 به ربات سنگ کاغذ قیچی خوش اومدی!",
        reply_markup=reply_markup
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "💰 موجودی":
        await update.message.reply_text("💰 موجودی شما: 0 سکه")

    elif text == "🪙 خرید سکه":
        await update.message.reply_text("🪙 بخش خرید سکه هنوز ساخته نشده.")

    elif text == "💸 برداشت وجه":
        await update.message.reply_text("💸 بخش برداشت هنوز ساخته نشده.")

    elif text == "👥 دعوت دوستان":
        await update.message.reply_text("👥 لینک دعوت شما بعداً نمایش داده می‌شود.")

    elif text == "🎮 شروع دوئل":
        await update.message.reply_text("🎮 این بخش در مرحله بعد ساخته می‌شود.")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buttons))

app.run_polling()
