# test_methods.py
import xarray as xr
from pivpy import io, pivpy
import numpy as np

import os
f1 = 'Run000001.T000.D000.P000.H001.L.vec'
f2 = 'Run000002.T000.D000.P000.H001.L.vec'
path = './data/'

_a = io.loadvec(os.path.join(path,f1))
_b = io.loadvec(os.path.join(path,f2))


def test_add():
    """ test add of two fields """
    # this operation should sum only velocities
    # xarray provides it out of the box for the variables
    # and not dimensions
    _c = _a + _b 

    assert np.allclose(_c.x,_a.x)
    assert np.allclose(_c.u, _a.u + _b.u)

def test_pan():
    """ test a shift by dx,dy using pan method """
    _c = _a.piv.pan(1.0,-1.0) # note the use of .piv.
    assert np.allclose(_c.coords['x'][0],1.312480)
    assert np.allclose(_c.coords['y'][0], -1.31248)


def test_mean():
    data = io.create_sample_dataset(10)
    assert data.piv.average.u.median() == 4.0

def test_vec2scal():
    data = io.create_sample_dataset()
    data.piv.vec2scal()
    # tests that first data['w'] exists and then 
    # the first value is 0.0
    assert data['w'][0,0,0] == 0.0

def test_add():
    data = io.create_sample_dataset()
    tmp = data + data
    assert tmp['u'][0,0,0] == 2.0
