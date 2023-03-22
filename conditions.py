import numpy as np

def hod_after(a,time:int):
    '''
    inclusive
    '''
    pos = np.argwhere(a[:,7] == time)[0, 0]
    return np.max(a[pos:,1])==np.max(a[:,1])

def hod_before(a,time:int):
    '''
    inclusive
    '''
    pos = np.argwhere(a[:,7] == time)[0, 0]
    return np.max(a[:pos+1,1])==np.max(a[:,1])

def hod_between(a,time1:int,time2:int):
    '''
    inclusive
    '''
    pos1 = np.argwhere(a[:,7] == time1)[0, 0]
    pos2 = np.argwhere(a[:, 7] == time2)[0, 0]
    return np.max(a[pos1:pos2+1,1])==np.max(a[:,1])

def hod_at(a,time:int):
    '''
    inclusive
    '''
    pos = np.argwhere(a[:,7] == time)[0, 0]
    return a[pos,1]==np.max(a[:,1])

def lod_after(a,time:int):
    '''
    inclusive
    '''
    pos = np.argwhere(a[:,7] == time)[0, 0]
    return np.min(a[pos:,2])==np.min(a[:,2])

def lod_before(a,time:int):
    '''
    inclusive
    '''
    pos = np.argwhere(a[:,7] == time)[0, 0]
    return np.min(a[:pos+1,2])==np.min(a[:,2])

def lod_between(a,time1:int,time2:int):
    '''
    inclusive
    '''
    pos1 = np.argwhere(a[:,7] == time1)[0, 0]
    pos2 = np.argwhere(a[:, 7] == time2)[0, 0]
    return np.min(a[pos1:pos2+1,2])==np.min(a[:,2])

def lod_at(a,time:int):
    '''
    inclusive
    '''
    pos = np.argwhere(a[:,7] == time)[0, 0]
    return a[pos,2]==np.min(a[:,2])

def high_after(a, time:int):
    '''
    inclusive
    '''
    pos = np.argwhere(a[:,7] == time)[0, 0]
    return np.max(a[pos:,1])

def high_before(a, time:int):
    '''
    inclusive
    '''
    pos = np.argwhere(a[:,7] == time)[0, 0]
    return np.max(a[:pos+1,1])

def high_between(a, time1:int, time2:int):
    '''
    inclusive
    '''
    pos1 = np.argwhere(a[:,7] == time1)[0, 0]
    pos2 = np.argwhere(a[:,7] == time2)[0, 0]
    return np.max(a[pos1:pos2+1,1])

def high_at(a, time:int):
    '''
    inclusive
    '''
    pos = np.argwhere(a[:,7] == time)[0, 0]
    return a[pos,1]

def low_after(a, time:int):
    '''
    inclusive
    '''
    pos = np.argwhere(a[:,7] == time)[0, 0]
    return np.min(a[pos:,2])

def low_before(a, time:int):
    '''
    inclusive
    '''
    pos = np.argwhere(a[:,7] == time)[0, 0]
    return np.min(a[:pos+1,2])

def low_between(a, time1:int, time2:int):
    '''
    inclusive
    '''
    pos1 = np.argwhere(a[:,7] == time1)[0, 0]
    pos2 = np.argwhere(a[:, 7] == time2)[0, 0]
    return np.min(a[pos1:pos2+1,2])

def low_at(a, time:int):
    '''
    inclusive
    '''
    pos = np.argwhere(a[:,7] == time)[0, 0]
    return a[pos,2]

def range_before(a,time:int):
    pos = np.argwhere(a[:,7] == time)[0, 0]
    max=np.max(a[:pos+1,1])
    min=np.min(a[:pos+1,2])
    return max-min

def range_after(a,time:int):
    pos = np.argwhere(a[:,7] == time)[0, 0]
    max=np.max(a[pos:,1])
    min=np.min(a[pos:,2])
    return max-min

def range_between(a, time1:int, time2:int):
    pos1 = np.argwhere(a[:, 7] == time1)[0, 0]
    pos2 = np.argwhere(a[:, 7] == time2)[0, 0]
    max=np.max(a[pos1:pos2+1,1])
    min=np.min(a[pos1:pos2+1,2])
    return max-min

def day_open(a):
    return a[0,0]

def day_close(a):
    return a[-1,3]

def day_high(a):
    return np.max(a[:,1])

def day_low(a):
    return np.min(a[:,2])

def day_date(a):
    return a[0,5]

def day_year(a,year:int):
    return day_date(a)//10000==year

def candle_open(a):
    return a[0]

def candle_close(a):
    return a[3]

def candle_high(a):
    return a[1]

def candle_low(a):
    return a[2]

def candle_date(a):
    return a[5]

def candle_time(a):
    return a[7]



