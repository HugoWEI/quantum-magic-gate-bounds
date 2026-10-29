"""Exact *finite enumeration*, evaluated in float64, for arbitrary pure two-qubit inputs.

For k<=2 and free global Clifford routing, candidate words are 1, 15
or 225 Pauli-axis sequences (compare all shorter counts as well).
Each R_out is a quartic polynomial of the 16 input Pauli expectations.
This generic algorithm is not a closed-form frontier or a CNOT optimizer.
"""
import numpy as np
from src.magic_bounds import expectations,normalize
from src.two_t_frontier_certificate import product_label,AXES

NONIDENTITY=AXES[1:]
INDEX={p:i for i,p in enumerate(AXES)}
ROOT2=np.sqrt(2.)

def rotate_moments(vector,axis):
    out=vector.copy()
    for i,p in enumerate(AXES):
        phase,partner=product_label(axis,p)
        if phase%2:
            sign=1 if phase==3 else -1
            out[i]=(vector[i]+sign*vector[INDEX[partner]])/ROOT2
    return out

def frontier(psi,max_t=2):
    if max_t not in (0,1,2):raise ValueError("max_t must be 0, 1 or 2")
    psi=normalize(psi)
    if psi.size!=4:raise ValueError("pure two-qubit input required")
    expectation=expectations(psi)
    vector=np.array([expectation[p] for p in AXES],float)
    initial=float(np.sum(vector**4))
    minimum=initial;best=()
    if max_t>=1:
        first={p:rotate_moments(vector,p) for p in NONIDENTITY}
        for p,v in first.items():
            val=float(np.sum(v**4))
            if val<minimum:minimum,best=val,(p,)
        if max_t>=2:
            for p,v in first.items():
                for q in NONIDENTITY:
                    val=float(np.sum(rotate_moments(v,q)**4))
                    if val<minimum:minimum,best=val,(p,q)
    return {"initial_R":initial,"minimum_R":minimum,
            "gain_bits":float(np.log2(initial/minimum)),
            "axes":best,"candidate_words":1+15*(max_t>=1)+225*(max_t>=2)}

if __name__=="__main__":
    from src.magic_bounds import schmidt_phase
    print(frontier(schmidt_phase(.4,.3)))
