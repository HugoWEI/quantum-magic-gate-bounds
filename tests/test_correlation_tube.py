"""Check measurable Pauli-correlation sufficient-condition implementation."""
import unittest
import numpy as np
from src.magic_bounds import normalize
from src.correlation_tube import (
    RADIUS,LOW,HIGH,curve,pauli_vector,nearest_point,certificate)

def family(s):
    return normalize(np.array([-1+3j,-7-1j,-1+1j,-1+(4+s)*1j]))

class CorrelationTubeTests(unittest.TestCase):
    def test_reference_curve_and_nearest_point(self):
        for s in (LOW,-.07,0,.1,HIGH):
            psi=family(s)
            np.testing.assert_allclose(pauli_vector(psi),curve(s),atol=2e-14)
            distance,location=nearest_point(psi)
            self.assertLess(distance,2e-12)
            self.assertAlmostEqual(location,s,places=8)
            self.assertTrue(certificate(psi)["certified"])

    def test_perturbations_and_unrelated_input(self):
        rng=np.random.default_rng(600)
        for s in (-.08,0,.17):
            psi=family(s)
            perturb=rng.normal(size=4)+1j*rng.normal(size=4)
            noisy=normalize(psi+1e-6*perturb)
            result=certificate(noisy)
            self.assertLess(result["distance"],RADIUS)
            self.assertTrue(result["certified"])
        far=normalize(np.array([1,0,0,0],complex))
        self.assertFalse(certificate(far)["certified"])

if __name__=="__main__":
    unittest.main()
