import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('https://stepik.org/media/attachments/lesson/40531/colleges.txt', sep='\t',
                 header=None, names=['School', 'School_Type', 'SAT', 'Acceptance', '$/Student',
                                     'Top 10%', "%PhD", 'Grad%']).drop(0, axis=0).astype({'SAT': 'int32', 'Acceptance'
: 'int32', '$/Student': 'int32', 'Top 10%': 'int32', '%PhD': 'int32', 'Grad%': 'int32'})

sns.set(style="whitegrid")
fig, axs = plt.subplots(ncols=3, nrows=4, figsize=(9, 7))
uni = df[df['School_Type'] == 'Univ']
art = df[df['School_Type'] == 'Lib Arts']
for i, j in enumerate(['SAT', 'Acceptance', '$/Student', 'Top 10%', '%PhD', 'Grad%']):
    plt.subplot(4, 3, i+1)
    sns.boxplot(uni[j])
    plt.subplot(4, 3, i + 7)
    sns.boxplot(art[j])

plt.show()

