import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, \
    InputFile
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler
from dotenv import load_dotenv
from convert_api import convert_file
import os

load_dotenv()
BOT_TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["awaiting_file"] = True
    user_first = update.effective_user.first_name
    text = f"Hi {user_first}! 👋 Send me the file you want me to convert."
    keyboard = [
        ["Convert"],
        ["About", "Help"]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=reply_markup
    )


async def hide_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Keyboard hidden.",
        reply_markup=ReplyKeyboardRemove()
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📄 **About This Bot**\n"
        "This bot helps you convert files between different formats.\n"
        "Just send a file and hit /convert to get started!"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text
    )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "/start - Begin using the bot\n"
        "/about - Learn what this bot does\n"
        "/convert - Start the conversion process\n"
        "/help - Show this help message"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text
    )


async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["awaiting_file"] = True
    text = (
        "📤 *Send me your file for conversion*\n\n"
        "📁 *Supported Format Conversions:*\n"
        "• DOC ➜ PDF, DOCX, TXT\n"
        "• ODT ➜ PDF, DOCX\n"
        "• DOCX ➜ PDF, DOC, TXT, HTML\n"
        "• ODS ➜ PDF, XLSX\n"
        "• XLS ➜ PDF, XLSX, CSV\n"
        "• XLSX ➜ PDF, XLS, CSV, TXT, HTML\n"
        "• PPT ➜ PDF, PPTX\n"
        "• PPTX ➜ PDF, PPT, TXT\n"
        "• ODP ➜ PDF, PPTX\n"
        "• KEY ➜ PDF, PPTX\n"
        "• PDF ➜ DOCX, PPTX, TXT\n\n"
        "📦 *Max file size:* 10.0 MB\n"
    )

    await update.message.reply_text(text, parse_mode='Markdown')


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("awaiting_file"):
        await update.message.reply_text("Please use /start or /convert before sending a file.")
        return

    document = update.message.document
    if not document:
        await update.message.reply_text("No document found.")
        return

    file = await context.bot.get_file(document.file_id)

    filename = document.file_name
    os.makedirs("downloads", exist_ok=True)
    file_path = os.path.join("downloads", filename)

    await file.download_to_drive(file_path)
    await update.message.reply_text(f"✅ File '{filename}' received!")

    context.user_data["awaiting_file"] = False

    # Detect file type and show conversion buttons
    file_ext = filename.split('.')[-1].lower()
    formats = {
        "doc": ["pdf", "docx", "txt"],
        "odt": ["pdf", "docx"],
        "docx": ["pdf", "doc", "txt", "html"],
        "ods": ["pdf", "xlsx"],
        "xls": ["pdf", "xlsx", "csv"],
        "xlsx": ["pdf", "xls", "csv", "txt", "html"],
        "ppt": ["pdf", "pptx"],
        "pptx": ["pdf", "ppt", "txt"],
        "odp": ["pdf", "pptx"],
        "key": ["pdf", "pptx"],
        "pdf": ["docx", "pptx", "txt"],
    }

    if file_ext not in formats:
        await update.message.reply_text("❌ Sorry, this file type is not supported.")
        return

    buttons = [
        [InlineKeyboardButton(f"Convert to {fmt.upper()}", callback_data=f"{file_path}|{fmt}")]
        for fmt in formats[file_ext]
    ]

    markup = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        "Select the format you want to convert to:",
        reply_markup=markup
    )


async def handle_format_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Unpack data from the button
    data = query.data
    if "|" not in data:
        await query.edit_message_text("Invalid conversion format.")
        return

    file_path, target_format = data.split("|")
    filename = os.path.basename(file_path)

    await query.edit_message_text(f"🔄 Converting `{filename}` to `{target_format.upper()}`...", parse_mode='Markdown')

    source_ext = file_path.split('.')[-1]
    result_file = convert_file(file_path, source_ext, target_format)

    converted_filename = f"converted_{os.path.basename(file_path).split('.')[0]}.{target_format}"
    file_to_send = InputFile(result_file, filename=converted_filename)

    if result_file:
        await context.bot.send_document(chat_id=query.message.chat.id, document=file_to_send)
    else:
        await context.bot.send_message(chat_id=query.message.chat.id, text="❌ Conversion failed or unsupported format.")

    if os.path.exists(file_path):
        os.remove(file_path)


async def reject_non_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_file"):
        await update.message.reply_text("❗ Please send a file to convert.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    about_handler = CommandHandler('about', about)
    application.add_handler(about_handler)
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^About$"), about))

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^Help"), help))

    hide_handler = CommandHandler("hide", hide_keyboard)
    application.add_handler(hide_handler)

    convert_handler = CommandHandler("convert", convert)
    application.add_handler(convert_handler)
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^Convert"), convert))

    document_handler = MessageHandler(filters.Document.ALL, handle_document)
    application.add_handler(document_handler)

    application.add_handler(CallbackQueryHandler(handle_format_choice))

    application.add_handler(MessageHandler(
        (filters.TEXT | filters.PHOTO) & ~filters.COMMAND,
        reject_non_file
    ))

    application.run_polling()
