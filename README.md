# McMoe's Crypto-Ticker

The Crypto-Ticker is a micropython project, to track your cryptocurrency investments via physical led displays.
This project is tested with an esp32 NodeMCU (Firmware = esp32-idf4-20200902-v1.13) connected to MAX7219 display 8 x (8 x 8 Pixel). If you use more or less than 8 Max7219 elements, you have to modify the code accordingly.

The Crypto-Ticker is working with the API from api.mcmoe.de (public release soon). You have to get your own API key there and save that key in the coinobject.py file. If you just want a testaccount or have any question regarding the api, please contact support@mcmoe.de.

Everytime new coins or exchanges are released via this API, you can track them with this code without editing your code.

If you do not 

# Features

- Track realtime price information of Bitcoin
- Track realtime price information of multiple altcoins
- Display current time (Use it as a clock)
- Display a custom text


# Installation

- Flash your esp32 with your micropython firmware (we used esp32-idf4-20200902-v1.13)
- Get the latest release of this github repository and copy the files to your esp board in the same structure (We used uPyCraft for that)
- That's it. Now connect your esp board to your power supply. The esp board will first run boot.py and after that run main.py.


# Usage

The Crypto-Ticker will 
