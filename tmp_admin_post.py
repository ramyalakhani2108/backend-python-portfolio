import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        await client.post(
            'http://localhost:8000/admin/login',
            data={'username': 'admin', 'password': 'adminn@gmail12312'},
        )
        resp = await client.post(
            'http://localhost:8000/admin/experience',
            data={
                'company_name': 'CLI Test',
                'role': 'Engineer',
                'description': 'Testing redirect',
                'start_date': '2026-01-31',
                'end_date': '',
                'learnings': '',
            },
            follow_redirects=False,
        )
        print('status', resp.status_code)
        print('headers', resp.headers)
        text = resp.text
        markers = ["Status:", "Payload:", "Response:"]
        for marker in markers:
            idx = text.find(marker)
            if idx != -1:
                print(marker, text[idx:idx+200])

asyncio.run(main())
