from aiogram.filters import BaseFilter

from config.secrets.secret_keys import ADMINS


class AdminFilter(BaseFilter):
    async def __call__(self, obj):
        return obj.chat.type == 'private' and obj.from_user.id in ADMINS
