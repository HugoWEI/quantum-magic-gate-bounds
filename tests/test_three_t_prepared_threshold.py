"""Independent dense physical-circuit tests for sharp four-T prep threshold."""
import unittest
from math import sqrt
import numpy as np
from src.three_t_prepared_threshold import certify,EXCEPTIONAL,FULL_SIZES
from src.one_t_natural_input_theorem import ALL,P,LOCAL
from src.one_cnot_universality import PERMS,CNOT_01,CNOT_10,signed_t,map_axis
from src.magic_bounds import fourth_moment,normalize

def state_from_r(sig):
    rho=sum(((a+b*sqrt(2))/16)*P[p] for p,(a,b) in zip(ALL,sig))/4
    ev,vec=np.linalg.eigh(rho)
    np.testing.assert_allclose(ev,[0,0,0,1],atol=1e-12)
    return normalize(vec[:,-1])

def run(psi,axes,signs=(-1,-1,-1)):
    for p,s in zip(axes,signs):psi=signed_t(psi,p,s)
    return psi

def compile_one_cnot(psi,axes):
    signs=(-1,-1,-1)
    if all(p in LOCAL for p in axes):return run(psi,axes),0
    for cut in range(4):
        if any(p not in LOCAL for p in axes[:cut]):continue
        for _,g0,_ in PERMS:
            for _,g1,_ in PERMS:
                for cnot in (CNOT_01,CNOT_10):
                    U=cnot@np.kron(g0,g1)
                    try: mapped=[map_axis(p,U) for p in axes[cut:]]
                    except AssertionError:continue
                    pre=run(psi,axes[:cut],signs[:cut])
                    actual=run(U@pre,[x[0] for x in mapped],
                               tuple(s*x[1] for s,x in zip(signs[cut:],mapped)))
                    np.testing.assert_allclose(actual,U@run(psi,axes),atol=1e-12)
                    return actual,1
    raise AssertionError('Missing physical 1-CNOT circuit')

class SharpFourTThresholdTests(unittest.TestCase):
    def test_full_exact_certificate(self):
        states,words=certify(False)
        self.assertEqual(sum(size for _,size in states),18900)
        self.assertEqual(len(FULL_SIZES),10)
        self.assertEqual(len(words),58)

    def test_all_58_independent_dense_physical_circuits(self):
        states,words=certify(False)
        for i,((sig,_),axes) in enumerate(zip(states,words)):
            psi=state_from_r(sig)
            physical,cost=compile_one_cnot(psi,axes)
            self.assertLessEqual(cost,1)
            target=463/256 if i in EXCEPTIONAL else 7/4
            self.assertAlmostEqual(fourth_moment(physical),target,places=11)

if __name__=='__main__':unittest.main()
