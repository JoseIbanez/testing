import asyncio
import time

import aiohttp


async def download_pep(pep_number: int) -> bytes:

    url = "http://localhost:5000/task/"
    print(f"Begin downloading {url}")

    body = {
            "name": str(pep_number),
            "delay": 1,
            "value": "1",
            "result": "ok"
            }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body) as resp:
            content = await resp.read()
            print(f"Finished query {url}")
            return content


async def write_to_file(pep_number: int, content: bytes) -> None:
    filename = f"/tmp/async_{pep_number}.html"
    with open(filename, "wb") as pep_file:
        print(f"Begin writing to {filename}")
        pep_file.write(content)
        print(f"Finished writing {filename}")


async def web_scrape_task(pep_number: int) -> None:
    content = await download_pep(pep_number)
    await write_to_file(pep_number, content)


async def main() -> None:
    tasks = []
    for i in range(8010, 8012):
        tasks.append(web_scrape_task(i))
    await asyncio.wait(tasks)


if __name__ == "__main__":
    s = time.perf_counter()

    asyncio.run(main())

    elapsed = time.perf_counter() - s
    print(f"Execution time: {elapsed:0.2f} seconds.")

