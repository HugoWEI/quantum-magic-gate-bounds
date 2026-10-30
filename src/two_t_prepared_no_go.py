"""Exact preparation-complexity no-go for two-qubit two-CNOT magic gains.

All pure 2q states obtainable from a stabilizer input using <=2 T and
arbitrary Cliffords form exactly 2580 Clifford orbit rays, partitioned
into 4 full-Clifford orbits / 16 local-Clifford classes. Every class
reaches R=7/4 (absolute max M2=log2(16/7)) with <=3 ADDITIONAL T and
<=1 CNOT. Hence a 3T two-CNOT magic gain needs input T-prep cost >=3.

Pure, noiseless, ancilla-free two-qubit unitary Clifford+T; input
preparation cost is NOT included in the subsequent 3T/1CNOT budget.
"""
from src.one_t_natural_input_theorem import (
    ALL,AXES,LOCAL,orbit,rotate,fourth_numerator,cnot_compatible_word)

STABILIZER=tuple((2,0) if p in ('II','IZ','ZI','ZZ') else (0,0)
                 for p in ALL) # r=(a+b sqrt2)/2

# Chronological Pauli axes, each with sign MINUS. Minus axis T is
# implemented by one ordinary T plus single-qubit S corrections.
WORDS=(('IY','YI','YY'),('IX','IY','XY'),
    ('IX','IY','ZY'),('XI','YI','YZ'),('IY','IX','ZX'),('IY','YX','ZZ'),
    ('IY','ZI','YY'),('IZ','YI','YY'),('IY','ZY','YI'),
    ('IY','ZY','YI'),('IX','IY','ZI'),
    ('IX','IX','YI'),('XX','XX','XX'),('ZZ','ZX','ZX'),
    ('IY','IY','IY'),('ZX','ZX','IY'))
SIZES=(36,24,72,72,144,72,144,144,144,144,144,288,576,144,288,144)
FULL_SIZES=(60,360,720,1440)

def seeds():
    # T_P normal form for <=2 Clifford-routed T operations on |00>.
    yield tuple((4*a,4*b) for a,b in STABILIZER)
    for p in AXES:
        first=rotate(STABILIZER,p,1)
        yield tuple((2*a,2*b) for a,b in first)
        for q in AXES:
            yield rotate(first,q,1)

def distinct_local_classes():
    visited=set();reps=[];full_sizes=[]
    for seed in seeds():
        if seed in visited:continue
        full=orbit(seed)
        assert not (visited&full)
        visited.update(full);full_sizes.append(len(full))
        remaining=set(full)
        while remaining:
            rep=min(remaining);local=orbit(rep,local_only=True)
            assert local<=remaining
            remaining-=local;reps.append((rep,len(local)))
    assert tuple(full_sizes)==FULL_SIZES,full_sizes
    assert len(visited)==2580
    assert len(reps)==16 and tuple(x[1] for x in reps)==SIZES
    return reps

def certify(verbose=True):
    classes=distinct_local_classes()
    for i,((rep,size),word) in enumerate(zip(classes,WORDS)):
        assert cnot_compatible_word(word),(i,word)
        # The orbit states have r=(a+b sqrt2)/8; coefficients are even.
        assert all(a%2==0 and b%2==0 for a,b in rep)
        vec=tuple((a//2,b//2) for a,b in rep) # denominator 4
        for axis in word:
            vec=rotate(vec,axis,-1)
        assert vec[0]==(32,0)
        assert fourth_numerator(vec)==(7*32**4//4,0),(i,word)
    if verbose:
        print('PASS four Clifford orbits (60,360,720,1440) = 2580 rays')
        print('PASS 16 local-Clifford classes with exact signed 3T witnesses')
        print('PASS all witnesses attain R=7/4 with <=1 physical CNOT')
        print('No 2-CNOT advantage for any <=2T-prepared input with 3 extra T')
    return classes,WORDS

if __name__=='__main__':certify()
