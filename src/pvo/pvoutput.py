"""Asynchronous client for the PVOutput API."""
from __future__ import annotations

import asyncio
import socket
from dataclasses import dataclass
from importlib import metadata
from typing import Any, Self

import async_timeout
from aiohttp.client import ClientError, ClientResponseError, ClientSession
from aiohttp.hdrs import METH_GET
from yarl import URL

from .exceptions import (
    PVOutputAuthenticationError,
    PVOutputConnectionError,
    PVOutputError,
    PVOutputNoDataError,
)
from .models import Status, System


@dataclass
class PVOutput:
    """Main class for handling connections with the PVOutput API."""

    api_key: str
    system_id: int

    request_timeout: float = 8.0
    session: ClientSession | None = None

    _close_session: bool = False

    async def _request(
        self,
        uri: str,
        *,
        method: str = METH_GET,
        data: dict[str, Any] | None = None,
    ) -> str:
        """Handle a request to the PVOutput API.

        A generic method for sending/handling HTTP requests done against
        the PVOutput API.

        Args:
        ----
            uri: Request URI, without '/service/r2/'.
            method: HTTP Method to use.
            data: Dictionary of parameters to send to the PVOutput API.

        Returns:
        -------
            The response body from the PVOutput API.

        Raises:
        ------
            PVOutputAuthenticationError: If the API key is invalid.
            PVOutputConnectionError: An error occurred while communicating with
                the PVOutput API.
            PVOutputError: Received an unexpected response from the PVOutput
                API.
        """
        version = metadata.version(__package__)
        url = URL("https://pvoutput.org/service/r2/").join(URL(uri))

        headers = {
            "Accept": "application/json",
            "User-Agent": f"PythonPVOutput/{version}",
            "X-Pvoutput-Apikey": self.api_key,
            "X-Pvoutput-SystemId": str(self.system_id),
        }

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self.session.request(
                    method,
                    url,
                    data=data,
                    headers=headers,
                )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            msg = "Timeout occurred while connecting to the PVOutput API"
            raise PVOutputConnectionError(msg) from exception
        except ClientResponseError as exception:
            if exception.status == 400 and uri.startswith("getstatus.jsp"):
                msg = "PVOutput has no status data available for this system"
                raise PVOutputNoDataError(msg) from exception
            if exception.status in [401, 403]:
                msg = "Authentication to the PVOutput API failed"
                raise PVOutputAuthenticationError(msg) from exception
            msg = "Error occurred while connecting to the PVOutput API"
            raise PVOutputError(msg) from exception
        except (ClientError, socket.gaierror) as exception:
            msg = "Error occurred while communicating with the PVOutput API"
            raise PVOutputConnectionError(msg) from exception

        return await response.text()

    async def status(self) -> Status:
        """Retrieve system status information and live output data.

        Returns
        -------
            An PVOutput Status object.
        """
        data = await self._request("getstatus.jsp")
        return Status.parse_obj(
            zip(
                [
                    "reported_date",
                    "reported_time",
                    "energy_generation",
                    "power_generation",
                    "energy_consumption",
                    "power_consumption",
                    "normalized_output",
                    "temperature",
                    "voltage",
                ],
                data.split(","),
                strict=True,
            ),
        )

    async def system(self) -> System:
        """Retrieve system information.

        Returns
        -------
            An PVOutput System object.
        """
        data = await self._request("getsystem.jsp")
        return System.parse_obj(
            zip(
                [
                    "system_name",
                    "system_size",
                    "zipcode",
                    "panels",
                    "panel_power",
                    "panel_brand",
                    "inverters",
                    "inverter_power",
                    "inverter_brand",
                    "orientation",
                    "array_tilt",
                    "shade",
                    "install_date",
                    "latitude",
                    "longitude",
                    "status_interval",
                ],
                data.partition(";")[0].split(","),
                strict=True,
            ),
        )

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns
        -------
            The PVOutput object.
        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.
        """
        await self.close()
