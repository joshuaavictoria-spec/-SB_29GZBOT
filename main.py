import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Lesson menu configuration
LESSONS = {
    "python": {
        "title": "Python Basics - Lesson 1",
        "text": "Welcome to Python Basics!\n\nA variable is a container for storing data values.\n\nExample:\nname = 'John'\nage = 25",
        "file": "lessons/lesson1.pdf"
    },
    "english": {
        "title": "English - Lesson 1",
        "text": "Welcome to English Lesson 1!\n\nToday's topic: Greetings.\n\nHello = Здравствуйте\nGood morning = Доброе утро",
        "file": "lessons/lesson2.pdf"
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the main lesson menu."""
    keyboard = [
        [InlineKeyboardButton("Python Basics", callback_data="python")],
        [InlineKeyboardButton("English Lesson 1", callback_data="english")],
    ]
    await update.message.reply_text(
        "Choose a free sample lesson:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help information."""
    await update.message.reply_text(
        "This bot provides free sample lessons.\n\n"
        "/start - Show lesson menu\n"
        "/help - Show this message"
    )

async def lesson_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle lesson selection and send content."""
    query = update.callback_query
    await query.answer()
    
    lesson_key = query.data
    lesson = LESSONS.get(lesson_key)
    
    if not lesson:
        await query.message.reply_text("Lesson not found.")
        return
    
    # Send text content
    await query.message.reply_text(f"**{lesson['title']}**\n\n{lesson['text']}", parse_mode="Markdown")
    
    # Send PDF if it exists
    file_path = lesson.get("file")
    if file_path and os.path.exists(file_path):
        try:
            with open(file_path, "rb") as f:
                await query.message.reply_document(
                    document=f,
                    filename=os.path.basename(file_path),
                    caption=f"📎 {lesson['title']} - PDF"
                )
        except Exception as e:
            await query.message.reply_text(f"Could not send PDF: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(lesson_handler))
    
    print("Starting bot with long polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
