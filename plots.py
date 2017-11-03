'''
Make an unreasonably large number of plots.
'''

import math
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = "Helvetica"

def plot_page(sp, other_sp, data):
    fig = plt.figure()
    n = int(math.ceil(np.sqrt(len(other_sp))))
    x = data[sp]
    x_err = data[sp+'_err']
    for i,sp2 in enumerate(other_sp):
        ax = fig.add_subplot(n, n, i+1)
        y = data[sp2]
        y_err = data[sp2+'_err']
        ax.errorbar(x, y, xerr=x_err, yerr=y_err, fmt='o', c='black', ecolor='black', ms=3, elinewidth=0.6)
        ax.set_ylabel('['+sp2+'/Fe]', fontsize=10)
        ax.set_xlabel('['+sp+'/Fe]', fontsize=10)
        ax.tick_params(length=5, width=0.8, labelsize=7, which='major', pad=2)
        ax.tick_params(length=3, width=0.6, which='minor')
        ax.set_xticks(np.arange(-0.2,0.5,0.2))
        ax.set_xticks(np.arange(-0.2,0.5,0.05), minor=True)
        ax.set_yticks(np.arange(-0.2,0.5,0.2))
        ax.set_yticks(np.arange(-0.2,0.5,0.05), minor=True)
        #if (i % n) != 0:
        #    ax.set_yticklabels('',visible=False)

        if sp2 not in other_sp[-n:]:
            ax.set_xticklabels('',visible=False)
    fig.subplots_adjust(hspace=.05, wspace=.5)
    return fig
    

if __name__ == "__main__":
    from astropy.table import Table
    data = Table.read('star_data.fits', format='fits')
    
    sp_names = np.asarray(['CI', 'CH', 'OI', 'NaI', 'MgI', 'AlI', 'SiI', 'SI', 'CaI', 'ScI',
       'ScII', 'TiI', 'TiII', 'VI', 'CrI', 'CrII', 'MnI', 'CoI', 'NiI',
       'CuI', 'ZnI', 'SrI', 'YII', 'ZrII', 'BaII', 'LaII', 'CeII', 'PrII',
       'NdII', 'SmII', 'EuII', 'GdII', 'DyII'])
       
    with PdfPages('element_space.pdf') as pdf:
        for i,sp in enumerate(sp_names):
            mask = sp_names == sp
            fig = plot_page(sp, sp_names[np.invert(mask)], data)
            pdf.savefig(fig, orientation='landscape') # save this page
            plt.close()
            print "{0}/{1}: {2} done".format(i, len(sp_names), sp)
    