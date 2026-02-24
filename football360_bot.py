import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Переменная BOT_TOKEN не установлена!")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Новости футбола", callback_data="news")],
        [InlineKeyboardButton("Турниры", callback_data="tournaments")],
        [InlineKeyboardButton("Статистика", callback_data="stats")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Добро пожаловать в Football 360° ⚽\nВыбери раздел:", reply_markup=reply_markup)

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "news":
        text = "Последние новости футбола:\n1. Матч A-B...\n2. Трансфер игрока X..."
    elif query.data == "tournaments":
        text = "Текущие турниры:\n- Чемпионат мира\n- Лига чемпионов"
    elif query.data == "stats":
        text = "Статистика игроков:\n- Игрок 1: 10 голов\n- Игрок 2: 7 голов"
    else:
        text = "Неверная команда."
    
    # Кнопка "Назад"
    keyboard = [[InlineKeyboardButton("Назад в меню", callback_data="back")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup)

# Обработка кнопки "Назад"
async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(update, context)

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Используй кнопки для навигации или /start для начала.")

# Основная функция
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler, pattern="^(news|tournaments|stats)$"))
    app.add_handler(CallbackQueryHandler(back, pattern="^back$"))

    print("⚡ Бот Football 360° запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
