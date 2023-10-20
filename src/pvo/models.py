"""Asynchronous client for the PVOutput API."""
from __future__ import annotations

from datetime import date, datetime, time, timezone

try:
    from pydantic.v1 import BaseModel, validator
except ImportError:  # pragma: no cover
    from pydantic import (  # type: ignore[assignment] # pragma: no cover
        BaseModel,
        validator,
    )


class Status(BaseModel):
    """Object holding the latest status information and live output data."""

    reported_date: date
    reported_time: time

    energy_consumption: int | None
    energy_generation: int | None
    normalized_output: float | None
    power_consumption: int | None
    power_generation: int | None
    temperature: float | None
    voltage: float | None

    @property
    def reported_datetime(self) -> datetime:
        """Return the timestamp of the status data.

        Returns
        -------
            A datetime object.
        """
        return datetime.combine(
            self.reported_date,
            self.reported_time,
            tzinfo=timezone.utc,
        )

    @validator(
        "energy_consumption",
        "energy_generation",
        "normalized_output",
        "power_consumption",
        "power_generation",
        "temperature",
        "voltage",
        pre=True,
    )
    @classmethod
    def filter_not_a_number(
        cls,
        value: str | float,
    ) -> str | int | float | None:
        """Filter out NaN values.

        Args:
        ----
            value: Value to filter.

        Returns:
        -------
            Filtered value.
        """
        return None if value == "NaN" else value

    @validator("reported_date", pre=True)
    @classmethod
    def preparse_date(cls, value: str) -> str:
        """Preparse date so Pydantic understands it.

        Args:
        ----
            value: Date value to preparse.

        Returns:
        -------
            Preparsed date value.
        """
        return f"{value[:4]}-{value[4:6]}-{value[6:]}"


class System(BaseModel):
    """Object holding the latest system information."""

    array_tilt: float | None
    install_date: date | None
    inverter_brand: str | None
    inverter_power: int | None
    inverters: int | None
    latitude: float | None
    longitude: float | None
    orientation: str | None
    panel_brand: str | None
    panel_power: int | None
    panels: int | None
    shade: str | None
    status_interval: int | None
    system_name: str
    system_size: int | None
    zipcode: str | None

    @validator("install_date", pre=True)
    @classmethod
    def preparse_date(cls, value: str) -> str | None:
        """Preparse date so Pydantic understands it.

        Args:
        ----
            value: Date value to preparse.

        Returns:
        -------
            Preparsed date value.
        """
        if not value:
            return None

        return f"{value[:4]}-{value[4:6]}-{value[6:]}"
