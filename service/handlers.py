from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from service.db import db
from service.dependecies import IsAdmin

router = Router()

# =====================================================================
# ХЕНДЛЕРЫ АДМИНА
# =====================================================================

@router.message(Command("start_stream"), IsAdmin())
async def cmd_start_stream(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("⚠️ Укажи ссылку на стрим!\nПример: `/start_stream https://twitch.tv/...`", parse_mode="Markdown")
        return
        
    stream_url = args[1]
    db.set_stream_status(1, stream_url)
    await message.answer(f"✅ Стрим запущен! Ссылка сохранена:\n{stream_url}\n\n*У всех пользователей сброшен статус (теперь им нужно дать согласие заново).*")

@router.message(Command("end_stream"), IsAdmin())
async def cmd_end_stream(message: types.Message):
    db.set_stream_status(0, None)
    await message.answer("🛑 Стрим завершен. Ссылка удалена из базы. Пользователи переведены в статус 'офф'.")

# =====================================================================
# ХЕНДЛЕРЫ ОБЫЧНЫХ ПОЛЬЗОВАТЕЛЕЙ
# =====================================================================

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    tg_id = message.from_user.id
    username = message.from_user.username or "Anonymous"
    
    # 1. Проверяем, есть ли сейчас активный стрим
    is_active, stream_url = db.get_stream_info()
    
    if not is_active:
        # Стрима нет — ответа нет
        return
        
    # 2. Стрим идет. Проверяем пользователя в БД
    has_agreed = db.get_user_agreement(tg_id)
    if has_agreed is None:
        db.add_user(tg_id, username)
        has_agreed = 0
        
    # 3. Если согласие на этот стрим уже получено
    if has_agreed == 1:
        await message.answer(f"Привет! Эфир уже идет, залетай:\n{stream_url}")
        return

    # 4. Стрим идет, но согласия еще нет — запрашиваем
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Да, готов", callback_data="consent_yes"),
            InlineKeyboardButton(text="Нет", callback_data="consent_no")
        ]
    ])
    
    await message.answer(
        "Готовы ли вы подписать файл о том что вы будете в эфире и вас будут выкладывать в сеть?", 
        reply_markup=kb
    )

@router.callback_query(F.data.startswith("consent_"))
async def process_consent(callback: types.CallbackQuery):
    tg_id = callback.from_user.id
    await callback.answer() 
    
    # Защита от старых кнопок: проверяем, идет ли стрим прямо сейчас
    is_active, stream_url = db.get_stream_info()
    if not is_active:
        await callback.message.edit_text("Эфир уже завершен. Согласие пока не требуется.")
        return

    if callback.data == "consent_no":
        await callback.message.edit_text("Вы отказались. Если передумаете, нажмите /start")
        return
        
    if callback.data == "consent_yes":
        # Активируем пользователя для текущего стрима
        db.agree_user(tg_id)
        await callback.message.edit_text(f"✅ Отлично, вы в деле! Эфир идет, вот ссылка:\n{stream_url}")