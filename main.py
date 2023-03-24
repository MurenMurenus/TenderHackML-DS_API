from src import app
import asyncio


async def main() -> None:
    app.app.run(port=5000, debug=True)


if __name__ == '__main__':
    asyncio.run(main())
