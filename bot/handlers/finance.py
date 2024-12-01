from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.utils.states import TransactionStates
from bot.keyboards.reply import get_transaction_type_keyboard, get_main_keyboard
from bot.database.repository import Repository
from bot.database.base import get_session
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.callback_query(F.data == "add_transaction")
async def start_transaction(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TransactionStates.choosing_type)
    await callback.message.edit_text(
        "Выберите тип операции:",
        reply_markup=get_transaction_type_keyboard()
    )

@router.callback_query(TransactionStates.choosing_type)
async def process_transaction_type(callback: CallbackQuery, state: FSMContext):
    if callback.data in ["income", "expense"]:
        await state.update_data(transaction_type=callback.data)
        await state.set_state(TransactionStates.entering_amount)
        await callback.message.edit_text(
            "Введите сумму операции (только число):"
        )

@router.message(TransactionStates.entering_amount)
async def process_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
        await state.update_data(amount=amount)
        
        # Получаем категории в зависимости от типа операции
        data = await state.get_data()
        categories = get_categories_keyboard(data["transaction_type"])
        
        await state.set_state(TransactionStates.choosing_category)
        await message.answer(
            "Выберите категорию:",
            reply_markup=categories
        )
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")

# Добавим вспомогательную функцию для получения категорий
def get_categories_keyboard(transaction_type: str):
    builder = InlineKeyboardBuilder()
    
    categories = {
        "income": ["Зарплата", "Подработка", "Проценты", "Другое"],
        "expense": ["Продукты", "Транспорт", "Жилье", "Развлечения", "Другое"]
    }
    
    for category in categories[transaction_type]:
        builder.button(text=category, callback_data=f"category_{category}")
    
    builder.button(text="↩️ Назад", callback_data="back_to_main")
    builder.adjust(2)
    return builder.as_markup() 

@router.callback_query(TransactionStates.choosing_category)
async def process_category(callback: CallbackQuery, state: FSMContext):
    category = callback.data.replace('category_', '')
    await state.update_data(category=category)
    
    await state.set_state(TransactionStates.entering_description)
    await callback.message.edit_text(
        "Введите описание операции (или отправьте '-' чтобы пропустить):"
    )

@router.message(TransactionStates.entering_description)
async def process_description(message: Message, state: FSMContext):
    description = None if message.text == '-' else message.text
    data = await state.get_data()
    
    # Сохраняем транзакцию в БД
    async for session in get_session():
        repo = Repository(session)
        user = await repo.get_or_create_user(
            message.from_user.id,
            message.from_user.username
        )
        
        transaction = await repo.add_transaction(
            user_id=user.id,
            type=data['transaction_type'],
            category=data['category'],
            amount=data['amount'],
            description=description
        )
    
    await state.clear()
    
    # Отправляем подтверждение
    transaction_type = "доход" if data['transaction_type'] == 'income' else "расход"
    await message.answer(
        f"✅ {transaction_type.capitalize()} успешно добавлен!\n\n"
        f"Сумма: {data['amount']} руб.\n"
        f"Категория: {data['category']}\n"
        f"Описание: {description or 'не указано'}",
        reply_markup=get_main_keyboard()
    )

@router.callback_query(F.data == "balance")
async def show_balance(callback: CallbackQuery):
    async for session in get_session():
        repo = Repository(session)
        user = await repo.get_or_create_user(
            callback.from_user.id,
            callback.from_user.username
        )
        balance = await repo.get_balance(user.id)
    
    await callback.message.edit_text(
        f"💰 Ваш текущий баланс: {balance:.2f} руб.",
        reply_markup=get_main_keyboard()
    ) 