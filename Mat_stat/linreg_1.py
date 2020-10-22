from scipy import stats
import numpy as np
import pandas as pd

df = pd.read_csv("https://stepik.org/media/attachments/lesson/26278/car_regr.txt", sep='\t')
Y = df.price
reg_2 = stats.linregress(df.year, Y)
b_1 = reg_2[0]
b_0 = reg_2[1]
e = round(Y[0] - b_0 - b_1 * df.year[0], 2)    # Остаточная сумма квадратов
RSS = np.sum([(Y[i] - b_0 - b_1 * df.year[i]) ** 2 for i in range(Y.size)])
S = np.sqrt(RSS / (Y.size - 2))    # Оценка дисперсии
accur = stats.t(Y.size - 2).ppf(1 - 0.05 / 2) * S * np.sqrt(1 / (Y.size * np.var(df.year)))    # Точность доверительного интервала
pred_2012 = b_0 + b_1 * 2012    # Предсказание стоимости
z = (pred_2012 - 290) / (S * np.sqrt((1 + ((2012 - (np.mean(df.year))) ** 2) / np.var(df.year)) / Y.size))
pred_less = 1 - stats.t(Y.size - 2).cdf(z)    # Вероятность того, что стоимость будет меньше 290

