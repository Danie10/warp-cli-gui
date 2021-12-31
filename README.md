# warp-cli-gui
<p>GUI app to read settings and stats from Cloudflare WARP CLI for Linux, and change some settings.</p>

![Screenshot Connected](assets/screenshot_connected.jpg)

![Screenshot Disconnected](assets/screenshot_disconnected.jpg)

[![Short Video](https://img.youtube.com/vi/MtlUrAmhWzI/0.jpg)](https://www.youtube.com/watch?v=MtlUrAmhWzI)

## Description
Python GUI program that will interact with Linux CLI to check status, and change basic settings, for Cloudflare WARP CLI.</p>

## Requirements and Execution
- Linux OS (tested on Manjaro Linux)
- Python 3 with pillow library
- warp-svc running as daemon (should be installed with warp-cli)
- warp-cli for Linux installed (instructions at https://developers.cloudflare.com/warp-client/get-started/linux)
- Copy these source files into a single folder, and execute with 'python warp-cli-gui.py'. For ease of use you can add this command, and the working directory, to a new menu item on Linux.

## License
This software is available under the GPL-3.0. You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/> for more info.

## Functionality
- Status button toggles connect / disconnect from WARP
- Family mode can be toggled between Full, Malware, Off
- Current WARP settings displayed, and refreshed if changed (or press refresh button)
- Current WARP stats displayed and will refresh automatically every 2 seconds after the refresh button has been pressed

## Todo's on the Road Map
- "Always stay connected" option setting
- Option to switch WARP modes
- Testing auto-refresh of stats frame with 2 sec interval - consider optional refresh in seconds or disable
- Maybe graphs where relevant eg. latency
- Can it show connect status on panel when minimized?

## Video
See my video about the initial creation of this app at https://youtu.be/hhPhiV0o5us

## Versions
- V0.1 29 Dec 2021 Initial commit. Basically functional but needs connect button to be activated.
- V0.2 Connect/Disconnect button working, Top frames and status button better aligned, connect status not reliable yet though
- V0.3 Connect/Disconnect button status is finally stable through IF condition testing more rigorously for alternatives being returned from status command
- V0.4 30 Dec 2021 Fixed size window, with fixed size frames and spacing
- V0.5 31 Dec 2021 Cloudflare Warp logo added, connect status button colours changed (thanks to my wife Chantel for helping with this), family mode radio button defaults to existing setting, stats auto refresh every 2 secs after Refresh button pressed
- V1.0 31 Dec 2021 First stable version with just README file updated