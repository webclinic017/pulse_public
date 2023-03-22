import numpy as np, time, datetime, os
from func import *
from conditions import *

np.set_printoptions(threshold=np.inf)
np.set_printoptions(formatter={'all': lambda x: str(x)})

stock="spy"

l1 = np.genfromtxt(f'storage/{stock.lower()}_1.csv')
l1=ar_separate_RTH_split(l1)

prev_close=0

for day in l1:
    if day_open(day)<prev_close*0.99 and day_low(day)==low_before(day,1100) and day_year(day,2022):
        print(day_date(day),
              round((day_open(day)*100/prev_close-100),2)
              )
    prev_close=day_close(day)


# for day in l1:
#     if day_open(day)<prev_close*0.99 and day_low(day)==low_before(day,1100) and :
#         print(day_date(day),
#               round((day_open(day)*100/prev_close-100),2)
#               )
#     prev_close=day_close(day)