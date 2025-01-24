import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from transformers import pipeline

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка модели для генерации текста
chatbot = pipeline("text-generation", model="sberbank-ai/rugpt3small_based_on_gpt2")

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я твой чат-бот. Напиши мне что-нибудь, и я постараюсь ответить.')

# Обработчик текстовых сообщений
async def echo(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    logger.info(f"User: {user_message}")

    # Генерация ответа с помощью модели
    bot_response = chatbot(user_message, max_length=50, num_return_sequences=1)[0]['generated_text']
    logger.info(f"Bot: {bot_response}")

    await update.message.reply_text(bot_response)

# Обработчик ошибок
async def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update {update} caused error {context.error}')

# Основная функция
def main() -> None:
    # Вставь сюда свой токен
    application = Application.builder().token("7083802706:AAEettPYqUtyaWQCzMzP6rtJZhyej4MGaVs").build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_error_handler(error)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()