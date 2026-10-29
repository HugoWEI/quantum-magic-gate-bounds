"""Independent complex state-vector tests of exact polynomial family certificate."""
import unittest
import numpy as np
from src.magic_bounds import normalize,fourth_moment
from src.one_cnot_universality import signed_t
from src.three_t_parametric_certificate import (
    certify,input_coefficients,rotate,fourth_moment_polynomial,AXES)
from src.three_t_symplectic_obstruction import (
    certify as certify_symplectic, cannot_localize)
from src.three_t_prelocalization import (
    full_symplectic_cliffords,LOCAL_INDICES,INDEX)

def eval_poly(f,s):
    a,b=f
    return sum(float(x)*s**i for i,x in enumerate(a))+np.sqrt(2)*sum(
        float(x)*s**i for i,x in enumerate(b))

class ParametricThreeTTests(unittest.TestCase):
    def test_uniform_exact_bernstein_proof(self):
        self.assertEqual(certify(verbose=False),(19897,179073))

    def test_dense_complex_matrix_independent(self):
        init=input_coefficients()
        words=[(('YY','XI','XY'),(1,1,1)),
               (('IX','YI','ZX'),(-1,1,-1)),
               (('IX','IZ','XY'),(1,-1,1))]
        for s in (-.125,-.045,0,.125,.25):
            psi=np.array([-1+3j,-7-1j,-1+1j,-1+1j*(4+s)])
            N=float(np.vdot(psi,psi).real)
            self.assertAlmostEqual(N,79+8*s+s*s,places=12)
            for word,signs in words:
                v=init
                state=normalize(psi)
                for axis,sgn in zip(word,signs):
                    v=rotate(v,AXES.index(axis),sgn)
                    state=signed_t(state,axis,sgn)
                R=eval_poly(fourth_moment_polynomial(v,3),s)/(8*N)**4
                self.assertAlmostEqual(R,fourth_moment(state),places=11)

    def test_graph_obstruction_matches_clifford_group(self):
        _,bad=certify_symplectic()
        self.assertEqual(dict(bad),{(3,2):1080,(3,3):360,(2,0):90})
        group=full_symplectic_cliffords()
        self.assertEqual(len(group),720)
        examples=[('YY','XI','XY'),('IX','IY','XX'),
                  ('XX','YY','ZZ'),('XI','IX','XX'),('XI','ZI','IX')]
        for word in examples:
            localizable=any(all(g[INDEX[p]] in LOCAL_INDICES for p in word)
                            for g in group)
            self.assertEqual(localizable,not cannot_localize(word))

if __name__=="__main__":
    unittest.main()
