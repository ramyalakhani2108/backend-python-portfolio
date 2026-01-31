import asyncio
import httpx

async def main():
    async with httpx.AsyncClient(follow_redirects=True) as client:
        login_resp = await client.post(
            "http://localhost:8000/admin/login",
            data={"username": "admin", "password": "adminn@gmail12312"},
        )
        print("login status", login_resp.status_code)
        resp = await client.post(
            "http://localhost:8000/admin/experience",
            data={
                "company_name": "Test Co",
                "role": "Tester",
                "description": "Desc",
                "start_date": "",
                "end_date": "",
                "learnings": "",
            },
        )
        print(resp.status_code)
        print(resp.headers.get('content-type'))
        print(resp.text[:500]) 
        

asyncio.run(main())
