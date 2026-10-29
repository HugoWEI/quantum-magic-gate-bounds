"""Independent exact certificate and dense 4x4 implementation tests."""
import unittest
import numpy as np
from src.three_t_exact_gap import certify,EXPECT,N,one_cnot_triples
from src.three_t_two_cnot_compiler import compile_three,apply_compiled,apply_target,verify
from src.magic_bounds import paulis,fourth_moment,normalize
from src.one_cnot_universality import AXES

class ThreeTCnotThresholdTests(unittest.TestCase):
    def test_exact_integer_certificate(self):
        global_best,one_cnot,gap=certify(verbose=False)
        self.assertEqual(EXPECT[0],79)
        self.assertEqual((len(one_cnot_triples()),len(AXES)**3),(2457,3375))
        self.assertEqual(gap,(2194865920,0))
        self.assertEqual(global_best[1],("YY","XI","XY"))
        self.assertEqual(one_cnot[0],(284758552576,0))

    def test_independent_matrix_two_cnot_witness(self):
        result=verify()
        self.assertEqual(result["cnot_count"],2)

    def test_general_three_rotation_compiler(self):
        rng=np.random.default_rng(330)
        psi=normalize(rng.normal(size=4)+1j*rng.normal(size=4))
        sample=[("YY","XI","XY"),("XI","IY","ZY")]
        sample += [tuple(rng.choice(AXES,size=3)) for _ in range(18)]
        for word in sample:
            compiled=compile_three(*word)
            got=apply_compiled(psi,compiled)
            expected=compiled["second_unitary"]@compiled["first_unitary"]@apply_target(psi,*word)
            self.assertTrue(np.allclose(got,expected,atol=2e-12),word)
            self.assertAlmostEqual(fourth_moment(got),
                                   fourth_moment(apply_target(psi,*word)),places=11)
            self.assertLessEqual(compiled["cnot_count"],2)

if __name__=="__main__":unittest.main()
