import trio
import httpx

from ignorant.modules.shopping.amazon import amazon


async def main():
    phone="5524330233"
    country_code="52"
    client = httpx.AsyncClient()
    out = []

    await amazon(phone, country_code, client, out)

    print(out)
    await client.aclose()

trio.run(main)