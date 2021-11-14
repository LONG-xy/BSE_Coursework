# Initial Setup
# Import all the libraries we need


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
import math
import seaborn as sns
import random
import scipy.stats as st
from scipy.stats import mannwhitneyu
from BSE import market_session

# do n runs experiment   
def n_runs(n, trial_id, start_time, end_time, traders_spec, order_sched):

    for i in range(n):
        trialId = trial_id 
        tdump = open(trialId + '_avg_balance.csv','a')
        market_session(trialId, start_time, end_time, traders_spec, order_sched, tdump, False, False) 
        tdump.close()
    

# !!! Don't use on it's own   
def getorderprice(i, sched, n, mode):
    pmin = min(sched[0][0], sched[0][1])
    pmax = max(sched[0][0], sched[0][1])
    prange = pmax - pmin
    stepsize = prange / (n - 1)
    halfstep = round(stepsize / 2.0)

    if mode == 'fixed':
        orderprice = pmin + int(i * stepsize)
    elif mode == 'jittered':
        orderprice = pmin + int(i * stepsize) + random.randint(-halfstep, halfstep)
    elif mode == 'random':
        if len(sched) > 1:
            # more than one schedule: choose one equiprobably
            s = random.randint(0, len(sched) - 1)
            pmin = min(sched[s][0], sched[s][1])
            pmax = max(sched[s][0], sched[s][1])
        orderprice = random.randint(pmin, pmax)
    return orderprice    

# plot sorted trades, useful is some situations - won't be used in this worksheet
def in_order_plot(trial_id):
    prices_fname = trial_id + '_transactions.csv'
    y = np.empty(0)
    with open(prices_fname, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            price = float(row[2])
            y = np.append(y,price)
    y = np.sort(y)
    x = list(range(len(y)))

    plt.plot(x, y, 'x', color='black')   


# schedule_offsetfn returns time-dependent offset, to be added to schedule prices
def schedule_offsetfn(t):
    pi2 = math.pi * 2
    c = math.pi * 3000
    wavelength = t / c
    gradient = 100 * t / (c / pi2)
    amplitude = 100 * t / (c / pi2)
    offset = gradient + amplitude * math.sin(wavelength * t)
    return int(round(offset, 0))

# 
def offset_t(t):
    return int(round(t,0))



# produce data

sellers_spec = [('ZIP', 15),('PRSH', 15)]
buyers_spec = sellers_spec
traders_spec = {'sellers':sellers_spec, 'buyers':buyers_spec}

range1 = (50, 100, schedule_offsetfn)
range2 = (150, 200, offset_t)

start_time = 0
change1_time = 60 * 3
change2_time = 60 * 7
end_time = 60 * 10
supply_schedule = [{'from': start_time, 'to': change1_time, 'ranges': [range1], 'stepmode': 'fixed'},
                   {'from': change1_time, 'to': change2_time, 'ranges': [range2], 'stepmode': 'fixed'},
                   {'from': change2_time, 'to': end_time, 'ranges': [range1], 'stepmode': 'fixed'}]
demand_schedule = supply_schedule

order_interval = 15
order_sched = {'sup': supply_schedule, 'dem': demand_schedule,
               'interval': order_interval, 'timemode': 'periodic'}

trial_id = 'CA3'
#tdump = open('CA3_avg_balance.csv','w')

n_runs(500, trial_id, start_time, end_time, traders_spec, order_sched)

                   
