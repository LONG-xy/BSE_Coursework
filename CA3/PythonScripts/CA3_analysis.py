from numpy.ma import mean
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy.stats as stats

# read csv
data = pd.read_csv('CA3/CA3_avg_balance.csv',header = None)

# describe the statistics of sample
data_PRSH=data.iloc[:,7]
data_ZIP=data.iloc[:,11]
list_to_tuple=list((zip(data_PRSH,data_ZIP)))
sample_df=pd.DataFrame(list_to_tuple,columns=['PRSH','ZIP'])
sample_df.describe()

PRSH_mean=np.mean(data_PRSH)
ZIP_mean=np.mean(data_ZIP)

# check normality and homoscedasticity
PRSH_norm_test = stats.normaltest(data_PRSH)
ZIP_norm_test = stats.normaltest(data_ZIP)
Homodasticity_test = stats.levene(data_PRSH,data_ZIP)
print(PRSH_norm_test,ZIP_norm_test,Homodasticity_test)

# boxplots
plt.figure(figsize=(5,5))
labels = ["PRSH",'ZIP']
plt.title('boxplots of PRSH and ZIP')
plt.boxplot([data_PRSH,data_ZIP],labels=labels, notch=True, showmeans=True)
plt.show()

# calculate confidence interval
CI1 = stats.t.interval(0.95, len(data_PRSH)-1, loc=np.mean(data_PRSH), scale=stats.sem(data_PRSH))
print(CI1)
CI2 = stats.t.interval(0.95, len(data_ZIP)-1, loc=np.mean(data_ZIP), scale=stats.sem(data_ZIP))
print(CI2)

# underlying ditribution
sns.histplot(data_PRSH,kde=True)
plt.xlabel('average profit per trader')
plt.title('histogram of PRSH')
plt.show()

sns.histplot(data_ZIP,kde=True)
plt.title('histogram of ZIP')
plt.xlabel('average profit per trader')
plt.show()

# confidence interval around mean
plt.figure(figsize=(5,5))
plt.title('confidence interval around mean')
plt.xlim(1, 3)

plt.vlines(x=1.5,ymin = CI1[0], ymax = CI1[1],label='PRSH',colors = 'blue')
plt.vlines(x=2,ymin = CI2[0], ymax = CI2[1],label='ZIP',colors = 'red')

plt.plot(1.5, CI1[0], marker = '_', markerfacecolor='blue')
plt.plot(1.5, CI1[1], marker = '_', markerfacecolor='blue')
plt.plot(1.5,PRSH_mean, marker = 'o', markerfacecolor='blue')

plt.plot(2, ZIP_mean, marker = 'o', markerfacecolor='red')
plt.plot(2, CI2[0], marker = '_', markerfacecolor='red')
plt.plot(2, CI2[1], marker = '_', markerfacecolor='red')

plt.xticks([])
plt.legend()
plt.text(1.4,63.5,'PRSH')
plt.text(2,63.5,'ZIP')
plt.show()

# hypothesis test
result = stats.mannwhitneyu(data_PRSH,data_ZIP,alternative='less')
print(result)


