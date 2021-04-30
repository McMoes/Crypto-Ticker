import urequests
import uasyncio as asyncio
import ujson
import gc

gc.collect()

async def ticker_worker(url, params, coinobject, coins, amounts, exchanges):
    textchain = ""
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
              if coinobject.currency == 'BTC':       
                  coinobject.coinprice = data['results'][datacounter]['btcprice']
                  coinobject.coinprice = float(coinobject.coinprice)
                  coinobject.coinprice = round(coinobject.coinprice, coinobject.roundvar)
                  #Get and format percantage change values
                  change1dfloat = round((float(data['results'][datacounter]['btc1d'])*100),2)
                  change7dfloat = round((float(data['results'][datacounter]['btc7d'])*100),2)
                  change30dfloat = round((float(data['results'][datacounter]['btc30d'])*100),2)
              elif coinobject.currency == 'USD':       
                  coinobject.coinprice = data['results'][datacounter]['usdprice']
                  coinobject.coinprice = float(coinobject.coinprice)
                  coinobject.coinprice = round(coinobject.coinprice, coinobject.roundvar)
                  #Get and format percantage change values
                  change1dfloat = round((float(data['results'][datacounter]['usd1d'])*100),2)
                  change7dfloat = round((float(data['results'][datacounter]['usd7d'])*100),2)
                  change30dfloat = round((float(data['results'][datacounter]['usd30d'])*100),2)
              elif coinobject.currency == 'EUR':       
                  coinobject.coinprice = data['results'][datacounter]['eurprice']
                  coinobject.coinprice = float(coinobject.coinprice)
                  coinobject.coinprice = round(coinobject.coinprice, coinobject.roundvar)
                  #Get and format percantage change values
                  change1dfloat = round((float(data['results'][datacounter]['eur1d'])*100),2)
                  change7dfloat = round((float(data['results'][datacounter]['eur7d'])*100),2)
                  change30dfloat = round((float(data['results'][datacounter]['eur30d'])*100),2)
              if change1dfloat > 0:
               coinobject.change1d = "+" + str(change1dfloat) + "%"
              else:
                coinobject.change1d = str(change1dfloat) + "%"
              if change7dfloat > 0:
                coinobject.change7d = "+" + str(change7dfloat) + "%"
              else:
                coinobject.change7d = str(change7dfloat) + "%"
              if change30dfloat > 0:
                coinobject.change30d = "+" + str(change30dfloat) + "%"
              else:
                coinobject.change30d = str(change30dfloat) + "%"
              #Calculate portfolio and format text if the amount is set and total only is not checked
              if coinobject.amount != '' and coinobject.totalonly == 'N' and coincounter < len(amounts):
                value = round((float(amounts[coincounter])*coinobject.coinprice),2)
                if coinobject.changeindicator == 'triple':
                  text = coin + ": " + str(coinobject.coinprice) + " " + coinobject.currency + " (" + str(value) + " " + coinobject.currency + ") " + coinobject.change1d + " " + coinobject.change7d + " " + coinobject.change30d
                elif coinobject.changeindicator == '1+7':
                  text = coin + ": " + str(coinobject.coinprice) + " " + coinobject.currency + " (" + str(value) + " " + coinobject.currency + ") " + coinobject.change1d + " " + coinobject.change7d
                elif coinobject.changeindicator == '1+30':
                  text = coin + ": " + str(coinobject.coinprice) + " " + coinobject.currency + " (" + str(value) + " " + coinobject.currency + ") " + coinobject.change1d + " " + coinobject.change30d
                elif coinobject.changeindicator == '7+30':
                  text = coin + ": " + str(coinobject.coinprice) + " " + coinobject.currency + " (" + str(value) + " " + coinobject.currency + ") " + coinobject.change7d + " " + coinobject.change30d
                elif coinobject.changeindicator == '1d':
                  text = coin + ": " + str(coinobject.coinprice) + " " + coinobject.currency + " (" + str(value) + " " + coinobject.currency + ") " + coinobject.change1d
                elif coinobject.changeindicator == '7d':
                  text = coin + ": " + str(coinobject.coinprice) + " " + coinobject.currency + " (" + str(value) + " " + coinobject.currency + ") " + coinobject.change7d
                elif coinobject.changeindicator == '30d':
                  text = coin + ": " + str(coinobject.coinprice) + " " + coinobject.currency + " (" + str(value) + " " + coinobject.currency + ") " + coinobject.change30d
                elif coinobject.changeindicator == 'no':
                  text = coin + ": " + str(coinobject.coinprice) + " " + coinobject.currency + " (" + str(value) + " " + coinobject.currency + ") "
                totalvalue += value
              #Format displayed text if there is no amount set
              else:
                try:
                  value = round((float(amounts[coincounter])*coinobject.coinprice),2)
                except:
                  pass
                if coinobject.changeindicator == 'triple':
                  text = coin + ": " + str(coinobject.coinprice) + " " + coinobject.currency + " " + coinobject.change1d + " " + coinobject.change7d + " " + coinobject.change30d
                elif coinobject.changeindicator == '1+7':
                  text = coin + ": " + str(coinobject.coinprice) + " " + coinobject.currency + " " + coinobject.change1d + " " + coinobject.change7d
                elif coinobject.changeindicator == '1+30':
                  text = coin + ": " + str(coinobject.coinprice) + " " + coinobject.currency + " " + coinobject.change1d + " " + coinobject.change30d
                elif coinobject.changeindicator == '7+30':
                  text = coin + ": " + str(coinobject.coinprice) + " " + coinobject.currency + " " + coinobject.change7d + " " + coinobject.change30d
                elif coinobject.changeindicator == '1d':
                  text = coin + ": " + str(coinobject.coinprice) + " " + coinobject.currency + " " + coinobject.change1d
                elif coinobject.changeindicator == '7d':
                  text = coin + ": " + str(coinobject.coinprice) + " " + coinobject.currency + " " + coinobject.change7d
                elif coinobject.changeindicator == '30d':
                  text = coin + ": " + str(coinobject.coinprice) + " " + coinobject.currency + " " + coinobject.change30d
                elif coinobject.changeindicator == 'no':
                  text = coin + ": " + str(coinobject.coinprice) + " " + coinobject.currency
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
    if coinobject.totalvalue == 'Y' and totalvalue:
      textchain = textchain + ', Total: ' + str(totalvalue) + ' ' + coinobject.currency
    return textchain