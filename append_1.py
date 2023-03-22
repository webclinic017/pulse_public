from ibapi.contract import Contract

import threading, time, datetime
import numpy as np

from symbol_list import maintain,t1
from classes import App_1
from func import correct_1day

np.set_printoptions(threshold=np. inf)
np.set_printoptions(formatter={'all': lambda x: str(x)})

# =======================================================================================
today=datetime.datetime.today()
# today=datetime.datetime.strptime("20221007_1610",'%Y%m%d_%H%M')

today_f=today.strftime(format='%Y%m%d_%H%M%S')
clientID=today.strftime(format='%f')

app = App_1()
app.connect('127.0.0.1', 7496, clientID)

time.sleep(2)

log=f"logs/{today_f}_1_append.txt"
open(log, "x")

g=0
while g < len(maintain):

    contract = Contract()
    contract.symbol = maintain[g].upper()
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    store = f"storage/{contract.symbol.lower()}_1.csv"

    api_thread = threading.Thread(target=app.run, daemon=True)
    api_thread.start()

    app.reqHistoricalData(g, contract, "", "1 D", "1 min", "TRADES", 0, 1, False, [])
    print(contract.symbol)
    v=0
    ready=0
    while ready == 0:
        for x in App_1.a1:
            if x[7] > 1600:
                ready = 1
                break  # break is for for loop, not while loop
        time.sleep(0.1)
        print(v, end='\r')
        v += 1

    if len(App_1.a1) > 0:
        a1 = correct_1day(App_1.a1,t1)
        if str(a1[0, 5]) == today.strftime(format='%Y%m%d.0'):
            # print(a1[0])
            with open(store, 'a') as o1:
                np.savetxt(o1, a1, fmt='%s')
            with open(log, 'a') as o2:
                o2.write(App_1.log_error)
                o2.write(f"\n{contract.symbol.lower()} {today_f}--TRUE\n\n")

        else:
            with open(log, 'a') as o2:
                o2.write(App_1.log_error)
                o2.write(f"\n{contract.symbol.lower()} {today_f}--FALSE--DATE MISMATCH\n\n")
            break

    else:
        with open(log, 'a') as o2:
            o2.write(App_1.log_error)
            o2.write(f"\n{contract.symbol.lower()} {today_f}--FALSE--EMPTY\n\n")

    App_1.a1 = []
    App_1.log_error=""
    g += 1

app.disconnect()