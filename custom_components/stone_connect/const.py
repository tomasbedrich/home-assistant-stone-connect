"""Constants for Stone Connect integration."""

DOMAIN = "stone_connect"

# Default values
DEFAULT_NAME = "Stone Connect Heater"
DEFAULT_SCAN_INTERVAL = 30  # seconds
DEFAULT_TIMEOUT = 10  # seconds

# Device information
MANUFACTURER = "Stone Connect"
MODEL = "WiFi Electric Heater"

# Supported operation modes for Home Assistant
HVAC_MODE_MAP = {
    "SBY": "off",  # STANDBY -> OFF
    "MAN": "heat",  # MANUAL -> HEAT
    "CMF": "heat",  # COMFORT -> HEAT
    "ECO": "heat",  # ECO -> HEAT
    "ANF": "heat",  # ANTIFREEZE -> HEAT
    "BST": "heat",  # BOOST -> HEAT
    "HIG": "heat",  # HIGH -> HEAT
    "MED": "heat",  # MEDIUM -> HEAT
    "LOW": "heat",  # LOW -> HEAT
    "SCH": "auto",  # SCHEDULE -> AUTO
    "HOL": "auto",  # HOLIDAY -> AUTO
}

# Reverse mapping for setting modes
HA_TO_STONE_MODE_MAP = {
    "off": "SBY",  # OFF -> STANDBY
    "heat": "MAN",  # HEAT -> MANUAL (we'll use manual for direct temp control)
    "auto": "SCH",  # AUTO -> SCHEDULE
}

# Temperature limits
MIN_TEMP = 0
MAX_TEMP = 30
TEMP_STEP = 1.0
