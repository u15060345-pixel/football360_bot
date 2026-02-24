import csv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler
)

# ---------------------------
# Настройки
# ---------------------------
BOT_TOKEN = "8744795446:AAE3pLgok4r-9jMHxd71ss45c2KNsHzxi-w"
ADMIN_ID = 7785582925
ORDERS_FILE = "orders.csv"
# ---------------------------

# Шаги диалога
NAME, LINK, AD_TYPE, DATE, TG = range(5)
user_data_dict = {}

# ---------------------------
# Команды
# ---------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚽ Добро пожаловать в Football 360°!\n"
        "🔥 Здесь вы можете заказать рекламу в нашем канале.\n\n"
        "Введите ваше имя:"
    )
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data_dict[chat_id] = {'name': update.message.text}
    await update.message.reply_text("Введите ссылку на ваш канал или группу:")
    return LINK

async def get_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data_dict[chat_id]['link'] = update.message.text

    keyboard = [
        [InlineKeyboardButton("Пост", callback_data="Пост")],
        [InlineKeyboardButton("Упоминание", callback_data="Упоминание")],
        [InlineKeyboardButton("Подборка", callback_data="Подборка")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите тип рекламы:", reply_markup=reply_markup)
    return AD_TYPE

async def get_ad_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id
    user_data_dict[chat_id]['ad_type'] = query.data
    await query.message.reply_text("Введите дату публикации (ДД.MM.ГГГГ):")
    return DATE

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data_dict[chat_id]['date'] = update.message.text
    await update.message.reply_text("Введите ваш Telegram (например @username):")
    return TG

async def get_tg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data_dict[chat_id]['tg'] = update.message.text
    data = user_data_dict[chat_id]

    prices = {"Пост": 10, "Упоминание": 5, "Подборка": 15}
    price = prices.get(data['ad_type'], 0)
    data['price'] = price

    with open(ORDERS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([data['name'], data['link'], data['ad_type'], data['date'], data['tg'], price])

    await update.message.reply_text(
        f"✅ Ваша заявка принята!\nСтоимость: {price}$\nМы свяжемся с вами."
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"💌 Новая заявка на рекламу!\n"
             f"👤 Имя: {data['name']}\n"
             f"🔗 Ссылка: {data['link']}\n"
             f"📅 Дата: {data['date']}\n"
             f"💰 Тип: {data['ad_type']}\n"
             f"Telegram: {data['tg']}\n"
             f"Цена: {price}$"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Заявка отменена.")
    return ConversationHandler.END

# ---------------------------
# Основной запуск
# ---------------------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_link)],
            AD_TYPE: [CallbackQueryHandler(get_ad_type)],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
            TG: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_tg)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(conv_handler)
    print("⚡ Бот Football 360° запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
