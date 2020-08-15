import numpy as np
import pandas as pd
from scipy import stats

df = pd.read_csv("https://stepik.org/media/attachments/lesson/28461/weights.txt", sep='\t')
n = df.race.size
k = 4
Y = df.weight
A = np.array([np.full(n, 1), df.race, df.educ, df.smoke, df.preg]).transpose()
E = np.linalg.inv(A.transpose() @ A) @ A.transpose() @ Y
E_o = np.array(
    [Y[i] - E[0] - E[1] * df.race[i] - E[2] * df.educ[i] - E[3] * df.smoke[i] - E[4] * df.preg[i] for i in range(n)])
RSS = E_o.transpose() @ E_o
S = np.sqrt(RSS / (n - k - 1))
accur = stats.t(n - k - 1).ppf(1 - 0.05 / 2) * S * np.sqrt(np.linalg.inv(A.transpose() @ A)[4][4])
R_2 = 1 - RSS / (np.sum([(Y[i] - Y.mean()) ** 2 for i in range(n)]))

q_f = stats.f(k, n - k - 1).ppf(1 - 0.05)
z_v = ((np.sum([(Y[i] - Y.mean()) ** 2 for i in range(n)]) - RSS) / k) / (RSS / (n - k - 1))
p_val = 1 - stats.f(k, n - k - 1).cdf(z_v)
akaike = 2*k + n*(np.log(RSS/n) + 1)
t_b_1 = "Раса значима" if np.abs(E[1] / (S * np.sqrt(np.linalg.inv(A.transpose() @ A)[1][1]))) > stats.t(n - k - 1).ppf(
    1 - 0.05 / 2) else "Раса не значима"
t_b_2 = "Образование значимо" if np.abs(E[2] / (S * np.sqrt(np.linalg.inv(A.transpose() @ A)[2][2]))) > stats.t(
    n - k - 1).ppf(1 - 0.05 / 2) else "Образование не значимо"
t_b_3 = "Курение значимо" if np.abs(E[3] / (S * np.sqrt(np.linalg.inv(A.transpose() @ A)[3][3]))) > stats.t(
    n - k - 1).ppf(1 - 0.05 / 2) else "Курение не значимо"
t_b_4 = "Срок беременности значим" if np.abs(E[4] / (S * np.sqrt(np.linalg.inv(A.transpose() @ A)[4][4]))) > stats.t(
    n - k - 1).ppf(1 - 0.05 / 2) else "Срок беременности не значим"
print("Была построена множественная линейная регрессия с целью определения значимости веса ребенка от \n расы, "
      "образования, курения и срока беременности. Вывод: "
      "","\n", t_b_1, "\n", t_b_2, "\n", t_b_3, "\n", t_b_4, "\n")


