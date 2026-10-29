"""Exact isomagic two-T separation with rational interval proof.

psi_A: (|00> + exp(i*phi)|11>)/sqrt2, cos(2*phi)=1/4.
psi_B: (Rx(pi/8)Ry(pi/8) tensor I)|Phi+>.
Both C=1 and R_in=49/16. Different maximal two-T magic gains.
"""
from itertools import product
from fractions import Fraction as F
import sympy as S
from src.two_t_frontier_certificate import AXES,rotate,moment

co,si=S.symbols("co si",real=True)
STATE={p:S.Integer(0) for p in AXES}
STATE.update({"II":1,"XX":co,"XZ":si,"YX":si**2,"YY":-co,
              "YZ":-co*si,"ZX":-co*si,"ZY":-si,"ZZ":co**2})

def rational_bracket(value,digits=18):
    """Propose decimal endpoints, then certify using exact inequalities."""
    scale=10**digits
    lo=F(int(S.floor(S.N(value,digits+25)*scale)),scale)
    return lo,lo+F(1,scale)

def parameters(digits=18):
    low2,hi2=rational_bracket(S.sqrt(2),digits)
    cl,cu=rational_bracket(S.cos(S.pi/8),digits)
    sl,su=rational_bracket(S.sin(S.pi/8),digits)
    assert low2>0 and low2**2<2<hi2**2
    assert 4*cl**2<2+low2 and 4*cu**2>2+hi2
    assert 4*sl**2<2-hi2 and 4*su**2>2-low2
    return cl,cu,sl,su

def rational_lower(poly,brackets):
    """Exact rational lower bound: c,s positive and each monomial monotone."""
    cl,cu,sl,su=brackets
    result=F(0)
    for (i,j),coefficient in S.Poly(poly,co,si).terms():
        a=F(coefficient)
        result+=a*(cl**i*sl**j if a>=0 else cu**i*su**j)
    return result

def certify(verbose=True):
    words={(a,b):moment(rotate(rotate(STATE,a),b))
           for a,b in product(AXES[1:],repeat=2)}
    assert len(words)==225
    classes=set(words.values())
    assert len(classes)==70
    best=words[("IZ","ZX")]
    cv,sv=S.cos(S.pi/8),S.sin(S.pi/8)
    exact=S.simplify(best.subs({co:cv,si:sv}))
    target=(597-70*S.sqrt(2)+(32*S.sqrt(2)-56)*S.sqrt(2+S.sqrt(2)))/256
    assert S.simplify(exact-target)==0
    bounds=parameters()
    positives=0;attain=0
    for formula in classes:
        diff=S.expand(formula-best)
        if S.simplify(diff.subs({co:cv,si:sv}))==0:
            attain+=1
        else:
            assert rational_lower(diff,bounds)>0
            positives+=1
    assert positives==69 and attain==1
    assert rational_lower(best-S.Rational(57,32),bounds)>0
    assert S.simplify(moment(STATE).subs({co:cv,si:sv})-S.Rational(49,16))==0
    if verbose:
        print("PASS 225 words, 70 polynomial classes, 69 strict rational certificates")
        print("State A: R_out min=57/32, gain=log2(98/57)")
        print("State B: R_out min=",exact," approximately ",exact.evalf())
        print("Both: concurrence=1, R_in=49/16, so C and M2 do not fix F2")
    return exact

if __name__=="__main__":certify()
