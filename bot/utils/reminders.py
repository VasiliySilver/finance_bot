import asyncio
from aiogram import Bot
from datetime import datetime, timedelta
from bot.database.repository import Repository
from bot.database.base import get_session

async def send_reminders(bot: Bot):
    async for session in get_session():
        repo = Repository(session)
        users = await repo.get_all_users()  # Получаем всех пользователей
        
        for user in users:
            settings = await repo.get_or_create_settings(user.id)
            if settings.notification_time:
                notification_time = datetime.strptime(settings.notification_time, "%H:%M").time()
                now = datetime.now().time()
                
                # Проверяем, если текущее время совпадает с временем уведомления
                if now.hour == notification_time.hour and now.minute == notification_time.minute:
                    await bot.send_message(
                        user.telegram_id,
                        "⏰ Время для вашего ежедневного напоминания о финансах! Не забудьте проверить свои расходы и доходы."
                    )
    
    await asyncio.sleep(60)  # Проверяем каждую минуту 