import numpy as np
from astropy.table import Table

root_dir = '/Users/mbedell/Documents/Research/HARPSTwins/Abundances/All/'
par = np.genfromtxt(root_dir+'final_parameters.csv', delimiter=',', dtype=None, names=True)
ages = np.genfromtxt(root_dir+'final_ages_combination.csv', delimiter=',', dtype=None, names=True)

a = np.genfromtxt(root_dir+'final_abundances_w_ncapture.csv', delimiter=',', dtype=None, names=True) 
gce = np.genfromtxt(root_dir+'GCE/gce_linear_w_ncapture.txt', delimiter=',', dtype=None, names=True)
a_gce = np.genfromtxt(root_dir+'GCE/harpstwins_gcecorrected_w_ncapture.csv', delimiter=',', dtype=None, names=True)
thin = [i not in ['HIP19911', 'HIP108158', 'HIP109821', 'HIP115577', 'HIP14501', 'HIP28066', 'HIP30476',
        'HIP33094', 'HIP65708', 'HIP73241', 'HIP74432'] for i in a['id']] # mask out SB2, thick-disk
thick = np.invert(thin)
   
t = Table()
t['star_name'] = a['id']
t['teff'] = par['teff']
t['teff_err'] = par['err_teff']
t['logg'] = par['logg']
t['logg_err'] = par['err_logg']
t['feh'] = par['feh']
t['feh_err'] = par['err_feh']
t['age'] = np.append(ages['age_mean'], 4.6)
t['age_err'] = np.append(ages['age_std'], 0.0)
t['mass'] = np.append(ages['mass_mean'], 1.0)
t['mass_err'] = np.append(ages['mass_std'], 0.0)
t['thick_disk'] = thick

sp_names = gce['element']
for i,sp in enumerate(sp_names):
    t[sp] = a[sp+'_1']  - par['feh']
    t[sp+'_err'] = a['err_'+sp]
    t[sp+'_gce'] = a_gce[sp+'Fe']
    t[sp+'_gce_err'] = a_gce['err_'+sp]    
    
t.write('star_data.fits', format='fits')    
