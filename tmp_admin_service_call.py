import asyncio
from app.admin.services import admin_api_service

async def main():
    result = await admin_api_service.create_experience({
        'company_name': 'Inline Test',
        'role': 'Engineer',
        'description': 'Testing admin service',
        'start_date': '2026-01-31T00:00:00',
        'end_date': None,
        'learnings': 'Testing',
    })
    print(result)

asyncio.run(main())
