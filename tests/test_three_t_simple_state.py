"""Independent dense-matrix verification of the exact rotated-Schmidt witness."""
import unittest
import numpy as np
from math import log2, pi
from src.magic_bounds import ONE,X,schmidt_phase,fourth_moment,concurrence,m2
from src.one_cnot_universality import signed_t
from src.three_t_simple_state_certificate import (
    certify,START,moment,sign,minus,times,one_cnot_triples,float_value)

def simple_state():
    rx=np.cos(pi/8)*ONE-1j*np.sin(pi/8)*X
    return np.kron(rx,ONE)@schmidt_phase(pi/12,pi/12)

def evolved(psi,axes,signs):
    for axis,sgn in zip(axes,signs):
        psi=signed_t(psi,axis,sgn)
    return psi

class SimpleStateThreeTTests(unittest.TestCase):
    def test_exact_full_enumeration(self):
        global_best,restricted,gap=certify(verbose=False)
        self.assertEqual(global_best[1],("XX","IZ","IY"))
        self.assertEqual(restricted[0],(30620672,0,-266240,0))
        self.assertEqual(len(one_cnot_triples()),2457)
        self.assertGreater(sign(minus(times(gap,25),(64**4,0,0,0))),0)
        self.assertEqual(moment(START,0),(40697856,0,0,0))

    def test_statevectors_and_magic_ceiling(self):
        psi=simple_state()
        self.assertAlmostEqual(concurrence(psi),.5,places=12)
        self.assertAlmostEqual(fourth_moment(psi),621/256,places=12)
        global_state=evolved(psi,("XX","IZ","IY"),(1,1,1))
        restricted_state=evolved(psi,("ZX","IY","ZI"),(-1,-1,-1))
        g,r,gap=certify(False)
        self.assertAlmostEqual(fourth_moment(global_state),float_value(g[0]),places=12)
        self.assertAlmostEqual(fourth_moment(restricted_state),float_value(r[0]),places=12)
        self.assertAlmostEqual(fourth_moment(restricted_state)-fourth_moment(global_state),
                               float_value(gap),places=12)
        self.assertLess(log2(16/7)-m2(global_state),.00033)
        self.assertGreater(m2(global_state)-m2(restricted_state),.038)

if __name__=="__main__":unittest.main()
