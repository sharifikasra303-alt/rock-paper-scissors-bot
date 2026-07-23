from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from database import add_user, get_balance, set_balance

TOKEN = "8674292035:AAHRlHUZlQJZHFcPuFwWQ8borwZbFzmzeaA"

ADMIN_ID = 5125387850


def get_keyboard(user_id):
    if user_id == ADMIN_ID:
        keyboard = [
            ["🎮 شروع دوئل", "💰 موجودی"],
            ["👥 دعوت دوستان", "🪙 خرید سکه"],
            ["💸 برداشت وجه", "👑 پنل مدیر"]
        ]
    else:
        keyboard = [
            ["🎮 شروع دوئل", "💰 موجودی"],
            ["👥 دعوت دوستان", "🪙 خرید سکه"],
            ["💸 برداشت وجه"]
        ]

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    add_user(user_id)

    await update.message.reply_text(
        "🎮 به ربات سنگ کاغذ قیچی خوش اومدی!",
        reply_markup=get_keyboard(user_id)
    )


async def add_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        target = int(context.args[0])
        amount = int(context.args[1])

        allowed = [5000, 25000, 50000, 100000, 200000]

        if amount not in allowed:
            await update.message.reply_text("❌ مقدار مجاز نیست.")
            return

        set_balance(target, amount)

        await update.message.reply_text(
            f"✅ {amount} سکه به کاربر {target} اضافه شد."
        )

    except:
        await update.message.reply_text(
            "مثال:\n"
            "/add 123456789 50000"
        )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if text == "💰 موجودی":
        balance = get_balance(user_id)
        await update.message.reply_text(
            f"💰 موجودی شما: {balance} سکه"
        )

    elif text == "🪙 خرید سکه":
        await update.message.reply_text(
            "🪙 خرید سکه\n\n"
            "5000 سکه\n"
            "25000 سکه\n"
            "50000 سکه\n"
            "100000 سکه\n"
            "200000 سکه"
        )

    elif text == "💸 برداشت وجه":
        await update.message.reply_text("💸 این بخش به‌زودی آماده می‌شود.")

    elif text == "👥 دعوت دوستان":
        await update.message.reply_text("👥 لینک دعوت به‌زودی اضافه می‌شود.")

    elif text == "🎮 شروع دوئل":
        await update.message.reply_text("🎮 بخش دوئل در مرحله بعد ساخته می‌شود.")

    elif text == "👑 پنل مدیر":
        if user_id != ADMIN_ID:
            return

        await update.message.reply_text(
            "👑 پنل مدیر\n\n"
            "برای افزودن سکه دستور زیر را ارسال کنید:\n\n"
            "/add USER_ID AMOUNT\n\n"
            "مثال:\n"
            "/add 123456789 50000"
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add_coin))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buttons))

app.run_polling()
