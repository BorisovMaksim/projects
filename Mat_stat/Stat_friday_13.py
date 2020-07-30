import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import pandas as pd


a = pd.read_csv('https://stepik.org/media/attachments/lesson/40531/13_6', sep='\t',
                   header=None, names=['data_type', 'year_month', 'friday_6', 'friday_13','shop_name'])
average = np.mean(a["friday_13"]) # Выборочное среднее
med = np.median(a["friday_13"]) # Выборочная медиана
dis = np.mean(abs(a["friday_13"] - average) ** 2) # Выборочная дисперсия
diff = pd.DataFrame({"diff": a["friday_13"] - a["friday_6"]})
diff_average = np.mean(diff)
diff_kurt = stats.kurtosis(diff) # Выборочный коэффициент эксцесса
diff_asym = stats.skew(diff["diff"]) # Кэффициент ассиметрии

df = a.join(diff)
sns.set(style="whitegrid")
fig, axs = plt.subplots(ncols=3, nrows=2, figsize=(9,7))

ax = sns.boxplot(data=df, ax=axs[0][0])
sns.distplot(df['friday_13'],kde = False, ax=axs[1][0], bins=20)
sns.distplot(df['friday_6'],kde = False, ax=axs[1][1], bins=20)
sns.distplot(df['diff'],kde = False, ax=axs[1][2], bins=20)
axs[0][1].remove()
axs[0][2].remove()
fig.tight_layout()
fig.savefig('Friday_13')
plt.show()

