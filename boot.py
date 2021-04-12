import esp
esp.osdebug(None)
# This file is executed on every boot (including wake-boot from deepsleep)

#import esp

#esp.osdebug(None)

#import uos, machine

#uos.dupterm(None, 1) # disable REPL on UART(0)

import gc

#import webrepl

#webrepl.start()

#Set reset pin
#rst = Pin(25, Pin.OUT)
#configdelete = Pin(4, Pin.IN, Pin.PULL_UP)

gc.collect()















