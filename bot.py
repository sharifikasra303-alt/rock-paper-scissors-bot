from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from database import (
    create_table,
    add_user,
    get_balance,
    get_all_users,
    create_payment,
    get_pending_payments,
    approve_payment,
    reject_payment
)


TOKEN = "8674292035:AAFB4y-isBof0U1YL9UPvbcevUbBdc0g8cY"

ADMIN_ID = 5125387850


def main_keyboard(user_id):

    keyboard = [
        ["🎮 شروع دوئل", "💰 موجودی"],
        ["👥 دعوت دوستان", "🪙 خرید سکه"],
        ["💸 برداشت وجه"]
    ]

    if user_id == ADMIN_ID:
        keyboard[2].append("👑 پنل مدیر")

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


def admin_keyboard():

    return ReplyKeyboardMarkup(
        [
            ["👥 لیست کاربران", "📊 آمار ربات"],
            ["🧾 درخواست‌های پرداخت"],
            ["🔙 بازگشت"]
        ],
        resize_keyboard=True
    )


def amount_keyboard():

    return ReplyKeyboardMarkup(
        [
            ["5000 تومان", "25000 تومان"],
            ["50000 تومان", "100000 تومان"],
            ["200000 تومان"],
            ["🔙 بازگشت"]
        ],
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


async def buy_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "💰 خرید سکه (شارژ حساب)\n\n"
        "💳 شماره کارت:\n"
        "6037991764297374\n"
        "به نام: علی شریفی\n\n"
        "⚠️ فقط کارت به کارت\n"
        "• رسید را ارسال کنید\n"
        "• مسئولیت واریز اشتباه با شماست",
        reply_markup=amount_keyboard()
    )


async def choose_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):

    amount = int(
        update.message.text.replace(" تومان", "")
    )

    context.user_data["amount"] = amount

    await update.message.reply_text(
        f"💰 خرید {amount} تومان\n\n"
        "💳 شماره کارت:\n"
        "6037991764297374\n"
        "به نام: علی شریفی\n\n"
        "⚠️ فقط کارت به کارت\n"
        "• رسید را ارسال کنید\n"
        "• مسئولیت واریز اشتباه با شماست\n\n"
        "🧾 لطفا رسید خود را ارسال کنید:"
    )


async def receive_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if "amount" not in context.user_data:
        return

    photo_id = update.message.photo[-1].file_id

    amount = context.user_data["amount"]

    user_id = update.effective_user.id

    create_payment(
        user_id,
        amount,
        photo_id
    )

    await update.message.reply_text(
        "✅ رسید شما دریافت شد.\n\n"
        "منتظر باشید رسید تایید شود و حساب شما شارژ شود."
    )

    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                "✅ تایید",
                callback_data=f"approve_{user_id}_{amount}"
            ),
            InlineKeyboardButton(
                "❌ رد",
                callback_data=f"reject_{user_id}_{amount}"
            )
        ]]
    )

    await context.bot.send_photo(
        ADMIN_ID,
        photo_id,
        caption=(
            "🧾 درخواست شارژ جدید\n\n"
            f"👤 کاربر: {update.effective_user.first_name}\n"
            f"🆔 آیدی: {user_id}\n"
            f"💰 مبلغ: {amount} تومان"
        ),
        reply_markup=keyboard
    )

    del context.user_data["amount"] async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user_id = update.effective_user.id


    if text == "💰 موجودی":

        balance = get_balance(user_id)

        await update.message.reply_text(
            f"💰 موجودی شما: {balance} تومان"
        )


    elif text == "🪙 خرید سکه":

        await buy_menu(update, context)


    elif text in [
        "5000 تومان",
        "25000 تومان",
        "50000 تومان",
        "100000 تومان",
        "200000 تومان"
    ]:

        await choose_amount(update, context)



    elif text == "🎮 شروع دوئل":

        await update.message.reply_text(
            "🎮 بخش دوئل به‌زودی آماده می‌شود."
        )


    elif text == "👥 دعوت دوستان":

        await update.message.reply_text(
            "👥 لینک دعوت به‌زودی اضافه می‌شود."
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

        users = get_all_users()

        message = "👥 لیست کاربران:\n\n"

        for user in users:

            message += (
                f"🆔 {user[0]}\n"
                f"👤 {user[1]}\n"
                f"💰 {user[3]} تومان\n\n"
            )

        await update.message.reply_text(
            message
        )



    elif text == "📊 آمار ربات":

        if user_id != ADMIN_ID:
            return

        users = get_all_users()

        total = len(users)

        await update.message.reply_text(
            f"📊 آمار ربات\n\n"
            f"👥 تعداد کاربران: {total}"
        )



    elif text == "🧾 درخواست‌های پرداخت":

        if user_id != ADMIN_ID:
            return

        payments = get_pending_payments()

        await update.message.reply_text(
            f"🧾 درخواست‌های در انتظار: {len(payments)}"
        )



    elif text == "🔙 بازگشت":

        await update.message.reply_text(
            "منوی اصلی",
            reply_markup=main_keyboard(user_id)
        )



async def payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()


    data = query.data.split("_")

    action = data[0]

    user_id = int(data[1])

    amount = int(data[2])


    payments = get_pending_payments()

    payment_id = None


    for payment in payments:

        if payment[1] == user_id and payment[2] == amount:

            payment_id = payment[0]

            break



    if payment_id is None:

        await query.edit_caption(
            "❌ درخواست پیدا نشد."
        )

        return



    if action == "approve":

        approve_payment(payment_id)


        await context.bot.send_message(
            user_id,
            f"✅ پرداخت شما تایید شد.\n\n"
            f"💰 مبلغ {amount} تومان اضافه شد.\n"
            f"💳 موجودی جدید: {get_balance(user_id)} تومان"
        )


        await query.edit_caption(
            "✅ پرداخت تایید شد."
        )



    elif action == "reject":

        reject_payment(payment_id)


        await context.bot.send_message(
            user_id,
            "❌ رسید شما تایید نشد."
        )


        await query.edit_caption(
            "❌ پرداخت رد شد."
        )



def main():

    create_table()


    app = Application.builder().token(TOKEN).build()


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            payment_callback
        )
    )


    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            receive_receipt
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
