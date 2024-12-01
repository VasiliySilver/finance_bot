from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.keyboards.reply import get_main_keyboard
from bot.database.models import User

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Добро пожаловать в Financial Bot!\n\n"
        "Я помогу вам вести учет ваших финансов. "
        "Используйте кнопки ниже для навигации:",
        reply_markup=get_main_keyboard()
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    help_text = (
        "📚 <b>Доступные команды:</b>\n\n"
        "/start - Начать работу с ботом\n"
        "/add - Добавить новую операцию\n"
        "/stats - Посмотреть статистику\n"
        "/balance - Текущий баланс\n"
        "/report - Сформировать отчет\n"
        "/settings - Настройки\n"
        "/help - Показать это сообщение\n\n"
        "Используйте кнопки меню для удобной навигации."
    )
    await message.answer(help_text, parse_mode="HTML")

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "Главное меню:",
        reply_markup=get_main_keyboard()
    ) 