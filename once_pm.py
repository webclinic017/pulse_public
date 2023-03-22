from ibapi.contract import Contract
from classes import App_1
from func import *
from symbol_list import *

import threading, time, datetime
import numpy as np

np.set_printoptions(threshold=np. inf)
np.set_printoptions(formatter={'all': lambda x: str(x)})
# ========================================================
today=datetime.datetime.today()

today_f=today.strftime(format='%Y%m%d_%H%M%S')
clientID=today.strftime(format='%f')

app = App_1()
app.connect('127.0.0.1', 7496, clientID)

time.sleep(2)
pf1=time.perf_counter()

stock='mrna'

contract = Contract()
contract.symbol = stock.upper()
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"

corr = f"sandbox/{contract.symbol.lower()}_1_corr.csv"
raw = f"sandbox/{contract.symbol.lower()}_1_raw.csv"

api_thread = threading.Thread(target=app.run, daemon=True)
api_thread.start()

# date1 = datetime.datetime.strftime(today, '%Y%m%d %H:%M:%S')
# date1 = datetime.datetime.strftime(today+datetime.timedelta(days=1), '%Y%m%d 00:00:00')
# date1 = datetime.datetime.strftime(today, '%Y%m%d 00:00:00')

#for ONE DAY ONLY, OTHERWISE PRE MARKET CANT NORMALIZE

run_time=datetime.datetime.strptime("20220930",'%Y%m%d')
run_time = run_time.strftime("%Y%m%d 20:10:00")

app.reqHistoricalData(0, contract, run_time, "1 D", "1 min", "TRADES", 0, 1, False, [])
# time.sleep(5)

ready = 0
v = 0
while ready == 0:
    for x in App_1.a1:
        if x[7] > 1600:
            ready = 1
            break
    time.sleep(0.1)
    print(v, end='\r')
    v += 1

if len(App_1.a1) > 0:
    a1 = np.array(App_1.a1, dtype=np.float_)
    # a2 = correct_1day(App_1.a1, t1)

    with open(raw, 'a') as o1:
        np.savetxt(o1, a1, fmt='%s')
    # with open(corr, 'a') as o2:
    #     np.savetxt(o2, a2, fmt='%s')

#     with open(log, 'a') as o2:
#         o2.write(App_1.log_error)
#         o2.write(f"\n{contract.symbol.lower()} {today_f}--TRUE\n\n")
#
# else:
#     with open(log, 'a') as o2:
#         o2.write(App_1.log_error)
#         o2.write(f"\n{contract.symbol.lower()} {today_f}--FALSE--EMPTY\n\n")

pf2=time.perf_counter()
print(pf2-pf1)

app.disconnect()
