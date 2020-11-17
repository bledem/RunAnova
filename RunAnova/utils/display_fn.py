import matplotlib.pyplot as plt
import numpy as np

def create_color(treatments):
    cmap = plt.get_cmap('jet')
    colors = [cmap(i) for i in np.arange(0, 1, 1/len(treatments))]
    return colors