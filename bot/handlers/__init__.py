from aiogram import Dispatcher
from .common import router as common_router
from .finance import router as finance_router
from .reports import router as reports_router
from .settings import router as settings_router
from .visualization import router as visualization_router
from .budgets import router as budgets_router

def register_all_handlers(dp: Dispatcher):
    dp.include_router(common_router)
    dp.include_router(finance_router)
    dp.include_router(reports_router)
    dp.include_router(settings_router)
    dp.include_router(visualization_router)
    dp.include_router(budgets_router) 