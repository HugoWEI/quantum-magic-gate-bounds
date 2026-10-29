"""Exact exhaustive two-qubit one-T non-saturation certificate.

A Bell state locally rotated by Rx(pi/8)Ry(pi/8) has R2=49/16 and
concurrence 1. All 15 Clifford-conjugate Pauli T deficits are positive.
"""
from itertools import product
from sympy import Rational, sqrt, simplify

paulis=["".join(a) for a in product("IXYZ",repeat=2)]

def local_product(x,y):
    if x=="I": return y
    if y=="I": return x
    if x==y: return "I"
    return ({"X","Y","Z"}-{x,y}).pop()

def product_label(x,y):
    return "".join(local_product(a,b) for a,b in zip(x,y))

def anticommuting(x,y):
    return sum(a!="I" and b!="I" and a!=b
               for a,b in zip(x,y))%2==1

v=(2+sqrt(2))/4
u=(2-sqrt(2))/4
# Squared Pauli expectations for (Rx(pi/8) Ry(pi/8) tensor I)|Phi+>.
r2={p:Rational(0) for p in paulis}
r2.update({"II":1,"XX":v,"XZ":u,"YX":u*u,"YY":v,
           "YZ":u*v,"ZX":u*v,"ZY":u,"ZZ":v*v})

def deficits():
    out={}
    for axis in paulis:
        if axis=="II": continue
        commuting=[p for p in paulis if not anticommuting(axis,p)]
        d=sum((r2[p]**2 for p in commuting),Rational(0))
        visited=set()
        for p in paulis:
            if not anticommuting(axis,p) or p in visited: continue
            partner=product_label(axis,p)
            assert anticommuting(axis,partner) and partner!=p
            visited.update((p,partner))
            a,b=r2[p],r2[partner]
            d+=-(a*a+b*b)+12*a*b
        out[axis]=simplify(d)
    return out

def verify():
    d=deficits()
    assert len(d)==15
    assert simplify(sum(v*v for v in r2.values())-Rational(49,16))==0
    for axis,val in d.items():
        assert val.is_positive is True,(axis,val)
    assert d["XY"]==Rational(1,16)
    print("PASS exact: R2=49/16 and all 15 one-T deficits >0")
    for p in sorted(d):
        print(f"{p}: D={d[p]} (~{float(d[p]):.10f})")

if __name__=="__main__":
    verify()
