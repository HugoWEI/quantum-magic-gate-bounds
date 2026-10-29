"""Independent local-Clifford 36-word tests and strict routing advantage."""
import unittest
from math import sin,pi,log2
from src.magic_bounds import schmidt_phase,fourth_moment,t_pauli,best_sequence
from src.local_clifford_frontier import certify

AXES=["IX","IY","IZ","XI","YI","ZI"]
class LocalCliffordTests(unittest.TestCase):
    def test_certificate(self):
        self.assertEqual(len(certify(verbose=False)),5)

    def test_local_36_word_statevectors(self):
        for theta,phi in ((0,0),(.25,.15),(.35,.4),(.45,pi/4),(.65,pi/4),(pi/4,pi/4)):
            psi=schmidt_phase(theta,phi)
            t=sin(2*theta)**2;x=sin(phi)**2
            A=(9-8*t+8*t*t+6*t*x-8*t*t*x+9*t*t*x*x)/4
            D=(11-11*t+(9+5*x-5*x*x)*t*t)/4
            R=fourth_moment(psi)
            outcomes=[fourth_moment(t_pauli(t_pauli(psi,p),q))
                      for p in AXES for q in AXES]
            self.assertAlmostEqual(min(outcomes),min(A,D),places=11)
            one=min(fourth_moment(t_pauli(psi,p)) for p in AXES)
            self.assertAlmostEqual(one,3*R/4,places=11)
            self.assertAlmostEqual(min(outcomes+[one,R]),min(A,D,3*R/4),places=11)

    def test_entangling_cliffords_strictly_help(self):
        psi=schmidt_phase(pi/8,pi/4)
        local=min([fourth_moment(t_pauli(t_pauli(psi,p),q))
                   for p in AXES for q in AXES]+[3*fourth_moment(psi)/4])
        unrestricted=fourth_moment(psi)/2**best_sequence(psi,2)[1]
        self.assertAlmostEqual(local,129/64,places=11)
        self.assertAlmostEqual(unrestricted,121/64,places=11)
        self.assertAlmostEqual(log2(local/unrestricted),log2(129/121),places=11)

if __name__=="__main__":unittest.main()
