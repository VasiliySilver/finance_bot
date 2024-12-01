from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    transactions = relationship("Transaction", back_populates="user")
    settings = relationship("UserSettings", back_populates="user", uselist=False)
    budgets = relationship("Budget", back_populates="user")

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    type = Column(String)  # 'income' или 'expense'
    category = Column(String)
    amount = Column(Float)
    description = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="transactions") 

class UserSettings(Base):
    __tablename__ = 'user_settings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    currency = Column(String, default='RUB')
    notification_time = Column(String, nullable=True)  # Время для ежедневных уведомлений
    custom_categories = Column(String, nullable=True)  # JSON строка с пользовательскими категориями
    
    user = relationship("User", back_populates="settings")

class Budget(Base):
    __tablename__ = 'budgets'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category = Column(String)
    amount = Column(Float)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    user = relationship("User", back_populates="budgets")