"""Exactly locate both magic-optimal 3T outputs relative to the 480-state
Clifford orbit of a known maximally magical two-qubit fiducial.

All *comparison* arithmetic uses Z[sqrt(2),sqrt(3)] and exact integer
radical-sign enclosures. The signed Clifford permutations are computed
using ONLY integer-valued complex 4x4 matrices: unnormalized Hadamard
numerators, S, and CNOT. No floating point orbit matching.

The fiducial |f>=(|00>+i|01>+i|10>+i|11>)/2 has M2=log2(16/7).
For psi_out=T_IY T_IZ T_XX chi, the unique closest member has fidelity
F=(17+3 sqrt(3)+4 sqrt(6))/32 ~0.999815981.
"""
from collections import deque
import numpy as np
from src.three_t_simple_state_certificate import (
    AXES,ALL,START,rotate,plus,times,minus,sign)

GAUSS={
    "I": np.eye(2,dtype=complex),
    "X": np.array([[0,1],[1,0]],complex),
    "Y": np.array([[0,-1j],[1j,0]],complex),
    "Z": np.diag([1,-1]).astype(complex),
}
P={k:np.kron(GAUSS[k[0]],GAUSS[k[1]]) for k in ALL}
I=GAUSS["I"]
HNUM=GAUSS["X"]+GAUSS["Z"]  # sqrt(2) * H, all integer entries
S=np.diag([1,1j]).astype(complex)
CNOT=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],complex)
GENERATORS=(
    ("H0",np.kron(HNUM,I),2),
    ("H1",np.kron(I,HNUM),2),
    ("S0",np.kron(S,I),1),
    ("S1",np.kron(I,S),1),
    ("CNOT",CNOT,1),
)

def signed_action(U,scale):
    """Exact Gaussian-integer matrix equality U P U† = scale*(±Q)."""
    mapping={}
    for p in ALL:
        transformed=U@P[p]@U.conj().T
        matches=[(q,sgn) for q in ALL for sgn in (-1,1)
                 if np.array_equal(transformed,scale*sgn*P[q])]
        assert len(matches)==1,(p,matches)
        mapping[p]=matches[0]
    assert mapping["II"]==("II",1)
    return mapping

ACTIONS=tuple((label,signed_action(U,scale))
              for label,U,scale in GENERATORS)

def fiducial_signature():
    """Exact doubled Pauli expectations of (1,i,i,i)/2."""
    v=np.array([1,1j,1j,1j],complex)
    result=[]
    for label in AXES:
        n=np.vdot(v,P[label]@v)
        assert n.imag==0 and int(n.real)==n.real and int(n.real)%2==0
        result.append(int(n.real)//2) # r_P = n/4; signature = 2*r_P
    assert sum(x*x for x in result)==12
    assert set(result).issubset({-1,0,1})
    return tuple(result)

def orbit():
    seed=fiducial_signature()
    found={seed:()}
    todo=deque([seed])
    while todo:
        v=todo.popleft()
        for name,action in ACTIONS:
            tmp={}
            for axis,value in zip(AXES,v):
                out,sgn=action[axis]
                tmp[out]=value*sgn
            new=tuple(tmp[axis] for axis in AXES)
            if new not in found:
                found[new]=found[v]+(name,)
                todo.append(new)
    assert len(found)==480 # distinct rays by Pauli expectation fingerprint
    for v in found:
        assert sum(x*x for x in v)==12
    return found

def output_pauli_numerators(word,signs):
    v=START
    for a,sgn in zip(word,signs):
        v=rotate(v,ALL.index(a)-1,sgn)
    assert v[0]==(64,0,0,0)
    return v[1:]

def overlap_numerator(signature,output):
    """F=Tr(rho sigma)=(128 + sum_i signature_i*output_i)/512."""
    n=(128,0,0,0)
    for x,v in zip(signature,output):
        n=plus(n,times(v,x))
    return n

def max_orbit_fidelity(output,signatures):
    best=None;next_best=None;argmax=()
    for signature,word in signatures.items():
        num=overlap_numerator(signature,output)
        if best is None or sign(minus(num,best))>0:
            next_best=best;best=num;argmax=word
        elif next_best is None or sign(minus(num,next_best))>0:
            next_best=num
    assert best is not None and next_best is not None
    assert sign(minus(best,next_best))>0
    return best,next_best,argmax

def exact_certificate(verbose=True):
    signatures=orbit()
    out2=output_pauli_numerators(("XX","IZ","IY"),(1,1,1))
    b,second,word=max_orbit_fidelity(out2,signatures)
    assert b==(272,0,48,64),b
    assert second==(228,14,28,50),second
    assert word==("H0","H1","S1"),word
    # The 1-CNOT *magic-optimal* output (not necessarily its best-fidelity
    # circuit) has an independent Clifford-orbit fidelity comparison.
    out1=output_pauli_numerators(("ZX","IY","ZI"),(-1,-1,-1))
    b1,second1,word1=max_orbit_fidelity(out1,signatures)
    assert b1==(156,66,52,62),(b1,word1)
    if verbose:
        print("PASS: 480 exactly generated maximal-magic Clifford signatures")
        print("PASS: closest 2-CNOT output fidelity = (17+3sqrt3+4sqrt6)/32")
        print("PASS: unique nearest representative (I tensor S)(H tensor H)(1,i,i,i)/2")
        print("PASS: 2nd-nearest and one-CNOT-magic-optimal output checked exactly")
    return b,second,b1,word,word1

if __name__=="__main__":
    exact_certificate()
