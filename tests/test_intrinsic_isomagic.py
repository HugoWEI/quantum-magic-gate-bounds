"""Independent exact-vs-matrix intrinsic-magic isomagic-pair checks."""
import unittest
from math import pi,asin,sqrt
import numpy as np
from src.magic_bounds import ONE,X,schmidt_phase,concurrence,fourth_moment,best_sequence,t_pauli,m2
from src.intrinsic_isomagic_separation import certify

class IntrinsicIsomagicTests(unittest.TestCase):
    def test_exact_rational_certificate(self):
        ra,rb=certify(False)
        self.assertLess(float(rb),float(ra))
    def test_direct_dense_state_vectors(self):
        theta=pi/6
        state_a=schmidt_phase(theta,.5*asin(sqrt(13/18)))
        rx=np.cos(pi/16)*ONE-1j*np.sin(pi/16)*X
        state_b=np.kron(rx,ONE)@schmidt_phase(theta,0)
        for psi in (state_a,state_b):
            self.assertAlmostEqual(concurrence(psi),sqrt(3)/2,places=12)
            self.assertAlmostEqual(fourth_moment(psi),91/32,places=12)
            self.assertGreater(m2(psi),.4)
        ra,rb=certify(False)
        optimal_a=fourth_moment(state_a)/2**best_sequence(state_a,2)[1]
        obtained_b=fourth_moment(t_pauli(t_pauli(state_b,"ZX"),"IZ"))
        self.assertAlmostEqual(optimal_a,float(ra),places=11)
        self.assertAlmostEqual(obtained_b,float(rb),places=11)
        self.assertGreater(optimal_a-obtained_b,.1)
if __name__=="__main__":unittest.main()
