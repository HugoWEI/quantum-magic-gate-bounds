"""Commutation-graph characterization of all 1530 nonlocalizable 3-Pauli triples.

A triple (P,Q,R) can be Clifford-conjugated to three weight-one
Pauli axes iff neither obstruction below holds:
 (a) rank_F2(span{P,Q,R})=3 and >=2 anticommuting pairs;
 (b) rank=2, all three are distinct and mutually commuting.
This is about one shared Clifford frame, not physical interleaved CNOT
circuit lower bounds. All 3375 triples counted by exact GF(2).
"""
from itertools import product
from collections import Counter

CODES={'I':(0,0),'X':(1,0),'Y':(1,1),'Z':(0,1)}
AXES=tuple(''.join(p) for p in product("IXYZ",repeat=2)
           if p!=('I','I'))

def binary(p):
    x0,z0=CODES[p[0]];x1,z1=CODES[p[1]]
    return (x0,z0,x1,z1)

def symplectic(p,q):
    a,b=binary(p),binary(q)
    return (a[0]*b[1]+a[1]*b[0]+a[2]*b[3]+a[3]*b[2])%2

def rank(triple):
    span={0}
    for p in triple:
        x,z,y,w=binary(p)
        val=x*8+z*4+y*2+w
        span|={i^val for i in tuple(span)}
    return len(span).bit_length()-1

def anticommutation_edges(triple):
    a,b,c=triple
    return symplectic(a,b)+symplectic(a,c)+symplectic(b,c)

def cannot_localize(triple):
    r=rank(triple)
    e=anticommutation_edges(triple)
    return (r==3 and e>=2) or (r==2 and e==0 and len(set(triple))==3)

def certify():
    classes=Counter();obstructions=Counter()
    for triple in product(AXES,repeat=3):
        key=(rank(triple),anticommutation_edges(triple))
        classes[key]+=1
        if cannot_localize(triple):obstructions[key]+=1
    assert sum(classes.values())==3375
    assert obstructions==Counter({(3,2):1080,(3,3):360,(2,0):90})
    assert sum(obstructions.values())==1530
    assert cannot_localize(('YY','XI','XY'))
    print('PASS 3375 triples; obstructions rank3/2 edges=1080, rank3/3 edges=360, commuting rank2 context=90')
    return classes,obstructions

if __name__=='__main__':certify()
