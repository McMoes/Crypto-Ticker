from . import coinobject
import uasyncio as asyncio
from .webpage import web_page_config
from .webpage_wifi import web_page_wifi
from . import ticker
import gc

urlescapes = {'%2C':','}
urlescapes2 = { '%24':'$','%26':'&','%2B':'+','%2C':',','%2F':'/','%3A':':','%3B':';','%3D':'=','%3F':'?','%21':'!','%40':'@','%20':' ',
                '%22':'?','%3C':'<','%3E':'>','%23':'#','%25':'%','%7B':'{','%7D':'}','%7C':'|','%5E':'^','%7E':'~','%5B':'[','%5D':']','%60':'`','+':' '}

async def main_handle_client(reader, writer):
  if ticker.validconfig == True:
    response = web_page_config()
  else:
    response = web_page_wifi()
  request = await reader.read(1024)
  requeststring = str(request).replace("\r\n", "")
  if 'get?ssid=' in requeststring and '&password=' in requeststring and '&helpvarcryptoticker=' in requeststring:
    requeststring = requeststring.replace('get?ssid=', 'ersatzvariablepythoncrypto')
    requeststring = requeststring.replace('&password=', 'ersatzvariablepythoncrypto')
    requeststring = requeststring.replace('&helpvarcryptoticker=', 'ersatzvariablepythoncrypto')
    splitvar = requeststring.split('ersatzvariablepythoncrypto')

    wifissid = splitvar[1]
    wifipassword = splitvar[2]
    for k,v in urlescapes2.items():
      wifipassword = wifipassword.replace(k, v)
    for k,v in urlescapes2.items():
      wifissid = wifissid.replace(k, v)
    #Write wifi config in a textfile
    with open('wificonfig.txt', 'w') as f:
      #f.write(configstring)
      f.write("%s ersatzvariablepythoncrypto %s" % (wifissid, wifipassword))
    #Setting wifi config to true forces the program to check the credentials
    ticker.wificonfig = True
  elif 'get?xcoinx=' in requeststring and '&helpvarcryptoticker=' in requeststring:
    requeststring = requeststring.replace('get?xcoinx=', 'ersatzvariablepythoncrypto')
    requeststring = requeststring.replace('&xexchangex=', 'ersatzvariablepythoncrypto')
    requeststring = requeststring.replace('&xamountx=', 'ersatzvariablepythoncrypto')
    requeststring = requeststring.replace('&xsumvaluex=', 'ersatzvariablepythoncrypto')
    requeststring = requeststring.replace('&xsumvalueonlyx=', 'ersatzvariablepythoncrypto')
    requeststring = requeststring.replace('&xcurrencyx=', 'ersatzvariablepythoncrypto')
    requeststring = requeststring.replace('&xroundx=', 'ersatzvariablepythoncrypto')
    requeststring = requeststring.replace('&xspeedx=', 'ersatzvariablepythoncrypto')
    requeststring = requeststring.replace('&xpercentagex=', 'ersatzvariablepythoncrypto')
    requeststring = requeststring.replace('&xtimeformatx=', 'ersatzvariablepythoncrypto')
    requeststring = requeststring.replace('&xcustomtextx=', 'ersatzvariablepythoncrypto')
    requeststring = requeststring.replace('&helpvarcryptoticker=', 'ersatzvariablepythoncrypto')
    splitvar = requeststring.split('ersatzvariablepythoncrypto')
    #Ckeck if totalyes or/and totalonlyyes were submitted and move them to the end of the list
    if 'totalyes' in splitvar:
      splitvar.pop(splitvar.index('totalyes'))
      splitvar.append('totalyes')
    if 'totalonlyyes' in splitvar:
      splitvar.pop(splitvar.index('totalonlyyes'))
      splitvar.append('totalonlyyes')
    #Check if current time should be diplayed instead of crypto prices
    if 'x24hx' in splitvar or 'x12hx' in splitvar:
      if 'x24hx' in splitvar:
        coinobject.coinobject.clocktime = '24h'
      elif 'x12hx' in splitvar:
        coinobject.coinobject.clocktime = '12h'
    #Else get crypto variables
    else:
      coinobject.coinobject.clocktime = ''
      if splitvar[1] != '':
        coinobject.coinobject.coin = splitvar[1].upper()
        for k,v in urlescapes.items():
          coinobject.coinobject.coin = coinobject.coinobject.coin.replace(k, v)
      coinobject.coinobject.exchange = splitvar[2]
      for k,v in urlescapes.items():
        coinobject.coinobject.exchange = coinobject.coinobject.exchange.replace(k, v)
      #Check if a vlid amount was given else delete it
      coinobject.coinobject.amount = splitvar[3]
      
      if coinobject.coinobject.amount and coinobject.coinobject.amount != '':
        try:
          for k,v in urlescapes.items():
            coinobject.coinobject.amount = coinobject.coinobject.amount.replace(k, v)
          amounts = coinobject.coinobject.amount.split(',')
          for amount in amounts:
            value = round(float(amount)*2,2)
        except:
          coinobject.coinobject.amount = ''
      #Check if total value should be displayed
      if 'totalyes' in splitvar:
        coinobject.coinobject.totalvalue = 'Y'
      else:
        coinobject.coinobject.totalvalue = 'N'
      #Check if only total should be displayed
      if 'totalonlyyes' in splitvar:
        coinobject.coinobject.totalonly = 'Y'
      else:
        coinobject.coinobject.totalonly = 'N'
      #Check if a valid currency was given else set it to USD
      if splitvar[4].upper() in ['BTC','USD','EUR']:
        coinobject.coinobject.currency = splitvar[4].upper()
      else:
        coinobject.coinobject.currency = 'USD'
      #Check if a valid roundvar was given else set it to 2
      if splitvar[5] != '':
        try:
          coinobject.coinobject.roundvar = int(splitvar[5])
        except:
          coinobject.coinobject.roundvar = 2
      else:
        coinobject.coinobject.roundvar = 2
      #Limit speed option for not let the text scroll forever
      if splitvar[6] != '':
        try:
          if float(splitvar[6]) > 1:
            coinobject.coinobject.speed = 0.02
          elif float(splitvar[6]) <= 0:
            coinobject.coinobject.speed = 0.02
          else:
            coinobject.coinobject.speed = float(splitvar[6])
        except:
          pass
      if 'x1dx' in splitvar and 'x7dx' in splitvar and 'x30dx' in splitvar:
        coinobject.coinobject.changeindicator='triple'
      elif 'x1dx' in splitvar and 'x7dx' in splitvar and not 'x30dx' in splitvar:
        coinobject.coinobject.changeindicator='1+7'
      elif 'x1dx' in splitvar and 'x30dx' in splitvar and not 'x7dx' in splitvar:
        coinobject.coinobject.changeindicator='1+30'
      elif 'x7dx' in splitvar and 'x30dx' in splitvar and not 'x1dx' in splitvar:
        coinobject.coinobject.changeindicator='7+30'
      elif 'x1dx' in splitvar and not 'x7dx' in splitvar and not 'x30dx' in splitvar:
        coinobject.coinobject.changeindicator='1d'
      elif 'x7dx' in splitvar and not 'x1dx' in splitvar and not 'x30dx' in splitvar:
        coinobject.coinobject.changeindicator='7d'
      elif 'x30dx' in splitvar and not 'x1dx' in splitvar and not 'x7dx' in splitvar:
        coinobject.coinobject.changeindicator='30d'
      elif not 'x1dx' in splitvar and not 'x7dx' in splitvar and not 'x30dx' in splitvar:
        coinobject.coinobject.changeindicator='no'
      #Check if a custom text was given
      coinobject.coinobject.customtext = ''
      if splitvar[7] != '' and coinobject.coinobject.changeindicator == 'no':
        coinobject.coinobject.customtext = str(splitvar[7])
        for k,v in urlescapes2.items():
          coinobject.coinobject.customtext = coinobject.coinobject.customtext.replace(k, v)
      #Write configuration to file
      with open('coinconfig.txt', 'w') as f:
        f.write("%s ersatzvariablepythoncrypto %s ersatzvariablepythoncrypto %s ersatzvariablepythoncrypto %s ersatzvariablepythoncrypto %s ersatzvariablepythoncrypto %s ersatzvariablepythoncrypto %d ersatzvariablepythoncrypto %.5f ersatzvariablepythoncrypto %s" % (coinobject.coinobject.coin, coinobject.coinobject.exchange, coinobject.coinobject.amount, coinobject.coinobject.totalvalue, coinobject.coinobject.totalonly, coinobject.coinobject.currency, coinobject.coinobject.roundvar, coinobject.coinobject.speed, coinobject.coinobject.changeindicator))
    #input = True
  await writer.awrite(response)
  await asyncio.sleep(0.2)
  await writer.wait_closed()  




