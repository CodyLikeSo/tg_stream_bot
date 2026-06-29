import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from service.handlers import router

# Включаем логирование
logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Подключаем роутер с нашими эндпоинтами
    dp.include_router(router)
    
    print("Бот запускается...")
    # Запускаем пуллинг
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")