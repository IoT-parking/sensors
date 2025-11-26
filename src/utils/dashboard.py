import time

from rich import box
from rich.console import Console
from rich.live import Live
from rich.table import Table

from sensor import Sensor


def generate_table(sensors: list[Sensor]) -> Table:
    """Creates a fresh table with current sensor data."""
    table = Table(title="IoT Sensor Network Status", box=box.ROUNDED)

    table.add_column("Sensor Name", style="cyan", no_wrap=True)
    table.add_column("Type", style="magenta")
    table.add_column("Status", justify="center")
    table.add_column("Interval", justify="right")
    table.add_column("Msgs Sent", justify="right", style="green")

    for sensor in sensors:
        status = sensor.status_label
        status_style = "green"
        if status == "PAUSED":
            status_style = "yellow"
        elif status == "STOPPED":
            status_style = "red"

        table.add_row(
            sensor.name,
            sensor.device_type,
            f"[{status_style}]{status}[/{status_style}]",
            f"{sensor._interval}s",
            str(sensor.messages_sent),
        )

    return table


def run_dashboard(sensors: list[Sensor]) -> None:
    console = Console()
    console.clear()

    console.print("[bold]Press Ctrl+C to stop the simulation.[/bold]")
    time.sleep(1)

    with Live(generate_table(sensors), refresh_per_second=4) as live:
        try:
            while True:
                live.update(generate_table(sensors))
                time.sleep(0.25)
        except KeyboardInterrupt:
            pass
