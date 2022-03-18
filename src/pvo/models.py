"""Asynchronous client for the PVOutput API."""
from __future__ import annotations

from datetime import date, datetime, time
from typing import Optional, Union

from pydantic import BaseModel, validator

class Statistic(BaseModel):
    """Object holding the statistic information."""


    energy_generated: Optional[int]
    energy_exported: Optional[int]
    average_generation: Optional[int]
    minimum_generation: Optional[int]
    maximum_generation: Optional[int]
    average_efficiency: Optional[float]
    outputs: Optional[int]
    actual_date_from: date
    actual_date_to: date
    record_efficiency: Optional[float]
    record_date: date

    @property
    def reported_datetime(self) -> datetime:
        """Return the timestamp of the status data.

        Returns:
            A datetime object.
        """
        return datetime.combine(self.reported_date, self.reported_time)

    @validator(
        "energy_generated",
        "energy_exported",
        "average_generation",
        "minimum_generation",
        "maximum_generation",
        "average_efficiency",
        "outputs",
        "record_efficiency",
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
        return None if value == "NaN" else value

    @validator(
        "actual_date_from",
        "actual_date_to",
        "record_date",
        pre=True
    )
    @classmethod
    def preparse_date(cls, value: str) -> str:  # noqa: F841
        """Preparse date so Pydantic understands it.

        Args:
            value: Date value to preparse.

        Returns:
            Preparsed date value.
        """
        return f"{value[:4]}-{value[4:6]}-{value[6:]}"



class Status(BaseModel):
    """Object holding the latest status information and live output data."""

    reported_date: date
    reported_time: time

    energy_consumption: Optional[int]
    energy_generation: Optional[int]
    normalized_output: Optional[float]
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
        "normalized_output",
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
        return None if value == "NaN" else value

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


class System(BaseModel):
    """Object holding the latest system information."""

    array_tilt: Optional[float]
    install_date: Optional[date]
    inverter_brand: Optional[str]
    inverter_power: Optional[int]
    inverters: Optional[int]
    latitude: Optional[float]
    longitude: Optional[float]
    orientation: Optional[str]
    panel_brand: Optional[str]
    panel_power: Optional[int]
    panels: Optional[int]
    shade: Optional[str]
    status_interval: Optional[int]
    system_name: str
    system_size: Optional[int]
    zipcode: Optional[str]

    @validator("install_date", pre=True)
    @classmethod
    def preparse_date(cls, value: str) -> str | None:  # noqa: F841
        """Preparse date so Pydantic understands it.

        Args:
            value: Date value to preparse.

        Returns:
            Preparsed date value.
        """
        if not value:
            return None

        return f"{value[:4]}-{value[4:6]}-{value[6:]}"
