"""Independent dense-vector checks for exact two-T isomagic counterexample."""
import unittest
from math import pi,sqrt,asin,log2
import numpy as np
from src.magic_bounds import ONE,X,Y,schmidt_phase,concurrence,fourth_moment,best_sequence
from src.two_t_isomagic_counterexample import certify

class IsomagicTwoTTests(unittest.TestCase):
    def test_algebraic_interval_certificate(self):
        self.assertGreater(float(certify(verbose=False)),57/32)

    def test_dense_matrix_225_word_enumeration(self):
        state_a=schmidt_phase(pi/4,.5*asin(sqrt(15)/4))
        R=lambda m:np.cos(pi/16)*ONE-1j*np.sin(pi/16)*m
        bell=np.array([1,0,0,1],dtype=complex)/sqrt(2)
        state_b=np.kron(R(X)@R(Y),ONE)@bell
        for state in (state_a,state_b):
            self.assertAlmostEqual(concurrence(state),1,places=12)
            self.assertAlmostEqual(fourth_moment(state),49/16,places=12)
        ga=best_sequence(state_a,2)[1]
        gb=best_sequence(state_b,2)[1]
        self.assertAlmostEqual(ga,log2(98/57),places=11)
        self.assertAlmostEqual(gb,log2((49/16)/float(certify(False))),places=11)
        self.assertGreater(ga-gb,.068)

if __name__=="__main__":unittest.main()
