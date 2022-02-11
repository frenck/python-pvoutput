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
    PVOutputNoDataError,
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
    assert status.normalized_output is None
    assert status.power_consumption is None
    assert status.power_generation == 0
    assert status.temperature == 21.2
    assert status.voltage == 220.1


@pytest.mark.asyncio
async def test_get_status_no_data(aresponses):
    """Test PVOutput status without data is handled."""
    aresponses.add(
        "pvoutput.org",
        "/service/r2/getstatus.jsp",
        "GET",
        aresponses.Response(text="Bad Request!", status=400),
    )

    async with aiohttp.ClientSession() as session:
        pvoutput = PVOutput(api_key="fake", system_id=12345, session=session)
        with pytest.raises(PVOutputNoDataError):
            await pvoutput.status()


@pytest.mark.asyncio
async def test_get_system(aresponses):
    """Test get system handling."""
    aresponses.add(
        "pvoutput.org",
        "/service/r2/getsystem.jsp",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "text/plain"},
            text=(
                "Frenck,5015,CO1,17,295,JA solar JAM-300,1,5000,"
                "SolarEdge SE5000H,S,20.0,Low,20180622,51.1234,6.1234,5;;0"
            ),
        ),
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


@pytest.mark.asyncio
async def test_get_system_empty_install_date(aresponses):
    """Test get system handling with an empty install date."""
    aresponses.add(
        "pvoutput.org",
        "/service/r2/getsystem.jsp",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "text/plain"},
            text=(
                "Frenck,5015,1234,17,295,JA solar JAM-300,1,5000,"
                "SolarEdge SE5000H,S,20.0,Low,,51.1234,6.1234,5;;0"
            ),
        ),
    )

    async with aiohttp.ClientSession() as session:
        pvoutput = PVOutput(api_key="fake", system_id=12345, session=session)
        system = await pvoutput.system()

    assert system.install_date is None
