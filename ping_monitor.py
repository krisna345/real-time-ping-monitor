#!/usr/bin/env python3
"""
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

import os
import platform
import subprocess
from datetime import datetime
import pandas as pd
from openpyxl import load_workbook
import tkinter as tk
from tkinter import simpledialog
import time
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import webbrowser  # to open the HTML file in the browser

def ping_host(host):
    """
    Ping a single host and return the output.
    
    Args:
        host (str): The IP or domain to ping.
        
    Returns:
        str or None: The output from the ping command if successful, otherwise None.
    """
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(["ping", param, "4", host],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return None
    except Exception as e:
        print(f"Error pinging {host}: {e}")
        return None

def parse_response_time(ping_output):
    """
    Extract and calculate average response time from ping output.
    
    Args:
        ping_output (str): The output from the ping command.
        
    Returns:
        int or float or None: The average response time in milliseconds,
                              or None if parsing fails.
    """
    if not ping_output:
        return None

    try:
        if platform.system().lower() == "windows":
            lines = ping_output.splitlines()
            for line in lines:
                if "Average =" in line:
                    # Extract the number before the "ms" text.
                    avg_time = line.split("Average = ")[-1].split("ms")[0].strip()
                    return int(avg_time)
        else:
            lines = ping_output.splitlines()
            for line in lines:
                if "rtt min/avg/max/mdev" in line:
                    avg_time = line.split("/")[1]
                    return float(avg_time)
    except Exception as e:
        print(f"Error parsing response time: {e}")
    return None

def log_to_excel(data, file_name="network_logs.xlsx"):
    """
    Log data to an Excel file (.xlsx). If the file doesn't exist, it creates a new file.
    
    Args:
        data (list): A list containing [Timestamp, Host, Status, Average Response Time].
        file_name (str): The name of the Excel file.
    """
    try:
        # Convert data to a DataFrame
        df = pd.DataFrame([data], columns=["Timestamp", "Host", "Status", "Average Response Time (ms)"])

        # Check if the file already exists
        try:
            # Append to the existing file
            with pd.ExcelWriter(file_name, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
                if "Logs" in writer.sheets:
                    # Find the next empty row in the sheet
                    startrow = writer.sheets["Logs"].max_row
                    df.to_excel(writer, sheet_name="Logs", index=False, header=False, startrow=startrow)
                else:
                    # Create the "Logs" sheet if it doesn't exist
                    df.to_excel(writer, sheet_name="Logs", index=False)
        except FileNotFoundError:
            # Create a new Excel file if it doesn't exist
            with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="Logs", index=False)

    except Exception as e:
        print(f"Error logging to Excel: {e}")

def update_plot(fig, x_data, y_data, host):
    """
    Update the Plotly figure with new data and write it to an HTML file.
    
    Args:
        fig (plotly.graph_objs.Figure): The Plotly figure object.
        x_data (list): Timestamps.
        y_data (list): Response times.
        host (str): The host being pinged.
    """
    # Update the trace data for the plot
    fig.data[0].x = x_data
    fig.data[0].y = y_data
    # Update the layout with a dynamic title and axis labels
    fig.update_layout(title=f"Real-Time Ping Monitoring for {host}",
                      xaxis_title="Timestamp", yaxis_title="Response Time (ms)")
    # Convert the figure to HTML string with Plotly JS included
    html_str = fig.to_html(include_plotlyjs='cdn', full_html=True)
    # Insert a meta refresh tag in the HTML so the page refreshes every 5 seconds.
    html_str = html_str.replace('<head>', '<head><meta http-equiv="refresh" content="5">')
    # Write the updated HTML to a file (temp_plot.html)
    with open("temp_plot.html", "w") as f:
        f.write(html_str)

def main():
    """
    Main function to run the Ping Monitor.
    """
    # Create a hidden Tkinter window to prompt for user input
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    host = simpledialog.askstring("Ping Tool", "Enter the IP or domain to ping (e.g., google.com, yahoo.com):")

    if not host:
        print("No host provided. Exiting...")
        return

    print("Starting Ping Tool with Real-Time Graph... Press Ctrl+C to stop.\n")

    log_file = "ping_results.xlsx"
    x_data = []  # List to store timestamps for the graph
    y_data = []  # List to store response times for the graph

    # Initialize a Plotly figure with one subplot
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x=[], y=[], mode="lines+markers", name="Response Time (ms)"))

    # Write the initial (empty) plot to an HTML file and open it in the browser.
    update_plot(fig, x_data, y_data, host)
    webbrowser.open("temp_plot.html")  # This opens one browser tab.

    try:
        # Continuously ping the host and update the graph/log file every 5 seconds.
        while True:
            print(f"Pinging {host}...")
            ping_output = ping_host(host)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if ping_output:
                avg_time = parse_response_time(ping_output)
                print(f"Ping successful. Average Response Time: {avg_time} ms\n")
                log_to_excel([timestamp, host, "Success", avg_time], log_file)
                x_data.append(timestamp)
                y_data.append(avg_time)
            else:
                print(f"Ping failed for {host}\n")
                log_to_excel([timestamp, host, "Failed", "N/A"], log_file)
                x_data.append(timestamp)
                y_data.append(None)

            # Update the graph by re-writing the HTML file.
            update_plot(fig, x_data, y_data, host)
            time.sleep(5)  # Wait 5 seconds before the next ping
    except KeyboardInterrupt:
        print("\nPing Tool stopped by user.")

if __name__ == "__main__":
    main()
