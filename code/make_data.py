'''
Just a dumb script to get data from MB's computer and write it in usable form.
'''

import numpy as np
from astropy.table import Table
from harps_hacks import read_harps
import h5py
from scipy.interpolate import interp1d

def make_star_data():
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
        t[sp+'_gce'] = np.append(a_gce[sp+'Fe'], 0.0)
        t[sp+'_gce_err'] = np.append(a_gce['err_'+sp], 0.0)  
    
    t.write('../data/star_data.fits', format='fits', overwrite=True)  
    
def make_spectra():
    root_dir = '/Users/mbedell/Documents/Research/HARPSTwins/Abundances/All/'
    a = np.genfromtxt(root_dir+'final_abundances_w_ncapture.csv', delimiter=',', dtype=None, names=True) 
    star_name = np.copy(a['id'])
    star_name = star_name[star_name != 'HIP114328'] # temporary bc the spectra files aren't combined
    N = len(star_name)
    
    root_dir = '/Users/mbedell/Documents/Research/HARPSTwins/Abundances/spectra_combined/'
    waves = np.arange(3800.0, 6900.0, 0.01)
    all_waves = np.tile(waves, (N,1))
    fluxs = np.zeros_like(all_waves)
    for i,star in enumerate(star_name):
        wave, flux = read_harps.read_spec(root_dir+star+'_n.fits')
        print star, wave[0], wave[-1]
        f = interp1d(wave, flux)
        fluxs[i,:] = f(waves)
    
    with h5py.File('../data/block_o_spectra.hdf5', 'w') as h:
        dset = h.create_dataset('fluxs', data=fluxs)
        dset = h.create_dataset('waves', data=waves)
        dset = h.create_dataset('star_name', data=star_name)
             

if __name__ == "__main__":
    make_star_data()
    make_spectra()
 
