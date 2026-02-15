#!/usr/bin/env python3
import psutil
import time
from rich.live import Live
from rich.panel import Panel
from rich.console import Console, Group
from rich.text import Text
import shutil

console = Console()
cpu_history = []
ram_history = []
GRAPH_CHARS = "▁▂▃▄▅▆▇█"

# ----------------------
# Utilities
# ----------------------
def get_graph_width():
    return max(10, shutil.get_terminal_size().columns - 20)

def generate_graph(history, color_map, label=""):
    width = get_graph_width()
    graph_width = width - len(label) - 1
    slice_hist = history[-graph_width:]
    slice_hist = [0]*(graph_width - len(slice_hist)) + slice_hist
    graph = Text(label)
    for val in slice_hist:
        idx = int(val / 100 * (len(GRAPH_CHARS)-1))
        graph.append(GRAPH_CHARS[idx], style=color_map(val))
    return graph

def cpu_color(val):
    if val < 50: return "green"
    if val < 80: return "yellow"
    return "red"

def ram_color(val):
    if val < 50: return "blue"
    if val < 80: return "cyan"
    return "bright_blue"

# ----------------------
# Dashboard Builder
# ----------------------
def build_dashboard():
    cpu = int(psutil.cpu_percent(interval=None))
    ram = int(psutil.virtual_memory().percent)
    disk = int(psutil.disk_usage("/").percent)
    net = psutil.net_io_counters()
    now = time.strftime("%Y-%m-%d %H:%M:%S")

    # Update histories
    width = get_graph_width()
    for hist, val in [(cpu_history, cpu), (ram_history, ram)]:
        if len(hist) >= width:
            hist.pop(0)
        hist.append(val)

    # Header panel
    header = Panel(f"Raspberry Pi System Analytics\n{now}", style="bold cyan")

    # Metrics panel
    metrics_text = (
        f"CPU Usage: {cpu}%\n"
        f"RAM Usage: {ram}%\n"
        f"Disk Usage: {disk}%\n"
        f"Network Sent: {net.bytes_sent/1_000_000:.2f} MB\n"
        f"Network Received: {net.bytes_recv/1_000_000:.2f} MB"
    )
    metrics_panel = Panel(metrics_text, title="System Metrics", border_style="blue", height=8)

    # Graph panel
    cpu_graph = generate_graph(cpu_history, cpu_color, label="CPU: ")
    ram_graph = generate_graph(ram_history, ram_color, label="RAM: ")
    disk_bar = f"Disk: [{'█'*int(disk/5):<20}] {disk}%"
    graph_panel = Panel(Group(cpu_graph, ram_graph, disk_bar),
                        title="Live Utilization", border_style="green", height=8)

    # Log metrics
    with open("system_metrics.log", "a") as f:
        f.write(f"{now} | CPU:{cpu}% RAM:{ram}% Disk:{disk}%\n")

    # Compose dashboard
    return Group(header, metrics_panel, graph_panel)

# ----------------------
# Main loop
# ----------------------
def main():
    with Live(build_dashboard(), refresh_per_second=2, screen=True) as live:
        while True:
            try:
                time.sleep(0.5)
                live.update(build_dashboard())
            except KeyboardInterrupt:
                console.print("\nExiting dashboard...")
                break

if __name__ == "__main__":
    main()
