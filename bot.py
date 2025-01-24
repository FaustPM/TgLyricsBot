import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import lyricsgenius
import asyncio
from requests.exceptions import ReadTimeout

# Вставьте ваш токен Telegram-бота
TELEGRAM_TOKEN = 'Ваш ключ'

# Вставьте ваш токен доступа Genius
GENIUS_ACCESS_TOKEN = 'Ваш ключ'

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация клиента Genius
genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf'Привет, {user.mention_html()}! Отправь мне название песни, и я пришлю тебе её текст.',
    )

async def get_lyrics(song_title: str) -> str:
    try:
        song = genius.search_song(song_title)
        if song:
            return song.lyrics
        else:
            return None
    except ReadTimeout as e:
        logger.error(f"Ошибка при поиске песни '{song_title}': {e}")
        return "Произошла ошибка при получении текста песни из-за проблем с подключением. Пожалуйста, попробуйте позже."
    except Exception as e:
        logger.error(f"Ошибка при поиске песни '{song_title}': {e}")
        return "Произошла ошибка при получении текста песни."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    lyrics = await get_lyrics(user_message)
    if lyrics:
        await update.message.reply_text(lyrics)
    else:
        await update.message.reply_text('Произошла ошибка при получении текста песни.')

def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
