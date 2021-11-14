import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy.stats as st

# read csv
data = pd.read_csv('CA3/CA3_avg_balance.csv',header = None)
data_PRSH=data.iloc[:,7]
data_ZIP=data.iloc[:,11]

# box plot
plt.figure(figsize=(5,5))
labels = ["PRSH",'ZIP']
plt.title('Boxplot',fontsize=20)
plt.boxplot([data_PRSH,data_ZIP],labels=labels, notch=True, showmeans=True, meanline=True)
plt.show()

#calculate confidence interval
CI1 = st.t.interval(0.95, len(data_PRSH)-1, loc=np.mean(data_PRSH), scale=st.sem(data_PRSH))
print(CI1)

CI2 = st.t.interval(0.95, len(data_ZIP)-1, loc=np.mean(data_ZIP), scale=st.sem(data_ZIP))
print(CI2)

# check underlying ditribution
sns.displot(data_PRSH,kde=True)
plt.title('displot of PRSH')
plt.show()

sns.displot(data_ZIP,kde=True)
plt.title('displot of ZIP')
plt.show()

# confidence interval around mean plot
plt.title('Confidence Interval around mean')
plt.xlim(1, 3)

plt.vlines(x=1.5,ymin = CI1[0], ymax = CI1[1],label='PRSH',colors = 'blue')
plt.vlines(x=2,ymin = CI2[0], ymax = CI2[1],label='ZIP',colors = 'red')

mean1=np.mean(data_PRSH)
mean2=np.mean(data_ZIP)

plt.plot(1.5, CI1[0], marker = '_', markerfacecolor='blue')
plt.plot(1.5, CI1[1], marker = '_', markerfacecolor='blue')
plt.plot(1.5,mean1, marker = 'o', markerfacecolor='blue')

plt.plot(2, mean2, marker = 'o', markerfacecolor='red')
plt.plot(2, CI2[0], marker = '_', markerfacecolor='red')
plt.plot(2, CI2[1], marker = '_', markerfacecolor='red')

plt.xticks([])
plt.legend()
plt.text(1.4,59.5,'PRSH')
plt.text(2,60,'ZIP')
plt.show()

 #hypothesis test
result = st.mannwhitneyu(data_PRSH,data_ZIP,alternative='less')
print(result)


