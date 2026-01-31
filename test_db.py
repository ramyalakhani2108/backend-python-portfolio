import asyncio
from sqlalchemy import text
from app.core.database import engine

async def test_db():
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text('SELECT 1'))
            print('Database connection successful')
    except Exception as e:
        print(f'Database connection failed: {e}')

if __name__ == "__main__":
    asyncio.run(test_db())