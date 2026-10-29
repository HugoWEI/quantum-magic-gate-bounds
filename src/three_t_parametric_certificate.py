"""Exact one-parameter 3T/2-CNOT magic-gap certificate in Q(sqrt(2)).

State: [-1+3i,-7-i,-1+i,-1+(4+s)i] / sqrt(79+8s+s²).
For EVERY s in [-1/8,1/4], with <=3 T and arbitrary local Cliffords:
the unrestricted 2-CNOT word (YY,XI,XY) beats all <=1-CNOT circuits
by MORE than 1/100 in final Pauli fourth moment. No numeric signs used.

The 19,897 candidate circuits are conservatively exhaustive: 241
shorter (0/1/2-T) unconstrained Clifford words and 2457 signed 3T
axis patterns * eight signs with zero/one CNOT at any time.
There are 9 positive Bernstein coefficients per candidate =179073.
"""
from itertools import product
from fractions import Fraction
from math import comb,lcm
import sympy as S
from src.three_t_exact_gap import (
    AXES,ALL,MATS as PAULI,MIX,one_cnot_triples,PSI as STATE,EXPECT)

BASIS=S.Matrix([0,0,0,S.I])

def input_coefficients():
    result=[]
    for p in ALL:
        P=S.kronecker_product(PAULI[p[0]],PAULI[p[1]])
        a=int((STATE.conjugate().T*P*STATE)[0])
        b=int((BASIS.conjugate().T*P*STATE+STATE.conjugate().T*P*BASIS)[0])
        c=int((BASIS.conjugate().T*P*BASIS)[0])
        result.append(((a,b,c),(0,0,0)))
    assert tuple(t[0][0] for t in result)==EXPECT
    assert result[0][0]==(79,8,1)
    return tuple(result)

def rotate(v,axis,sgn):
    out=[]
    for (aa,bb),(j,phase) in zip(v,MIX[axis]):
        if not phase:
            out.append((tuple(2*x for x in aa),tuple(2*x for x in bb)))
        else:
            cc,dd=v[j]
            out.append((tuple(2*(bb[k]+sgn*phase*dd[k]) for k in range(3)),
                        tuple(aa[k]+sgn*phase*cc[k] for k in range(3))))
    return tuple(out)

def convolution(a,b):
    result=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:result[i+j]+=x*y
    return result

def fourth_moment_polynomial(v,depth):
    A=[0]*9;B=[0]*9
    for aa,bb in v:
        a2=convolution(aa,aa)
        b2=convolution(bb,bb)
        ab=convolution(aa,bb)
        re=[a2[k]+2*b2[k] for k in range(5)]
        im=[2*x for x in ab]
        re4=convolution(re,re)
        im4=convolution(im,im)
        cross=convolution(re,im)
        for k in range(9):
            A[k]+=re4[k]+2*im4[k]
            B[k]+=2*cross[k]
    fac=2**(4*(3-depth))
    return (tuple(x*fac for x in A),tuple(x*fac for x in B))

def difference(u,v):
    return (tuple(x-y for x,y in zip(u[0],v[0])),
            tuple(x-y for x,y in zip(u[1],v[1])))

def bernstein_matrix(L=Fraction(-1,8),U=Fraction(1,4)):
    L=Fraction(L);U=Fraction(U)
    d=lcm(L.denominator,U.denominator)
    n=int(d*L);w=int(d*(U-L))
    assert Fraction(n,d)==L and Fraction(w,d)==U-L
    mat=[]
    for i in range(9):
        row=[]
        for j in range(9):
            val=sum((Fraction(comb(j,k)*w**k*n**(j-k)*d**(8-j)*comb(i,k),
                              comb(8,k)) for k in range(min(i,j)+1)),Fraction(0))
            row.append(val)
        mat.append(row)
    den=lcm(*(x.denominator for row in mat for x in row))
    return tuple(tuple(int(x*den) for x in row) for row in mat),den

def sign_pair(a,b):
    if a==0 and b==0:return 0
    if a>=0 and b>=0:return 1
    if a<=0 and b<=0:return -1
    if a>0:return 1 if a*a>2*b*b else -1
    return 1 if 2*b*b>a*a else -1

def strictly_positive_gap(D,M):
    """Bernstein: certify positive difference AND uniform >1/100."""
    A,B=D
    # Max normalizing N(s) is 1297/16. Matrix is 35*8**8 scaled.
    # Require each Bernstein coefficient /[(35*8**8)(8*Nmax)**4]>1/100.
    cutoff=35*(8**8)*(1297**4)
    for row in M:
        a=sum(v*x for v,x in zip(row,A))
        b=sum(v*x for v,x in zip(row,B))
        if sign_pair(1600*a-cutoff,1600*b)<=0:return False
    return True

def certify(verbose=True):
    init=input_coefficients()
    v=init
    for axis in ('YY','XI','XY'):
        v=rotate(v,AXES.index(axis),1)
    witness=fourth_moment_polynomial(v,3)
    M,den=bernstein_matrix()
    assert den==35
    checked=0
    def assert_above(vec,k):
        nonlocal checked
        checked+=1
        D=difference(fourth_moment_polynomial(vec,k),witness)
        assert strictly_positive_gap(D,M),f'failed candidate #{checked}'
    # Allow all unrestricted shorter circuits: superset of <=1-CNOT cases.
    assert_above(init,0)
    for a in range(15):
        v1=rotate(init,a,1)
        assert_above(v1,1)
        for b in range(15):
            assert_above(rotate(v1,b,1),2)
    axes={p:i for i,p in enumerate(AXES)}
    groups={}
    words=one_cnot_triples()
    for a,b,c in words:
        groups.setdefault(axes[a],{}).setdefault(axes[b],[]).append(axes[c])
    for sign1,sign2,sign3 in product((-1,1),repeat=3):
        for a,seconds in groups.items():
            v1=rotate(init,a,sign1)
            for b,thirds in seconds.items():
                v2=rotate(v1,b,sign2)
                for c in thirds:
                    assert_above(rotate(v2,c,sign3),3)
    assert len(words)==2457 and checked==19897
    if verbose:
        print('PASS: 19,897 exact circuit candidates, 179,073 Bernstein coefficients')
        print('PASS: every s in [-1/8,1/4] has min_R(<=1CNOT)-R_(YY,XI,XY)>1/100')
        print('Input squared norm: 79+8s+s^2')
    return checked,9*checked

if __name__=='__main__':
    certify()
