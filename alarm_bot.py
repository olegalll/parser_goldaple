import asyncio
import telegram
import config

async def send_message():
    bot = telegram.Bot(token=config.telegram_bot_token)
    await bot.send_message(chat_id=config.chat_id, text='Ваш код завершил работу!')

if __name__ == "__main__":
    asyncio.run(send_message())