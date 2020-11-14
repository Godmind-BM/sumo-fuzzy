import numpy as np 
import matplotlib.pyplot as plt
import os
from typing import List
from app import Config

class Visualizer(object):
    def __init__(self, dpi=96):
        super().__init__()
        self.dpi = dpi

    def plot_data(self, labels:List[tuple], datas: List[list], files: List[list], color='#696969') -> None:
        for data, filename, label in zip(datas, files, labels):
            min_val = np.min(data)
            max_val = np.max(data)
            plt.rcParams.update({'font.size': 24})  # set font size bigger
            fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[15, 7])
            plt.plot(data, 'o-', color=color)
            # plt.xlabel(label[0])
            # plt.ylabel(label[1])
            plt.margins(0)
            fig.set_size_inches(20, 11.25)
            ticks = ax.get_xticks()
            ax.grid(True)
            ax.spines['bottom'].set_position('zero')
            ax.spines['left'].set_position('zero')
            ax.set_xlim(left=0)
            ax.set_ylim(bottom=0)
            label_config = {
                'fontsize': '18',
                'fontname': 'serif',
                'color': '#696969',
                'labelpad': 5,
            }
            ax.set_xlabel(label[0], **label_config)
            ax.set_ylabel(label[1], **label_config)
            title_config = {
                'size': 24,
                'color': '#696969',
                'family': 'serif',
                'pad': 20,
            }
            # print(ax.get_xscale())
            fig.savefig(os.path.join(Config.PLOTS_URI, 'plot-' + filename + '.png'), dpi=self.dpi)
            plt.close('all')

    def __repr__(self):
        return f'{self.__class__.__name__}({self.dpi})'