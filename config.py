import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Превращаем строку "928116885,123456789" в список целых чисел
_admin_ids_str = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(x.strip()) for x in _admin_ids_str.split(",") if x.strip().isdigit()]

ADMIN_LIST = [item.strip() for item in _admin_ids_str.split(",") if item.strip()]