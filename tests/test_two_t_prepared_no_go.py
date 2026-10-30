"""Independent dense-matrix regressions for 2T-prepared state no-go theorem."""
import unittest
from math import sqrt
import numpy as np
from src.two_t_prepared_no_go import certify,SIZES,FULL_SIZES
from src.one_t_natural_input_theorem import ALL,P,LOCAL
from src.one_cnot_universality import PERMS,CNOT_01,CNOT_10,signed_t,map_axis
from src.magic_bounds import fourth_moment,normalize

def state_from_signature(sig):
    rho=sum(((a+b*sqrt(2))/8)*P[p] for p,(a,b) in zip(ALL,sig))/4
    eigen,vec=np.linalg.eigh(rho)
    np.testing.assert_allclose(eigen,[0,0,0,1],atol=2e-12)
    return normalize(vec[:,-1])

def run(psi,axes,signs):
    for p,s in zip(axes,signs):psi=signed_t(psi,p,s)
    return psi

def physical_compiler(psi,axes,signs):
    if all(p in LOCAL for p in axes):return run(psi,axes,signs),0
    for cut in range(4):
        if not all(p in LOCAL for p in axes[:cut]):continue
        for _,g0,_ in PERMS:
            for _,g1,_ in PERMS:
                for cnot in (CNOT_01,CNOT_10):
                    U=cnot@np.kron(g0,g1)
                    try:
                        mapped=[map_axis(p,U) for p in axes[cut:]]
                    except AssertionError:continue
                    input_state=run(psi,axes[:cut],signs[:cut])
                    candidate=run(U@input_state,[x[0] for x in mapped],
                                  [x[1]*s for x,s in zip(mapped,signs[cut:])])
                    target=U@run(psi,axes,signs)
                    np.testing.assert_allclose(candidate,target,atol=2e-12)
                    return candidate,1
    raise AssertionError('No physical <=1CNOT compiler')

class TwoTPreparedNoGoTests(unittest.TestCase):
    def test_exact_enumeration_and_witnesses(self):
        classes,words=certify(False)
        self.assertEqual(sum(SIZES),2580)
        self.assertEqual(FULL_SIZES,(60,360,720,1440))
        self.assertEqual(len(classes),16)
        self.assertEqual(len(words),16)

    def test_independent_complex_matrices_all_16_classes(self):
        classes,words=certify(False)
        for (state,size),axes in zip(classes,words):
            psi=state_from_signature(state)
            exact=run(psi,axes,(-1,-1,-1))
            self.assertAlmostEqual(fourth_moment(exact),7/4,places=11)
            physical,cost=physical_compiler(psi,axes,(-1,-1,-1))
            self.assertLessEqual(cost,1)
            self.assertAlmostEqual(fourth_moment(physical),7/4,places=11)

if __name__=='__main__':unittest.main()
