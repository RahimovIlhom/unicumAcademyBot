from aiogram.filters import BaseFilter


class PrivateFilter(BaseFilter):
    async def __call__(self, obj):
        return obj.chat.type == 'private'
