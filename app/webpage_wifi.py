def web_page_wifi():
  html = """<!DOCTYPE html><html lang="de">
  <head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  </head>
  <body>
  <form action="/get">
  <h1>Wifi configuration</h1>
  <br>
  <a href= "mailto:support@mcmoe.de">contact support</a>
  <br>
  <br>
  <label for="ssid">SSID:</label>
  <input type="text" id="ssid" name="ssid"><br><br>
  <label for="password">Password:</label>
  <input type="password" id="password" name="password"><br><br>
  <input type="hidden" id="helpvarcryptoticker" name="helpvarcryptoticker"><br>
  <input type="submit" value="Submit">
  </form></body>"""
  return html
