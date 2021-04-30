import sys
import urequests
import ujson
import time
import gc
from . import coinobject
from . import max7219
from . import helpvar
from . import ticker_worker
from machine import Pin, SPI
import uasyncio as asyncio
import network

wifissid = ''
wifipassword = ''
ssid = 'McMoes_CryptoTicker'
password = 'mcmoe_2021'
wificonfigs = ''


async def display(screen, delay, text, counter):
    for i in range((len(text)*8)+64):
        screen.fill(0)
        screen.text(text, counter, 0, 1)
        counter-=1
        await asyncio.sleep(delay)
        screen.show()

async def ticker():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password)
    while ap.active() == False:
      pass
    sck = Pin(18, Pin.OUT)
    mosi = Pin(23, Pin.OUT)
    miso = Pin(19, Pin.IN)
    cs = Pin(15, Pin.OUT)
    spi = SPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
    screen = max7219.Matrix8x8(spi, cs, 8)
    screen.brightness(15)
    screen.fill(1)
    screen.show()
    screen.fill(0)
    screen.show()
    while helpvar.helpobj.validconfig == False:
      try:
        #If there is a wifi configfile already, open it
        f = open('wificonfig.txt', 'r')
        content = f.read()
        wificonfigs = content.split(' ersatzvariablepythoncrypto ')
        wifissid = wificonfigs[0]
        wifipassword = wificonfigs[1]
        f.close()
        #Connect esp to wifi
        station.connect(wifissid, wifipassword)

        #Try to connect to Wifi for 20 seconds, else remove wificonfig file
        t_end = time.time() + 10
        text = "Can`t connect to Wifi! Please set new Wifi credentials!"
        helpvar.helpobj.wificonfig = False
        while station.isconnected() == False and helpvar.helpobj.wificonfig == False:
          if time.time() > t_end:
              #Delete wifi config
              try:
                uos.remove("wificonfig.txt")
              except:
                pass
              counter = 63
              await display(screen, coinobject.coinobject.speed, text, counter)
          else:
            pass
        #If Wifi connection is established, show IP address of esp on display
        if station.isconnected() == True:
          helpvar.helpobj.validconfig = True
          ap.active(False)
          #Show IP address of device inside wlan on display
          ip = station.ifconfig()[0]
          text = "McMoe`s Crypto-Ticker WLAN-IP: %s" % (ip)
          counter = 63
          await display(screen, coinobject.coinobject.speed, text, counter)
      except:
        #Show access point IP address on display, only if there is no wifi configfile
        ip = ap.ifconfig()[0]
        text = "Connect to Wifi McMoes_CryptoTicker and enter the IP address into your browser: %s" % (ip)
        while helpvar.helpobj.wificonfig == False:
          counter = 63
          await display(screen, coinobject.coinobject.speed, text, counter)
    while True:
        #Check wich function is selected (Clock, Ticker, Custom text) and run the function
        #Check if clock should be displayed
        if coinobject.coinobject.clocktime != '':
            url = "http://worldtimeapi.org/api/ip"
            while coinobject.coinobject.clocktime != '':
                #Get current time based on ip address from api
                try:
                    response = urequests.request('GET', url)
                    data = ujson.loads(response.text)
                    response.close()
                    #Format time
                    if coinobject.coinobject.clocktime == '24h':
                        timestring = data['datetime'][11:16]
                        position = 12
                    else:
                        hour = int(data['datetime'][11:13])
                        if hour > 12:
                            timestring = str(hour-12) + data['datetime'][13:16] + ' pm'
                        else:
                            timestring = data['datetime'][11:16] + ' am'
                        position = 5
                    #Display time
                    screen.fill(0)
                    screen.text(timestring, position, 0, 1)
                    screen.show()
                    await asyncio.sleep(60)
                except:
                    pass
        #Check if custom text should be displayed
        elif coinobject.coinobject.customtext != '':
            while coinobject.coinobject.customtext != '':
                text = coinobject.coinobject.customtext
                try:       
                    #Show custom text on display
                    counter = 63
                    await display(screen, coinobject.coinobject.speed, text, counter)
                    await asyncio.sleep(0.5)
                except:
                    pass
        #Else show coin prices from McMoe's API
        else:
            while coinobject.coinobject.customtext == '' and coinobject.coinobject.clocktime == '':
                gc.collect()
                if station.isconnected()==False:
                    station.connect(wifissid, wifipassword)
                    while station.isconnected()==False:
                        pass
                coins = coinobject.coinobject.coin.split(',')
                #If amounts were set then split them
                if coinobject.coinobject.amount != "":
                  amounts = coinobject.coinobject.amount.split(',')
                else:
                  amounts = []
                #If exchanges were set then split them
                if coinobject.coinobject.exchange != "":
                  exchanges = coinobject.coinobject.exchange.split(',')
                else:
                  exchanges = []
                #Fill an empty exchange element into list is there as long as there is one missing for a coin
                while len(exchanges) < len(coins):
                  exchanges.append('')
                url = "https://api.mcmoe.de/api_v01/coinprices/?coin=%s&limit=20&offset=0" % (coinobject.coinobject.coin)
                params = {
                  'Api-Key': coinobject.coinobject.apikey,
                }
                try:
                    textchain = await ticker_worker.ticker_worker(url, params, coinobject.coinobject, coins, amounts, exchanges)
                    counter = 63
                    await display(screen, coinobject.coinobject.speed, textchain, counter) 
                except Exception as e:
                    print(str(e))
                    if '-202' in str(e) or ('Errno 113' in str(e) and 'EHOSTUNREACH' in str(e)) or '118' == str(e):
                        station.disconnect()
                    else:
                        counter = 63
                        text = str(e)
                        await display(screen, coinobject.coinobject.speed, text, counter) 








