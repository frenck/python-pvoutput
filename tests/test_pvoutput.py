"""Asynchronous client for the PVOutput API."""
# pylint: disable=protected-access
import asyncio
from datetime import date, datetime, time

import aiohttp
import pytest

from pvo import PVOutput
from pvo.exceptions import (
    PVOutputAuthenticationError,
    PVOutputConnectionError,
    PVOutputError,
)


@pytest.mark.asyncio
async def test_request(aresponses):
    """Test response is handled correctly."""
    aresponses.add(
        "pvoutput.org",
        "/service/r2/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "text/plain"},
            text="ok",
        ),
    )
    async with aiohttp.ClientSession() as session:
        pvoutput = PVOutput(api_key="fake", system_id=12345, session=session)
        response = await pvoutput._request("test")
        assert response == "ok"
        await pvoutput.close()


@pytest.mark.asyncio
async def test_internal_session(aresponses):
    """Test response is handled correctly."""
    aresponses.add(
        "pvoutput.org",
        "/service/r2/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "text/plain"},
            text="ok",
        ),
    )
    async with PVOutput(api_key="fake", system_id=12345) as pvoutput:
        response = await pvoutput._request("test")
        assert response == "ok"


@pytest.mark.asyncio
async def test_post_request(aresponses):
    """Test post requests are handled correctly."""
    aresponses.add(
        "pvoutput.org",
        "/service/r2/test",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "text/plain"},
            text="ok",
        ),
    )
    async with aiohttp.ClientSession() as session:
        pvoutput = PVOutput(api_key="fake", system_id=12345, session=session)
        response = await pvoutput._request(
            "test", method=aiohttp.hdrs.METH_POST, data={}
        )
        assert response == "ok"


@pytest.mark.asyncio
async def test_timeout(aresponses):
    """Test request timeout from the API."""
    # Faking a timeout by sleeping
    async def response_handler(_):
        """Response handler for this test."""
        await asyncio.sleep(0.2)
        return aresponses.Response(body="Goodmorning!")

    aresponses.add("pvoutput.org", "/service/r2/test", "GET", response_handler)

    async with aiohttp.ClientSession() as session:
        pvoutput = PVOutput(
            api_key="fake", system_id=12345, session=session, request_timeout=0.1
        )
        with pytest.raises(PVOutputConnectionError):
            assert await pvoutput._request("test")


@pytest.mark.asyncio
async def test_http_error400(aresponses):
    """Test HTTP 404 response handling."""
    aresponses.add(
        "pvoutput.org",
        "/service/r2/test",
        "GET",
        aresponses.Response(text="OMG PUPPIES!", status=404),
    )

    async with aiohttp.ClientSession() as session:
        pvoutput = PVOutput(api_key="fake", system_id=12345, session=session)
        with pytest.raises(PVOutputError):
            assert await pvoutput._request("test")


@pytest.mark.asyncio
async def test_http_error401(aresponses):
    """Test HTTP 401 response handling."""
    aresponses.add(
        "pvoutput.org",
        "/service/r2/test",
        "GET",
        aresponses.Response(text="Access denied!", status=401),
    )

    async with aiohttp.ClientSession() as session:
        pvoutput = PVOutput(api_key="fake", system_id=12345, session=session)
        with pytest.raises(PVOutputAuthenticationError):
            assert await pvoutput._request("test")


@pytest.mark.asyncio
async def test_get_status(aresponses):
    """Test get status handling."""
    aresponses.add(
        "pvoutput.org",
        "/service/r2/getstatus.jsp",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "text/plain"},
            text="20211222,18:00,3636,0,NaN,NaN,NaN,21.2,220.1",
        ),
    )

    async with aiohttp.ClientSession() as session:
        pvoutput = PVOutput(api_key="fake", system_id=12345, session=session)
        status = await pvoutput.status()

    assert status.reported_date == date(2021, 12, 22)
    assert status.reported_time == time(18, 0)
    assert status.reported_datetime == datetime(2021, 12, 22, 18, 0)
    assert status.energy_consumption is None
    assert status.energy_generation == 3636
    assert status.normalized_ouput is None
    assert status.power_consumption is None
    assert status.power_generation == 0
    assert status.temperature == 21.2
    assert status.voltage == 220.1
