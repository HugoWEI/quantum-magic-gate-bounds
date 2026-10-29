"""Independent full state-vector tests for the exact Schmidt-phase two-T frontier."""
import math
import unittest
from src.magic_bounds import fourth_moment,schmidt_phase,t_pauli
from src.two_t_frontier_certificate import certify,moments_by_word,q,z

def predicted(t):
    t1=(3-math.sqrt(5))/2
    t2=2*(math.sqrt(2)-1)
    if t<=t1: return (36-20*t+25*t*t)/16
    if t<=t2: return (44-44*t+33*t*t)/16
    return (64-64*t+28*t*t)/16

class ExactTwoTFrontierTests(unittest.TestCase):
    def test_symbolic_certificate(self):
        *_,classes=certify(verbose=False)
        self.assertEqual(sum(len(v) for v in classes.values()),225)
        self.assertEqual(len(classes),15)

    def test_statevector_matches_every_symbolic_word(self):
        words=moments_by_word()
        for t in (0,0.05,0.2,0.4,0.6,0.83,0.95,1):
            theta=math.asin(math.sqrt(t))/2
            psi=schmidt_phase(theta,math.pi/4)  # NOT pi/2!
            zval=math.sqrt(1-t)
            qval=math.sqrt(t)
            minimum=1000
            for (a,b),p in words.items():
                result=fourth_moment(t_pauli(t_pauli(psi,a),b))
                algebra=float(p.subs({q:qval,z:zval}))
                self.assertAlmostEqual(result,algebra,places=11,
                                       msg=f"t={t},axes={a,b}")
                minimum=min(minimum,result)
            self.assertAlmostEqual(minimum,predicted(t),places=11)

    def test_zero_one_two_gate_comparison(self):
        for t in (0,0.01,0.381966,0.5,0.828427,0.99,1):
            r0=4-4*t+3*t*t
            r1=3*r0/4
            r2=predicted(t)
            self.assertLessEqual(r2,r1+1e-12)
            self.assertLess(r2,r0)
            self.assertLessEqual(math.log2(r0/r2),2*math.log2(4/3)+1e-12)

if __name__=="__main__":
    unittest.main()
