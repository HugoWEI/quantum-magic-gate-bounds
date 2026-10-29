"""Exact envelope certificate and independently evaluated 4x4 matrices."""
import unittest
import numpy as np
from src.three_t_exact_branch_frontier import (
    certify,PG,PR,GAP_POLY)
from src.one_cnot_universality import signed_t
from src.magic_bounds import normalize,fourth_moment

def value(coeffs,s):
    return sum(float(x)*s**i for i,x in enumerate(coeffs))

class ThreeTExactBranchTests(unittest.TestCase):
    def test_all_polynomial_classes_certified(self):
        global_set,restricted_set=certify(verbose=False)
        self.assertEqual((len(global_set),len(restricted_set)),(1876,1258))

    def test_direct_statevector_branches(self):
        for s in (-.125,-.08,0,.06,.19,.25):
            psi=normalize(np.array([-1+3j,-7-1j,-1+1j,
                                    -1+(4+s)*1j]))
            N=79+8*s+s*s
            actual=[]
            for word in (("ZI","ZY"),("YY","XI","XY")):
                output=psi
                for p in word:output=signed_t(output,p,1)
                actual.append(fourth_moment(output))
            self.assertAlmostEqual(actual[0],value(PR,s)/N**4,places=11)
            self.assertAlmostEqual(actual[1],value(PG,s)/(16*N**4),places=11)
            gap=actual[0]-actual[1]
            self.assertAlmostEqual(gap,value(GAP_POLY,s)/(16*N**4),places=11)
            self.assertGreater(gap,.01)

if __name__=="__main__":
    unittest.main()
