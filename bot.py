from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

TOKEN = "8674292035:AAFl58vbAHReyPMQqWe8X5_44ceFJyRn8ws"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("🎮 شروع دوئل", callback_data="duel"),
            InlineKeyboardButton("🏆 بازی‌های امروز", callback_data="today"),
        ],
        [
            InlineKeyboardButton("💰 موجودی", callback_data="wallet"),
            InlineKeyboardButton("🪙 خرید سکه", callback_data="buy"),
        ],
        [
            InlineKeyboardButton("👥 دعوت دوستان", callback_data="invite"),
            InlineKeyboardButton("💸 برداشت", callback_data="withdraw"),
        ],
        [
            InlineKeyboardButton("📞 پشتیبانی", callback_data="support"),
        ]
    ]

    text = f"""
🎮 به ربات سنگ، کاغذ، قیچی خوش آمدید.

👤 نام: {update.effective_user.first_name}

💰 موجودی: ۰ سکه
🏆 بازی امروز: ۰

یکی از گزینه‌های زیر را انتخاب کنید.
"""

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "duel":
        keyboard = [
            [InlineKeyboardButton("5000", callback_data="bet_5000")],
            [InlineKeyboardButton("20000", callback_data="bet_20000")],
            [InlineKeyboardButton("50000", callback_data="bet_50000")],
            [InlineKeyboardButton("100000", callback_data="bet_100000")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back")]
        ]

        await query.edit_message_text(
            "💰 مبلغ دوئل را انتخاب کنید.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "wallet":
        await query.edit_message_text("💰 موجودی شما: ۰ سکه")

    elif data == "buy":
        await query.edit_message_text("🪙 بخش خرید سکه")

    elif data == "invite":
        await query.edit_message_text("👥 لینک دعوت شما:\nhttps://t.me/YourBot?start=123")

    elif data == "withdraw":
        await query.edit_message_text("💸 درخواست برداشت")

    elif data == "support":
        await query.edit_message_text("📞 آیدی پشتیبانی:\n@Support")

    elif data == "today":
        await query.edit_message_text("🏆 تعداد بازی امروز: ۰")

    elif data == "back":
        await start(update, context)
