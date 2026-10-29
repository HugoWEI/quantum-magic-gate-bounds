"""EXACT 3-T / 2-CNOT separation. Integer arithmetic in Q(sqrt(2)).

Input [-1+3i,-7-i,-1+i,-1+4i]/sqrt(79).
Global <=3-T circuits: 1+15+225+3375 positive Pauli words.
<=1-CNOT circuits: all 0/1/2-T unrestricted words (overapproximation),
plus 2457 signed Pauli triples x 8 sign choices, covering ALL positions
of the physical CNOT and all local Clifford orientations.
A strict gap proves 2 CNOTs necessary; constructive two-CNOT compiler
proves sufficiency. No ancillas, measurement, or other entangling gates.
"""
from itertools import product
import sympy as S
from src.one_cnot_universality import AXES,LOCAL,PERMS,label_under_local,cnot_label
from src.two_t_frontier_certificate import product_label

ALL=("II",)+tuple(AXES)
INDEX={p:i for i,p in enumerate(ALL)}
MATS={"I":S.eye(2),"X":S.Matrix([[0,1],[1,0]]),
      "Y":S.Matrix([[0,-S.I],[S.I,0]]),"Z":S.diag(1,-1)}
PSI=S.Matrix([-1+3*S.I,-7-S.I,-1+S.I,-1+4*S.I])
N=int((PSI.conjugate().T*PSI)[0])
EXPECT=tuple(int((PSI.conjugate().T*
       S.kronecker_product(MATS[p[0]],MATS[p[1]])*PSI)[0]) for p in ALL)
assert N==79

# Each Pauli moment after k T gates is (a+b sqrt(2))/(2**k*N).
MIX=[]
for p in AXES:
    row=[]
    for q in ALL:
        phase,other=product_label(p,q)
        row.append((INDEX[other],1 if phase==3 else -1 if phase==1 else 0))
    MIX.append(tuple(row))

def rotate(v,axis,sign):
    out=[]
    for (a,b),(j,s) in zip(v,MIX[axis]):
        if not s:out.append((2*a,2*b))
        else:
            c,d=v[j]
            out.append((2*(b+sign*s*d),a+sign*s*c))
    return tuple(out)

def pauli_moment(vec,depth):
    A=B=0
    for a,b in vec:
        A+=a**4+12*a*a*b*b+4*b**4
        B+=4*a*b*(a*a+2*b*b)
    # All moments expressed with common denominator (8*N)^4.
    scale=2**(4*(3-depth))
    return A*scale,B*scale

def sign_qsqrt2(pair):
    a,b=pair
    if a==0 and b==0:return 0
    if a>=0 and b>=0:return 1
    if a<=0 and b<=0:return -1
    if a>0:return 1 if a*a>2*b*b else -1
    return 1 if 2*b*b>a*a else -1

def smaller(x,y):return sign_qsqrt2((x[0]-y[0],x[1]-y[1]))<0

def one_cnot_triples():
    """All 3-T Pauli words possible using 0 or 1 interleaved CNOT,
    up to a trailing Clifford; signs handled separately.
    """
    out=set(product(LOCAL,repeat=3))
    for p0,_,_ in PERMS:
        for p1,_,_ in PERMS:
            for ctrl in (0,1):
                transformed={label_under_local(cnot_label(p,ctrl),(p0,p1))
                             for p in LOCAL}
                for cut in range(4):
                    out.update(product(*([LOCAL]*cut+[tuple(transformed)]*(3-cut))))
    assert len(out)==2457
    return out

def certify(verbose=True):
    init=tuple((x,0) for x in EXPECT)
    global_best=(pauli_moment(init,0),())
    restricted=(global_best[0],())
    for p in range(15):
        v1=rotate(init,p,1)
        m=pauli_moment(v1,1)
        if smaller(m,global_best[0]):global_best=(m,(AXES[p],))
        if smaller(m,restricted[0]):restricted=(m,(AXES[p],))
        for q in range(15):
            v2=rotate(v1,q,1)
            m=pauli_moment(v2,2)
            if smaller(m,global_best[0]):global_best=(m,(AXES[p],AXES[q]))
            if smaller(m,restricted[0]):restricted=(m,(AXES[p],AXES[q]))
            for r in range(15):
                m=pauli_moment(rotate(v2,r,1),3)
                if smaller(m,global_best[0]):
                    global_best=(m,(AXES[p],AXES[q],AXES[r]))
    accessible=one_cnot_triples()
    lookup={}
    for a,b,c in accessible:
        lookup.setdefault(AXES.index(a),{}).setdefault(AXES.index(b),[]).append(AXES.index(c))
    for s1,s2,s3 in product((-1,1),repeat=3):
        for a,seconds in lookup.items():
            v1=rotate(init,a,s1)
            for b,thirds in seconds.items():
                v2=rotate(v1,b,s2)
                for c in thirds:
                    m=pauli_moment(rotate(v2,c,s3),3)
                    if smaller(m,restricted[0]):
                        restricted=(m,((AXES[a],AXES[b],AXES[c]),(s1,s2,s3)))
    assert global_best==((282563686656,0),("YY","XI","XY"))
    assert restricted[0]==(284758552576,0)
    gap=(restricted[0][0]-global_best[0][0],
         restricted[0][1]-global_best[0][1])
    assert gap==(2194865920,0) and sign_qsqrt2(gap)>0
    if verbose:
        print("PASS unrestricted: 3616 Pauli words incl. shorter counts",global_best)
        print("PASS <=1-CNOT: 241 shorter candidates + 2457*8 signed triples",restricted)
        print("PASS exact R difference =",S.Rational(gap[0],(8*N)**4))
        print("Two-CNOT upper-bound witness: (YY,XI,XY)")
    return global_best,restricted,gap

if __name__=="__main__":certify()
