"""Independent complex 4x4 Clifford checks and exact CNOT-cost evaluation."""
import unittest
import numpy as np
from src.magic_bounds import normalize,schmidt_phase,fourth_moment
from src.one_cnot_universality import AXES,witness,local_permutation_gates,signed_t,verify_all
from src.cnot_cost_oracle import cnot_cost
from src.arbitrary_input_oracle import frontier

class UniversalOneCnotTests(unittest.TestCase):
    def test_all_225_axis_pairs_with_clifford_signs(self):
        witnesses=verify_all()
        self.assertEqual((len(witnesses),
                          sum(w[4]==0 for w in witnesses.values()),
                          sum(w[4]==1 for w in witnesses.values())),
                         (225,36,189))
        self.assertEqual(len(local_permutation_gates()),6)

    def test_local_clifford_normalizer(self):
        rng=np.random.default_rng(2228)
        for _ in range(2):
            psi=normalize(rng.normal(size=4)+1j*rng.normal(size=4))
            for p in AXES:
                for q in AXES:
                    U,description,(p2,s1),(q2,s2),count=witness(p,q)
                    goal=signed_t(signed_t(psi,p,1),q,1)
                    actual=signed_t(signed_t(U@psi,p2,s1),q2,s2)
                    self.assertTrue(np.allclose(U@goal,actual,atol=1e-12))
                    self.assertAlmostEqual(fourth_moment(goal),fourth_moment(actual),places=11)
                    self.assertIn(count,(0,1))

    def test_one_cnot_finite_frontier_all_orientations(self):
        rng=np.random.default_rng(9276)
        for _ in range(8):
            psi=normalize(rng.normal(size=4)+1j*rng.normal(size=4))
            full=frontier(psi)
            routing=cnot_cost(psi)
            self.assertAlmostEqual(full['minimum_R'],routing['global_R'],places=11)
            self.assertLessEqual(routing['global_R'],routing['local_R']+1e-11)
            axes=full['axes']
            if len(axes)==2:
                U,_,mapped1,mapped2,cost=witness(*axes)
                phi=U@psi
                phi=signed_t(phi,*mapped1)
                phi=signed_t(phi,*mapped2)
                self.assertAlmostEqual(fourth_moment(phi),full['minimum_R'],places=11)
            elif len(axes)==1:
                U,_,mapped1,_,cost=witness(axes[0],axes[0])
                phi=signed_t(U@psi,*mapped1)
                self.assertAlmostEqual(fourth_moment(phi),full['minimum_R'],places=11)

    def test_strict_cnot_needed(self):
        psi=schmidt_phase(np.pi/8,np.pi/4)
        r=cnot_cost(psi)
        self.assertEqual(r['minimum_cnot'],1)
        self.assertAlmostEqual(r['local_R'],129/64,places=11)
        self.assertAlmostEqual(r['global_R'],121/64,places=11)
        self.assertGreater(r['routing_advantage_bits'],.09)

    def test_zero_cnot_case(self):
        psi=np.array([1,0,0,0],complex)
        r=cnot_cost(psi)
        self.assertEqual(r['minimum_cnot'],0)
        self.assertAlmostEqual(r['global_R'],r['local_R'],places=11)

if __name__=='__main__':unittest.main()
