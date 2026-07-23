from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from database import create_table, add_user, get_balance, set_balance


TOKEN = "8674292035:AAFB4y-isBof0U1YL9UPvbcevUbBdc0g8cY"


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
        f"🎮 به ربات سنگ، کاغذ، قیچی خوش آمدید!"
    )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    money = get_balance(user.id)

    await update.message.reply_text(
        f"💰 موجودی شما: {money} تومان"
    )


def main():
    create_table()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("balance", balance)
    )

    print("Bot started...")

    app.run_polling()


if __name__ == "__main__":
    main()
