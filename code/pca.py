'''
This file is part of the silver-robot project.
Copyright 2017 Megan Bedell (Flatiron) and David W. Hogg (NYU).

purpose:
========
Run PCA and make output, which can be subsequently be made into a huge number of plots.

issues:
=======
- Needs to do cross-validation: For each K, for each n in N, for each d in D!
- Need to patch rather than exclude missing abundance.
- Ought to save to files and plotting should be perfomed in a separate file.
- Search for HACK and MAGIC and QUESTION
'''

import numpy as np
import matplotlib.pyplot as plt
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
    log_rectangle = np.zeros((N, D))
    for d, name in enumerate(sp_names):
        log_rectangle[:, d] = data[name]

    # FOR NOW: remove one object HACK
    good = np.isfinite(log_rectangle)
    bad = ~good
    mask = np.sum(bad, axis=1) == 0
    log_rectangle = log_rectangle[mask] # remove one star with one missing abundance
    linear_rectangle = np.power(10., log_rectangle) # taking off the logs

    # PCA the fuck out of shit.
    for prefix, rectangle in [("log", log_rectangle), ("linear", linear_rectangle)]:
        mean = np.mean(rectangle, axis=0)
        print(mean)
        drectangle = rectangle - mean[None, :]
        u, s, v = np.linalg.svd(drectangle, full_matrices=False)
        pcas = u * s[None, :]
        reconstruction = mean[None, :] + np.dot(pcas, v)
        print (u.shape, s.shape, v.shape)

        # reformat eigenvectors back into log space, if necessary
        # QUESTION: do we divide by the mean or by the Solar values?
        if prefix == "linear":
            # log10v = (v / mean[:,None]) / np.log(10.) # dvide by the mean
            log10v = (v / np.ones_like(v)) / np.log(10.) # divide by the Sun - no-op
        else:
            log10v = v

        # plot variance vs K
        plt.clf()
        plt.plot(s, "ko")
        plt.xlabel("componennt")
        plt.ylabel("contribution to variance")
        plt.title("{} analysis".format(prefix))
        plt.savefig("pca_{}_variances.png".format(prefix))

        # plot eigenvectors in abundance space
        #   many people died to tell us that v[3,:] (say) is the third eigenvector
        #   (and not v[:, 3])
        for i in range(16):
            plt.clf()
            plt.axhline(0., color="k", alpha=0.5)
            for d in range(D):
                plt.axvline(d, color="k", alpha=0.2)
            plt.plot(log10v[i,:], "ko") # putting logs back on
            plt.xticks(range(D), sp_names, rotation="vertical")
            plt.ylabel("amplitude in eigenvector (dex)")
            plt.title("eigenvector {:02d}, {} analysis".format(i, prefix))
            plt.savefig("pca_{}_eigenvec_{:02d}.png".format(prefix, i))

if False:
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
