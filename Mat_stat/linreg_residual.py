import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


Y = np.array([4.7, 8.9, 6.2, 7.8, 8.1, 11.7, 7.2, 15.8, 1.1, 6.8, 9.1, 4.6, 21.5, 7.6, 6.2, 13.6, 30.1, 25.5, -0.1])
X = np.array([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0])
b_0, b_1 = 4.66, 1.03
n = Y.size
k = 1
A = np.array([np.full(n, 1), X]).transpose()
Y_difference = np.array([Y[i] - b_0 - b_1*X[i] for i in range(n)])
RSS = Y_difference.transpose() @ Y_difference
S = np.sqrt(RSS/(n-k-1))
h = A @ np.linalg.inv(A.transpose() @ A) @ A.transpose()
D = [Y_difference[i]/(S*np.sqrt(1 - h[i][i])) for i in range(n)]



sns.set(style="whitegrid")
fig, axs = plt.subplots(ncols=3, nrows=2, figsize=(10, 6))

axs[0][0].plot(Y_difference, D, color='r')
axs[0][0].set_xlabel("y_diff")
axs[0][0].set_ylabel("d")
percentile_theoretical = np.percentile(np.sort(Y_difference)[:-1], 100*np.linspace(1/n, (n-1)/n, n-1))
axs[0][1].plot(np.sort(Y_difference)[:-1], percentile_theoretical)
axs[0][1].set_xlabel("y_diff")
axs[0][1].set_ylabel("percentile_theoretical")
axs[0][2].plot(range(n), D, color='g')
axs[0][2].set_xlabel("num")
axs[0][2].set_ylabel("d")

axs[1][0].plot(X, D, color='r')
axs[1][0].set_xlabel("X")
axs[1][0].set_ylabel("d")

axs[1][1].plot(Y, D, color='r')
axs[1][1].set_xlabel("Y")
axs[1][1].set_ylabel("d")

plt.show()
