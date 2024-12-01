from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from bot.utils.visualization import Visualization
from bot.database.repository import Repository

router = Router()

@router.callback_query(F.data == "visualization")
async def start_visualization(callback: CallbackQuery, state: FSMContext):
    repo = callback.model.repository
    user = await repo.get_or_create_user(callback.from_user.id)
    transactions = await repo.get_transactions_by_period(user.id, days=30)  # За последний месяц

    if not transactions:
        await callback.message.edit_text(" У вас нет транзакций за последний месяц.")
        return

    # Генерируем график
    image_data = Visualization.plot_income_expense(transactions)

    # Отправляем график пользователю
    await callback.message.answer_photo(image_data, caption="📊 График доходов и расходов за последний месяц.") 