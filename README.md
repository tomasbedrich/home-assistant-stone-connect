# Stone Connect Heater Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/tomasbedrich/home-assistant-stone-connect.svg)](https://github.com/tomasbedrich/home-assistant-stone-connect/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Home Assistant custom integration for controlling Stone Connect WiFi electric heaters via their local HTTPS API.

## Features

- **Local Control**: Direct communication with your heater without cloud dependency
- **Climate Entity**: Full Home Assistant climate control with temperature and mode settings
- **Device Registry**: Proper device information display in Home Assistant
- **Config Flow**: Easy setup through the Home Assistant UI
- **Real-time Updates**: Regular polling for current status
- **Power Monitoring**: Display power consumption and daily energy usage (if supported by device)

## Supported Operations

- 🌡️ **Temperature Control**: Set target temperature (0-30°C)
- 🔥 **HVAC Modes**: Off (Standby) and Heat (Manual) modes
- 📊 **Status Monitoring**: Power consumption, energy usage, WiFi signal strength
- 🔒 **Device Information**: Model, firmware version, serial number

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots menu and select "Custom repositories"
4. Add this repository URL: `https://github.com/tomasbedrich/home-assistant-stone-connect`
5. Select "Integration" as the category
6. Click "Add"
7. Find "Stone Connect Heater" in the integration list and install it
8. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/tomasbedrich/home-assistant-stone-connect/releases)
2. Extract the `stone_connect` folder to your `custom_components` directory
3. Restart Home Assistant

## Configuration

1. Go to Settings → Devices & Services
2. Click "Add Integration"
3. Search for "Stone Connect Heater"
4. Enter your heater's IP address
5. The integration will test the connection and create the device

## Usage

Once configured, you'll have a climate entity that allows you to:

- Turn the heater on/off
- Set target temperature (0-30°C)
- View current operation mode
- Monitor power consumption and energy usage
- Check WiFi signal strength and error status

### Supported HVAC Modes

- **Off**: Heater in standby mode
- **Heat**: Manual temperature control

### Additional Attributes

The climate entity provides additional state attributes:

- `stone_connect_mode`: Current Stone Connect operation mode
- `power_consumption`: Current power usage in watts
- `daily_energy`: Daily energy consumption
- `error_code`: Device error code (0 = no error)
- `lock_status`: Device lock status
- `wifi_signal`: WiFi signal strength (RSSI)

## Troubleshooting

### Connection Issues

- Ensure your heater is connected to the same network as Home Assistant
- Check that the IP address is correct and accessible
- Verify the heater's WiFi connection is stable

### Integration Not Working

- Check Home Assistant logs for error messages
- Ensure the stone-connect Python library is properly installed
- Try removing and re-adding the integration

## Dependencies

This integration requires the [stone-connect](https://github.com/tomasbedrich/stone-connect) Python library, which will be automatically installed.

## Support

For issues and feature requests, please use the [GitHub Issues](https://github.com/tomasbedrich/home-assistant-stone-connect/issues) page.

## Disclaimer

This integration is not officially associated with Stone Connect or any heater manufacturer. It is developed through reverse engineering of the public API for personal and educational use. Use at your own risk.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
