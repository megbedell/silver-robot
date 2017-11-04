'''
This file is part of the silver-robot project.
Copyright 2017 Megan Bedell (Flatiron) and David W. Hogg (NYU).

purpose:
========
Run PCA and make output, which can be subsequently be made into a huge number of plots.

issues:
=======
- Not yet written!
'''

import math
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = "Helvetica" # ZOMG, Bedell!
from astropy.table import Table

if __name__ == "__main__":

    # what Bedell say
    data = Table.read('../data/star_data.fits', format='fits')
    sp_names = np.asarray(['CI', 'CH', 'OI', 'NaI', 'MgI', 'AlI', 'SiI', 'SI', 'CaI', 'ScI',
       'ScII', 'TiI', 'TiII', 'VI', 'CrI', 'CrII', 'MnI', 'CoI', 'NiI',
       'CuI', 'ZnI', 'SrI', 'YII', 'ZrII', 'BaII', 'LaII', 'CeII', 'PrII',
       'NdII', 'SmII', 'EuII', 'GdII', 'DyII'])

    # make rectangular data
    N = len(data)
    D = len(sp_names)
    rectangle = np.zeros((N, D))
    for d, name in enumerate(sp_names):
        rectangle[:, d] = data[name]

    # FOR NOW: remove one object HACK
    good = np.isfinite(rectangle)
    bad = ~good
    mask = np.sum(bad, axis=1) == 0
    rectangle = rectangle[mask]

    # PCA the fuck out of shit.
    mean = np.mean(rectangle, axis=0)
    print(mean)
    drectangle = rectangle - mean[None, :]
    u, s, v = np.linalg.svd(drectangle, full_matrices=False)
    pcas = u * s[None, :]
    reconstruction = mean[None, :] + np.dot(pcas, v)

    # plot some things
    plt.clf()
    plt.plot(s, "ko")
    plt.xlabel("componennt")
    plt.ylabel("contribution to variance")
    plt.savefig("pca001.png")

    for i, j in [(0, 1), (3, 4), (9, 10), (20, 21)]:
        plt.clf()
        plt.plot(pcas[:,i], pcas[:,j], "k.")
        plt.xlabel("pca {:02d}".format(i))
        plt.xlim(-0.3, 0.3)
        plt.ylabel("pca {:02d}".format(j))
        plt.ylim(-0.3, 0.3)
        plt.savefig("pca_{:02d}_{:02d}.png".format(i, j))
