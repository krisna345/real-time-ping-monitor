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

1. **Clone the Repository:**

   ```bash
