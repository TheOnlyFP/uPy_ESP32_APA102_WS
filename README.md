# uPy ESP32 APA102 WS
Attempt at creating a bit-bang based module to control APA102 LEDs over a WS connection.

# Board used
ESP32 Wroom (Sparkfun ESP32 Thing Plus) <br>
[https://www.sparkfun.com/products/14689](https://www.sparkfun.com/products/14689)

# Frozen modules
`net_funcs.py`, `apa.py` & `page.py` were frozen at the build of micropython.

# Flashing the main
[uPyCraft](http://docs.dfrobot.com/upycraft/) was used to flash the `main.py` to the ESP32.

# Wiring 
The in code defined pin-connections for the APA102 LED's are as follows:

| ESP32 | APA102 |
|-----|----------|
| 21  |clock (clk)|
| 17  | data     |
| VSUB| 5V       |
| GND | Ground   |

# How to add the code
- Clone micropython from [https://github.com/micropython/micropython/](https://github.com/micropython/micropython/)
- Configure micropython following the guide in the `README.md` file and install all dependencies
- Navigate to `micropython/ports/esp32/modules`
- Moves this repo's .py files into it (except `main.py`)
- `make` to build the port
- connect ESP32 via USB
- `make deploy` to flash the build to the chip
- `make clean` can be used to remove the previous build if a mistake was made
- use uPyCraft or possibly esptool [https://github.com/espressif/esptool](https://github.com/espressif/esptool)
- execute code by pressing `button 0` while booting the chip

# Controlling the LED's colour
- Connect to the ESP32's AP
- Go to the ESP32's IP [192.168.4.1](192.168.4.1)
- use the the jscolor colour-picker (the coloured box) to change the colour | Can be found here: [http://jscolor.com](http://jscolor.com)

__Note:__ as the APA102s require 5V they can only be used optimally when the ESP32 is connected to an USB power-source.
