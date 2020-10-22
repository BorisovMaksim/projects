from scipy import stats
import numpy as np
import pandas as pd

df = pd.read_csv("https://stepik.org/media/attachments/lesson/26278/car_regr.txt", sep='\t')
Z = [int(x == "MT") for x in df.auto]
A = np.array([np.full(44, 1), df.year, df.mileage, Z]).transpose()
E = np.linalg.inv(A.transpose() @ A) @ A.transpose() @ df.price
a = 0.05
n = df.year.size
k = 3
# Остатки
E_o = np.array([df.price[i] - E[0] - E[1]*df.year[i] - E[2]*df.mileage[i] - E[3]*Z[i] for i in range(n)])
S = np.sqrt((E_o.transpose() @ E_o)/(n-k-1))
# Точность интервала
accur = stats.t(n - k - 1).ppf(1 - a/2)*S*np.sqrt(np.linalg.inv(A.transpose() @ A)[2][2])
RSS = E_o.transpose() @ E_o
R_2 = 1 - RSS/(np.sum([(df.price[i] - df.price.mean())**2 for i in range(n)]))
q_f = stats.f(k, n-k-1).ppf(1 - 0.05)
z_v = ((np.sum([(df.price[i] - df.price.mean())**2 for i in range(n)]) - RSS)/k)/(RSS/(n-k-1))
# Стандартизированный остаток
stand_rem = E_o[1]/(S * np.sqrt(1 - (A @ np.linalg.inv(A.transpose() @ A) @ A.transpose())[1][1]))

print(round(R_2, 2), q_f, z_v)
