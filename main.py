import sys
import gc
from app.ticker import *
from app.main_handle_client import main_handle_client
import uasyncio as asyncio      
import app.coinobject

gc.collect()

#Get last saved configuration
try:
  #If there is a display configfile already, open it
  f = open('coinconfig.txt', 'r')
  content = f.read()
  coinconfig = content.split(' ersatzvariablepythoncrypto ')
  coinobject.coinobject.coin = coinconfig[0]
  coinobject.coinobject.exchange = coinconfig[1]
  coinobject.coinobject.amount = coinconfig[2]
  coinobject.coinobject.totalvalue = coinconfig[3]
  coinobject.coinobject.totalonly = coinconfig[4]
  coinobject.coinobject.currency = coinconfig[5]
  coinobject.coinobject.roundvar = int(coinconfig[6])
  coinobject.coinobject.speed = float(coinconfig[7])
  coinobject.coinobject.changeindicator = coinconfig[8]
  f.close()
except:
    pass
   
        
async def tickermain():
  #Start the webserver and the ticker program
  tasks = (ticker(),asyncio.start_server(main_handle_client, "", 80))
  await asyncio.gather(*tasks)
  
asyncio.run(tickermain())





