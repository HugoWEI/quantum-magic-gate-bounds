"""Independent 225-word numeric tests on randomly oriented two-qubit inputs."""
import unittest
import numpy as np
from src.arbitrary_input_oracle import frontier,rotate_moments,AXES
from src.magic_bounds import normalize,expectations,t_pauli,best_sequence,schmidt_phase
class ArbitraryInputOracleTests(unittest.TestCase):
    def test_each_axis_heisenberg_conversion(self):
        rng=np.random.default_rng(20261029)
        for _ in range(20):
            psi=normalize(rng.normal(size=4)+1j*rng.normal(size=4))
            v=np.array([expectations(psi)[p] for p in AXES])
            for axis in AXES[1:]:
                expected=expectations(t_pauli(psi,axis))
                np.testing.assert_allclose(rotate_moments(v,axis),
                    [expected[p] for p in AXES],atol=2e-14,rtol=0)
    def test_arbitrary_orientations(self):
        rng=np.random.default_rng(1729001)
        for _ in range(14):
            psi=normalize(rng.normal(size=4)+1j*rng.normal(size=4))
            direct=max(best_sequence(psi,1)[1],best_sequence(psi,2)[1])
            result=frontier(psi)
            self.assertAlmostEqual(result["gain_bits"],direct,places=11)
            self.assertEqual(result["candidate_words"],241)
    def test_schmidt_regression(self):
        for theta,phi in [(0,0),(.3,.42),(.5,.63),(.7,.2)]:
            psi=schmidt_phase(theta,phi)
            self.assertAlmostEqual(frontier(psi)["gain_bits"],
                best_sequence(psi,2)[1],places=11)
if __name__=="__main__":unittest.main()
