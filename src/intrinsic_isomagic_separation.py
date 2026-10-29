"""Exact orientation-sensitive separation with unavoidable pre-existing magic.

A and B are partially entangled (C=sqrt(3)/2) with the same R_in=91/32.
A's exact optimal two-T fourth moment exceeds that attained by a single
specified Pauli word on B. We do *not* claim to know B's exact optimum.
"""
from fractions import Fraction as F
import sympy as S
from src.two_t_frontier_certificate import AXES,rotate,moment

q,c,s=S.symbols("q c s",positive=True)
z=S.Rational(1,2)
# B: apply Rx(pi/8) to the first qubit of
# cos(pi/6)|00>+sin(pi/6)|11>.
EXPECT={p:S.Integer(0) for p in AXES}
EXPECT.update({"II":1,"IZ":z,"XX":q,"YI":-s*z,"ZI":c*z,
               "YY":-c*q,"ZY":-s*q,"YZ":-s,"ZZ":c})

def rational_upper(poly,brackets):
    total=F(0)
    for powers,coefficient in S.Poly(poly,q,c,s).terms():
        coefficient=F(coefficient)
        value=F(1)
        for letter,power in zip((q,c,s),powers):
            value*=brackets[letter][1 if coefficient>=0 else 0]**power
        total+=coefficient*value
    return total

def certify(verbose=True):
    q0=S.sqrt(3)/2
    c0=S.sqrt(2+S.sqrt(2))/2
    s0=S.sqrt(2-S.sqrt(2))/2
    x=(6-S.sqrt(10))/12
    t=S.Rational(3,4)
    R_initial_A=4*(1-t+t*t*(1-x+x*x))
    R_initial_B=S.simplify(moment(EXPECT).subs({q:q0,c:c0,s:s0}))
    assert S.simplify(R_initial_A-S.Rational(91,32))==0
    assert S.simplify(R_initial_B-S.Rational(91,32))==0
    # A's *global optimum* is certified by general_phase_frontier.py/notes.
    A=(9-8*t+8*t*t+6*t*x-8*t*t*x+9*t*t*x*x)/4
    B=S.Rational(11,4)*(1-t+t*t*(1-x+x*x))
    C=(16-16*t+(9-8*x+8*x*x)*t*t)/4
    assert S.simplify(A-(S.Rational(1167,512)-27*S.sqrt(10)/256))==0
    assert (B-A).is_positive and (C-A).is_positive
    witness=moment(rotate(rotate(EXPECT,"ZX"),"IZ"))
    exact=S.simplify(witness.subs({q:q0,c:c0,s:s0}))
    bounds={q:(F(866,1000),F(867,1000)),
            c:(F(923,1000),F(925,1000)),
            s:(F(382,1000),F(384,1000))}
    for letter,value in [(q,q0),(c,c0),(s,s0)]:
        lower,upper=bounds[letter]
        assert S.simplify(value-S.Rational(lower.numerator,lower.denominator)).is_positive
        assert S.simplify(S.Rational(upper.numerator,upper.denominator)-value).is_positive
    certified_upper=rational_upper(witness,bounds)
    # sqrt(10)<16/5, so A is bounded below by the rational quantity.
    certified_lower_A=S.Rational(1167,512)-S.Rational(27,256)*S.Rational(16,5)
    assert certified_upper<F(19,10)<certified_lower_A
    if verbose:
        print("PASS: same C=sqrt(3)/2, same R_in=91/32, intrinsic magic")
        print("PASS: A exact optimal R=",S.simplify(A),float(A))
        print("PASS: B word (ZX,IZ) gives R=",exact,float(exact))
        print("PASS: strict exact rational bound R_B(word)<1.9<R_A(best)")
    return S.simplify(A),exact

if __name__=="__main__":certify()
