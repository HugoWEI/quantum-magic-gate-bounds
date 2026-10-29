"""Exact two-CNOT magic separation for a simple rotated-Schmidt input.

chi = (Rx(pi/4) tensor I)[cos(pi/12)|00> + exp(i*pi/12)sin(pi/12)|11>].
With at most 3 T gates and arbitrary single-qubit Cliffords, an
unrestricted output has a strictly better Pauli fourth moment than ANY
0/1-CNOT circuit. No ancillas/measurement. Physical CNOT count, not depth.

Exact ring: Q(sqrt(2),sqrt(3)) represented as integer coefficients
(a,b,c,d) for a+b*sqrt(2)+c*sqrt(3)+d*sqrt(6).
Each initial Pauli expectation is /8; after k T it is /[8*2**k].
The program compares every result with integer-certified radical intervals.
"""
from itertools import product
from math import isqrt, sqrt, log2
from src.one_cnot_universality import AXES, LOCAL, PERMS, label_under_local, cnot_label
from src.two_t_frontier_certificate import product_label

ALL=("II",)+tuple(AXES)
LOOKUP={p:i for i,p in enumerate(ALL)}
O=(0,0,0,0)
INITIAL={p:O for p in ALL}
INITIAL.update({
    "II":(8,0,0,0),"IZ":(0,0,4,0),
    "ZI":(0,0,0,2),"YI":(0,0,0,-2),
    "XX":(0,1,0,1),"XY":(0,-1,0,1),
    "YX":(-1,0,1,0),"YY":(-1,0,-1,0),
    "YZ":(0,-4,0,0),"ZX":(-1,0,1,0),
    "ZY":(-1,0,-1,0),"ZZ":(0,4,0,0)
})
START=tuple(INITIAL[p] for p in ALL)
def plus(x,y): return tuple(a+b for a,b in zip(x,y))
def minus(x,y): return tuple(a-b for a,b in zip(x,y))
def times(x,k): return tuple(a*k for a in x)
def times_root2(x):
    a,b,c,d=x
    return (2*b,a,2*d,c)
def mul(x,y):
    a,b,c,d=x;e,f,g,h=y
    return (a*e+2*b*f+3*c*g+6*d*h,
            a*f+b*e+3*c*h+3*d*g,
            a*g+c*e+2*b*h+2*d*f,
            a*h+d*e+b*g+c*f)

MIX=[]
for p in AXES:
    row=[]
    for q in ALL:
        phase,other=product_label(p,q)
        row.append((LOOKUP[other],1 if phase==3 else -1 if phase==1 else 0))
    MIX.append(tuple(row))

def rotate(v,axis,sgn):
    result=[]
    for a,(j,phase) in zip(v,MIX[axis]):
        result.append(times_root2(plus(a,times(v[j],sgn*phase)))
                      if phase else times(a,2))
    return tuple(result)

def moment(v,depth):
    result=O
    for x in v:
        squared=mul(x,x)
        result=plus(result,mul(squared,squared))
    return times(result,2**(4*(3-depth))) # denominator 64**4

PREC=10**40
RAD={n:(isqrt(n*PREC*PREC),isqrt(n*PREC*PREC)+1) for n in (2,3,6)}
def sign(n):
    if n==O:return 0
    low=high=n[0]*PREC
    for c,r in zip(n[1:],(2,3,6)):
        a,b=RAD[r]
        low+=c*(a if c>=0 else b)
        high+=c*(b if c>=0 else a)
    if low>0:return 1
    if high<0:return -1
    raise ArithmeticError("Increase radical interval precision")

def less(x,y):return sign(minus(x,y))<0
def float_value(n):
    a,b,c,d=n
    return (a+b*sqrt(2)+c*sqrt(3)+d*sqrt(6))/(64**4)

def one_cnot_triples():
    out=set(product(LOCAL,repeat=3))
    for p0,_,_ in PERMS:
        for p1,_,_ in PERMS:
            for ctrl in (0,1):
                after=tuple({label_under_local(cnot_label(p,ctrl),(p0,p1))
                             for p in LOCAL})
                for cut in range(4):
                    out.update(product(*([LOCAL]*cut+[after]*(3-cut))))
    assert len(out)==2457
    return out

def certify(verbose=True):
    global_best=(moment(START,0),())
    restricted_best=global_best
    for i,p in enumerate(AXES):
        a=rotate(START,i,1)
        m=moment(a,1)
        if less(m,global_best[0]):global_best=(m,(p,))
        if less(m,restricted_best[0]):restricted_best=(m,(p,))
        for j,q in enumerate(AXES):
            b=rotate(a,j,1)
            m=moment(b,2)
            if less(m,global_best[0]):global_best=(m,(p,q))
            if less(m,restricted_best[0]):restricted_best=(m,(p,q))
            for k,r in enumerate(AXES):
                m=moment(rotate(b,k,1),3)
                if less(m,global_best[0]):global_best=(m,(p,q,r))

    words=one_cnot_triples()
    by_prefix={}
    for p,q,r in words:
        by_prefix.setdefault((AXES.index(p),AXES.index(q)),[]).append(AXES.index(r))
    for signs in product((-1,1),repeat=3):
        for (i,j),lasts in by_prefix.items():
            v=rotate(rotate(START,i,signs[0]),j,signs[1])
            for k in lasts:
                m=moment(rotate(v,k,signs[2]),3)
                if less(m,restricted_best[0]):
                    restricted_best=(m,((AXES[i],AXES[j],AXES[k]),signs))

    assert global_best==((33389568,-774144,-1806336,81920),
                         ("XX","IZ","IY"))
    assert restricted_best==((30620672,0,-266240,0),
                             (("ZX","IY","ZI"),(-1,-1,-1))) or (
        restricted_best[0]==(30620672,0,-266240,0))
    gap=minus(restricted_best[0],global_best[0])
    assert gap==(-2768896,774144,1540096,-81920)
    assert sign(minus(times(gap,25),(64**4,0,0,0)))>0  # gap > 1/25
    if verbose:
        print("PASS exact: 3616 unrestricted, 19897 conservative <=1-CNOT candidates")
        print("Input R0=621/256; C=1/2")
        print("Unrestricted:",global_best,"R=",float_value(global_best[0]))
        print("<=1 CNOT:",restricted_best,"R=",float_value(restricted_best[0]))
        print("Strict gap > 1/25:",float_value(gap))
        print("Additional M2 bits:",log2(float_value(restricted_best[0])/float_value(global_best[0])))
    return global_best,restricted_best,gap

if __name__=="__main__":certify()
