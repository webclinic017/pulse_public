from ibapi.contract import Contract
from classes import App_1
from symbol_list import symbol,same_date

import threading, time, datetime
import numpy as np

np.set_printoptions(threshold=np. inf)
np.set_printoptions(formatter={'all': lambda x: str(x)})

# =======================================================================================
today=datetime.datetime.today()
# today=datetime.datetime.strptime("20220708_1610",'%Y%m%d_%H%M')

today_f=today.strftime(format='%Y%m%d_%H%M%S')
clientID=today.strftime(format='%f')

app = App_1()
app.connect('127.0.0.1', 7496, clientID)

time.sleep(2)

stock='meta'

# log=f"logs/{today_f}_1_short.txt"
# open(log, "x")

# store = f"sandbox/{contract.symbol.lower()}_1.csv"
# open(store, "x")

contract = Contract()
contract.symbol = stock.upper()
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"
# contract.primaryExchange='NASDAQ' #without this, META doesnt download or some bullshit downloads instead

i=0

api_thread = threading.Thread(target=app.run, daemon=True)
api_thread.start()

run_time=datetime.datetime.strptime("20190930_1610",'%Y%m%d_%H%M')
run_time = run_time.strftime("%Y%m%d 00:00:00")

app.reqHistoricalData(0, contract, run_time, "1 D", "1 min", "TRADES", 1, 1, False, [])
time.sleep(5)

if len(App_1.a1) > 0:

    a1 = np.array(App_1.a1, dtype=np.float_)
    print(a1)

#     with open(store, 'a') as o1:
#         np.savetxt(o1, a1, fmt='%s')
#     with open(log, 'a') as o2:
#         o2.write(App_1.log_error)
#         o2.write(f"\n{contract.symbol.lower()} {today_f}--TRUE\n\n")
#
# else:
#     with open(log, 'a') as o2:
#         o2.write(App_1.log_error)
#         o2.write(f"\n{contract.symbol.lower()} {today_f}--FALSE--EMPTY\n\n")

app.disconnect()
