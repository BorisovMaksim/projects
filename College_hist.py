import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import pandas as pd
import math

df = pd.read_csv('https://stepik.org/media/attachments/lesson/40531/colleges.txt', sep='\t',
                 header=None, names=['School', 'School_Type', 'SAT', 'Acceptance', '$/Student',
                                     'Top 10%', "%PhD", 'Grad%']).drop(0, axis=0).astype({'SAT': 'int32', 'Acceptance'
: 'int32', '$/Student': 'int32', 'Top 10%': 'int32', '%PhD': 'int32', 'Grad%': 'int32'})

uni = df[df['School_Type'] == 'Univ']
art = df[df['School_Type'] == 'Lib Arts']

plt.figure(figsize=(17,11))
for i, j in enumerate(['SAT', 'Acceptance', '$/Student', 'Top 10%', '%PhD', 'Grad%']):
    plt.subplot(2, 3, i+1)
    sns.distplot(uni[j], label='uni')
    sns.distplot(art[j], label='art')
    plt.legend()
plt.show()

print(np.mean(art["SAT"]))
print(df["Acceptance"].quantile(0.75))
print(df.iloc[[np.argmax(df["$/Student"])]]["School"])
