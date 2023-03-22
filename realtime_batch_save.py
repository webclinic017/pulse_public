from ibapi.contract import Contract
from classes import App_realtime

import threading, time, datetime
import numpy as np
from symbol_list import *

np.set_printoptions(threshold=np. inf)
np.set_printoptions(formatter={'all': lambda x: str(x)})

# =====================================================
now=datetime.datetime.today().replace(microsecond=0)
clientID=datetime.datetime.today().strftime(format='%f')
print(clientID)
app = App_realtime()
app.connect('127.0.0.1', 7496, clientID)

time.sleep(2)

c1 = {x: [[],[]] for x in symbol}
times=[]

target=datetime.datetime.today().replace(hour=9,minute=35,second=10,microsecond=0)
# start=datetime.datetime.today().replace(hour=13,minute=55,second=30,microsecond=0)

print(target)

while now != target:
    now = datetime.datetime.today().replace(microsecond=0)
    print(f'waiting to launch {target-now}',end="\r")
    time.sleep(0.1)

i=0
n = 48

while i<78:

    t1 = time.perf_counter()

    api_thread = threading.Thread(target=app.run, daemon=True)
    api_thread.start()
    time.sleep(1)

    g = 0
    m=0

    while g < len(symbol):
        if m<n:
            if App_realtime.error_id in server_errors:
                print('server error ',App_realtime.error_id)
                g=0
                m=0
                n-=2

                App_realtime.a1=[]
                App_realtime.error_id=0

                api_thread = threading.Thread(target=app.run, daemon=True)
                api_thread.start()
                time.sleep(1)

            elif App_realtime.error_id in connect_errors:
                print('connect error ', App_realtime.error_id)
                g = 0
                m = 0

                App_realtime.a1 = []
                App_realtime.error_id = 0

                w1=0
                while App_realtime.error_id != 1102:
                    time.sleep(0.1)
                    print(f'waiting for connection to restore {w1}', end="\r")
                    w1+=1

                api_thread = threading.Thread(target=app.run, daemon=True)
                api_thread.start()
                time.sleep(1)

            else:
                contract = Contract()
                contract.symbol = symbol[g].upper()
                contract.secType = "STK"
                contract.exchange = "SMART"
                contract.currency = "USD"

                run_time = target.strftime("%Y%m%d %H:%M:00")

                app.reqHistoricalData(g, contract, run_time, "300 S", "5 mins", "TRADES", 0, 1, False, [])
                # print(App_realtime.error_id)
                g += 1
                m += 1

        else:
            time.sleep(2)
            m=0

    while len(App_realtime.a1)<len(symbol):
        time.sleep(0.1)

    if App_realtime.a1[-1][0][0]==len(symbol)-1:
        for r,x in enumerate(symbol):
            c1[x][0].append(App_realtime.a1[r][1])

            vwap = 0
            total_dollars = 0
            total_vlm = 0

            for y in c1[x][0]:  # one 5min candle
                total_vlm += y[4]
                total_dollars += (y[1] + y[2]) / 2 * y[4]
                vwap = round((total_dollars / total_vlm),2) #this is vwap value for 1 candle

            c1[x][1].append(vwap)
#######################################################################
        for a, b in c1.items():
            print(a)
            for c in b[0]:
                print(c)

        t2 = time.perf_counter()
        exec_time = round((t2 - t1), 2)
        print(exec_time)
        times.append([exec_time])

        target += datetime.timedelta(minutes=5)

        print(f'target {target}')

        App_realtime.a1 = []

        now = datetime.datetime.today().replace(microsecond=0)

        if target>now:

            while now != target:
                now = datetime.datetime.today().replace(microsecond=0)
                print(f'waiting for target time {target - now}', end="\r")
                time.sleep(0.1)

            i += 1

        else:
            i+=1
            time.sleep(2)


    else: #theoretically it will attempt to redownload the entire thing. hasnt happened yet, so not sure
        print('mismatch')
        App_realtime.a1 = []
        App_realtime.error_id=0

######################################################################
for a,b in c1.items():
    store = f"scan_storage/{a}_5.csv"
    open(store, "x")
    a1 = np.array(b[0], dtype=np.float_)
    with open(store, 'a') as o1:
        np.savetxt(o1, a1, fmt='%s')

store_times = f"scan_storage/times.csv"
open(store_times, "x")
a1 = np.array(times, dtype=np.float_)
with open(store_times, 'a') as o2:
    np.savetxt(o2, a1, fmt='%s')

app.disconnect()