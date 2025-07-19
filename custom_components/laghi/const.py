"""Constants for the Laghi.net integration."""

DOMAIN = "laghi"

# Configuration keys
CONF_LAKES = "lakes"

# Update interval in minutes
DEFAULT_SCAN_INTERVAL = 30

# Available lakes
AVAILABLE_LAKES = [
    "Lago Maggiore",
    "Lago di Como", 
    "Lago d'Iseo",
    "Lago d'Idro",
    "Lago di Garda"
]

# Lake data mappings
LAKE_SENSORS = {
    "level": {
        "name": "Level",
        "icon": "mdi:water",
        "device_class": None,
        "state_class": "measurement",
    },
    "inflow": {
        "name": "Inflow",
        "icon": "mdi:water-plus",
        "device_class": None,
        "state_class": "measurement",
    },
    "outflow": {
        "name": "Outflow", 
        "icon": "mdi:water-minus",
        "device_class": None,
        "state_class": "measurement",
    },
    "fill": {
        "name": "Fill Percentage",
        "icon": "mdi:water-percent",
        "device_class": None,
        "state_class": "measurement",
    },
}
