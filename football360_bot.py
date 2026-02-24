import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8744795446:AAFg-dxLgWnu-ajqZcsIAN75R98ycoNFrSo"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

subscribers = []
ads_orders = []  # сюда будут складываться рекламные заказы

# Подписка на рассылку
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in subscribers:
        subscribers.append(user_id)
    await update.message.reply_text("Вы подписались на рассылку рекламы!")

# Получение рекламного заказа
async def send_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    ads_orders.append(text)  # сохраняем заказ
    await update.message.reply_text("Ваш рекламный заказ принят!")

# Рассылка выбранной рекламы (только для админа)
async def send_ad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = 123456789  # замените на свой ID
    if update.message.from_user.id != admin_id:
        await update.message.reply_text("Ты не админ!")
        return

    if not ads_orders:
        await update.message.reply_text("Нет заказов для рассылки.")
        return

    # Отправляем все заказы подписчикам
    for ad in ads_orders:
        for user_id in subscribers:
            try:
                await context.bot.send_message(chat_id=user_id, text=ad)
            except Exception as e:
                logging.error(f"Не удалось отправить пользователю {user_id}: {e}")
    await update.message.reply_text("Все рекламные заказы отправлены!")
    ads_orders.clear()  # очищаем после рассылки

# Главная функция
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_order))  # все тексты считаем заказами
    app.add_handler(CommandHandler("send_ad", send_ad))

    print("⚡ Бот для рекламы с приёмом заказов запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
