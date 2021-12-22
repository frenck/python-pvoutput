# pylint: disable=W0621
"""Asynchronous client for the PVOutput API."""

import asyncio

from pvo import PVOutput


async def main():
    """Show example on using the PVOutput API client."""
    async with PVOutput(
        api_key="API_KEY_FROM_PVOUTPUT_ORG",
        system_id=60017,
    ) as pvoutput:

        status = await pvoutput.status()
        print(status)


if __name__ == "__main__":
    asyncio.run(main())
