from ibapi.contract import Contract

import threading, time, datetime
import numpy as np
from symbol_list import symbol
from func import *
from classes import App_1

np.set_printoptions(threshold=np. inf)
np.set_printoptions(formatter={'all': lambda x: str(x)})

# =======================================================================================
avg={}

for stock in symbol:
    l1 = np.genfromtxt(f'temp/{stock.lower()}_time_vlm_avg_5.csv').tolist()

    avg[stock] = l1

today=datetime.datetime.today()
clientID=today.strftime(format='%f')

app = App_1()
app.connect('127.0.0.1', 7496, clientID)

time.sleep(2)

while True:

    g=0
    today = datetime.datetime.today()

    while g < len(symbol):

        contract = Contract()
        contract.symbol = symbol[g].upper()
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"

        api_thread = threading.Thread(target=app.run, daemon=True)
        api_thread.start()

        run_time = today.strftime("%Y%m%d %H:%M:00")
        app.reqHistoricalData(g, contract, run_time, "300 S", "5 mins", "TRADES", 0, 1, False, [])

        while len(App_1.a1) ==0:
            time.sleep(0.1)

        a1=list(map(float, App_1.a1[0]))

        for x in avg[contract.symbol]:
            if x[0]==a1[7]:
                x.append(a1[4])
                # if x[1]>a1[4]:
                #     print(contract.symbol,a1[7])

        App_1.a1 = []
        g += 1
    #calculate

    for x, y in avg.items():
        print(x)
        for m in y:
            print(m)
        print('------------------')

    time.sleep(300)

app.disconnect()