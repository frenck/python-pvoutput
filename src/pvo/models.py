"""Asynchronous client for the PVOutput API."""
from __future__ import annotations

from datetime import date, datetime, time
from typing import Optional, Union

from pydantic import BaseModel, validator


class Status(BaseModel):
    """Object holding the latest status information and live output data."""

    reported_date: date
    reported_time: time

    energy_consumption: Optional[int]
    energy_generation: Optional[int]
    normalized_ouput: Optional[float]
    power_consumption: Optional[int]
    power_generation: Optional[int]
    temperature: Optional[float]
    voltage: Optional[float]

    @property
    def reported_datetime(self) -> datetime:
        """Return the timestamp of the status data.

        Returns:
            A datetime object.
        """
        return datetime.combine(self.reported_date, self.reported_time)

    @validator(
        "energy_consumption",
        "energy_generation",
        "normalized_ouput",
        "power_consumption",
        "power_generation",
        "temperature",
        "voltage",
        pre=True,
    )
    @classmethod
    def filter_not_a_number(
        cls, value: Union[str, int, float]  # noqa: F841
    ) -> Optional[Union[str, int, float]]:
        """Filter out NaN values.

        Args:
            value: Value to filter.

        Returns:
            Filtered value.
        """
        if value == "NaN":
            return None
        return value

    @validator("reported_date", pre=True)
    @classmethod
    def preparse_date(cls, value: str) -> str:  # noqa: F841
        """Preparse date so Pydantic understands it.

        Args:
            value: Date value to preparse.

        Returns:
            Preparsed date value.
        """
        return f"{value[:4]}-{value[4:6]}-{value[6:]}"
