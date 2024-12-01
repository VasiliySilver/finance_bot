from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.database.base import get_session
from bot.database.models import Budget
from bot.keyboards.reply import get_categories_keyboard
from bot.utils.states import BudgetStates
from bot.database.repository import Repository
from datetime import datetime, timedelta
import json

router = Router()

@router.callback_query(F.data == "set_budget")
async def start_budget_setting(callback: CallbackQuery, state: FSMContext):
    async for session in get_session():  # Получаем сессию
        repo = Repository(session)  # Создаем репозиторий
        user = await repo.get_or_create_user(callback.from_user.id)  # Получаем или создаем пользователя
        settings = await repo.get_or_create_settings(user.id)  # Получаем или создаем настройки
        
        custom_categories = json.loads(settings.custom_categories or '[]')  # Получаем категории
        
        if not custom_categories:
            await callback.message.edit_text("❌ У вас нет доступных категорий для бюджета. Пожалуйста, добавьте их в настройках.")
            return
        
        # Создаем клавиатуру с категориями
        keyboard = get_categories_keyboard(custom_categories)  # Передаем список категорий
        
        await callback.message.edit_text(
            "Выберите категорию для бюджета:",
            reply_markup=keyboard
        )

@router.callback_query(F.data.startswith("category_"))
async def process_budget_category(callback: CallbackQuery, state: FSMContext):
    category = callback.data.split("category_")[1]  # Извлекаем название категории
    await state.update_data(category=category)  # Сохраняем категорию в состоянии
    await state.set_state(BudgetStates.entering_amount)  # Устанавливаем состояние для ввода суммы

    await callback.message.edit_text(
        "Введите сумму бюджета:"
    )

@router.message(BudgetStates.entering_amount)
async def process_budget_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text)  # Пробуем преобразовать введенное значение в число
        await state.update_data(amount=amount)  # Сохраняем сумму в состоянии
        data = await state.get_data()  # Получаем данные из состояния

        # Здесь вы можете добавить логику для сохранения бюджета в базу данных
        # Например:
        async for session in get_session():
            repo = Repository(session)
            user = await repo.get_or_create_user(message.from_user.id)
            budget = Budget(
                user_id=user.id,
                category=data['category'],
                amount=amount,
                # Добавьте другие необходимые поля, такие как даты
            )
            await repo.add_budget(budget)  # Сохраняем бюджет в базе данных

        await message.answer(
            f"✅ Бюджет на категорию '{data['category']}' установлен на сумму {amount}."
        )
        await state.clear()  # Очищаем состояние после завершения
    except ValueError:
        await message.answer("❌ Пожалуйста, введите корректное число.")

@router.message(BudgetStates.entering_dates)
async def process_budget_dates(message: Message, state: FSMContext):
    dates = message.text.split()
    if len(dates) != 2:
        await message.answer("Пожалуйста, введите две даты (начало и конец) через пробел.")
        return

    start_date_str, end_date_str = dates
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        data = await state.get_data()
        repo = message.model.repository
        user = await repo.get_or_create_user(message.from_user.id)

        budget = Budget(
            user_id=user.id,
            category=data['category'],
            amount=data['amount'],
            start_date=start_date,
            end_date=end_date
        )
        await repo.add_budget(budget)

        await message.answer(
            f"✅ Бюджет на категорию '{data['category']}' установлен на сумму {data['amount']} с {start_date_str} по {end_date_str}."
        )
        await state.clear()
    except ValueError:
        await message.answer("Неверный формат даты. Пожалуйста, используйте формат ГГГГ-ММ-ДД.") 