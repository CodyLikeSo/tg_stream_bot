from aiogram.filters import BaseFilter
from aiogram.types import Message
from config import ADMIN_IDS, ADMIN_LIST

class IsAdmin(BaseFilter):
    """
    Фильтр проверяет, находится ли пользователь в списке администраторов.
    Проверка идет как по Telegram ID, так и по Username (без @).
    Никаких запросов в БД не требуется.
    """
    async def __call__(self, message: Message) -> bool:
        user_id = str(message.from_user.id)
        # Если у пользователя нет никнейма, ставим пустую строку, чтобы не поймать None
        username = message.from_user.username or "" 
        
        # Проверяем: совпал ли ID (как строка) ИЛИ никнейм в нашем списке
        return (user_id in ADMIN_LIST) or (username in ADMIN_LIST)