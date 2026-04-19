"""Asynchronous client for the PVOutput API."""

# pylint: disable=protected-access
import socket
from datetime import UTC, date, datetime, time
from unittest.mock import patch

import aiohttp
import pytest
from aioresponses import aioresponses
from syrupy.assertion import SnapshotAssertion

from pvo import PVOutput
from pvo.exceptions import (
    PVOutputAuthenticationError,
    PVOutputConnectionError,
    PVOutputError,
    PVOutputNoDataError,
)


async def test_request() -> None:
    """Test response is handled correctly."""
    with aioresponses() as mocked:
        mocked.get(
            "https://pvoutput.org/service/r2/test",
            status=200,
            body="ok",
            content_type="text/plain",
        )
        async with aiohttp.ClientSession() as session:
            pvoutput = PVOutput(api_key="fake", system_id=12345, session=session)
            response = await pvoutput._request("test")
            assert response == "ok"
            await pvoutput.close()


async def test_internal_session() -> None:
    """Test response is handled correctly."""
    with aioresponses() as mocked:
        mocked.get(
            "https://pvoutput.org/service/r2/test",
            status=200,
            body="ok",
            content_type="text/plain",
        )
        async with PVOutput(api_key="fake", system_id=12345) as pvoutput:
            response = await pvoutput._request("test")
            assert response == "ok"


async def test_post_request() -> None:
    """Test post requests are handled correctly."""
    with aioresponses() as mocked:
        mocked.post(
            "https://pvoutput.org/service/r2/test",
            status=200,
            body="ok",
            content_type="text/plain",
        )
        async with aiohttp.ClientSession() as session:
            pvoutput = PVOutput(api_key="fake", system_id=12345, session=session)
            response = await pvoutput._request(
                "test",
                method=aiohttp.hdrs.METH_POST,
                data={},
            )
            assert response == "ok"


async def test_timeout() -> None:
    """Test request timeout from the API."""
    with aioresponses() as mocked:
        mocked.get(
            "https://pvoutput.org/service/r2/test",
            exception=TimeoutError(),
        )
        async with aiohttp.ClientSession() as session:
            pvoutput = PVOutput(
                api_key="fake",
                system_id=12345,
                session=session,
                request_timeout=0.1,
            )
            with pytest.raises(PVOutputConnectionError):
                assert await pvoutput._request("test")


async def test_http_error400() -> None:
    """Test HTTP 404 response handling."""
    with aioresponses() as mocked:
        mocked.get(
            "https://pvoutput.org/service/r2/test",
            status=404,
            body="OMG PUPPIES!",
            content_type="text/plain",
        )
        async with aiohttp.ClientSession() as session:
            pvoutput = PVOutput(api_key="fake", system_id=12345, session=session)
            with pytest.raises(PVOutputError):
                assert await pvoutput._request("test")


async def test_http_error401() -> None:
    """Test HTTP 401 response handling."""
    with aioresponses() as mocked:
        mocked.get(
            "https://pvoutput.org/service/r2/test",
            status=401,
            body="Access denied!",
            content_type="text/plain",
        )
        async with aiohttp.ClientSession() as session:
            pvoutput = PVOutput(api_key="fake", system_id=12345, session=session)
            with pytest.raises(PVOutputAuthenticationError):
                assert await pvoutput._request("test")


async def test_communication_error() -> None:
    """Test communication error handling."""
    async with aiohttp.ClientSession() as session:
        pvoutput = PVOutput(api_key="fake", system_id=12345, session=session)
        with (
            patch.object(
                session,
                "request",
                side_effect=socket.gaierror,
            ),
            pytest.raises(PVOutputConnectionError),
        ):
            assert await pvoutput._request("test")


async def test_get_status(snapshot: SnapshotAssertion) -> None:
    """Test get status handling."""
    with aioresponses() as mocked:
        mocked.get(
            "https://pvoutput.org/service/r2/getstatus.jsp",
            status=200,
            body="20211222,18:00,3636,0,NaN,NaN,NaN,21.2,220.1",
            content_type="text/plain",
        )
        async with aiohttp.ClientSession() as session:
            pvoutput = PVOutput(api_key="fake", system_id=12345, session=session)
            status = await pvoutput.status()

    assert status.reported_date == date(2021, 12, 22)
    assert status.reported_time == time(18, 0)
    assert status.reported_datetime == datetime(
        2021,
        12,
        22,
        18,
        0,
        tzinfo=UTC,
    )
    assert status.energy_consumption is None
    assert status.energy_generation == 3636
    assert status.normalized_output is None
    assert status.power_consumption is None
    assert status.power_generation == 0
    assert status.temperature == 21.2
    assert status.voltage == 220.1

    assert status.to_dict() == snapshot


async def test_get_status_no_data() -> None:
    """Test PVOutput status without data is handled."""
    with aioresponses() as mocked:
        mocked.get(
            "https://pvoutput.org/service/r2/getstatus.jsp",
            status=400,
            body="Bad Request!",
            content_type="text/plain",
        )
        async with aiohttp.ClientSession() as session:
            pvoutput = PVOutput(api_key="fake", system_id=12345, session=session)
            with pytest.raises(PVOutputNoDataError):
                await pvoutput.status()


async def test_get_system(snapshot: SnapshotAssertion) -> None:
    """Test get system handling."""
    with aioresponses() as mocked:
        mocked.get(
            "https://pvoutput.org/service/r2/getsystem.jsp",
            status=200,
            body=(
                "Frenck,5015,CO1,17,295,JA solar JAM-300,1,5000,"
                "SolarEdge SE5000H,S,20.0,Low,20180622,51.1234,6.1234,5;;0"
            ),
            content_type="text/plain",
        )
        async with aiohttp.ClientSession() as session:
            pvoutput = PVOutput(api_key="fake", system_id=12345, session=session)
            system = await pvoutput.system()

    assert system.array_tilt == 20.0
    assert system.install_date == date(2018, 6, 22)
    assert system.inverter_brand == "SolarEdge SE5000H"
    assert system.inverter_power == 5000
    assert system.inverters == 1
    assert system.latitude == 51.1234
    assert system.longitude == 6.1234
    assert system.orientation == "S"
    assert system.panel_brand == "JA solar JAM-300"
    assert system.panel_power == 295
    assert system.panels == 17
    assert system.shade == "Low"
    assert system.status_interval == 5
    assert system.system_name == "Frenck"
    assert system.system_size == 5015
    assert system.zipcode == "CO1"

    assert system.to_dict() == snapshot


async def test_get_system_empty_install_date() -> None:
    """Test get system handling with an empty install date."""
    with aioresponses() as mocked:
        mocked.get(
            "https://pvoutput.org/service/r2/getsystem.jsp",
            status=200,
            body=(
                "Frenck,5015,1234,17,295,JA solar JAM-300,1,5000,"
                "SolarEdge SE5000H,S,20.0,Low,,51.1234,6.1234,5;;0"
            ),
            content_type="text/plain",
        )
        async with aiohttp.ClientSession() as session:
            pvoutput = PVOutput(api_key="fake", system_id=12345, session=session)
            system = await pvoutput.system()

    assert system.install_date is None
