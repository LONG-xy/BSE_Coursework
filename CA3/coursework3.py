# Initial Setup
# Import all the libraries we need


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
import math 
import random
import scipy.stats as st
from scipy.stats import mannwhitneyu
from BSE import market_session

# The next are helper functions that you will use later, if they don't make 
# much sense now, don't worry too much about it they will become clearer later:

# Use this to plot trades of a single experiment
def plot_trades(trial_id):
    prices_fname = trial_id + '_transactions.csv'
    x = np.empty(0)
    y = np.empty(0)
    with open(prices_fname, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            time = float(row[1])
            price = float(row[2])
            x = np.append(x,time)
            y = np.append(y,price)

    plt.plot(x, y, 'x', color='black') 

# do n runs experiment   
def n_runs(n, trial_id, start_time, end_time, traders_spec, order_sched):
    x = np.empty(0)
    y = np.empty(0)

    for i in range(n):
        trialId = trial_id 
        tdump = open(trialId + '_avg_balance.csv','a')

        market_session(trialId, start_time, end_time, traders_spec, order_sched, tdump, False, False)
        
        tdump.close()
    
def n_runs_plot_Modify(n, trial_id, start_time, end_time, traders_spec, order_sched):
    x = np.empty(0)
    y = np.empty(0)

    for i in range(n):
        trialId = trial_id 
        market_session(trialId, start_time, end_time, traders_spec, order_sched, tdump, True, False)

        with open(trialId + '_transactions.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                time = float(row[1])
                price = float(row[2])
                x = np.append(x,time)
                y = np.append(y,price)

    plt.plot(x, y, 'x', color='black');



# Use this to run an experiment n times and plot all trades
def n_runs_plot(n, trial_id, start_time, end_time, traders_spec, order_sched):
    x = np.empty(0)
    y = np.empty(0)

    for i in range(n):
        trialId = trial_id + '_' + str(i)
        tdump = open(trialId + '_avg_balance.csv','w')

        market_session(trialId, start_time, end_time, traders_spec, order_sched, tdump, True, False)
        
        tdump.close()

        with open(trialId + '_transactions.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                time = float(row[1])
                price = float(row[2])
                x = np.append(x,time)
                y = np.append(y,price)

    plt.plot(x, y, 'x', color='black');

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

# !!! Don't use on it's own
def make_supply_demand_plot(bids, asks):
    # total volume up to current order
    volS = 0
    volB = 0

    fig, ax = plt.subplots()
    plt.ylabel('Price')
    plt.xlabel('Quantity')
    
    pr = 0
    for b in bids:
        if pr != 0:
            # vertical line
            ax.plot([volB,volB], [pr,b], 'r-')
        # horizontal lines
        line, = ax.plot([volB,volB+1], [b,b], 'r-')
        volB += 1
        pr = b
    if bids:
        line.set_label('Demand')
        
    pr = 0
    for s in asks:
        if pr != 0:
            # vertical line
            ax.plot([volS,volS], [pr,s], 'b-')
        # horizontal lines
        line, = ax.plot([volS,volS+1], [s,s], 'b-')
        volS += 1
        pr = s
    if asks:
        line.set_label('Supply')
        
    if bids or asks:
        plt.legend()
    plt.show()

# Use this to plot supply and demand curves from supply and demand ranges and stepmode
def sup_dem(seller_num, sup_ranges, buyer_num, dem_ranges, stepmode):
    asks = []
    for s in range(seller_num):
        asks.append(getorderprice(s, sup_ranges, seller_num, stepmode))
    asks.sort()
    bids = []
    for b in range(buyer_num):
        bids.append(getorderprice(b, dem_ranges, buyer_num, stepmode))
    bids.sort()
    bids.reverse()
    
    make_supply_demand_plot(bids, asks) 

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

# produce data

# read csv
datafile1 = 'SolutionTest/test_7_avg_balance.csv'
datafile2 = 'SolutionTest/test_7_avg_balance.csv'

data1 = pd.read_csv(datafile1,header = None)
data2 = pd.read_csv(datafile2,header = None)

box_1=data1.iloc[:,7]
box_2=data2.iloc[:,11]
labels = ["PRSH",'ZIP']

# analyse gifure
'''
plt.figure(figsize=(10,5))#设置画布的尺寸
plt.title('Examples of boxplot',fontsize=20)#标题，并设定字号大小

plt.boxplot([box_1,box_2],labels=labels, notch=True, showmeans=True, meanline=True)

plt.show()#显示图像
'''

mean1 = np.mean(box_1)
mean2 = np.mean(box_2)
sd1 = np.std(box_1)
sd2 = np.std(box_2)
se1 = sd1/np.sqrt(len(box_1))
se2 = sd2/np.sqrt(len(box_2))

CI1 = st.t.interval(0.95, len(box_1)-1, loc=np.mean(box_1), scale=st.sem(box_1))
print(CI1)

CI2 = st.t.interval(0.95, len(box_2)-1, loc=np.mean(box_2), scale=st.sem(box_2))
print(CI2)

plt.figure(figsize=(5,5))#设置画布的尺寸
plt.title('Confidence Interval Test')

plt.xlim(1, 3)

plt.vlines(x=1.5,ymin = CI1[0], ymax = CI1[1],label='PRSH',colors = 'blue')

plt.vlines(x=2,ymin = CI2[0], ymax = CI2[1],label='ZIP',colors = 'red')

plt.plot(1.5, CI1[0], marker = '_', markerfacecolor='blue')
plt.plot(1.5, CI1[1], marker = '_', markerfacecolor='blue')
plt.plot(1.5, mean1, marker = 'o', markerfacecolor='blue')

plt.plot(2, mean2, marker = 'o', markerfacecolor='red')
plt.plot(2, CI2[0], marker = '_', markerfacecolor='red')
plt.plot(2, CI2[1], marker = '_', markerfacecolor='red')


plt.xticks([])
plt.legend()
plt.text(1.4,59.5,'PRSH')
plt.text(2,60,'ZIP')

plt.ylabel('Condidence interval of the mean')
plt.show()

result = mannwhitneyu(box_1,box_2,alternative='less')
print(result)


