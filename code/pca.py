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
    rectangle = np.power(10., rectangle[mask]) # taking off the logs

    # PCA the fuck out of shit.
    mean = np.mean(rectangle, axis=0)
    print(mean)
    drectangle = rectangle - mean[None, :]
    u, s, v = np.linalg.svd(drectangle, full_matrices=False)
    pcas = u * s[None, :]
    reconstruction = mean[None, :] + np.dot(pcas, v)
    print (u.shape, s.shape, v.shape)

    # reformat eigenvectors back into log space
    log10v = (v / mean[:,None]) / np.log(10.)

    # plot eigenvectors in abundance space
    #   many people died to tell us that v[3,:] (say) is the third eigenvector
    #   (and not v[:, 3])
    for i in range(16):
        plt.clf()
        plt.axhline(0., color="k", alpha=0.5)
        for d in range(D):
            plt.axvline(d, color="k", alpha=0.2)
        plt.plot(log10v[i,:], "ko") # putting logs back on
        plt.xlabel("elemnent")
        plt.xticks(range(D), sp_names, rotation="vertical")
        plt.ylabel("log10 amplitude in eigenvector")
        plt.title("eigenvector {:02d}".format(i))
        plt.savefig("pca_eigenvec_{:02d}.png".format(i))

if False:
    # plot variance vs K
    plt.clf()
    plt.plot(s, "ko")
    plt.xlabel("componennt")
    plt.ylabel("contribution to variance")
    plt.savefig("pca001.png")

    # plot PCA amplitude vs PCA amplitude
    for i in range(D - 1):
        j = i + 1
        plt.clf()
        plt.plot(pcas[:,i], pcas[:,j], "k.")
        plt.xlabel("pca {:02d}".format(i))
        plt.xlim(-0.3, 0.3)
        plt.ylabel("pca {:02d}".format(j))
        plt.ylim(-0.3, 0.3)
        plt.savefig("pca_{:02d}_{:02d}.png".format(i, j))
