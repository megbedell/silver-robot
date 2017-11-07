'''
This file is part of the silver-robot project.
Copyright 2017 Megan Bedell (Flatiron) and David W. Hogg (NYU).

purpose:
========
Make some (data- and theory-driven) predictions about the expected PCA results.

issues:
=======
- Not yet written!
'''

import math
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = "Helvetica" # don't font-shame me
from astropy.table import Table

if __name__ == "__main__":
    
    # GCE fit slopes from [X/Fe] vs age:
    gce = np.genfromtxt('../data/gce_fits.csv', delimiter=',', dtype=None, names=True)
    
    D = len(gce['element'])
    plt.axhline(0., color="k", alpha=0.5)
    for d in range(D):
        plt.axvline(d, color="k", alpha=0.2)
    plt.plot(gce['slope'], "ko")
    plt.xlabel("element")
    plt.xticks(range(D), gce['element'], rotation="vertical", fontsize=16)
    plt.ylabel(r"abundance/age slope (dex Gyr$^{-1}$)")
    plt.savefig("age_prediction.png")
    