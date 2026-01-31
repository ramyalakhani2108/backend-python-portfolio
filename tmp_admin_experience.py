import asyncio
import httpx

async def main():
    async with httpx.AsyncClient(follow_redirects=True) as client:
        await client.post(
            "http://localhost:8000/admin/login",
            data={"username": "admin", "password": "adminn@gmail12312"},
        )
        resp = await client.post(
            "http://localhost:8000/admin/experience",
            data={
                "company_name": "Contractor",
                "role": "Engineer",
                "description": "Building things",
                "start_date": "2024-01-01",
                "end_date": "",
                "learnings": "Learned fastapi",
            },
        )
        text = resp.text
        print("status", resp.status_code)
        print("contains Internal Server Error?", "Internal Server Error" in text)
        print("contains API call failed", "API call failed" in text)
        print(text)

asyncio.run(main())
