# warp-cli-gui
<p>GUI app to read settings and stats from Cloudflare WARP CLI for Linux, and change some settings</p>

![Screenshot_20211229_164126](https://user-images.githubusercontent.com/1153726/147673769-e71ec9e9-8901-4021-bcb4-5ea5784e4ef1.jpg)

<p>Description: Python program that will interact with Linux CLI to check status, and change basic settings, for Cloudflare WARP CLI</p>

<p>Prequisites:
- Linux OS (tested on Manjaro Linux)
- Python 3 with pillow library
- warp-svc running as daemon
- warp-cli for Linux installed (instructions at https://developers.cloudflare.com/warp-client/get-started/linux)</p>

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
    
**Todo's on the roadmap:**
- Connect/Disconnect button action
- Pull though current Family Mode status to radio buttons
- Fix spacings and layout
- "Always stay connected" option setting
- Option to switch WARP modes
- Consider auto-refresh with optional refresh in seconds
- Maybe graphs where relevant eg. latency
- Can it show connect status on panel when minimized?

**Versions:**
V0.1 - Initial release on 29 Dec 2021. Basically functional but needs connect button to be activated.
