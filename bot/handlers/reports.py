from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from bot.utils.states import ReportStates
from bot.keyboards.reply import get_report_period_keyboard, get_report_type_keyboard
from bot.utils.reports import ReportGenerator
import tempfile

router = Router()

@router.callback_query(F.data == "statistics")
async def start_report(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ReportStates.choosing_period)
    await callback.message.edit_text(
        "Выберите период для отчета:",
        reply_markup=get_report_period_keyboard()
    )

@router.callback_query(ReportStates.choosing_period)
async def process_report_period(callback: CallbackQuery, state: FSMContext):
    if callback.data.startswith("report_"):
        days = int(callback.data.split("_")[1])
        await state.update_data(days=days)
        await state.set_state(ReportStates.choosing_type)
        await callback.message.edit_text(
            "Выберите тип отчета:",
            reply_markup=get_report_type_keyboard()
        )

@router.callback_query(ReportStates.choosing_type)
async def process_report_type(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    days = data['days']
    
    repo = callback.model.repository
    user = await repo.get_or_create_user(callback.from_user.id)
    transactions = await repo.get_transactions_by_period(user.id, days)
    
    if callback.data == "report_summary":
        report = ReportGenerator.generate_summary(transactions)
        await callback.message.edit_text(
            report,
            parse_mode="HTML",
            reply_markup=get_report_type_keyboard()
        )
    
    elif callback.data == "report_categories":
        report = ReportGenerator.generate_category_report(transactions)
        await callback.message.edit_text(
            report,
            parse_mode="HTML",
            reply_markup=get_report_type_keyboard()
        )
    
    elif callback.data == "report_excel":
        excel_data = ReportGenerator.generate_excel_report(transactions)
        
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            tmp.write(excel_data)
            tmp.flush()
            
            file = FSInputFile(tmp.name, filename=f"finance_report_{days}days.xlsx")
            await callback.message.answer_document(
                file,
                caption=" Ваш отчет готов!"
            )
    
    await state.clear() 