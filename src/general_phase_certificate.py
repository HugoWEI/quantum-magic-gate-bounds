"""Exact general-phase two-T frontier; 225 words / 21 moment classes.

Domain: 0<=theta,phi<=pi/4, state cos(theta)|00>+exp(i phi)sin(theta)|11>.
Arbitrary global two-qubit Clifford routing, no ancilla, 0/1/2 T gates.
Proof: 18 inactive classes excluded via 42 exact Q(sqrt2) Bernstein
rectangles. Run: python -m src.general_phase_certificate
"""
from fractions import Fraction as F
from itertools import product
from math import comb
import sympy as S
from src.two_t_frontier_certificate import AXES,q,z,rotate,moment

u,v=S.symbols("u v",real=True)
r,s=S.symbols("r s",real=True)
kappa=S.sqrt(2)-1
INPUT={p:S.Integer(0) for p in AXES}
INPUT.update({"II":1,"ZZ":1,"IZ":z,"ZI":z,
              "XX":q*u,"XY":q*v,"YX":q*v,"YY":-q*u})
WORDS=list(product(AXES[1:],repeat=2))
A_WORD=("IX","YI");B_WORD=("IX","ZY");C_WORD=("IX","ZX")
ZERO=(F(0),F(0))

def all_moments():
    return {word:moment(rotate(rotate(INPUT,word[0]),word[1]))
            for word in WORDS}

def rationalize(expr):
    """Multiply by positive (1+r²)^4(1+(kappa*s)²)^4.
    r=tan(theta), kappa*s=tan(phi/2), r,s in [0,1].
    """
    out=0
    for (a,b,c,d),co in S.Poly(expr,q,z,u,v).terms():
        assert a+b<=4 and c+d<=4
        out+=co*(2*r)**a*(1-r*r)**b*(1+r*r)**(4-a-b) * (
            (1-kappa*kappa*s*s)**c*(2*kappa*s)**d *
            (1+kappa*kappa*s*s)**(4-c-d))
    return S.Poly(S.expand(out),r,s)

def pair(expr):
    e=S.expand(expr)
    a=e.coeff(S.sqrt(2),0);b=e.coeff(S.sqrt(2),1)
    assert S.simplify(e-a-b*S.sqrt(2))==0
    return F(a),F(b)
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def times(a,k):return (a[0]*k,a[1]*k)
def nonnegative(ab):
    a,b=ab
    if b>=0:return a>=0 or 2*b*b>=a*a
    return a>0 and a*a>=2*b*b

def bernstein(poly):
    """Degree (8,8) Bernstein coefficients on [0,1]^2 in Q(sqrt(2))."""
    power=[[ZERO for j in range(9)] for i in range(9)]
    for (i,j),co in poly.terms():power[i][j]=pair(co)
    out=[[ZERO for j in range(9)] for i in range(9)]
    for i in range(9):
        for j in range(9):
            a=ZERO
            for k in range(i+1):
                for l in range(j+1):
                    a=add(a,times(power[k][l],
                        F(comb(i,k)*comb(j,l),comb(8,k)*comb(8,l))))
            out[i][j]=a
    return out

def difference(a,b):
    return [[sub(x,y) for x,y in zip(rowa,rowb)]
            for rowa,rowb in zip(a,b)]
def midpoint(vec):
    vec=vec[:];left=[vec[0]];right=[vec[-1]]
    while len(vec)>1:
        vec=[times(add(a,b),F(1,2)) for a,b in zip(vec,vec[1:])]
        left.append(vec[0]);right.append(vec[-1])
    return left,right[::-1]
def bisect(mat,axis):
    a=[[ZERO]*9 for _ in range(9)];b=[[ZERO]*9 for _ in range(9)]
    if axis==0:
        for j in range(9):
            l,h=midpoint([mat[i][j] for i in range(9)])
            for i in range(9):a[i][j]=l[i];b[i][j]=h[i]
    else:
        for i in range(9):a[i],b[i]=midpoint(mat[i])
    return a,b
def valid(mat):
    return all(nonnegative(x) for row in mat for x in row)

def verify_branches(words):
    t,x=S.symbols("t x",real=True)
    def reduce(expr):
        a=0
        for (i,j,k,l),co in S.Poly(expr,q,z,u,v).terms():
            assert all(p%2==0 for p in (i,j,k,l))
            a+=co*t**(i//2)*(1-t)**(j//2)*(1-x)**(k//2)*x**(l//2)
        return S.expand(a)
    A,B,C=[reduce(words[w]) for w in (A_WORD,B_WORD,C_WORD)]
    K=1-t+t*t*(1-x+x*x)
    assert A==S.expand((9-8*t+8*t*t+6*t*x-8*t*t*x+9*t*t*x*x)/4)
    assert B==S.expand(S.Rational(11,4)*K)
    assert C==S.expand((16-16*t+(9-8*x+8*x*x)*t*t)/4)
    assert reduce(moment(INPUT))==S.expand(4*K)
    assert S.factor(A-C)==(t*x-t+7)*(t*x+t-1)/4
    xstar=S.sqrt(5)-2;tstar=(1+S.sqrt(5))/4
    assert S.simplify((A-B).subs({x:xstar,t:tstar}))==0
    assert S.simplify((B-C).subs({x:xstar,t:tstar}))==0
    resultant=S.factor(S.resultant(4*(A-B),4*(B-C),t))
    assert resultant.has(x*x+4*x-1)
    # B alone produces 11/16 R_in < 3/4 R_in (best 1-T).
    assert S.expand(S.Rational(3,4)*4*K-B)==S.expand(K/4)

def certify(verbose=True):
    words=all_moments()
    classes={}
    for word,expr in words.items():classes.setdefault(expr,[]).append(word)
    assert len(words)==225 and len(classes)==21
    verify_branches(words)
    exps=list(classes)
    coeff=[bernstein(rationalize(p)) for p in exps]
    indices=[exps.index(words[w]) for w in (A_WORD,B_WORD,C_WORD)]
    proof={}
    for i,expr in enumerate(exps):
        if i in indices:continue
        mats=[difference(coeff[i],coeff[j]) for j in indices]
        leaves=[]
        def visit(matrices,depth=0,axis=0,box=(F(0),F(1),F(0),F(1))):
            for j,mat in enumerate(matrices):
                if valid(mat):
                    leaves.append((box,"ABC"[j]))
                    return
            if depth>=16:raise AssertionError(("unproved class",i,box))
            pieces=[bisect(mat,axis) for mat in matrices]
            a,b,c,d=box
            if axis==0:
                mid=(a+b)/2;boxes=((a,mid,c,d),(mid,b,c,d))
            else:
                mid=(c+d)/2;boxes=((a,b,c,mid),(a,b,mid,d))
            for half in (0,1):
                visit([p[half] for p in pieces],depth+1,1-axis,boxes[half])
        visit(mats)
        proof[classes[expr][0]]=leaves
    assert len(proof)==18
    assert sum(map(len,proof.values()))==42
    if verbose:
        print("PASS: 225 two-T words, exactly 21 quartic classes")
        print("PASS: 18 inactive classes dominated on 42 exact Q(sqrt2) Bernstein rectangles")
        print("PASS: 3 attainable branch formulas; exact triple point and at-most-2-T comparison")
        for word,leaves in proof.items():print(word,len(leaves),"cells")
    return words,classes,proof

if __name__=="__main__":certify()
