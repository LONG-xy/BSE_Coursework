import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy.stats as st

# read csv
datafile1 = 'CA3/CA3_avg_balance.csv'
datafile2 = 'CA3/CA3_avg_balance.csv'

data = pd.read_csv(datafile1,header = None)

box_1=data.iloc[:,7]
box_2=data.iloc[:,11]
labels = ["PRSH",'ZIP']

# analyse gifure

plt.figure(figsize=(10,5))#设置画布的尺寸
plt.title('Examples of boxplot',fontsize=20)#标题，并设定字号大小

plt.boxplot([box_1,box_2],labels=labels, notch=True, showmeans=True, meanline=True)

plt.show()#显示图像


mean1 = np.mean(box_1)
mean2 = np.mean(box_2)
sd1 = np.std(box_1)
sd2 = np.std(box_2)
se1 = sd1/np.sqrt(len(box_1))
se2 = sd2/np.sqrt(len(box_2))
a=st.sem(box_1)
print(a,se1)

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

result = st.mannwhitneyu(box_1,box_2,alternative='less')
print(result)


sns.displot(box_1,kde=True)
plt.show()

sns.displot(box_2,kde=True)
plt.show()


alpha = 0.05
sample_size = 50
