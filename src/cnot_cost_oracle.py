"""Exact finite 0-vs-1 CNOT cost test for <=2 T and arbitrary 2-qubit input.

Returns numerical evaluation of quartic moment polynomials (not a
symbolic closed-form chamber decomposition). The one-CNOT universality
lemma proves the unrestricted 241-candidate optimum uses <=1 CNOT.
"""
import numpy as np
from src.magic_bounds import expectations,normalize
from src.arbitrary_input_oracle import AXES,rotate_moments

ALL=tuple(p for p in AXES if p!='II')
LOCAL=tuple(p for p in ALL if p.count('I')==1)

def cnot_cost(psi, atol=1e-10):
    psi=normalize(psi)
    if psi.size!=4:raise ValueError('2 qubits only')
    exp=expectations(psi)
    vec=np.array([exp[p] for p in AXES],float)
    initial=float(np.sum(vec**4))
    global_best=(initial,())
    local_best=(initial,())
    first={p:rotate_moments(vec,p) for p in ALL}
    for p,v in first.items():
        moment=float(np.sum(v**4))
        if moment<global_best[0]:global_best=(moment,(p,))
        if p in LOCAL and moment<local_best[0]:local_best=(moment,(p,))
        for q in ALL:
            moment=float(np.sum(rotate_moments(v,q)**4))
            if moment<global_best[0]:global_best=(moment,(p,q))
            if p in LOCAL and q in LOCAL and moment<local_best[0]:local_best=(moment,(p,q))
    delta=local_best[0]-global_best[0]
    assert delta>=-atol
    cost=0 if delta<=atol else 1
    return {'minimum_cnot':cost,'initial_R':initial,
            'local_R':local_best[0],'global_R':global_best[0],
            'local_axes':local_best[1],'global_axes':global_best[1],
            'routing_advantage_bits':float(np.log2(local_best[0]/global_best[0]))}

def sample(seed=20261029,n=200):
    rng=np.random.default_rng(seed)
    data=[]
    for i in range(n):
        psi=normalize(rng.normal(size=4)+1j*rng.normal(size=4))
        data.append(cnot_cost(psi))
    advantages=np.array([x['routing_advantage_bits'] for x in data])
    print(f'Haar-sampled {n} pure inputs, fixed seed {seed}')
    print('Strict one-CNOT advantage (tolerance=1e-10):',int(np.sum(advantages>1e-10)),'/',n)
    print('Median advantage bits:',float(np.median(advantages)))
    print('Max advantage bits:',float(advantages.max()))
    print('Mean advantage bits:',float(advantages.mean()))
    return data

if __name__=='__main__':sample()
