from users.models import PREFERRED_TIME_SLOTS, LANGUAGES, LEVELS, STATUS_CHOICES, REGISTERED_TYPES

preferred_time_slots = dict(PREFERRED_TIME_SLOTS)
languages = dict(LANGUAGES)
levels = dict(LEVELS)
status_choices = dict(STATUS_CHOICES)
registered_types = dict(REGISTERED_TYPES)

headers_users = [
    "Telegram ID",                         # Telegram ID
    "F.I.Sh.",                             # F.I.Sh. (F.I.Sh. - F.I.Sh. (Ism, Otasining ismi, Familiya))
    "Telegram kontakti",                   # Telegram kontakti
    "Telefon raqami",                      # Telefon raqami
    "Afzal vaqt",                          # Afzal vaqt
    "Til",                                 # Til
    "Tanlangan daraja",                   # Tanlangan daraja
    "Tasdiqlangan daraja",                # Tasdiqlangan daraja
    "Tavsiya etilgan daraja",             # Tavsiya etilgan daraja
    "Holat",                               # Holat
    "Ro'yxatdan o'tish turi",             # Ro'yxatdan o'tish turi
    "Ro'yxatdan o'tgan vaqt",             # Ro'yxatdan o'tgan vaqt
    "Yangilangan vaqt"                     # Yangilangan vaqt
]