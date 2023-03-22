from ibapi.contract import Contract
from classes import App_1
from symbol_list import download_symbols,t1
from func import *

import threading, time, datetime
import numpy as np

# =======================================================================================
today=datetime.datetime.today()

today_f=today.strftime(format='%Y%m%d_%H%M%S')
clientID=today.strftime(format='%f')

log=f"logs/{today_f}_1_get.txt"

app = App_1()
app.connect('127.0.0.1', 7496, clientID)

time.sleep(2)

g=0
while g < len(download_symbols):

    template = np.genfromtxt(f'purgatory/{download_symbols[g].lower()}_d.csv')

    contract = Contract()
    contract.symbol = download_symbols[g].upper()
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    store = f"purgatory/{contract.symbol.lower()}_1.csv"
    open(store, "x")

    i=0

    while i<len(template):

        api_thread = threading.Thread(target=app.run, daemon=True)
        api_thread.start()

        start_date = datetime.datetime.strptime(str(template[i, 5]), '%Y%m%d.0')

        ready = 0
        r=0
        times=[20,19,18,17,16]

        while ready==0:
            date1=start_date.strftime(format=f'%Y%m%d {times[r]}:10:00')

            app.reqHistoricalData(g, contract, date1, "1 D", "1 min", "TRADES", 0, 1, False, [])
            print(contract.symbol,date1)

            v=0
            while ready == 0:
                for x in App_1.a1:
                    if x[7] > 1600:
                        ready = 1
                        break #break is for for loop, not while loop
                time.sleep(0.1)
                print(v,end='\r')
                v+=1
                if v==300:
                    break

            r+=1

        if len(App_1.a1) > 0:
            a1 = correct_1day(App_1.a1, t1)
            # print(a1[0])
            with open(store, 'a') as o1:
                np.savetxt(o1, a1, fmt='%s')
            with open(log, 'a') as o2:
                o2.write(App_1.log_error)
                o2.write(f"\n{contract.symbol.lower()} {today_f}--TRUE\n\n")

        else:
            with open(log, 'a') as o2:
                o2.write(App_1.log_error)
                o2.write(f"\n{contract.symbol.lower()} {today_f}--FALSE--EMPTY\n\n")

        App_1.a1 = []
        App_1.log_error = ""
        i+=1

    g+=1

app.disconnect()
