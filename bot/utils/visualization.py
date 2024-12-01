import matplotlib.pyplot as plt
import io
from bot.database.models import Transaction

class Visualization:
    @staticmethod
    def plot_income_expense(transactions: list[Transaction]) -> bytes:
        income = sum(t.amount for t in transactions if t.type == 'income')
        expense = sum(t.amount for t in transactions if t.type == 'expense')
        
        labels = ['Доходы', 'Расходы']
        sizes = [income, expense]
        colors = ['#4CAF50', '#F44336']
        
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Сохраняем график в байтовый поток
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)  # Закрываем фигуру, чтобы освободить память
        return buf.getvalue() 