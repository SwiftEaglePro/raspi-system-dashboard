# raspi-system-dashboard
A Python‑based real‑time system monitor for Raspberry Pi using the Rich TUI library

# Raspberry Pi System Dashboard

A lightweight, real-time terminal dashboard for monitoring Raspberry Pi system performance.  
Built with Python and the `rich` library, it displays CPU, RAM, disk usage, and network activity with simple live graphs.

## Features

- Live updating CPU and RAM usage graphs  
- Disk usage bar  
- Network upload/download totals  
- Clean terminal UI using `rich`  
- Logs system metrics to `system_metrics.log`  
- Works on any Raspberry Pi running Python 3

## Requirements

- Python 3  
- `psutil`  
- `rich`

Install dependencies:

\`\`\`bash
pip install psutil rich
\`\`\`

## Run the dashboard

\`\`\`bash
python3 system_dashboard.py
\`\`\`

Press **Ctrl + C** to exit.

## Why I made this

A small experiment to learn Python, system monitoring, and terminal UI design.  
Simple, functional, and a fun way to watch your Pi’s performance in real time.
