"""Universal <=1-CNOT realization of any TWO Pauli-T rotations on two qubits.

Mathematical scope: Clifford-invariant state functional (e.g. M2), <=2 T
and arbitrary single-qubit Cliffords; physical CNOT count <=1 (either direction).
No ancillas, measurements, geometric restrictions, or single-qubit depth bound.

Certifies all 225 ordered axes with signed conjugation identities, not merely
numerical optimization. build_witnesses() is named all_witnesses().
"""
from __future__ import annotations
from itertools import product
import numpy as np
from src.magic_bounds import ONE, X, Y, Z, paulis, normalize

I = ONE
H = (X+Z)/np.sqrt(2)
S = np.diag([1,1j]).astype(complex)
CNOT_01 = np.array([[1,0,0,0], [0,1,0,0], [0,0,0,1], [0,0,1,0]],complex)
CNOT_10 = np.array([[1,0,0,0], [0,0,0,1], [0,0,1,0], [0,1,0,0]],complex)
SINGLE = {"X":X,"Y":Y,"Z":Z}
AXES = tuple(k for k in paulis(2) if k!="II")
LOCAL = tuple(p for p in AXES if p.count("I")==1)

def axis_image(unitary, local_axis):
    result = unitary@SINGLE[local_axis]@unitary.conj().T
    for name,mat in SINGLE.items():
        sign = int(np.rint(np.real(np.trace(mat@result)/2)))
        if sign and np.allclose(result, sign*mat,atol=1e-12):
            return name,sign
    raise AssertionError("Not a Clifford")

def local_permutation_gates():
    """All six single-qubit Pauli-axis permutations, with H/S word witnesses."""
    found={}; queue=[(I,"I")]
    while queue:
        gate,word=queue.pop(0)
        perm=tuple(axis_image(gate,a)[0] for a in "XYZ")
        if perm in found:continue
        found[perm]=(gate,word)
        for char,mat in (("H",H),("S",S)):
            queue.append((mat@gate,char+word))
    assert len(found)==6
    return tuple((perm,mat,word) for perm,(mat,word) in found.items())

PERMS=local_permutation_gates()

def label_under_local(label,perms):
    return "".join("I" if c=="I" else perms[i]["XYZ".index(c)]
                   for i,c in enumerate(label))

def cnot_label(label,control):
    bits={"I":(0,0),"X":(1,0),"Y":(1,1),"Z":(0,1)}
    rev={v:k for k,v in bits.items()}
    x=[bits[c][0] for c in label];z=[bits[c][1] for c in label]
    target=1-control
    x[target]^=x[control];z[control]^=z[target]
    return "".join(rev[(x[j],z[j])] for j in (0,1))

def map_axis(pauli, unitary):
    transformed=unitary@paulis(2)[pauli]@unitary.conj().T
    for name in LOCAL:
        target=paulis(2)[name]
        sign=int(np.rint(np.real(np.trace(transformed@target)/4)))
        if sign and np.allclose(transformed,sign*target,atol=3e-12):
            return name,sign
    raise AssertionError("Axis is not local after conjugation")

def witness(a,b):
    """Return (U, description, (P',signP), (Q',signQ), CNOT count).

    U conjugates both axes to signed local Paulis, using <=1 CNOT
    BEFORE the two local T gates. Final U^dagger is omitted for M2.
    """
    if a not in AXES or b not in AXES:raise ValueError("Nonidentity two-qubit Pauli axes required")
    if a in LOCAL and b in LOCAL:
        return np.eye(4,dtype=complex),"identity",(a,1),(b,1),0
    for p0,g0,w0 in PERMS:
        for p1,g1,w1 in PERMS:
            x=label_under_local(a,(p0,p1))
            y=label_under_local(b,(p0,p1))
            for control,cn in ((0,CNOT_01),(1,CNOT_10)):
                aa,bb=cnot_label(x,control),cnot_label(y,control)
                if aa in LOCAL and bb in LOCAL:
                    unitary=cn@np.kron(g0,g1)
                    ma=map_axis(a,unitary)
                    mb=map_axis(b,unitary)
                    assert ma[0]==aa and mb[0]==bb
                    return unitary,f"CNOT_{control}{1-control} (L0={w0}, L1={w1})",ma,mb,1
    raise AssertionError(f"No one-CNOT witness for {a}, {b}")

def all_witnesses():
    out={}
    for a,b in product(AXES,repeat=2):out[(a,b)]=witness(a,b)
    assert len(out)==225
    assert sum(item[4]==0 for item in out.values())==36
    assert sum(item[4]==1 for item in out.values())==189
    return out

def signed_t(state,axis,sign):
    v=normalize(state)
    return np.cos(np.pi/8)*v-1j*sign*np.sin(np.pi/8)*(paulis(2)[axis]@v)

def verify_all():
    rng=np.random.default_rng(29)
    all_pairs=all_witnesses()
    for _ in range(4):
        state=normalize(rng.normal(size=4)+1j*rng.normal(size=4))
        for (p,q),(U,_,(a,sa),(b,sb),cost) in all_pairs.items():
            expected=signed_t(signed_t(state,p,1),q,1)
            actual=signed_t(signed_t(U@state,a,sa),b,sb)
            assert np.allclose(actual,U@expected,atol=3e-12), (p,q)
            assert cost in (0,1)
    print("PASS all 225 axis pairs, signed Clifford identities, 4 arbitrary complex states")
    return all_pairs

if __name__=="__main__":verify_all()
