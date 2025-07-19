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
- **Proper HA Integration**: Uses Home Assistant sensor entities with appropriate icons and state classes
- **Error Handling**: Graceful handling of API failures without breaking Home Assistant
- **Configurable Updates**: Customizable scan intervals (default 15 minutes)
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
   │       ├── sensor.py
   │       ├── laghi.py
   │       ├── const.py
   │       └── manifest.json
   ```

2. Restart Home Assistant completely

3. Add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry
sensor:
  - platform: laghi
    scan_interval: 900  # Optional: update every 15 minutes (default)
    lakes:  # Optional: specify which lakes to monitor (default: all lakes)
     - "Lago Maggiore"
     - "Lago di Como" 
     - "Lago d'Iseo"
     - "Lago d'Idro"
     - "Lago di Garda"
```

4. Restart Home Assistant again to load the configuration

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `scan_interval` | integer | 900 | Update interval in seconds (minimum 300 seconds / 5 minutes) |
| `lakes` | list | All lakes | List of lakes to monitor (see available lakes below) |

### Available Lakes

- `Lago Maggiore`
- `Lago di Como`
- `Lago d'Iseo`
- `Lago d'Idro`
- `Lago di Garda`

### Example Advanced Configuration

```yaml
sensor:
  - platform: laghi
    scan_interval: 900  # Update every 15 minutes
    lakes:  # Monitor only specific lakes
      - "Lago Maggiore"
      - "Lago di Como"
```

### Configuration Examples

**Monitor all lakes (default):**
```yaml
sensor:
  - platform: laghi
```

**Monitor only Lago Maggiore:**
```yaml
sensor:
  - platform: laghi
    lakes:
      - "Lago Maggiore"
```

**Monitor northern lakes only:**
```yaml
sensor:
  - platform: laghi
    lakes:
      - "Lago Maggiore"
      - "Lago di Como"
      - "Lago d'Iseo"
```

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
