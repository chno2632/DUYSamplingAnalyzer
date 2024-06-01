from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

x_1 = np.linspace(0,5,10)
y_1 = x_1**2
#plt.plot = (x_1, y_1)
plt.title("Days Squared Chart")
plt.plot(x_1, y_1, color='r', linestyle='--', marker='.')
plt.show()


