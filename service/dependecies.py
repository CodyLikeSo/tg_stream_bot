from aiogram.filters import BaseFilter
from aiogram.types import Message
from config import ADMIN_IDS

class IsAdmin(BaseFilter):
    """
    Фильтр проверяет, находится ли ID пользователя в списке ADMIN_IDS.
    Если да — пропускает к хендлеру. Если нет — игнорирует апдейт.
    """
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ADMIN_IDS