from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Добавить операцию", callback_data="add_transaction")
    builder.button(text="📊 Статистика", callback_data="statistics")
    builder.button(text="💰 Баланс", callback_data="balance")
    builder.button(text="📈 Визуализация", callback_data="visualization")
    builder.button(text="💵 Установить бюджет", callback_data="set_budget")
    builder.button(text="⚙️ Настройки", callback_data="settings")
    builder.adjust(2)
    return builder.as_markup()

def get_transaction_type_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="➕ Доход", callback_data="income")
    builder.button(text="➖ Расход", callback_data="expense")
    builder.button(text="↩️ Назад", callback_data="back_to_main")
    builder.adjust(2)
    return builder.as_markup()

def get_report_period_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="За неделю", callback_data="report_7")
    builder.button(text="За месяц", callback_data="report_30")
    builder.button(text="За 3 месяца", callback_data="report_90")
    builder.button(text="За год", callback_data="report_365")
    builder.button(text="↩️ Назад", callback_data="back_to_main")
    builder.adjust(2)
    return builder.as_markup()

def get_report_type_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="📊 Сводка", callback_data="report_summary")
    builder.button(text="📋 По категориям", callback_data="report_categories")
    builder.button(text="📥 Выгрузить Excel", callback_data="report_excel")
    builder.button(text="↩️ Назад", callback_data="back_to_main")
    builder.adjust(2)
    return builder.as_markup()

def get_categories_keyboard(custom_categories):
    builder = InlineKeyboardBuilder()
    
    for category in custom_categories:
        builder.button(text=category, callback_data=f"category_{category}")
    
    builder.button(text="↩️ Назад", callback_data="back_to_main")
    builder.adjust(2)
    return builder.as_markup() 