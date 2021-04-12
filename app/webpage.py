from .coinobject import *

def web_page_config():
  html = """<!DOCTYPE html><html lang="de">
  <head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  </head>
  <body>
  <form action="/get">
  <h1><a href="https://mcmoe.de">McMoe`s Crypto-Ticker</a></h1>
  <br>
  <a href= "mailto:support@mcmoe.de">contact support</a>
  <br>
  <br>
  <h2>Coin configuration</h2>
  <label for="xcoinx">Coin Symbol:</label>
  <input type="text" id="xcoinx" name="xcoinx" placeholder="%s"><br>
  <label for="xexchangex">Exchange:</label>
  <input type="text" id="xexchangex" name="xexchangex" placeholder="%s"><br>
  <label for="xamountx">Amount:</label>
  <input type="text" id="xamountx" name="xamountx" placeholder="%s"><br>
  <label for="xcurrencyx">Fiat currency:</label>
  <input type="text" id="xcurrencyx" name="xcurrencyx" placeholder="%s"><br>
  <div>
  <input type="checkbox" id="xsumvaluex" name="xsumvaluex" value="totalyes">
  <label for="xsumvaluex">Display total value</label>
  <input type="checkbox" id="xsumvalueonlyx" name="xsumvalueonlyx" value="totalonlyyes">
  <label for="xsumvalueonlyx">Total only</label>
  </div>  
  <br>
  <h2>Display configuration</h2>
  <label for="xroundx">Round digits:</label>
  <input type="text" id="xroundx" name="xroundx" placeholder="%d"><br>
  <label for="xspeedx">Display speed (delay in seconds):</label>
  <input type="text" id="xspeedx" name="xspeedx" placeholder="%.5f"><br>
  <fieldset>
  <legend>Choose displayed percentage change</legend>
  <div>
  <input type="checkbox" id="1d" name="xpercentagex" value="x1dx">
  <label for="1d">1 day</label>
  </div>
  <div>
  <input type="checkbox" id="7d" name="xpercentagex" value="x7dx">
  <label for="7d">7 days</label>
  </div>
  <div>
  <input type="checkbox" id="30d" name="xpercentagex" value="x30dx">
  <label for="30d">30 days</label>
  </div>
  </fieldset>
  <br>
  <h2>Clock configuration</h2>
  <fieldset>
  <legend>Display time instead of crypto prices</legend>
  <div>
  <input type="checkbox" id="24h" name="xtimeformatx" value="x24hx">
  <label for="24h">24h format</label>
  </div>
  <div>
  <input type="checkbox" id="12h" name="xtimeformatx" value="x12hx">
  <label for="12h">12h format</label>
  </div>
  </fieldset>
  <br>
  <h2>Show custom text</h2>
  <label for="xcustomtextx">Type your text:</label>
  <input type="text" id="xcustomtextx" name="xcustomtextx"><br>
  <input type="hidden" id="helpvarcryptoticker" name="helpvarcryptoticker"><br>
  <input type="submit" value="Submit">
  </form></body>""" % (coinobject.coin, coinobject.exchange, coinobject.amount, coinobject.currency, coinobject.roundvar, coinobject.speed)
  return html

