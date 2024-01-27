# ShinyPy
An API wrapper for ShinyDB!

Example:
```
from shinypy import ShinyClient
import asyncio


async def main():
	client = ShinyClient(key = "API-KEY")
	user = await client.get_user("RyZe")
	print(user)
	await client.close()


asyncio.run(main())

```