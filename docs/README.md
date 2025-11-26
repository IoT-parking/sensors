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

### 6. Running

Choose one of the following methods:

**In the docker container:**
```bash

```

**Local launch**
```bash
uv run src/main.py
```





