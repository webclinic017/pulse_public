import numpy as np,time,datetime
from func import *

np. set_printoptions(threshold=np. inf)
np.set_printoptions(formatter={'all': lambda x: str(x)})
t1=time.perf_counter()

stock="spy"

l1 = np.genfromtxt(f'storage/{stock}_d.csv')

print(check_daily(l1))