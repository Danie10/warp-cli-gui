# warp-cli-gui
<p>GUI app to read settings and stats from Cloudflare WARP CLI for Linux, and change some settings.</p>

![Screenshot Connected](assets/screenshot_connected.jpg)

![Screenshot Disconnected](assets/screenshot_disconnected.jpg)
## Description
Python program that will interact with Linux CLI to check status, and change basic settings, for Cloudflare WARP CLI.</p>

## Requirements and Execution
- Linux OS (tested on Manjaro Linux)
- Python 3 with pillow library
- warp-svc running as daemon (should be installed with warp-cli)
- warp-cli for Linux installed (instructions at https://developers.cloudflare.com/warp-client/get-started/linux)
- Copy these source files into a single folder, and execute with 'python warp-cli-gui.py'

## License
This software is available under the GPL-3.0. You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/> for more info.

## Functionality
- Status button toggles connect or disconnect from WARP
- Family mode can be toggled between Full, Malware, Off
- Current settings displayed and refreshed if changed (press refresh button)
- Current stats displayed and refreshed if refresh button pressed (manual refresh only right now)

## Todo's on the Road Map
- Connect/Disconnect button action (test it more as sometimes manual refresh needed after reconnection to show green)
- Pull though current Family Mode status to radio buttons
- Fix spacings and layout
- "Always stay connected" option setting
- Option to switch WARP modes
- Consider auto-refresh with optional refresh in seconds
- Maybe graphs where relevant eg. latency
- Can it show connect status on panel when minimized?

## Video
See my video about the initial creation of this app at https://youtu.be/hhPhiV0o5us

## Versions
- V0.1 Initial release on 29 Dec 2021. Basically functional but needs connect button to be activated.
- V0.2 Connect/Disconnect button working, Top frames and status button better aligned, connect status not reliable yet though