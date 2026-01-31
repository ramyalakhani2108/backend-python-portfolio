import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        resp = await client.get('http://localhost:8000/api/v1/experience')
        print(resp.status_code)
        print(resp.text)

asyncio.run(main())
