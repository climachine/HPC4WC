"""
Example for workflow for gapfilling remote sensing data from diverse sources
Explicit stencil filter

    @author: verena bessenbacher
    @date: 12 06 2020
"""

import numpy as np
from datetime import datetime
import xarray as xr
from scipy.ndimage.filters import generic_filter

shape = (3, 30, 72, 140) # real shape is (22, 3653, 720, 1440)
frac_missing = 0.42
filepath = '/net/so4/landclim/bverena/large_files/data_small.nc'

# create example array
print(f'create data array with shape {shape}')
data = xr.open_dataarray(filepath)

# subset more for speedup of first tests
print(f'subset even more because very large dataset')
data = data[:,::10,:,:]

shape = np.shape(data)

# gapfilling the missing values with spatiotemporal mean
print('gapfilling missing values with spatiotemporal mean')
tic = datetime.now()
result = np.zeros(shape)
result[:,:,:,:] = np.nan
for var in range(0,shape[0]):
    for t in range(2,shape[1]-2):
        print('new time t ='+str(t))
        for i in range(2,shape[2]-2):
            for j in range(2,shape[3]-2):
                values = data[var,t-2:t+3,i-2:i+3,j-2:j+3].copy()
                #print(np.shape(data), np.shape(values))
                values[2,2,2] = np.nan
                summed = np.sum(np.isnan(values))
                tot = np.nansum(values)
                if values.size - summed != 0:
                    result[var,t,i,j] = tot / (values.size - summed)
toc = datetime.now()
print(f'this filter function took {toc-tic}')
data = data.fillna(result)

# test if results are the same as in "ground truth"
from unittest_simple import test_simple
res = xr.open_dataarray('baseline_result.nc')
import IPython; IPython.embed()
test_simple(data, res)


# my PhD Project goes on with:
# gapfill each variable by regressing over all the others
# in an iterative EM-like fashion 
# with spatiotemporal gapfill as initial guess
# until estimates for missing values converge
