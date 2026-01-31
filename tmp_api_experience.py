import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            'http://localhost:8000/api/v1/experience',
            json={
                'company_name': 'Contractor',
                'role': 'Engineer',
                'description': 'Building things',
                'start_date': '2026-01-31T00:00:00',
                'end_date': None,
                'learnings': None,
            },
        )
        print(resp.status_code)
        print(resp.text)

asyncio.run(main())
