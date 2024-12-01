from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_settings_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="💱 Изменить валюту", callback_data="settings_currency")
    builder.button(text="📋 Управление категориями", callback_data="settings_categories")
    builder.button(text="🔔 Уведомления", callback_data="settings_notifications")
    builder.button(text="↩️ Назад", callback_data="back_to_main")
    builder.adjust(2)
    return builder.as_markup()

def get_currency_keyboard():
    builder = InlineKeyboardBuilder()
    currencies = [("RUB", "₽"), ("USD", "$"), ("EUR", "€")]
    for code, symbol in currencies:
        builder.button(text=f"{code} {symbol}", callback_data=f"currency_{code}")
    builder.button(text="↩️ Назад", callback_data="back_to_settings")
    builder.adjust(2)
    return builder.as_markup()

def get_categories_management_keyboard(custom_categories=None):
    builder = InlineKeyboardBuilder()
    builder.button(text="➕ Добавить категорию", callback_data="add_category")
    if custom_categories:
        for category in custom_categories:
            builder.button(
                text=f"❌ {category}", 
                callback_data=f"delete_category_{category}"
            )
    builder.button(text="↩️ Назад", callback_data="back_to_settings")
    builder.adjust(2)
    return builder.as_markup() 