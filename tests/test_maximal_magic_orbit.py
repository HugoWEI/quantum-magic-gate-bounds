"""Test exact orbit-distance theorem with independent complex state vectors."""
import unittest
from math import pi,sqrt
import numpy as np
from src.magic_bounds import ONE,X,schmidt_phase,fourth_moment,m2,concurrence
from src.one_cnot_universality import signed_t
from src.maximal_magic_orbit_certificate import (
    orbit,exact_certificate,GENERATORS)

class MaximalMagicOrbitTests(unittest.TestCase):
    def test_exact_480_orbit_and_algebraic_fidelity(self):
        best,second,restricted,word,word1=exact_certificate(verbose=False)
        self.assertEqual(len(orbit()),480)
        self.assertEqual(best,(272,0,48,64))
        self.assertEqual(second,(228,14,28,50))
        self.assertEqual(restricted,(156,66,52,62))
        self.assertEqual(word,("H0","H1","S1"))

    def test_independent_dense_fidelity_and_concurrence(self):
        rx=np.cos(pi/8)*ONE-1j*np.sin(pi/8)*X
        psi=np.kron(rx,ONE)@schmidt_phase(pi/12,pi/12)
        for p in ("XX","IZ","IY"):
            psi=signed_t(psi,p,1)
        fid=np.array([1+3j,1+1j,1-1j,1+1j],complex)/4
        F=abs(np.vdot(fid,psi))**2
        expected=(17+3*sqrt(3)+4*sqrt(6))/32
        self.assertAlmostEqual(F,expected,places=12)
        self.assertAlmostEqual(concurrence(fid),1/sqrt(2),places=12)
        self.assertLess(abs(concurrence(psi)-1/sqrt(2)),.004)
        self.assertAlmostEqual(m2(fid),np.log2(16/7),places=12)
        self.assertLess(np.log2(16/7)-m2(psi),.00033)

    def test_all_clifford_generators_are_integer_exact(self):
        for _,num,scale in GENERATORS:
            self.assertTrue(np.array_equal(num.real,np.rint(num.real)))
            self.assertTrue(np.array_equal(num.imag,np.rint(num.imag)))
            self.assertIn(scale,(1,2))

if __name__=="__main__":
    unittest.main()
