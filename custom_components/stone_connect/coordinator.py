"""Data update coordinator for Stone Connect integration."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from stone_connect.client import StoneConnectHeater
from stone_connect.models import OperationMode

from .const import DEFAULT_SCAN_INTERVAL, DEFAULT_TIMEOUT, DOMAIN

_LOGGER = logging.getLogger(__name__)


class StoneConnectDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Stone Connect API."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""
        self.entry = entry
        self.host: str = entry.data[CONF_HOST]
        self.heater: StoneConnectHeater | None = None

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        try:
            if self.heater is None:
                await self._setup_heater()
            assert self.heater is not None  # help mypy

            # Get current status and device info
            status = await self.heater.get_status()
            info = await self.heater.get_info()

            return {
                "status": status,
                "info": info,
            }

        except Exception as err:
            _LOGGER.error("Error communicating with Stone Connect heater: %s", err)
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    async def _setup_heater(self) -> None:
        """Set up the heater client."""
        try:
            session = async_get_clientsession(self.hass)
            self.heater = StoneConnectHeater(
                host=self.host,
                timeout=DEFAULT_TIMEOUT,
                session=session,
            )

            # Test the connection
            await self.heater.get_info()
            _LOGGER.info(
                "Successfully connected to Stone Connect heater at %s", self.host
            )

        except Exception as err:
            _LOGGER.error("Failed to setup Stone Connect heater: %s", err)
            raise err

    async def async_shutdown(self) -> None:
        """Close the heater connection."""
        if self.heater:
            await self.heater.close()
            self.heater = None

    async def async_set_temperature_and_mode(
        self, temperature: float, mode: str
    ) -> None:
        """Set temperature and mode on the heater."""
        if self.heater is None:
            raise UpdateFailed("Heater not connected")

        try:
            # Convert string mode to OperationMode enum
            operation_mode = OperationMode(mode)
            await self.heater.set_temperature_and_mode(temperature, operation_mode)

            # Request immediate refresh
            await self.async_request_refresh()

        except Exception as err:
            _LOGGER.error("Failed to set temperature and mode: %s", err)
            raise UpdateFailed(f"Failed to set temperature and mode: {err}") from err

    async def async_set_hvac_mode(self, mode: str) -> None:
        """Set HVAC mode on the heater."""
        if self.heater is None:
            raise UpdateFailed("Heater not connected")

        try:
            # Convert string mode to OperationMode enum
            operation_mode = OperationMode(mode)
            await self.heater.set_operation_mode(operation_mode)

            # Request immediate refresh
            await self.async_request_refresh()

        except Exception as err:
            _LOGGER.error("Failed to set HVAC mode: %s", err)
            raise UpdateFailed(f"Failed to set HVAC mode: {err}") from err
