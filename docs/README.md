# iot-parking : sensors

## Environment setup

### 1. Install `uv` (if not installed)

Choose one of the following methods:

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Alternative (via pip):**
```bash
pip install uv
```

### 2. Clone the Repository

```bash
git clone https://github.com/IoT-parking/sensors.git
cd sensors
```

### 3. Setup Virtual Environment and Dependencies

```bash
uv sync
```

This command:
- Creates a virtual environment in `.venv/`
- Installs all dependencies from `pyproject.toml`
- Sets up the development environment

### 4. Environment variables setup

Create a `.env` file in the project root:
```bash
cp .env.example .env
```

> [!IMPORTANT]  
> The values in ```.env.example``` are already set to the default, compatible with the main [iot-parking](https://github.com/IoT-parking/iot-parking) service. These values will be set through ```docker-compose``` in the root project.


### 5. Adding dependecies

To add a new package, use:
```bash
uv add <package-name>
```

For development dependencies:
```bash
uv add --dev <package-name>
```

## Internal CLI

App provides internal CLI as stated in requirements:

```
--- IoT-parking Sensor Simulation ---
MQTT Broker Hostname: mosquitto:1883
Number of sensor instances per type: 4
-------------------------------------
Available Commands:
  start       - Start the sensor simulation (Blocking)
  healthcheck - Check connectivity to MQTT Broker
  help        - Show this menu
  exit        - Quit the application
  
iot-parking> 
```

## Running

### 1. Mock mode

If you wish to test out the measurment generation logic locally - use the `mock mode` through:

```bash
uv run src/main.py --mock
```

This method does not require MQTT connection.

### 2. As a part of [`iot-parking`](https://github.com/IoT-parking/iot-parking)

Run docker-compose and attach to the container:

```bash
// iot-parking
docker compose up --build -d 
docker attach sensors
```

and then using the internal CLI, run the sensor simulation:

```
iot-parking> start
```






