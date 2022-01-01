"""
Name: warp-cli-gui

Description: Python GUI program that will interact with the Linux command line to check status, and change basic settings, for Cloudflare WARP CLI.

Prequisites:
- Linux OS (tested on Manjaro Linux)
- Python 3 with pillow library
- warp-svc running as daemon
- warp-cli for Linux installed (instructions at https://developers.cloudflare.com/warp-client/get-started/linux)

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

Versions:
- V0.1 29 Dec 2021 Initial commit. Basically functional but needs connect button to be activated.
- V0.2 Connect/Disconnect button working, Top frames and status button better aligned, connect status not reliable yet though
- V0.3 Connect/Disconnect button status is finally stable through IF condition testing more rigorously for alternatives being returned from status command
- V0.4 30 Dec 2021 Fixed size window, with fixed size frames and spacing
- V0.5 31 Dec 2021 Cloudflare Warp logo added, connect status button colours changed (thanks to my wife Chantel for helping with this), family mode radio button defaults to existing setting, stats auto refresh every 2 secs after Refresh button pressed
- V1.0 31 Dec 2021 First stable version with just README file updated
- V1.1 1 Jan 2022 Tidied up button press color, optimized some code, added Always On toggle setting

TODO: - Option to switch WARP modes
TODO: - Testing auto-refresh with 2 sec interval - optional refresh in seconds
TODO: - Maybe graphs where relevant eg. latency
TODO: - Can it show connect status on panel when minimized? Qt can.
"""

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
import time


# Set global variable to test during execution
version = "V1.1"
connected = True
update_interval = 2000 # Milliseconds


# set root window called root
root = Tk()
# Set window title
root.title('Cloudflare WARP GUI ' + version)
# Set window logo
root.iconphoto(True, PhotoImage(file="warp_logo.png"))
# Set size of main window
root.geometry("420x410")
# Prevent resizing of root window
root.resizable(width=False, height=False)


# Define Our Toggle Images
toggle_on = PhotoImage(file = "on.png")
toggle_off = PhotoImage(file = "off.png")


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
    messagebox.showerror("Error", "Start daemon from CLI with\n'sudo systemctl start warp-svc'\nand ensure registration has run")
    sys.exit()

# Define frame for Connection Status
frame_status = LabelFrame(root, text="Status", padx=10, pady=10)
frame_status.grid(row=0, column=0, padx=10, pady=10)

# Define frame for Settings
frame_settings = LabelFrame(root, width=230, height=190, text="Settings", padx=10, pady=10)
frame_settings.grid(rowspan=2, sticky=NW, row=0, column=1, padx=10, pady=10)
frame_settings.grid_propagate(False)  # Stops frame shrinking with smaller contents

# Define frame for Stats
frame_stats = LabelFrame(root, width=230, height=130, text="Stats", padx=10, pady=10)
frame_stats.grid(row=2, column=1, padx=10, pady=10)
frame_stats.grid_propagate(False)  # Stops frame shrinking with smaller contents

# Define frame for family mode toggle
frame_family = LabelFrame(root, width=130, height=120, text="Family Mode", padx=10, pady=10)
frame_family.grid(sticky=N, row=1, column=0, padx=10, pady=10)
frame_family.grid_propagate(False)  # Stops frame shrinking with smaller contents

# Define frame for Always On toggle
frame_aon = LabelFrame(root, width=130, height=130, text="Always On Mode", padx=10, pady=10)
frame_aon.grid(sticky=N, row=2, column=0, padx=10, pady=10)
frame_aon.grid_propagate(False)  # Stops frame shrinking with smaller contents


def family_clicked(value):
    # Function to handle Family Mode Radio button click
    # Execute the set-families-mode change using value brought over from radio button press
    # Todo = test result for valid execution
    result = (subprocess.run(['warp-cli', 'set-families-mode', value], capture_output=True, text=True)).stdout
    # Refresh settings frame as value may have changed
    refresh_settings()


def update_conn_status():
    # Check if warp-cli connection is connected by running status command, and format returned text, and set connect status variable
    # Use globally defined connected variable
    global connected
    # Runs CLI command to check status for connectivity
    warp_connected = ((subprocess.run(['warp-cli', 'status'], capture_output=True)).stdout).splitlines()
    # Extract part where "b'Status update: Connected'"" or "b'Status update: Connected'"" should appear and set warp_connected to that
    # "b'Success'" or "b'Status update: Connecting'" are also possible, but if returned, then retest again by recalling function
    warp_connected = str(warp_connected[1])
    
    if warp_connected == "b'Status update: Connected'":
        connected = True
    elif warp_connected == "b'Status update: Disconnected'":
        connected = False
    else:
        # Means any of the two sought status' were not returned yet, so retry
        update_conn_status()

    # Debug Condition to check extracted text
    #print("|" + warp_connected + "|")


def connect_clicked():
    if connected:
        # Run command to disconnect and result should be 'Success' as result[0]
        result = (subprocess.run(['warp-cli', 'disconnect'], capture_output=True, text=True)).stdout
    else:
        # Run command to connect and result should be 'Success' as result[0]
        result = (subprocess.run(['warp-cli', 'connect'], capture_output=True, text=True)).stdout
    # Now refresh
    refresh_all()


def refresh_settings():
    global family_mode_status
    global always_connected
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
    # Set global family_mode_status to just extracted value at end
    family_mode_status = warp_settings_family[25 : ].lower()
    # Set global value always_connected to boolean of retrieved warp_settings_aon
    if str(warp_settings_aon) == "b'Always On: false'":
        always_connected = False
    elif str(warp_settings_aon) == "b'Always On: true'":
        always_connected = True
    else:
        # Pause 0.5 sec and retry as no valid option returned yet
        time.sleep(0.5)
        refresh_settings()

    # Define labels and display in frame for above settings
    warp_settings_aon_lbl = Label(frame_settings, text=warp_settings_aon)
    warp_settings_aon_lbl.grid(row=0, column=0, sticky=W)

    warp_settings_switch_lbl = Label(frame_settings, text=warp_settings_switch)
    warp_settings_switch_lbl.grid(row=1, column=0, sticky=W)

    warp_settings_mode_lbl = Label(frame_settings, text=warp_settings_mode)
    warp_settings_mode_lbl.grid(row=2, column=0, sticky=W)

    warp_settings_family_lbl = Label(frame_settings, text= warp_settings_family)
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

    # If connected do stats, if not connected then just display message
    if connected:
        # Check and read output of stats into a list, every line split into new list item, displayed in frame
        warp_stats = ((subprocess.run(['warp-cli', 'warp-stats'], capture_output=True)).stdout).splitlines()
        warp_stats_time = warp_stats[1]
        warp_stats_data = warp_stats[2]
        warp_stats_latency = warp_stats[3]
        warp_stats_loss = warp_stats[4]
    
        # Define labels and display in frame for above settings
        warp_stats_time_lbl = Label(frame_stats, text=warp_stats_time).grid(row=0, column=0, sticky=W)
        warp_stats_data_lbl = Label(frame_stats, text=warp_stats_data).grid(row=1, column=0, sticky=W)
        warp_stats_latency_lbl = Label(frame_stats, text=warp_stats_latency).grid(row=2, column=0, sticky=W)
        warp_stats_loss_lbl = Label(frame_stats, text=warp_stats_loss).grid(row=3, column=0, sticky=W)
    else:
        warp_stats_noconnect_lbl = Label(frame_stats, text="Not connected").grid(padx=60, pady=25)

def toggle_aon():
    global always_connected
    if always_connected:
        # Run command to toggle to always connected off
        result = (subprocess.run(['warp-cli', 'disable-always-on'], capture_output=True, text=True)).stdout
    else:
        # Run command to toggle to always connected on
        result = (subprocess.run(['warp-cli', 'enable-always-on'], capture_output=True, text=True)).stdout
    refresh_settings()  # Will retrieve changed always_connected settings from CLI
    display_aon()

def display_aon():
    global toggle_off, toggle_on
    global always_connected
    if always_connected:
        # ALWAYS CONNECTED toggle button to AON frame
        always_conn_btn = Button(frame_aon, image = toggle_on, command=toggle_aon)
    else:
        # ALWAYS CONNECTED toggle button to AON frame
        always_conn_btn = Button(frame_aon, image = toggle_off, command=toggle_aon)
    always_conn_btn.grid(row=0, column=0, pady=20)

def display_connect_btn():
    # Add CONNECT BUTTON to Status frame with text description and colour
    if connected:
        myConnect_Btn = Button(frame_status, text=" Connected ", width=10, bg="#76a633", activebackground="#76a633", relief=RAISED, command=connect_clicked)
    else:
        myConnect_Btn = Button(frame_status, text="Disconnected", width=10, bg="#ff8d00", activebackground="#ff8d00", relief=SUNKEN, command=connect_clicked)
    myConnect_Btn.grid(row=0, column=0)


def refresh_all():
    update_conn_status()
    display_connect_btn()
    refresh_settings()
    refresh_stats()
    display_aon()
    # Start auto refresh stats function (only after refresh button pressed)
    auto_refresh_stats()

def auto_refresh_stats():
    # Testing a  auto refresh loop every 2 secs
    # Functions to call to auto refresh
    if connected:
        refresh_stats()
        root.after(update_interval, auto_refresh_stats)


# Main program starts here
update_conn_status()
display_connect_btn()
refresh_settings()
display_aon()
refresh_stats()



# Family mode radio buttons to Family frame
family_mode = StringVar()
# Set default radio button to family_mode_status returned from checking settings
family_mode.set(family_mode_status)
# Define radio buttons and display
Radiobutton(frame_family, text="Full", variable=family_mode, value="full", command=lambda: family_clicked(family_mode.get())).pack(anchor=W)
Radiobutton(frame_family, text="Malware       ", variable=family_mode, value="malware", command=lambda: family_clicked(family_mode.get())).pack(anchor=W)
Radiobutton(frame_family, text="Off", variable=family_mode, value="off", command=lambda: family_clicked(family_mode.get())).pack(anchor=W)


# Add REFRESH BUTTON to update settings, connection status and stats
button_refresh = Button(root, text="Refresh", command=refresh_all)
button_refresh.grid(row=6, column=0)

# Add QUIT BUTTON
button_quit = Button(root, text="Exit", command=root.quit)
button_quit.grid(row=6, column=1)

# mainLoop ensures root window widget is constantly running and scanning for input
root.mainloop()