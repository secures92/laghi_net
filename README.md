# Laghi.net Home Assistant Integration

This is a custom Home Assistant integration for monitoring Italian lake data from laghi.net. It provides real-time monitoring of water levels, inflow, outflow, and fill percentages for major Italian lakes including Maggiore, Como, Iseo, Idro, and Garda.

## Features

- **Real-time Lake Monitoring**: Fetches live data from laghi.net REST API
- **Complete Lake Coverage**: Supports all 5 major Italian lakes (Maggiore, Como, Iseo, Idro, Garda)
- **Multiple Sensor Types**: Creates 4 sensors per lake:
  - Water Level (cm or m slm)
  - Inflow Rate (m³/s)
  - Outflow Rate (m³/s)  
  - Fill Percentage (%)
- **Proper HA Integration**: Config-entry based integration following Home Assistant best practices
- **Error Handling**: Graceful handling of API failures — temporary outages trigger auto-retry, permanent errors are surfaced clearly in the UI
- **Configurable Updates**: Customizable scan intervals (default 30 minutes)
- **Timestamp Tracking**: Includes last update timestamp for each measurement

## Installation


### Manual Installation

1. Copy the entire `custom_components/laghi/` folder to your Home Assistant `custom_components/` directory

   Your folder structure should look like:
   ```
   <config_dir>/
   ├── custom_components/
   │   └── laghi/
   │       ├── __init__.py
   │       ├── coordinator.py
   │       ├── sensor.py
   │       ├── laghi.py
   │       ├── const.py
   │       └── manifest.json
   ```

2. Restart Home Assistant completely

3. Go to **Settings → Devices & Services → Add Integration** and search for **Laghi.net**

4. The integration will fetch data automatically — no `configuration.yaml` changes required

## Configuration

This integration is configured via the Home Assistant UI (config entries). No `configuration.yaml` setup is needed.

### Available Lakes

- `Lago Maggiore`
- `Lago di Como`
- `Lago d'Iseo`
- `Lago d'Idro`
- `Lago di Garda`

By default all 5 lakes are monitored. You can limit which lakes are tracked via the integration options in **Settings → Devices & Services → Laghi.net → Configure**.

## Sensor Entities

After installation, you'll have sensor entities based on your configuration:
- **All lakes (default)**: 20 sensor entities (4 per lake)
- **Selected lakes**: 4 sensor entities per configured lake

### Lago Maggiore
- `sensor.lago_maggiore_level` - Water level in cm
- `sensor.lago_maggiore_inflow` - Inflow rate in m³/s  
- `sensor.lago_maggiore_outflow` - Outflow rate in m³/s
- `sensor.lago_maggiore_fill_percentage` - Fill percentage in %

### Lago di Como
- `sensor.lago_di_como_level` - Water level in cm
- `sensor.lago_di_como_inflow` - Inflow rate in m³/s
- `sensor.lago_di_como_outflow` - Outflow rate in m³/s  
- `sensor.lago_di_como_fill_percentage` - Fill percentage in %

### Lago d'Iseo
- `sensor.lago_d_iseo_level` - Water level in cm
- `sensor.lago_d_iseo_inflow` - Inflow rate in m³/s
- `sensor.lago_d_iseo_outflow` - Outflow rate in m³/s
- `sensor.lago_d_iseo_fill_percentage` - Fill percentage in %

### Lago d'Idro  
- `sensor.lago_d_idro_level` - Water level in m slm
- `sensor.lago_d_idro_inflow` - Inflow rate in m³/s
- `sensor.lago_d_idro_outflow` - Outflow rate in m³/s
- `sensor.lago_d_idro_fill_percentage` - Fill percentage in %

### Lago di Garda
- `sensor.lago_di_garda_level` - Water level in cm  
- `sensor.lago_di_garda_inflow` - Inflow rate in m³/s
- `sensor.lago_di_garda_outflow` - Outflow rate in m³/s
- `sensor.lago_di_garda_fill_percentage` - Fill percentage in %


## Contributing

This integration follows Home Assistant custom component best practices. Feel free to submit issues or improvements.

## License

This integration is provided as-is for monitoring Italian lake data. Data is sourced from laghi.net under their terms of service.
