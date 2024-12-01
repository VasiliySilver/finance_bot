from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from .models import User, Transaction, UserSettings, Budget

class Repository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_user(self, telegram_id: int, username: str = None) -> User:
        async with self.session.begin():
            query = select(User).where(User.telegram_id == telegram_id)
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            
            if user is None:
                user = User(telegram_id=telegram_id, username=username)
                self.session.add(user)
                await self.session.commit()
            
            return user

    async def add_transaction(
        self, 
        user_id: int, 
        type: str, 
        category: str, 
        amount: float, 
        description: str = None
    ) -> Transaction:
        async with self.session.begin():
            transaction = Transaction(
                user_id=user_id,
                type=type,
                category=category,
                amount=amount,
                description=description
            )
            self.session.add(transaction)
            await self.session.commit()
            return transaction

    async def get_balance(self, user_id: int) -> float:
        async with self.session.begin():
            query = select(Transaction).where(Transaction.user_id == user_id)
            result = await self.session.execute(query)
            transactions = result.scalars().all()
            
            balance = 0
            for transaction in transactions:
                if transaction.type == 'income':
                    balance += transaction.amount
                else:
                    balance -= transaction.amount
            
            return balance

    async def get_transactions_by_period(
        self, 
        user_id: int, 
        days: int = 30
    ) -> list[Transaction]:
        async with self.session.begin():
            date_from = datetime.now() - timedelta(days=days)
            query = select(Transaction).where(
                Transaction.user_id == user_id,
                Transaction.date >= date_from
            )
            result = await self.session.execute(query)
            return result.scalars().all()

    async def get_or_create_settings(self, user_id: int) -> UserSettings:
        async with self.session.begin():
            query = select(UserSettings).where(UserSettings.user_id == user_id)
            result = await self.session.execute(query)
            settings = result.scalar_one_or_none()
            
            if settings is None:
                settings = UserSettings(user_id=user_id)
                self.session.add(settings)
                await self.session.commit()
            
            return settings

    async def save_settings(self, settings: UserSettings):
        if not self.session.is_active:
            async with self.session.begin():
                self.session.add(settings)
        else:
            self.session.add(settings)
        await self.session.commit()

    async def get_all_users(self) -> list[User]:
        async with self.session.begin():
            query = select(User)
            result = await self.session.execute(query)
            return result.scalars().all()

    async def add_budget(self, budget: Budget):
        async with self.session.begin():
            self.session.add(budget)
            await self.session.commit() 