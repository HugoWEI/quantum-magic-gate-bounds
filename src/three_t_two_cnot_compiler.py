"""Two-CNOT realization of any 3 Pauli T rotations, up to final Clifford.

Localize first two Pauli axes using <=1 CNOT (previous universal
lemma), apply their local signed T rotations. Then localize the third
transformed axis using <=1 additional CNOT, apply its local signed T.
Final Clifford U2 U1 is ignored only for Clifford-invariant objectives.
"""
import numpy as np
from src.one_cnot_universality import AXES,LOCAL,witness,signed_t
from src.magic_bounds import paulis,normalize,fourth_moment

def match_axis(mat):
    for axis in AXES:
        for sign in (-1,1):
            if np.allclose(mat,sign*paulis(2)[axis],atol=1e-12):
                return axis,sign
    raise AssertionError("Expected Clifford-conjugated Hermitian Pauli")

def compile_three(p,q,r):
    U1,desc1,a,b,cost1=witness(p,q)
    transformed,phase=match_axis(U1@paulis(2)[r]@U1.conj().T)
    U2,desc2,c,_,cost2=witness(transformed,transformed)
    axis3=(c[0],c[1]*phase)
    assert cost1+cost2<=2
    return {"first_unitary":U1,"second_unitary":U2,
            "local_axes":(a,b,axis3),"cnot_count":cost1+cost2,
            "descriptions":(desc1,desc2)}

def apply_compiled(psi,compiled):
    v=compiled["first_unitary"]@normalize(psi)
    for axis in compiled["local_axes"][:2]:
        v=signed_t(v,*axis)
    v=compiled["second_unitary"]@v
    return signed_t(v,*compiled["local_axes"][2])

def apply_target(psi,p,q,r):
    v=normalize(psi)
    for axis in (p,q,r):v=signed_t(v,axis,1)
    return v

def verify():
    psi=normalize(np.array([-1+3j,-7-1j,-1+1j,-1+4j],complex))
    for word in [("YY","XI","XY"),("IX","IY","XX"),
                 ("XX","YZ","XI"),("XY","ZX","ZY")]:
        compiled=compile_three(*word)
        expected=compiled["second_unitary"]@compiled["first_unitary"]@apply_target(psi,*word)
        actual=apply_compiled(psi,compiled)
        assert np.allclose(expected,actual,atol=2e-12),word
    result=compile_three("YY","XI","XY")
    assert result["cnot_count"]==2
    obtained=fourth_moment(apply_compiled(psi,result))
    target=1103764401/623201296
    assert abs(obtained-target)<1e-12
    print("PASS: constructive exactly two-CNOT 3-T optimum",target)
    return result

if __name__=="__main__":verify()
