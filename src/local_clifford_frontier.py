"""Exact at-most-two-T frontier with LOCAL-ONLY Clifford routing.

Input cos(theta)|00> + exp(i phi)sin(theta)|11>.
Arbitrary single-qubit Cliffords allowed, NO entangling Cliffords.
Not a theorem about physical hardware circuit depth.
"""
import sympy as S
from src.general_phase_certificate import (
    all_moments,rationalize,bernstein,difference,valid,A_WORD,INPUT,u,v)
from src.two_t_frontier_certificate import AXES,moment,q,z

D_WORD=("IX","IY")
def certify(verbose=True):
    words=all_moments()
    local=[p for p in AXES if p.count("I")==1]
    allowed={(a,b):words[(a,b)] for a in local for b in local}
    classes={}
    for key,e in allowed.items():classes.setdefault(e,[]).append(key)
    assert len(allowed)==36 and len(classes)==5
    A,D=words[A_WORD],words[D_WORD]
    assert A!=D
    ref=bernstein(rationalize(A))
    for e,ws in classes.items():
        if e in (A,D):continue
        assert valid(difference(bernstein(rationalize(e)),ref)),ws[0]
    t,x=S.symbols("t x",real=True)
    def reduce(e):
        out=0
        for (i,j,k,l),co in S.Poly(e,q,z,u,v).terms():
            assert all(a%2==0 for a in (i,j,k,l))
            out+=co*t**(i//2)*(1-t)**(j//2)*(1-x)**(k//2)*x**(l//2)
        return S.expand(out)
    Dform=(11-11*t+(9+5*x-5*x*x)*t*t)/4
    assert S.expand(reduce(D)-Dform)==0
    initial=reduce(moment(INPUT))
    assert S.expand(initial-4*(1-t+t*t*(1-x+x*x)))==0
    # Zhu's best one-T moment, attained for this family, is 3/4 R_in.
    if verbose:
        print("PASS: 36 local Pauli-axis words form 5 exact classes")
        print("PASS: 3 inactive classes dominated by A via exact Q(sqrt2) Bernstein coefficients")
        print("Sharp 2T: min(A,D); at-most-2T: min(A,D,3*R_in/4)")
    return classes

if __name__=="__main__":certify()
