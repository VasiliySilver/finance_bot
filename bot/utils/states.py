from aiogram.fsm.state import State, StatesGroup

class TransactionStates(StatesGroup):
    choosing_type = State()        # Выбор типа операции (доход/расход)
    entering_amount = State()      # Ввод суммы
    choosing_category = State()    # Выбор категории
    entering_description = State() # Ввод описания (опционально)
    confirming = State()          # Подтверждение операции

class ReportStates(StatesGroup):
    choosing_period = State()      # Выбор периода отчета
    choosing_type = State()        # Выбор типа отчета 

class SettingsStates(StatesGroup):
    choosing_setting = State()     # Выбор настройки для изменения
    setting_currency = State()     # Установка валюты
    adding_category = State()      # Добавление новой категории
    setting_notification = State() # Установка времени уведомлений

class BudgetStates(StatesGroup):
    setting_budget = State()        # Установка бюджета
    choosing_category = State()      # Выбор категории для бюджета
    entering_amount = State()        # Ввод суммы бюджета
    entering_dates = State()         # Ввод дат начала и окончания бюджета