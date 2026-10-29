"""Exact two-T input-conditioned Schmidt-phase frontier; only SymPy needed.

python -m src.two_t_frontier_certificate
Input: cos(theta)|00> + exp(i*pi/4)sin(theta)|11>.
Arbitrary two-qubit Clifford routing, no ancillas or Clifford depth limit.
"""
from itertools import product
import sympy as S

q,z,t,w=S.symbols("q z t w",real=True)
h=S.sqrt(2)/2
AXES=["".join(x) for x in product("IXYZ",repeat=2)]
LOCAL={
"I":{"I":(0,"I"),"X":(0,"X"),"Y":(0,"Y"),"Z":(0,"Z")},
"X":{"I":(0,"X"),"X":(0,"I"),"Y":(1,"Z"),"Z":(3,"Y")},
"Y":{"I":(0,"Y"),"X":(3,"Z"),"Y":(0,"I"),"Z":(1,"X")},
"Z":{"I":(0,"Z"),"X":(1,"Y"),"Y":(3,"X"),"Z":(0,"I")}}
INITIAL={p:S.Integer(0) for p in AXES}
INITIAL.update({"II":1,"ZZ":1,"IZ":z,"ZI":z,
                "XX":q*h,"XY":q*h,"YX":q*h,"YY":-q*h})

def product_label(a,b):
    terms=[LOCAL[x][y] for x,y in zip(a,b)]
    return sum(k for k,_ in terms)%4,"".join(v for _,v in terms)

def rotate(v,axis):
    out=dict(v)
    for p in AXES:
        k,other=product_label(axis,p)
        if k%2:
            out[p]=S.expand(h*(v[p]+(1 if k==3 else -1)*v[other]))
    return out

def moment(v):
    return S.expand(sum(x**4 for x in v.values()))

def moments_by_word():
    return {(a,b):moment(rotate(rotate(INITIAL,a),b))
            for a,b in product(AXES[1:],repeat=2)}

def to_t(v):
    out=S.Integer(0)
    for (j,k),co in S.Poly(v,q,z).terms():
        if j%2 or k%2:
            raise ValueError("Radical class")
        out+=co*t**(j//2)*(1-t)**(k//2)
    return S.expand(out)

def bernstein_coefficients(p,left,right):
    poly=S.Poly(S.expand(p.subs(t,left+(right-left)*w)),w)
    assert poly.degree()<=2
    return tuple(S.factor(sum(poly.nth(k)*S.binomial(i,k)/S.binomial(2,k)
                   for k in range(i+1))) for i in range(3))

def certify(verbose=True):
    words=moments_by_word()
    classes={}
    for key,m in words.items():
        classes.setdefault(m,[]).append(key)
    assert len(words)==225 and len(classes)==15
    A,B,C=[words[x] for x in [("IX","XI"),("IX","ZY"),("IX","ZX")]]
    a,b,c=map(to_t,[A,B,C])
    assert a==(36-20*t+25*t*t)/16
    assert b==(44-44*t+33*t*t)/16
    assert c==(64-64*t+28*t*t)/16
    t1=(3-S.sqrt(5))/2
    t2=2*(S.sqrt(2)-1)
    assert S.simplify((a-b).subs(t,t1))==0
    assert S.simplify((b-c).subs(t,t2))==0
    assert S.simplify((a-c)+(3*t-2)*(t-14)/16)==0
    assert S.Rational(3,8)<t1<S.Rational(2,5)
    assert S.Rational(4,5)<t2<S.Rational(5,6)
    regions=[(S.S(0),S.Rational(2,5),a),
             (S.Rational(3,8),S.Rational(5,6),b),
             (S.Rational(4,5),S.S(1),c)]
    polynomial_count=0
    radical=[]
    for m,axis_words in classes.items():
        if m in (A,B,C): continue
        if any(j%2 or k%2 for (j,k),co in S.Poly(m,q,z).terms()):
            radical.append((m,axis_words))
            continue
        expression=to_t(m)
        for L,R,reference in regions:
            coeffs=bernstein_coefficients(expression-reference,L,R)
            assert all(x>=0 for x in coeffs),(axis_words[0],coeffs)
        polynomial_count+=1
    assert polynomial_count==10 and len(radical)==2
    core=(44+36*t-29*t*t)/16
    N=S.expand(16*(core-a))
    assert N==8+56*t-54*t*t
    assert bernstein_coefficients(N,S.S(0),S.S(1))==(8,36,10)
    gap=S.factor(N*N-2*t*(1-t)*(8-28*t)**2)
    P=1121*t**4-2128*t**3+824*t*t+192*t+16
    assert S.expand(gap-4*P)==0
    poly=S.Poly(P,t)
    coefs=tuple(S.factor(sum(poly.nth(k)*S.binomial(i,k)/S.binomial(4,k)
                  for k in range(i+1))) for i in range(5))
    assert coefs==(16,64,S.Rational(748,3),40,25)
    for m,axis_words in radical:
        reduced=S.expand(m.subs({q**4:t**2,z**4:(1-t)**2,
                  q**2*z**2:t*(1-t),q**3*z:q*z*t,
                  q*z**3:q*z*(1-t)}))
        target=core+S.sqrt(2)*q*z*(8-28*t)/16
        assert S.simplify(reduced-target)==0 or S.simplify(reduced-(2*core-target))==0
    # Certify "at most two": a single T has optimal R_one=3*R_in/4
    # by Zhu and an explicit saturating axis for this family.
    r_initial=4-4*t+3*t*t
    r_one=S.expand(S.Rational(3,4)*r_initial)
    for L,R,reference in regions:
        coefs=bernstein_coefficients(S.expand(r_one-reference),L,R)
        assert all(value>=0 for value in coefs),("one-T case",coefs)
    if verbose:
        print("PASS 225 words, 15 exact classes")
        print("PASS 30 rational Bernstein certificates for 10 inactive polynomial classes")
        print("PASS two radical classes excluded by strict quartic Bernstein certificate")
        print("PASS three exact branch crossings")
        print("t1=",t1,"t2=",t2)
        print("A=",a," B=",b," C=",c)
        for m,axis_words in classes.items():
            print(axis_words[0],len(axis_words))
    return a,b,c,t1,t2,classes

if __name__=="__main__":
    certify()
