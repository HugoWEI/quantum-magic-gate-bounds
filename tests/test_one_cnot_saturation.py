"""End-to-end physical CNOT-count checks for the exact Schmidt frontier."""
import unittest
import numpy as np
from src.magic_bounds import schmidt_phase,fourth_moment,t_pauli,best_sequence
from src.one_cnot_saturation import CNOT,CZ,branch_circuit,reference_circuit,moments,verify_dense

class CnotOneTests(unittest.TestCase):
    def test_exact_circuit_equivalence(self):
        verify_dense()
    def test_one_cnot_matches_unrestricted_optimum(self):
        for theta,phi in [(0,0),(.22,.35),(.4,.12),(.61,.58),
                          (np.pi/8,np.pi/4),(np.pi/4,np.pi/4)]:
            psi=schmidt_phase(theta,phi)
            physical=min(fourth_moment(branch_circuit(psi,p)) for p in "ABC")
            global_best=fourth_moment(psi)/2**best_sequence(psi,2)[1]
            self.assertAlmostEqual(physical,global_best,places=11)
    def test_some_inputs_require_one_cnot(self):
        psi=schmidt_phase(np.pi/8,np.pi/4)
        local=["IX","IY","IZ","XI","YI","ZI"]
        zero=min([fourth_moment(t_pauli(t_pauli(psi,p),q))
                  for p in local for q in local]+[3*fourth_moment(psi)/4])
        one=min(fourth_moment(branch_circuit(psi,p)) for p in "ABC")
        self.assertAlmostEqual(zero,129/64,places=12)
        self.assertAlmostEqual(one,121/64,places=12)
        self.assertLess(one,zero)
if __name__=="__main__":unittest.main()
