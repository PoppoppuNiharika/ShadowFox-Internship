import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

data = np.array([[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]])

sns.heatmap(data, annot=True)

plt.title("Seaborn Heatmap")
plt.show()