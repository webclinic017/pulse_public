from ibapi.contract import Contract

import threading, time, datetime
import numpy as np

from symbol_list import maintain
from classes import App_d

np.set_printoptions(threshold=np. inf)
np.set_printoptions(formatter={'all': lambda x: str(x)})

# =======================================================================================
today=datetime.datetime.today()
# today=datetime.datetime.strptime("20221007_1610",'%Y%m%d_%H%M')

today_f=today.strftime(format='%Y%m%d_%H%M%S')
clientID=today.strftime(format='%f')

app = App_d()
app.connect('127.0.0.1', 7496, clientID)

time.sleep(2)

log=f"logs/{today_f}_d_append.txt"
open(log, "x")

g=0
while g < len(maintain):

    contract = Contract()
    contract.symbol = maintain[g].upper()
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    store = f"storage/{contract.symbol.lower()}_d.csv"

    api_thread = threading.Thread(target=app.run, daemon=True)
    api_thread.start()

    app.reqHistoricalData(g, contract, "", "1 D", "1 day", "TRADES", 1, 1, False, [])
    print(contract.symbol)

    v = 0
    while len(App_d.a1) == 0:
        time.sleep(0.1)
        print(v, end='\r')
        v += 1

    a1 = np.array(App_d.a1, dtype=np.float_)

    if a1.size>0:
        if str(a1[0, 5]) == today.strftime(format='%Y%m%d.0'):
            # print(a1[0])
            with open(store, 'a') as o1:
                np.savetxt(o1, a1, fmt='%s')
            with open(log, 'a') as o2:
                o2.write(App_d.log_error)
                o2.write(f"\n{contract.symbol.lower()} {today_f}--TRUE\n\n")

        else:
            with open(log, 'a') as o2:
                o2.write(App_d.log_error)
                o2.write(f"\n{contract.symbol.lower()} {today_f}--FALSE--DATE MISMATCH\n\n")
            break

    else:
        with open(log, 'a') as o2:
            o2.write(App_d.log_error)
            o2.write(f"\n{contract.symbol.lower()} {today_f}--FALSE--EMPTY\n\n")

    App_d.a1 = []
    App_d.log_error = ""
    g += 1

app.disconnect()