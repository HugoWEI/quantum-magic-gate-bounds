"""Independent state-vector tests, including all 15 algebraic deficits."""
import unittest
import numpy as np
from src.magic_bounds import (
    ONE,X,Y,schmidt_phase,schmidt_moment,fourth_moment,gain,
    concurrence,m2,best_axis,best_sequence,zhu_deficit,paulis,t_pauli
)
from src.exact_counterexample import deficits

class MagicBoundsTests(unittest.TestCase):
    def test_schmidt_family_closed_forms(self):
        for theta in [0.0,0.1,0.3,np.pi/4]:
            for phi in [-0.6,-0.2,0,0.25,np.pi/4,np.pi/2]:
                psi=schmidt_phase(theta,phi)
                r0,rz,rx=schmidt_moment(theta,phi)
                self.assertAlmostEqual(fourth_moment(psi),r0,places=12)
                self.assertAlmostEqual(fourth_moment(t_pauli(psi,"ZI")),rz,places=12)
                self.assertAlmostEqual(fourth_moment(t_pauli(psi,"XI")),rx,places=12)
                self.assertAlmostEqual(concurrence(psi),np.sin(2*theta),places=12)

    def test_magic_entangled_saturation(self):
        psi=schmidt_phase(np.pi/4,np.pi/4)
        self.assertAlmostEqual(m2(psi),np.log2(4/3),places=12)
        self.assertAlmostEqual(gain(psi,"XI"),np.log2(4/3),places=12)
        self.assertAlmostEqual(gain(psi,"ZI"),-np.log2(4/3),places=12)
        self.assertAlmostEqual(zhu_deficit(psi,"XI"),0,places=12)

    def test_zhu_bound_random_two_qubit_all_axes(self):
        rng=np.random.default_rng(20261029)
        limit=np.log2(4/3)
        for _ in range(100):
            psi=rng.normal(size=4)+1j*rng.normal(size=4)
            psi/=np.linalg.norm(psi)
            for axis in paulis(2):
                if axis=="II": continue
                self.assertLessEqual(gain(psi,axis),limit+1e-11)
                self.assertGreaterEqual(zhu_deficit(psi,axis),-1e-11)

    def test_generic_state_strict(self):
        rng=np.random.default_rng(1729)
        psi=rng.normal(size=4)+1j*rng.normal(size=4)
        psi/=np.linalg.norm(psi)
        self.assertLess(best_axis(psi)[1],np.log2(4/3)-1e-4)

    def test_isomagic_counterexample_all_axes(self):
        from math import sqrt,asin,pi
        angle=pi/8
        rx=np.cos(angle/2)*ONE-1j*np.sin(angle/2)*X
        ry=np.cos(angle/2)*ONE-1j*np.sin(angle/2)*Y
        bell=np.array([1,0,0,1],dtype=complex)/sqrt(2)
        a=schmidt_phase(pi/4,0.5*asin(sqrt(15)/4))
        b=np.kron(rx@ry,ONE)@bell
        for p in (a,b):
            self.assertAlmostEqual(concurrence(p),1.0,places=12)
            self.assertAlmostEqual(fourth_moment(p),49/16,places=12)
        self.assertAlmostEqual(best_sequence(a,1)[1],np.log2(4/3),places=12)
        self.assertAlmostEqual(best_sequence(b,1)[1],np.log2(49/37),places=12)
        for axis,deficit in deficits().items():
            self.assertAlmostEqual(zhu_deficit(b,axis),float(deficit),places=11)

if __name__=="__main__":
    unittest.main()
