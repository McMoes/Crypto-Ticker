# McMoe's Crypto-Ticker

The Crypto-Ticker is a micropython project, to track your cryptocurrency investments via physical led displays.
This project is tested with an esp32 NodeMCU (Firmware = esp32-idf4-20200902-v1.13) connected to MAX7219 display 8 x (8 x 8 Pixel). If you use more or less than 8 Max7219 elements, you have to modify the code accordingly. We used Max7219 library from Mike Causer for communication between the esp board and the displays. Please keep in mind that the esp32 supports 2,4 GHz Wifi and WPA/WPA2 encryption.

Connect the pins of your esp32 NodeMCU with your Max7219 in the following way to get this code running:

Max7219     Esp32
VCC         V5
GND         GND (Use the GND pin 4 pins next to the V5 pin)
DIN         G23
CS          G15
CLK         G18


The Crypto-Ticker is working with the API from api.mcmoe.de. You have to get your own API key there and save that key in the coinobject.py file. If you just want a testaccount or have any question regarding the api, please contact support@mcmoe.de or use their contact form at the homepage https://www.mcmoe.de/en/contact/.

Everytime new coins or exchanges are released via this API, you can track them with this code without editing your code.

Examples:
- [Low budget](https://github.com/McMoes/Crypto-Ticker/tree/main/img/20210302_230349.jpg)
- [Low budget](https://github.com/McMoes/Crypto-Ticker/tree/main/img/20210302_230624.jpg)


# Features

- Track realtime price information of Bitcoin
- Track realtime price information of multiple altcoins
- Display current time (Use it as a clock)
- Display a custom text


# Installation

- Connect your esp board to your Max7219 displays
- Flash your esp32 with your micropython firmware (we used esp32-idf4-20200902-v1.13)
- IMPORTANT: Edit coinobject.py and replace 'YOUR_API_KEY_FROM_MCMOE.DE' with your personal API-Key 
- Get the latest release of this github repository and copy the needed files to your esp board (We used uPyCraft for that). You need boot.py and main.py in your root folder. And you need the app folder. To prevent memory issues (esp32 is a low performance board) i highly recommend to use .mpy files instead of the .py files. for that delete your app folder and put the .mpy files from the mpy_files [folder](https://github.com/McMoes/Crypto-Ticker/tree/main/mpy_files/) there. These files are precompiled python files, so the board does not have to compile itself a lot and you save a lot memory. Of course you can freeze this code in your own custom firmware wich would be the best way to save RAM.
- That's it. Now connect your esp board to your power supply. The esp board will first run boot.py and after that run main.py.


# Usage

At the first boot, your cryptoticker has no internet connection. You have to connect to it by following the instruction scrolling over the display (Connect to Wifi McMoes_CryptoTicker and type 192.168.4.1 in your browser). Now you can submit your [wifi credentials](https://github.com/McMoes/Crypto-Ticker/tree/main/img/WIFI_Configuration.png) to your esp board via the displayed html form. Now you will see the IP address, with wich you can communicate with your ticker during your wifi connection, on the display. After that the Crypto-Ticker will connect to McMoe's API and display the standard configurated information. You can now connect to your Ticker by typing the mentioned IP address into the browser of any device wich is connected to the same wifi as your Ticker. [Here](https://github.com/McMoes/Crypto-Ticker/tree/main/img/Configuration.JPG) you can set your preferred configuration and wich coins you want to track. On a bad crypto day you can also change to clock-mode here.

for more detailed information please read the [manual](https://github.com/McMoes/Crypto-Ticker/tree/main/manual/McMoes_CryptoTicker_manual.pdf).

# License

The code of McMoe's Crypto-Ticker is released under the terms of the MIT license. See LICENSE for more information or see https://opensource.org/licenses/MIT.
