"""Exact three-T/two-CNOT threshold for EXACT maximal two-qubit magic.

The fixed, already-magical input is (Rx(pi/4) tensor I)(A|00>+B|11>),
 A=(1-sqrt2+i(1+2sqrt2))/4, B=(1-sqrt2+i)/4.
With three T gates, word (XX,IZ,IY) produces exactly the known maximal
magic Clifford fiducial (1+3i,1+i,1-i,1+i)/4 up to global phase.

All input Pauli moments are in Q(sqrt2). This executable certificate
exhausts 3616 unrestricted 0-3T Pauli words, 241 shorter unrestricted
and 2457*8 signed one-CNOT-compatible 3T words. Every comparison is
exact integer arithmetic in Z[sqrt2], no floating-point minimization.
No input-preparation cost is included. No ancillas or measurements.
"""
from itertools import product
from src.three_t_simple_state_certificate import (
    AXES,ALL,LOCAL,MIX,one_cnot_triples)

# Initial Pauli expectations r_P=(a+b sqrt2)/4 in canonical 16-Pauli order.
INIT={
    "II":(4,0),
    "IZ":(2,1),
    "ZI":(1,1), "YI":(-1,-1),
    "XX":(2,0), "XY":(2,-1),
    "YX":(-1,1), "YY":(0,-1),
    "YZ":(0,-2), "ZX":(-1,1),
    "ZY":(0,-1), "ZZ":(0,2)
}
START=tuple(INIT.get(k,(0,0)) for k in ALL)
INDEX={name:i for i,name in enumerate(AXES)}

def rotate(v,axis,sign):
    """After k gates r_P=(a+b sqrt2)/(4*2**k)."""
    result=[]
    for (a,b),(j,phase) in zip(v,MIX[axis]):
        if phase:
            c,d=v[j]
            result.append((2*(b+sign*phase*d),a+sign*phase*c))
        else:
            result.append((2*a,2*b))
    return tuple(result)

def fourth_numerator(v,depth):
    """Common positive denominator (4*2**3)**4=32**4."""
    a=b=0
    for x,y in v:
        a+=x**4+12*x*x*y*y+4*y**4
        b+=4*x*y*(x*x+2*y*y)
    mult=2**(4*(3-depth))
    return a*mult,b*mult

def sign_qsqrt2(value):
    a,b=value
    if a==0:return (b>0)-(b<0)
    if b==0:return (a>0)-(a<0)
    if a>0 and b>0:return 1
    if a<0 and b<0:return -1
    if a>0:return 1 if a*a>2*b*b else -1
    return 1 if 2*b*b>a*a else -1

def less(a,b):
    return sign_qsqrt2((a[0]-b[0],a[1]-b[1]))<0

def run_word(word,signs=None):
    v=START
    if signs is None:signs=(1,)*len(word)
    for p,s in zip(word,signs):v=rotate(v,INDEX[p],s)
    return v

def certify(verbose=True):
    global_best=(fourth_numerator(START,0),())
    restricted_best=global_best
    n_global=1
    for p in AXES:
        v1=rotate(START,INDEX[p],1)
        value=fourth_numerator(v1,1)
        n_global+=1
        if less(value,global_best[0]):global_best=(value,(p,))
        if less(value,restricted_best[0]):restricted_best=(value,(p,))
        for q in AXES:
            v2=rotate(v1,INDEX[q],1)
            value=fourth_numerator(v2,2)
            n_global+=1
            if less(value,global_best[0]):global_best=(value,(p,q))
            if less(value,restricted_best[0]):restricted_best=(value,(p,q))
            for r in AXES:
                value=fourth_numerator(rotate(v2,INDEX[r],1),3)
                n_global+=1
                if less(value,global_best[0]):global_best=(value,(p,q,r))

    permitted=one_cnot_triples()
    grouped={}
    for p,q,r in permitted:
        grouped.setdefault((INDEX[p],INDEX[q]),[]).append(INDEX[r])
    n_restricted=1+len(AXES)+len(AXES)**2
    for signs in product((-1,1),repeat=3):
        for (p,q),third_axes in grouped.items():
            v2=rotate(rotate(START,p,signs[0]),q,signs[1])
            for r in third_axes:
                value=fourth_numerator(rotate(v2,r,signs[2]),3)
                n_restricted+=1
                if less(value,restricted_best[0]):
                    restricted_best=(value,((AXES[p],AXES[q],AXES[r]),signs))

    assert (n_global,n_restricted,len(permitted))==(3616,19897,2457)
    assert global_best==((1835008,0),("XX","IZ","IY"))
    assert restricted_best[0]==(2115840,-165888)
    assert ("YI","XY","IX") in permitted
    assert fourth_numerator(run_word(("YI","XY","IX"),(-1,-1,-1)),3)==restricted_best[0]
    gap=(restricted_best[0][0]-global_best[0][0],
         restricted_best[0][1]-global_best[0][1])
    assert gap==(280832,-165888)
    assert sign_qsqrt2((gap[0]-40960,gap[1]))>0 # gap > 1/25

    # The unrestricted output has exactly the 12 +/- 1/2 and 3 zero
    # Pauli expectations of the explicitly stated maximal-magic fiducial.
    v=run_word(("XX","IZ","IY"))
    assert v==tuple({
        "II":(32,0),"IX":(16,0),"IZ":(16,0),
        "XX":(16,0),"XZ":(-16,0),
        "YI":(-16,0),"YX":(-16,0),"YY":(-16,0),"YZ":(-16,0),
        "ZI":(16,0),"ZX":(16,0),"ZY":(-16,0),"ZZ":(16,0)
    }.get(p,(0,0)) for p in ALL)
    assert fourth_numerator(START,0)==(2506752,0) # R_input = 153/64

    if verbose:
        print("PASS 3616 unrestricted, 19897 overcomplete <=1-CNOT candidates")
        print("PASS: exact maximal two-qubit M2 reached by (XX,IZ,IY)")
        print("PASS unrestricted R=7/4; restricted R=8265/4096-81sqrt2/512")
        print("PASS strict R gap=(1097-648sqrt2)/4096 >1/25")
        print("PASS final Pauli signature exactly matches a maximal-magic fiducial")
    return global_best,restricted_best,gap

if __name__=="__main__":
    certify()
