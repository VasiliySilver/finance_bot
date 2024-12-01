from datetime import datetime, timedelta
import pandas as pd
import io
from bot.database.models import Transaction

class ReportGenerator:
    @staticmethod
    def generate_summary(transactions: list[Transaction]) -> str:
        if not transactions:
            return "За выбранный период операций не найдено."
        
        income = sum(t.amount for t in transactions if t.type == 'income')
        expense = sum(t.amount for t in transactions if t.type == 'expense')
        balance = income - expense
        
        return (
            "📊 <b>Сводка за период:</b>\n\n"
            f"📈 Доходы: {income:.2f} руб.\n"
            f"📉 Расходы: {expense:.2f} руб.\n"
            f"💰 Баланс: {balance:.2f} руб.\n\n"
            f"Количество операций: {len(transactions)}"
        )

    @staticmethod
    def generate_category_report(transactions: list[Transaction]) -> str:
        if not transactions:
            return "За выбранный период операций не найдено."
        
        categories = {}
        for t in transactions:
            if t.category not in categories:
                categories[t.category] = {'income': 0, 'expense': 0}
            categories[t.category][t.type] += t.amount
        
        report = "📊 <b>Отчет по категориям:</b>\n\n"
        
        for category, amounts in categories.items():
            report += f"<b>{category}</b>\n"
            if amounts['income'] > 0:
                report += f"  Доходы: {amounts['income']:.2f} руб.\n"
            if amounts['expense'] > 0:
                report += f"  Расходы: {amounts['expense']:.2f} руб.\n"
            report += "\n"
        
        return report

    @staticmethod
    def generate_excel_report(transactions: list[Transaction]) -> bytes:
        data = []
        for t in transactions:
            data.append({
                'Дата': t.date,
                'Тип': 'Доход' if t.type == 'income' else 'Расход',
                'Категория': t.category,
                'Сумма': t.amount,
                'Описание': t.description or ''
            })
        
        df = pd.DataFrame(data)
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Операции', index=False)
        
        output.seek(0)
        return output.getvalue() 