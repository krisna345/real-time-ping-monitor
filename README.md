
Ping Monitor with Real-Time Graph

This script pings a specified host (IP/domain) continuously and displays the
real-time average response time on a graph in your browser. The results are also
logged to an Excel file.

Features:
- Pings a host every 5 seconds.
- Extracts the average response time from the ping output.
- Logs the timestamp, host, status, and average response time to an Excel file.
- Updates a Plotly graph (saved as HTML) that auto-refreshes in the browser.

Requirements:
- Python 3.x
- pandas
- openpyxl
- plotly
- tkinter (usually included with Python)
- A modern browser to view the real-time graph

Usage:
1. Run the script: `python3 ping_monitor.py`
2. Enter the IP or domain when prompted.
3. A browser tab will open with the real-time graph, which refreshes every 5 seconds.

Press Ctrl+C to stop the tool.
"""
# real-time-ping-monitor

# Real-Time Ping Monitor with Graph

This project is a Python-based tool that continuously pings a user-specified host (IP or domain) and displays the average response time in real-time on a browser-based graph. It also logs each ping's results into an Excel file for further analysis.

## Features

- **Continuous Pinging:** The script pings the target host every 5 seconds.
- **Real-Time Graph:** Uses Plotly to generate a real-time graph that updates in your browser.
- **Excel Logging:** Each ping's results (timestamp, host, status, average response time) are logged in an Excel file (`network_logs.xlsx`).
- **Cross-Platform:** Works on Windows and Unix-based systems.

## Requirements

- Python 3.x
- [pandas](https://pandas.pydata.org/)
- [openpyxl](https://openpyxl.readthedocs.io/)
- [plotly](https://plotly.com/python/)
- tkinter (usually included with Python)
- A modern web browser (Chrome, Firefox, etc.)

## Installation

nstall Required Packages:

You can install the required Python packages using pip:

bash
pip install pandas openpyxl plotly
