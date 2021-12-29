"""
Name: warp-cli-gui
Description: Python program that will interact with Linux CLI to check status, and change basic settings, for Cloudflare WARP CLI
Prequisites: Linux OS, Python 3 with pillow library, warp-svc running as daemon, warp-cli for Linux installed
License: GPL-3.0
    Copyright (C) 2022  Danie van der Merwe e-mail:gadgeteerza10@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Versions:
# Version 0.1 initial commit 29 Dec 2021


# TODO: - Fix clearing of frames
# TODO: - Connect/Disconnect button action
# TODO: - Fix spacings and layout
# TODO: - "Always on" function's radio buttons / button
# TODO: - Consider auto-refresh
# TODO: - maybe graphs where relevant eg. latency
# TODO: - Can it show connect status on panel when minimized?

# Import all tkinter GUI library stuff
from tkinter import *
# Import image handling library for JPGs, etc. Make sure pillow library is installed on CLI with 'pip install pillow'
from PIL import ImageTk, Image
# Display popup message boxes
from tkinter import messagebox
# To interact with OS
import sys
# To execute external CLI commands to read status and change settings
import subprocess

# Set global variable to test during execution if connected
connected = True

# set root window called root
root = Tk()
# Set window title
root.title('Cloudflare WARP GUI')
# Set window logo
root.iconphoto(True, PhotoImage(file="hardheadlogo32.png"))
# Set size of main window
root.geometry("400x450")


# Checks first to see if the app is running on Linux otherwise pops error and exits
if sys.platform != "linux":
    messagebox.showerror("Error", "This only runs on Linux!")
    sys.exit()

# Checks if Python 3 or greater running otherwise exits
if sys.version_info.major < 3:
    messagebox.showerror("Error", "This requires Python 3 or above!")
    sys.exit()

# Check if warp-svc daemon running (status = 0), otherwise display instructions to start it, and exits
daemon = subprocess.call(['systemctl', 'is-active', '--quiet', 'warp-svc'])
if daemon != 0:
    messagebox.showerror("Error", "Start daemon with 'systemctl start warp-svc'")
    sys.exit()


# Define frame for Connection Status
frame_status = LabelFrame(root, text="Status", padx=10, pady=10)
frame_status.grid(row=0, column=0, padx=10, pady=10)

# Define frame for Settings
frame_settings = LabelFrame(root, text="Settings", padx=10, pady=10)
frame_settings.grid(row=0, column=1, padx=10, pady=10)

# Define frame for Stats
frame_stats = LabelFrame(root, text="Stats", padx=10, pady=10)
frame_stats.grid(row=1, column=1, padx=10, pady=10)

# Define frame for family mode toggle
frame_family = LabelFrame(root, text="Family Mode", padx=10, pady=10)
frame_family.grid(row=1, column=0, padx=10, pady=10)


# Function to handle Family Mode Radio button click
def family_clicked(value):
    # Execute the set-families-mode change using value brought over from radio button press
    # Todo = test result for valid execution
    result = (subprocess.run(['warp-cli', 'set-families-mode', value], capture_output=True, text=True)).stdout
    # Refresh settings frame as value may have changed
    refresh_settings()

def update_conn_status():
    # Check if warp-cli connection is connected by running status command, and format returned text
    # TODO: Need to try improve reliability for extraction part
    # Use globally defined connected variable
    global connected
    warp_connected = ((subprocess.run(['warp-cli', 'status'], capture_output=True)).stdout).splitlines()
    # Extract part where 'Connected' should appear
        # warp_connected_msg = warp_connected[23 : 32]
    warp_connected_msg = str(warp_connected[1])
    if warp_connected_msg == "b'Status update: Connected'":
        myConnect_Btn = Button(frame_status, text=" Connected ", bg="green")
        connected = True
    else:
        myConnect_Btn = Button(frame_status, text="Disconnected", bg="red")
        connected = False
    # Display button with colour as status
    myConnect_Btn.grid(row=0, column=0)
    # Debug Condition to check extracted text
    #print("|" + warp_connected_msg + "|")


def refresh_settings():
    # Clear any previous widgets displays before displaying new data
    for widgets in frame_settings.winfo_children():
        widgets.destroy()
    # Check and read output of 'warp-cli settings' into a Python list, every line split into new list item
    warp_settings = ((subprocess.run(['warp-cli', 'settings'], capture_output=True)).stdout).splitlines()
    warp_settings_aon = warp_settings[0]
    warp_settings_switch = warp_settings[1]
    warp_settings_mode = warp_settings[2]
    warp_settings_family = warp_settings[3]
    warp_settings_wifi = warp_settings[4]
    warp_settings_eth = warp_settings[5]
    warp_settings_dns = warp_settings[6]

    # Define labels and display in frame for above settings
    warp_settings_aon_lbl = Label(frame_settings, text=warp_settings_aon)
    warp_settings_aon_lbl.grid(row=0, column=0, sticky=W)

    warp_settings_switch_lbl = Label(frame_settings, text=warp_settings_switch)
    warp_settings_switch_lbl.grid(row=1, column=0, sticky=W)

    warp_settings_mode_lbl = Label(frame_settings, text=warp_settings_mode)
    warp_settings_mode_lbl.grid(row=2, column=0, sticky=W)

    warp_settings_family_lbl = Label(frame_settings, text=warp_settings_family)
    warp_settings_family_lbl.grid(row=3, column=0, sticky=W)

    warp_settings_wifi_lbl = Label(frame_settings, text=warp_settings_wifi)
    warp_settings_wifi_lbl.grid(row=4, column=0, sticky=W)

    warp_settings_eth_lbl = Label(frame_settings, text=warp_settings_eth)
    warp_settings_eth_lbl.grid(row=5, column=0, sticky=W)

    warp_settings_dns_lbl = Label(frame_settings, text=warp_settings_dns)
    warp_settings_dns_lbl.grid(row=6, column=0, sticky=W)


def refresh_stats():
    # Clear any previous widgets displays before displaying message
    for widgets in frame_stats.winfo_children():
        widgets.destroy()    

    # If connected do stats, if not nothing to display so output message
    if connected:
        # Check and read output of stats into a list, every line split into new list item, displayed in frame
        warp_stats = ((subprocess.run(['warp-cli', 'warp-stats'], capture_output=True)).stdout).splitlines()
        warp_stats_time = warp_stats[1]
        warp_stats_data = warp_stats[2]
        warp_stats_latency = warp_stats[3]
        warp_stats_loss = warp_stats[4]
    
        # Define labels and display in frame for above settings
        warp_stats_time_lbl = Label(frame_stats, text=warp_stats_time)
        warp_stats_time_lbl.grid(row=0, column=0, sticky=W)

        warp_stats_data_lbl = Label(frame_stats, text=warp_stats_data)
        warp_stats_data_lbl.grid(row=1, column=0, sticky=W)

        warp_stats_latency_lbl = Label(frame_stats, text=warp_stats_latency)
        warp_stats_latency_lbl.grid(row=2, column=0, sticky=W)

        warp_stats_loss_lbl = Label(frame_stats, text=warp_stats_loss)
        warp_stats_loss_lbl.grid(row=3, column=0, sticky=W)
    else:
        warp_stats_noconnect_lbl = Label(frame_stats, text="   Not connected   ")
        warp_stats_noconnect_lbl.grid(row=0, column=0, sticky=W)


def refresh_all():
    update_conn_status()
    refresh_settings()
    refresh_stats()


# Main program starts here
update_conn_status()
refresh_settings()
refresh_stats()

# Family mode radio buttons
family_mode = StringVar()
# Get existing value
family_mode.set("malware")
# Define radio buttons and display
Radiobutton(frame_family, text="Full", variable=family_mode, value="full", command=lambda: family_clicked(family_mode.get())).pack(anchor=W)
Radiobutton(frame_family, text="Malware", variable=family_mode, value="malware", command=lambda: family_clicked(family_mode.get())).pack(anchor=W)
Radiobutton(frame_family, text="Off", variable=family_mode, value="off", command=lambda: family_clicked(family_mode.get())).pack(anchor=W)


# Add REFRESH BUTTON to update settings, connection status and stats
button_refresh = Button(root, text="Refresh", command=refresh_all)
button_refresh.grid(row=6, column=0)

# Add QUIT BUTTON
button_quit = Button(root, text="Exit", command=root.quit)
button_quit.grid(row=6, column=1)

# mainLoop ensures root window widget is constantly running and scanning for input
root.mainloop()