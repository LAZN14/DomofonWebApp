import os
from dotenv import load_dotenv
from telegram import Update, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import json

# Настраиваем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
WEB_APP_URL = "https://ваш_url_веб_приложения"  # Замените на URL вашего веб-приложения

# Проверяем наличие токена
if not TOKEN:
    raise ValueError("Не найден BOT_TOKEN в файле .env")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    logger.info(f"Пользователь {user.id} запустил команду start")
    
    # Создаем кнопку для веб-приложения
    web_app_button = KeyboardButton(
        text="Открыть веб-приложение", 
        web_app=WebAppInfo(url=WEB_APP_URL)
    )
    
    # Создаем клавиатуру с кнопкой
    keyboard = ReplyKeyboardMarkup(
        [[web_app_button]], 
        resize_keyboard=True
    )
    
    try:
        await update.message.reply_text(
            f'Привет, {user.first_name}! Я ваш новый телеграм бот.\n'
            'Нажмите на кнопку ниже, чтобы открыть веб-приложение, или используйте /help для списка команд.',
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Ошибка в команде start: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    user = update.effective_user
    logger.info(f"Пользователь {user.id} запустил команду help")
    try:
        await update.message.reply_text(
            'Доступные команды:\n'
            '/start - Начать взаимодействие с ботом\n'
            '/help - Показать это сообщение\n'
            'Также вы можете использовать кнопку "Открыть веб-приложение" для доступа к веб-интерфейсу.'
        )
    except Exception as e:
        logger.error(f"Ошибка в команде help: {e}")

async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик данных от веб-приложения"""
    try:
        data = update.effective_message.web_app_data.data
        data_dict = json.loads(data)
        logger.info(f"Получены данные от веб-приложения: {data}")
        
        if data_dict.get('authenticated'):
            phone = data_dict.get('phone', 'не указан')
            await update.message.reply_text(
                f"Получены данные от авторизованного пользователя:\n"
                f"Телефон: {phone}\n"
                f"Сообщение: {data_dict.get('message', '')}"
            )
        else:
            await update.message.reply_text("Получены данные от неавторизованного пользователя")
            
    except Exception as e:
        logger.error(f"Ошибка при обработке данных веб-приложения: {e}")
        await update.message.reply_text("Произошла ошибка при обработке данных")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Эхо-ответ на сообщения пользователя"""
    user = update.effective_user
    logger.info(f"Пользователь {user.id} отправил сообщение: {update.message.text}")
    try:
        await update.message.reply_text(update.message.text)
    except Exception as e:
        logger.error(f"Ошибка в эхо-обработчике: {e}")

def main():
    """Основная функция запуска бота"""
    try:
        logger.info(f"Используется токен: {TOKEN[:10]}...")
        
        # Создаем приложение
        application = Application.builder().token(TOKEN).build()

        # Добавляем обработчики команд
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        
        # Добавляем обработчик данных от веб-приложения
        application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
        
        # Добавляем обработчик текстовых сообщений
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

        # Запускаем бота
        logger.info("Бот запускается...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        raise e

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}") 