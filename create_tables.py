import asyncio
from bot.database.base import create_tables

async def main():
    await create_tables()

if __name__ == "__main__":
    asyncio.run(main()) 