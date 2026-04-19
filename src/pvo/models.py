"""Asynchronous client for the PVOutput API."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, time

from mashumaro import DataClassDictMixin
from mashumaro.config import BaseConfig
from mashumaro.types import SerializationStrategy


class NaNisNone(SerializationStrategy):
    """The `NaN` string value should result in None."""

    def serialize(self, value: float | None) -> float | str:
        """Serialize NoneType into NaN."""
        if value is None:  # pragma: no cover
            return "NaN"
        return value

    def deserialize(self, value: float | str) -> float | None:
        """Deserialize NaN into NoneType."""
        if value == "NaN":
            return None
        return float(value)


class DateStrategy(SerializationStrategy):
    """String serialization strategy to handle the date format."""

    def serialize(self, value: date) -> str:
        """Serialize a date to its specific format."""
        return datetime.strftime(value, "%Y%m%d")

    def deserialize(self, value: str) -> date | None:
        """Deserialize a date string to a date object."""
        if not value:
            return None

        return datetime.strptime(value, "%Y%m%d").replace(tzinfo=UTC).date()


@dataclass
# pylint: disable-next=too-many-instance-attributes
class Status(DataClassDictMixin):
    """Object holding the latest status information and live output data."""

    # pylint: disable-next=too-few-public-methods
    class Config(BaseConfig):
        """Mashumaro configuration."""

        serialization_strategy = {  # noqa: RUF012
            date: DateStrategy(),
            float: NaNisNone(),
            int: NaNisNone(),
        }

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
            tzinfo=UTC,
        )


@dataclass
# pylint: disable-next=too-many-instance-attributes
class System(DataClassDictMixin):
    """Object holding the latest system information."""

    # pylint: disable-next=too-few-public-methods
    class Config(BaseConfig):
        """Mashumaro configuration."""

        serialization_strategy = {  # noqa: RUF012
            date: DateStrategy(),
            float: NaNisNone(),
            int: NaNisNone(),
        }

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
