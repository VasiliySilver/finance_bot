import json
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.database.base import get_session
from bot.database.repository import Repository
from bot.utils.states import SettingsStates
from bot.keyboards.settings import (
    get_settings_keyboard,
    get_currency_keyboard,
    get_categories_management_keyboard
)
from datetime import datetime
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.callback_query(F.data == "settings")
async def show_settings(callback: CallbackQuery):
    await callback.message.edit_text(
        "⚙️ Настройки\n\n"
        "Выберите параметр для настройки:",
        reply_markup=get_settings_keyboard()
    )

@router.callback_query(F.data == "settings_currency")
async def show_currency_settings(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsStates.setting_currency)
    await callback.message.edit_text(
        "💱 Выберите валюту:",
        reply_markup=get_currency_keyboard()
    )

@router.callback_query(SettingsStates.setting_currency)
async def process_currency_setting(callback: CallbackQuery, state: FSMContext):
    if callback.data.startswith("currency_"):
        currency = callback.data.split("_")[1]
        repo = callback.model.repository
        user = await repo.get_or_create_user(callback.from_user.id)
        
        # Обновляем настройки пользователя
        settings = await repo.get_or_create_settings(user.id)
        settings.currency = currency
        await repo.save_settings(settings)
        
        await callback.message.edit_text(
            f"✅ Валюа успешно изменена на {currency}",
            reply_markup=get_settings_keyboard()
        )
        await state.clear()

@router.callback_query(F.data == "settings_categories")
async def show_categories_settings(callback: CallbackQuery, state: FSMContext):
    async for session in get_session():
        repo = Repository(session)
        user = await repo.get_or_create_user(callback.from_user.id)
        settings = await repo.get_or_create_settings(user.id)
        
        custom_categories = json.loads(settings.custom_categories or '[]')
        
        await callback.message.edit_text(
            "📋 Управление категориями\n\n"
            "Добавьте свои категории или удалите существующие:",
            reply_markup=get_categories_management_keyboard(custom_categories)
        )

@router.callback_query(F.data == "add_category")
async def start_category_adding(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsStates.adding_category)
    await callback.message.edit_text(
        "Введите название новой категории:"
    )

@router.message(SettingsStates.adding_category)
async def process_new_category(message: Message, state: FSMContext):
    new_category = message.text.strip()
    
    async for session in get_session():  # Получаем сессию
        repo = Repository(session)  # Создаем репозиторий
        user = await repo.get_or_create_user(message.from_user.id)  # Получаем или создаем пользователя
        settings = await repo.get_or_create_settings(user.id)  # Получаем или создаем настройки
        
        custom_categories = json.loads(settings.custom_categories or '[]')
        if new_category not in custom_categories:
            custom_categories.append(new_category)
            settings.custom_categories = json.dumps(custom_categories)
            await repo.save_settings(settings)
        
        await message.answer(
            f"✅ Категория '{new_category}' добавлена!",
            reply_markup=get_categories_management_keyboard(custom_categories)
        )
        await state.clear()

@router.callback_query(F.data == "settings_notifications")
async def show_notification_settings(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsStates.setting_notification)
    await callback.message.edit_text(
        "🔔 Установите время для ежедневных уведомлений (в формате ЧЧ:ММ):"
    )

@router.message(SettingsStates.setting_notification)
async def process_notification_time(message: Message, state: FSMContext):
    time_str = message.text.strip()
    try:
        # Проверяем, что время в правильном формате
        datetime.strptime(time_str, "%H:%M")
        
        async for session in get_session():  # Получаем сессию
            repo = Repository(session)  # Создаем репозиторий
            user = await repo.get_or_create_user(message.from_user.id)
            settings = await repo.get_or_create_settings(user.id)
            
            settings.notification_time = time_str
            await repo.save_settings(settings)
            
            await message.answer(
                f"✅ Время уведомления успешно установлено на {time_str}.",
                reply_markup=get_settings_keyboard()
            )
            await state.clear()
    except ValueError:
        await message.answer("❌ Неверный формат времени. Пожалуйста, используйте формат ЧЧ:ММ.") 