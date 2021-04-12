import sys
import urequests
import ujson
import time
import gc
from . import coinobject
from . import max7219
from machine import Pin, SPI
import uasyncio as asyncio
import network

#gc.collect()

closewriter = False
wificonfig = False
validconfig = False
wifissid = ''
wifipassword = ''
ssid = 'McMoes_CryptoTicker'
password = 'mcmoe_2021'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)

sck = Pin(18, Pin.OUT)
mosi = Pin(23, Pin.OUT)
miso = Pin(19, Pin.IN)
cs = Pin(2, Pin.OUT)
spi = SPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
screen = max7219.Matrix8x8(spi, cs, 8)
screen.brightness(15)
screen.fill(1)
screen.show()
screen.fill(0)
screen.show()

while ap.active() == False:
  pass
  
async def ticker():
    global screen
    global wificonfig
    global closewriter
    global validconfig
    while validconfig == False:
      try:
        #If there is a wifi configfile already, open it
        f = open('wificonfig.txt', 'r')
        content = f.read()
        wificonfig = content.split(' ersatzvariablepythoncrypto ')
        wifissid = wificonfig[0]
        wifipassword = wificonfig[1]
        f.close()
        #Connect esp to wifi
        station = network.WLAN(network.STA_IF)

        station.active(True)
        station.connect(wifissid, wifipassword)

        #Try to connect to Wifi for 20 seconds, else remove wificonfig file
        t_end = time.time() + 10
        text = "Can`t connect to Wifi! Please set new Wifi credentials!"
        wificonfig = False
        while station.isconnected() == False and wificonfig == False:
          if time.time() > t_end:
              #Delete wifi config
              try:
                uos.remove("wificonfig.txt")
              except:
                pass
              counter = 63
              for i in range((len(text)*8)+64):
                screen.fill(0)
                screen.text(text, counter, 0, 1)
                counter-=1
                await asyncio.sleep(0.015)
                screen.show()
          else:
            pass
        #If Wifi connection is established, show IP address of esp on display
        if station.isconnected() == True:
          validconfig = True
          ap.active(False)
          closewriter = True
          #Show IP address of device inside wlan on display
          ip = station.ifconfig()[0]
          text = "McMoe`s Crypto-Ticker WLAN-IP: %s" % (ip)
          counter = 63
          for i in range((len(text)*8)+64):
            screen.fill(0)
            screen.text(text, counter, 0, 1)
            counter-=1
            await asyncio.sleep(0.015)
            screen.show()
      except:
        #Show access point IP address on display, only if there is no wifi configfile
        ip = ap.ifconfig()[0]
        text = "Connect to Wifi McMoes_CryptoTicker and enter the IP address into your browser: %s" % (ip)
        while wificonfig == False:
          counter = 63
          for i in range((len(text)*8)+64):
            screen.fill(0)
            screen.text(text, counter, 0, 1)
            counter-=1
            await asyncio.sleep(0.015)
            screen.show()
    while True:
        #gc.collect()
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
                    for i in range((len(text)*8)+64):
                        screen.fill(0)
                        screen.text(text, counter, 0, 1)
                        counter-=1
                        await asyncio.sleep(coinobject.coinobject.speed)
                        screen.show()
                    await asyncio.sleep(0.5)
                except:
                    pass
        #Else show coin prices from McMoe's API
        else:
            while coinobject.coinobject.customtext == '' and coinobject.coinobject.clocktime == '':
                #gc.collect()
                #Reconnect if Wifi connection is lost
                if not station.isconnected():
                  station.active(True)
                  station.connect(wifissid, wifipassword)
                  while not station.isconnected():
                    pass
                textchain = ""
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
                try:
                  #print(gc.mem_free())
                  url = "https://api.mcmoe.de/api_v01/coinprices/?coin=%s&limit=100&offset=0" % (coinobject.coinobject.coin)
                  params = {
                    'Api-Key': coinobject.coinobject.apikey,
                  }
                  response = urequests.request('GET', url, headers=params)
                  data = ujson.loads(response.text)
                  response.close()
                  totalvalue = 0
                  coincounter = 0
                  for coin in coins:
                    #Take the data from selected exchange. If no exchange is selected then take the first (Most 24h Value)
                    datacounter = 0
                    for element in data['results']:
                      if coin == element['coin']:
                        if (exchanges[coincounter] != '' and exchanges[coincounter] == element['exchangename']) or (exchanges[coincounter] == ''):
                          if coinobject.coinobject.currency == 'BTC':       
                              coinobject.coinobject.coinprice = data['results'][datacounter]['btcprice']
                              coinobject.coinobject.coinprice = float(coinobject.coinobject.coinprice)
                              coinobject.coinobject.coinprice = round(coinobject.coinobject.coinprice, coinobject.coinobject.roundvar)
                              #Get and format percantage change values
                              change1dfloat = round((float(data['results'][datacounter]['btc1d'])*100),2)
                              change7dfloat = round((float(data['results'][datacounter]['btc7d'])*100),2)
                              change30dfloat = round((float(data['results'][datacounter]['btc30d'])*100),2)
                          elif coinobject.coinobject.currency == 'USD':       
                              coinobject.coinobject.coinprice = data['results'][datacounter]['usdprice']
                              coinobject.coinobject.coinprice = float(coinobject.coinobject.coinprice)
                              coinobject.coinobject.coinprice = round(coinobject.coinobject.coinprice, coinobject.coinobject.roundvar)
                              #Get and format percantage change values
                              change1dfloat = round((float(data['results'][datacounter]['usd1d'])*100),2)
                              change7dfloat = round((float(data['results'][datacounter]['usd7d'])*100),2)
                              change30dfloat = round((float(data['results'][datacounter]['usd30d'])*100),2)
                          elif coinobject.coinobject.currency == 'EUR':       
                              coinobject.coinobject.coinprice = data['results'][datacounter]['eurprice']
                              coinobject.coinobject.coinprice = float(coinobject.coinobject.coinprice)
                              coinobject.coinobject.coinprice = round(coinobject.coinobject.coinprice, coinobject.coinobject.roundvar)
                              #Get and format percantage change values
                              change1dfloat = round((float(data['results'][datacounter]['eur1d'])*100),2)
                              change7dfloat = round((float(data['results'][datacounter]['eur7d'])*100),2)
                              change30dfloat = round((float(data['results'][datacounter]['eur30d'])*100),2)
                          if change1dfloat > 0:
                           coinobject.coinobject.change1d = "+" + str(change1dfloat) + "%"
                          else:
                            coinobject.coinobject.change1d = str(change1dfloat) + "%"
                          if change7dfloat > 0:
                            coinobject.coinobject.change7d = "+" + str(change7dfloat) + "%"
                          else:
                            coinobject.coinobject.change7d = str(change7dfloat) + "%"
                          if change30dfloat > 0:
                            coinobject.coinobject.change30d = "+" + str(change30dfloat) + "%"
                          else:
                            coinobject.coinobject.change30d = str(change30dfloat) + "%"
                          #Calculate portfolio and format text if the amount is set and total only is not checked
                          if coinobject.coinobject.amount != '' and coinobject.coinobject.totalonly == 'N' and coincounter < len(amounts):
                            value = round((float(amounts[coincounter])*coinobject.coinobject.coinprice),2)
                            if coinobject.coinobject.changeindicator == 'triple':
                              text = coin + ": " + str(coinobject.coinobject.coinprice) + " " + coinobject.coinobject.currency + " (" + str(value) + " " + coinobject.coinobject.currency + ") " + coinobject.coinobject.change1d + " " + coinobject.coinobject.change7d + " " + coinobject.coinobject.change30d
                            elif coinobject.coinobject.changeindicator == '1+7':
                              text = coin + ": " + str(coinobject.coinobject.coinprice) + " " + coinobject.coinobject.currency + " (" + str(value) + " " + coinobject.coinobject.currency + ") " + coinobject.coinobject.change1d + " " + coinobject.coinobject.change7d
                            elif coinobject.coinobject.changeindicator == '1+30':
                              text = coin + ": " + str(coinobject.coinobject.coinprice) + " " + coinobject.coinobject.currency + " (" + str(value) + " " + coinobject.coinobject.currency + ") " + coinobject.coinobject.change1d + " " + coinobject.coinobject.change30d
                            elif coinobject.coinobject.changeindicator == '7+30':
                              text = coin + ": " + str(coinobject.coinobject.coinprice) + " " + coinobject.coinobject.currency + " (" + str(value) + " " + coinobject.coinobject.currency + ") " + coinobject.coinobject.change7d + " " + coinobject.coinobject.change30d
                            elif coinobject.coinobject.changeindicator == '1d':
                              text = coin + ": " + str(coinobject.coinobject.coinprice) + " " + coinobject.coinobject.currency + " (" + str(value) + " " + coinobject.coinobject.currency + ") " + coinobject.coinobject.change1d
                            elif coinobject.coinobject.changeindicator == '7d':
                              text = coin + ": " + str(coinobject.coinobject.coinprice) + " " + coinobject.coinobject.currency + " (" + str(value) + " " + coinobject.coinobject.currency + ") " + coinobject.coinobject.change7d
                            elif coinobject.coinobject.changeindicator == '30d':
                              text = coin + ": " + str(coinobject.coinobject.coinprice) + " " + coinobject.coinobject.currency + " (" + str(value) + " " + coinobject.coinobject.currency + ") " + coinobject.coinobject.change30d
                            elif coinobject.coinobject.changeindicator == 'no':
                              text = coin + ": " + str(coinobject.coinobject.coinprice) + " " + coinobject.coinobject.currency + " (" + str(value) + " " + coinobject.coinobject.currency + ") "
                            totalvalue += value
                          #Format displayed text if there is no amount set
                          else:
                            try:
                              value = round((float(amounts[coincounter])*coinobject.coinobject.coinprice),2)
                            except:
                              pass
                            if coinobject.coinobject.changeindicator == 'triple':
                              text = coin + ": " + str(coinobject.coinobject.coinprice) + " " + coinobject.coinobject.currency + " " + coinobject.coinobject.change1d + " " + coinobject.coinobject.change7d + " " + coinobject.coinobject.change30d
                            elif coinobject.coinobject.changeindicator == '1+7':
                              text = coin + ": " + str(coinobject.coinobject.coinprice) + " " + coinobject.coinobject.currency + " " + coinobject.coinobject.change1d + " " + coinobject.coinobject.change7d
                            elif coinobject.coinobject.changeindicator == '1+30':
                              text = coin + ": " + str(coinobject.coinobject.coinprice) + " " + coinobject.coinobject.currency + " " + coinobject.coinobject.change1d + " " + coinobject.coinobject.change30d
                            elif coinobject.coinobject.changeindicator == '7+30':
                              text = coin + ": " + str(coinobject.coinobject.coinprice) + " " + coinobject.coinobject.currency + " " + coinobject.coinobject.change7d + " " + coinobject.coinobject.change30d
                            elif coinobject.coinobject.changeindicator == '1d':
                              text = coin + ": " + str(coinobject.coinobject.coinprice) + " " + coinobject.coinobject.currency + " " + coinobject.coinobject.change1d
                            elif coinobject.coinobject.changeindicator == '7d':
                              text = coin + ": " + str(coinobject.coinobject.coinprice) + " " + coinobject.coinobject.currency + " " + coinobject.coinobject.change7d
                            elif coinobject.coinobject.changeindicator == '30d':
                              text = coin + ": " + str(coinobject.coinobject.coinprice) + " " + coinobject.coinobject.currency + " " + coinobject.coinobject.change30d
                            elif coinobject.coinobject.changeindicator == 'no':
                              text = coin + ": " + str(coinobject.coinobject.coinprice) + " " + coinobject.coinobject.currency
                            try:
                              totalvalue += value
                            except:
                              pass
                          if textchain == "":
                            textchain = text
                          else:
                            textchain = textchain + ", " + text
                          coincounter += 1
                          break
                      datacounter += 1
                  #Display total value if checkbox was checked
                  if coinobject.coinobject.totalvalue == 'Y' and totalvalue:
                    textchain = textchain + ', Total: ' + str(totalvalue) + ' ' + coinobject.coinobject.currency
                  counter = 63
                  for i in range((len(textchain)*8)+64):
                      screen.fill(0)
                      screen.text(textchain, counter, 0, 1)
                      counter-=1
                      await asyncio.sleep(coinobject.coinobject.speed)
                      screen.show()
                except Exception as e:
                  #Show error on display, if it is [errno 113 ehostunreach] pass and try again
                  if ('Errno 113' in str(e) and 'EHOSTUNREACH' in str(e)) or '118' == str(e):
                    gc.collect()
                    pass
                  else:
                    gc.collect()
                    text = str(e)
                    counter = 63
                    for i in range((len(text)*8)+64):
                      screen.fill(0)
                      screen.text(text, counter, 0, 1)
                      counter-=1
                      await asyncio.sleep(0.015)
                      screen.show()     







