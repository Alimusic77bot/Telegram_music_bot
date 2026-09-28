import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.environ["BOT_TOKEN"]
PORT = int(os.environ.get("PORT", "10000"))
RENDER_URL = os.environ["RENDER_EXTERNAL_URL"]
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "musicbotsecret")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📁 پلی‌لیست‌ها", callback_data="playlists")],
        [InlineKeyboardButton("➕ افزودن آهنگ", callback_data="add_song")],
        [InlineKeyboardButton("🔎 جستجو", callback_data="search")],
        [InlineKeyboardButton("❤️ موردعلاقه‌ها", callback_data="favorites")],
    ]

    await update.message.reply_text(
        "🎵 به موزیک‌بات شخصی من خوش آمدی!\n\n"
        "از منوی زیر انتخاب کن:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "playlists":
        keyboard = [
            [InlineKeyboardButton("🎤 رپ", callback_data="playlist_rap")],
            [InlineKeyboardButton("🇮🇷 ایرانی", callback_data="playlist_iranian")],
            [InlineKeyboardButton("🌎 خارجی", callback_data="playlist_foreign")],
            [InlineKeyboardButton("➕ ساخت پلی‌لیست", callback_data="new_playlist")],
            [InlineKeyboardButton("⬅️ برگشت", callback_data="home")],
        ]

        await query.edit_message_text(
            "📁 پلی‌لیست‌های من:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "add_song":
        await query.edit_message_text(
            "🎵 برای افزودن آهنگ، در مرحله بعدی کافی است "
            "فایل آهنگ را برای بات بفرستی."
        )

    elif query.data == "search":
        await query.edit_message_text(
            "🔎 قابلیت جستجو را در مرحله بعد فعال می‌کنیم."
        )

    elif query.data == "favorites":
        await query.edit_message_text(
            "❤️ فعلاً لیست موردعلاقه‌ها خالی است."
        )

    elif query.data.startswith("playlist_"):
        await query.edit_message_text(
            "🎵 این پلی‌لیست فعلاً خالی است.\n\n"
            "بعد از اضافه کردن سیستم ذخیره آهنگ، "
            "آهنگ‌های اینجا نمایش داده می‌شوند."
        )

    elif query.data == "new_playlist":
        await query.edit_message_text(
            "➕ ساخت پلی‌لیست در مرحله بعد فعال می‌شود."
        )

    elif query.data == "home":
        keyboard = [
            [InlineKeyboardButton("📁 پلی‌لیست‌ها", callback_data="playlists")],
            [InlineKeyboardButton("➕ افزودن آهنگ", callback_data="add_song")],
            [InlineKeyboardButton("🔎 جستجو", callback_data="search")],
            [InlineKeyboardButton("❤️ موردعلاقه‌ها", callback_data="favorites")],
        ]

        await query.edit_message_text(
            "🎵 منوی اصلی:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook",
        webhook_url=f"{RENDER_URL}/webhook",
        secret_token=WEBHOOK_SECRET,
    )


if __name__ == "__main__":
    main()
