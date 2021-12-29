# warp-cli-gui
GUI app to read settings and stats from Cloudflare WARP CLI for Linux, and change some settings

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
    
Todo's on the roadmap:
TODO: - Fix clearing of frames
TODO: - Connect/Disconnect button action
TODO: - Fix spacings and layout
TODO: - "Always on" function's radio buttons / button
TODO: - Consider auto-refresh
TODO: - maybe graphs where relevant eg. latency
TODO: - Can it show connect status on panel when minimized?

Versions:
V0.1 - Initial release on 29 Dec 2021. Basically functional but needs connect button to be activated.
