"""Independent dense-statevector verification of the two-parameter theorem."""
import math
import unittest
from src.magic_bounds import paulis, schmidt_phase, t_pauli, fourth_moment, best_sequence
from src.general_phase_certificate import certify,A_WORD,B_WORD,C_WORD

def branches(t,phi):
    x=math.sin(phi)**2
    return ((9-8*t+8*t*t+6*t*x-8*t*t*x+9*t*t*x*x)/4,
            11*(1-t+t*t*(1-x+x*x))/4,
            (16-16*t+(9-8*x+8*x*x)*t*t)/4)

class GeneralPhaseTests(unittest.TestCase):
    def test_symbolic_42_region_certificate(self):
        words,groups,proof=certify(verbose=False)
        self.assertEqual((len(words),len(groups),len(proof)),(225,21,18))
        self.assertEqual(sum(len(x) for x in proof.values()),42)

    def test_all_225_statevectors_independently(self):
        axes=[p for p in paulis(2) if p!="II"]
        phi_star=math.asin(math.sqrt(math.sqrt(5)-2))
        theta_star=math.asin(math.sqrt((1+math.sqrt(5))/4))/2
        cases=[(0,0),(math.pi/4,0),(math.pi/8,math.pi/4),
               (math.pi/4,math.pi/4),(theta_star,phi_star),
               (.14,.05),(.21,.18),(.3,.32),(.37,.63),
               (.38,.52),(.41,.73),(.46,.4),(.51,.65),(.64,.28),
               (.72,.55),(.73,.76)]
        for theta,phi in cases:
            psi=schmidt_phase(theta,phi)
            A,B,C=branches(math.sin(2*theta)**2,phi)
            samples=[fourth_moment(t_pauli(t_pauli(psi,p),q))
                     for p in axes for q in axes]
            self.assertAlmostEqual(min(samples),min(A,B,C),places=11,
                                   msg=f"{theta=} {phi=}")
            for (p,q),v in zip((A_WORD,B_WORD,C_WORD),(A,B,C)):
                self.assertAlmostEqual(fourth_moment(t_pauli(t_pauli(psi,p),q)),v,places=11)
            self.assertLessEqual(min(samples),3*fourth_moment(psi)/4+1e-11)

    def test_phase_symmetry(self):
        for phi in (.16,.28,.62):
            values=[best_sequence(schmidt_phase(.3,phase),2)[1]
                    for phase in (phi,-phi,math.pi/2-phi,phi+math.pi/2)]
            self.assertLess(max(values)-min(values),1e-11)

if __name__=="__main__":unittest.main()
