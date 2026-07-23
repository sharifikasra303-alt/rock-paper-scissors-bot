from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    ConversationHandler
)

from database import (
    add_user,
    get_balance,
    create_table,
    get_all_users,
    add_balance
)


TOKEN = "8674292035:AAFB4y-isBof0U1YL9UPvbcevUbBdc0g8cY"

ADMIN_ID = 5125387850


ADD_USER_ID, ADD_AMOUNT = range(2)


# منوی اصلی
def main_keyboard(user_id):

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


# منوی مدیر
def admin_keyboard():

    keyboard = [
        ["👥 لیست کاربران", "💰 افزودن موجودی"],
        ["📊 آمار ربات"],
        ["🔙 بازگشت"]
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
        "🎮 به ربات سنگ، کاغذ، قیچی خوش آمدید!",
        reply_markup=main_keyboard(user.id)
    )


# شروع شارژ کاربر
async def start_add_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return ConversationHandler.END

    await update.message.reply_text(
        "🆔 آیدی کاربری که می‌خواهی شارژ کنی را ارسال کن:"
    )

    return ADD_USER_ID



# گرفتن آیدی
async def get_target_user(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        user_id = int(update.message.text)

        context.user_data["target_user"] = user_id

        await update.message.reply_text(
            "💰 مقدار شارژ را وارد کن:"
        )

        return ADD_AMOUNT


    except:

        await update.message.reply_text(
            "❌ آیدی صحیح نیست."
        )

        return ADD_USER_ID



# گرفتن مبلغ
async def save_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        amount = int(update.message.text)

        user_id = context.user_data["target_user"]

        add_balance(
            user_id,
            amount
        )


        await update.message.reply_text(
            f"✅ {amount} تومان به کاربر {user_id} اضافه شد."
        )


    except:

        await update.message.reply_text(
            "❌ مبلغ اشتباه است."
        )


    return ConversationHandler.END



# لیست کاربران
async def show_users(update: Update):

    users = get_all_users()

    if not users:

        await update.message.reply_text(
            "❌ کاربری وجود ندارد."
        )

        return


    text = "👥 لیست کاربران:\n\n"


    for i, user in enumerate(users, start=1):

        uid, name, username, balance = user

        text += (
            f"{i}) {name}\n"
            f"🆔 {uid}\n"
            f"👤 @{username if username else 'ندارد'}\n"
            f"💰 {balance} تومان\n\n"
        )


    await update.message.reply_text(text)



async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user_id = update.effective_user.id


    if text == "💰 موجودی":

        balance = get_balance(user_id)

        await update.message.reply_text(
            f"💰 موجودی شما: {balance} تومان"
        )



    elif text == "🎮 شروع دوئل":

        await update.message.reply_text(
            "🎮 بخش دوئل به‌زودی ساخته می‌شود."
        )



    elif text == "🪙 خرید سکه":

        await update.message.reply_text(
            "🪙 خرید سکه به‌زودی فعال می‌شود."
        )



    elif text == "👥 دعوت دوستان":

        await update.message.reply_text(
            "👥 لینک دعوت به‌زودی ساخته می‌شود."
        )



    elif text == "💸 برداشت وجه":

        await update.message.reply_text(
            "💸 بخش برداشت به‌زودی آماده می‌شود."
        )



    elif text == "👑 پنل مدیر":

        if user_id != ADMIN_ID:
            return

        await update.message.reply_text(
            "👑 پنل مدیریت",
            reply_markup=admin_keyboard()
        )



    elif text == "👥 لیست کاربران":

        if user_id != ADMIN_ID:
            return

        await show_users(update)



    elif text == "📊 آمار ربات":

        if user_id != ADMIN_ID:
            return

        users = get_all_users()

        await update.message.reply_text(
            f"📊 آمار ربات\n\n"
            f"👥 تعداد کاربران: {len(users)}"
        )



    elif text == "🔙 بازگشت":

        await update.message.reply_text(
            "منوی اصلی",
            reply_markup=main_keyboard(user_id)
        )



async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(
        "برای شارژ از پنل مدیر استفاده کن."
    )



def main():

    create_table()

    app = Application.builder().token(TOKEN).build()


    charge_handler = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex("^💰 افزودن موجودی$"),
                start_add_balance
            )
        ],

        states={

            ADD_USER_ID: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_target_user
                )
            ],

            ADD_AMOUNT: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    save_balance
                )
            ]
        },

        fallbacks=[]
    )


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(charge_handler)


    app.add_handler(
        CommandHandler(
            "add",
            add_command
        )
    )


    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            buttons
        )
    )


    print("Bot started...")


    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
