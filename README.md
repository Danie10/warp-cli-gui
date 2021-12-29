# warp-cli-gui
<p>GUI app to read settings and stats from Cloudflare WARP CLI for Linux, and change some settings.</p>

![Screenshot_20211229_164126](https://user-images.githubusercontent.com/1153726/147673769-e71ec9e9-8901-4021-bcb4-5ea5784e4ef1.jpg)

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
    
## Todo's on the Road Map
- Connect/Disconnect button action
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
V0.1 - Initial release on 29 Dec 2021. Basically functional but needs connect button to be activated.
