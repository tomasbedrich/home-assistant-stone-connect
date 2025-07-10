"""Climate platform for Stone Connect integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    HA_TO_STONE_MODE_MAP,
    HVAC_MODE_MAP,
    MANUFACTURER,
    MAX_TEMP,
    MIN_TEMP,
    MODEL,
    TEMP_STEP,
)
from .coordinator import StoneConnectDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Stone Connect climate entities."""
    coordinator: StoneConnectDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([StoneConnectClimate(coordinator, entry)])


class StoneConnectClimate(CoordinatorEntity, ClimateEntity):
    """Representation of a Stone Connect heater."""

    coordinator: StoneConnectDataUpdateCoordinator

    def __init__(
        self,
        coordinator: StoneConnectDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the climate entity."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_name = f"Stone Connect {coordinator.host}"
        self._attr_unique_id = f"{coordinator.host}_climate"

        # Climate entity features
        self._attr_supported_features = (
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        )

        # Temperature settings
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_min_temp = MIN_TEMP
        self._attr_max_temp = MAX_TEMP
        self._attr_target_temperature_step = TEMP_STEP

        # Supported HVAC modes
        self._attr_hvac_modes = [HVACMode.OFF, HVACMode.HEAT, HVACMode.AUTO]

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        info = self.coordinator.data.get("info") if self.coordinator.data else None

        device_info: DeviceInfo = {
            "identifiers": {(DOMAIN, self.coordinator.host)},
            "name": f"Stone Connect Heater ({self.coordinator.host})",
            "manufacturer": MANUFACTURER,
            "model": MODEL,
            "sw_version": None,
            "hw_version": None,
        }

        if info:
            if info.appliance_name:
                device_info["name"] = info.appliance_name
            if info.fw_version:
                device_info["sw_version"] = info.fw_version
            if info.pcb_version:
                device_info["hw_version"] = info.pcb_version
            if info.appliance_sn:
                device_info["serial_number"] = info.appliance_sn

        return device_info

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        # Stone Connect heaters don't have temperature sensors
        # They only have setpoints
        return None

    @property
    def target_temperature(self) -> float | None:
        """Return the temperature we try to reach."""
        if not self.coordinator.data:
            return None

        status = self.coordinator.data.get("status")
        if not status:
            return None

        return status.set_point

    @property
    def hvac_mode(self) -> HVACMode | None:
        """Return current operation mode."""
        if not self.coordinator.data:
            return None

        status = self.coordinator.data.get("status")
        if not status or not status.operative_mode:
            return None

        stone_mode = status.operative_mode.value
        ha_mode = HVAC_MODE_MAP.get(stone_mode)

        if ha_mode == "off":
            return HVACMode.OFF
        elif ha_mode == "heat":
            return HVACMode.HEAT
        elif ha_mode == "auto":
            return HVACMode.AUTO

        return HVACMode.HEAT  # Default fallback

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes."""
        if not self.coordinator.data:
            return None

        status = self.coordinator.data.get("status")
        if not status:
            return None

        attrs = {}

        if status.operative_mode:
            attrs["stone_connect_mode"] = status.operative_mode.value.lower()

        if status.power_consumption_watt is not None:
            attrs["power_consumption"] = status.power_consumption_watt

        if status.daily_energy is not None:
            attrs["daily_energy"] = status.daily_energy

        if status.error_code is not None:
            attrs["error_code"] = status.error_code

        if status.lock_status is not None:
            attrs["lock_status"] = status.lock_status

        if status.rssi is not None:
            attrs["wifi_signal"] = status.rssi

        return attrs

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return

        # Use manual mode when setting temperature directly
        await self.coordinator.async_set_temperature_and_mode(
            temperature, HA_TO_STONE_MODE_MAP["heat"]
        )

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""
        if hvac_mode not in self.hvac_modes:
            _LOGGER.error("Unsupported HVAC mode: %s", hvac_mode)
            return

        stone_mode = HA_TO_STONE_MODE_MAP.get(hvac_mode.value)
        if stone_mode is None:
            _LOGGER.error("Cannot map HVAC mode %s to Stone Connect mode", hvac_mode)
            return

        await self.coordinator.async_set_hvac_mode(stone_mode)

    async def async_turn_on(self) -> None:
        """Turn the entity on."""
        await self.async_set_hvac_mode(HVACMode.HEAT)

    async def async_turn_off(self) -> None:
        """Turn the entity off."""
        await self.async_set_hvac_mode(HVACMode.OFF)
