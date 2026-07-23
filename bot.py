from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from database import add_user, get_balance, set_balance, create_table


TOKEN = "8674292035:AAFB4y-isBof0U1YL9UPvbcevUbBdc0g8cY"

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

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    add_user(
        user.id,
        user.first_name,
        user.username
    )

    balance = get_balance(user.id)

    await update.message.reply_text(
        f"سلام {user.first_name} 👋\n\n"
        f"🆔 آیدی شما: {user.id}\n"
        f"💰 موجودی شما: {balance} تومان\n\n"
        f"🎮 به ربات سنگ، کاغذ، قیچی خوش آمدید!",
        reply_markup=get_keyboard(user.id)
    )


async def add_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        target = int(context.args[0])
        amount = int(context.args[1])

        allowed = [
            5000,
            25000,
            50000,
            100000,
            200000
        ]

        if amount not in allowed:
            await update.message.reply_text(
                "❌ مقدار مجاز نیست."
            )
            return

        set_balance(target, amount)

        await update.message.reply_text(
            f"✅ {amount} تومان به کاربر {target} اضافه شد."
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
            f"💰 موجودی شما: {balance} تومان"
        )


    elif text == "🪙 خرید سکه":
        await update.message.reply_text(
            "🪙 خرید سکه\n\n"
            "5000 تومان\n"
            "25000 تومان\n"
            "50000 تومان\n"
            "100000 تومان\n"
            "200000 تومان"
        )


    elif text == "💸 برداشت وجه":
        await update.message.reply_text(
            "💸 این بخش به‌زودی آماده می‌شود."
        )


    elif text == "👥 دعوت دوستان":
        await update.message.reply_text(
            "👥 لینک دعوت به‌زودی اضافه می‌شود."
        )


    elif text == "🎮 شروع دوئل":
        await update.message.reply_text(
            "🎮 بخش دوئل در مرحله بعد ساخته می‌شود."
        )


    elif text == "👑 پنل مدیر":
        if user_id != ADMIN_ID:
            return

        await update.message.reply_text(
            "👑 پنل مدیر\n\n"
            "برای افزودن موجودی:\n\n"
            "/add USER_ID AMOUNT\n\n"
            "مثال:\n"
            "/add 123456789 50000"
        )


def main():
    create_table()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("add", add_coin)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            buttons
        )
    )

    print("Bot started...")

    aapp.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
