import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# 🔑 Вставьте сюда ваш токен
BOT_TOKEN = "8744795446:AAFg-dxLgWnu-ajqZcsIAN75R98ycoNFrSo"

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я Football 360° бот. Напиши любое сообщение, и я отвечу."
    )

# Простой эхо-обработчик
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"Вы написали: {text}")

# Главная функция запуска бота
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

    # Запуск бота
    print("⚡ Бот Football 360° запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
