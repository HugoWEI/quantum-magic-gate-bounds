"""Sharp four-T INPUT preparation threshold for a 3T conversion 2-CNOT gain.

Every pure two-qubit input generated from a stabilizer with <=3 T and
Cliffords has equal maximal output M2 under <=1 CNOT and unrestricted
Cliffords, when <=3 ADDITIONAL T are allowed. Exact finite proof:
18900 distinct pure input rays, 10 global Clifford orbits, 58 local
Clifford classes; 48 classes reach R=7/4 with <=1 CNOT, while 10
exceptional classes reach R=463/256; unrestricted optimality for those
two exceptional full Clifford orbits is proved by exact 3616-word checks.

Combined with the independently certified prep-T-count=4, strict
two-CNOT witness, this makes prep-count threshold exactly 4.
Pure, ancilla-free, noiseless, local Cliffords free in conversion.
"""
from src.one_t_natural_input_theorem import (
    ALL,AXES,orbit,rotate,fourth_numerator,cnot_compatible_word)

STAB=tuple((2,0) if p in ('II','IZ','ZI','ZZ') else (0,0) for p in ALL)
FULL_SIZES=(60,360,720,720,720,5760,1440,480,2880,5760)
# Each word is chronologically ordered, all T signs NEGATIVE, with
# physical conjugation to local T before S-dagger corrections.
WORDS=(
 ('IY','YI','YY'),('IX','IY','XY'),('IX','IY','ZY'),('XI','YI','YZ'),
 ('IY','IX','ZX'),('IY','YX','ZZ'),('IY','ZI','YY'),('IZ','YI','YY'),
 ('IY','ZY','YI'),('IY','ZY','YI'),('IX','IY','ZI'),
 ('IY','YY','IZ'),('YI','YY','ZY'),('IY','YI','XZ'),('IY','XY','IZ'),
 ('IY','ZI','YX'),('IY','YY','IZ'),('YI','YY','ZY'),('IY','YI','XZ'),
 ('IY','XY','IZ'),('IY','ZI','YZ'),
 ('IZ','XX','YZ'),('IY','XY','YI'),('IX','XX','ZX'),('IX','XI','ZX'),
 ('IX','XI','ZI'),('XY','ZZ','YZ'),('XY','ZZ','XI'),('ZI','XX','ZY'),
 ('IX','IY','XI'),('YI','YX','IY'),('YI','YX','YZ'),('IX','XI','XY'),
 ('YX','ZZ','IX'),('YX','ZZ','ZY'),
 ('IX','IX','YI'),('XX','XX','XX'),('ZZ','ZX','ZX'),('IY','IY','IY'),
 ('ZX','ZX','IY'),('IX','XI','XX'),('IX','ZI','ZX'),
 ('XY','YZ','ZZ'),('IZ','IY','XI'),('XI','IZ','XY'),('IX','ZX','XX'),
 ('IX','ZI','YI'),('XY','IY','ZX'),
 ('IY','XI','IY'),('XI','XI','XI'),('IY','IY','XZ'),('IX','IX','IX'),
 ('XX','IZ','IZ'),('IX','IX','IX'),('YX','YX','YX'),('XX','XX','XX'),
 ('XX','XX','XX'),('XX','XX','IZ'))
assert len(WORDS)==58
EXCEPTIONAL=tuple(range(11,21))

def seeds():
    yield tuple((8*a,8*b) for a,b in STAB),()
    for p in AXES:
        v1=rotate(STAB,p,1)
        yield tuple((4*a,4*b) for a,b in v1),(p,)
        for q in AXES:
            v2=rotate(v1,q,1)
            yield tuple((2*a,2*b) for a,b in v2),(p,q)
            for r in AXES:
                yield rotate(v2,r,1),(p,q,r)

def exact_classes():
    visited=set();full_sizes=[];reps=[];sources=[]
    for seed,source in seeds():
        if seed in visited:continue
        full=orbit(seed)
        assert not (visited&full)
        full_sizes.append(len(full));visited.update(full)
        remaining=set(full)
        while remaining:
            rep=min(remaining);local=orbit(rep,local_only=True)
            assert local<=remaining
            remaining-=local;reps.append((rep,len(local)))
            sources.append(source)
    assert tuple(full_sizes)==FULL_SIZES,full_sizes
    assert len(visited)==18900 and len(reps)==58
    assert sum(size for _,size in reps)==18900
    assert sources[11:16]==[('IX','IY','IX')]*5
    assert sources[16:21]==[('IX','IY','IZ')]*5
    return reps,sources

def sign_sqrt2(pair):
    a,b=pair
    if not a:return (b>0)-(b<0)
    if not b:return (a>0)-(a<0)
    if a>0 and b>0:return 1
    if a<0 and b<0:return -1
    return (1 if a*a>2*b*b else -1) if a>0 else (
        1 if 2*b*b>a*a else -1)

def scaled_moment(v,k):
    a,b=fourth_numerator(v)
    factor=2**(4*(3-k))
    return a*factor,b*factor # shared denominator 128**4

def unrestricted_minimum(initial):
    # Exact 1+15+225+3375 Pauli T words.
    minimum=scaled_moment(initial,0)
    def lower(a,b):
        return sign_sqrt2((a[0]-b[0],a[1]-b[1]))<0
    for p in AXES:
        one=rotate(initial,p,1)
        val=scaled_moment(one,1)
        if lower(val,minimum):minimum=val
        for q in AXES:
            two=rotate(one,q,1)
            val=scaled_moment(two,2)
            if lower(val,minimum):minimum=val
            for r in AXES:
                three=rotate(two,r,1)
                val=scaled_moment(three,3)
                if lower(val,minimum):minimum=val
    return minimum

def certify(verbose=True):
    reps,sources=exact_classes()
    for i,((state,size),word) in enumerate(zip(reps,WORDS)):
        vec=state  # denominator 16 before additional T rotations
        for axis in word:
            vec=rotate(vec,axis,-1)
        target=(463*128**4//256,0) if i in EXCEPTIONAL else (
                7*128**4//4,0)
        assert fourth_numerator(vec)==target,(i,word)
        assert vec[0]==(128,0)
        assert cnot_compatible_word(word),(i,word)
    # Each exception is one full Clifford orbit: global Clifford
    # routing preserves its unrestricted optimum.
    for i in (11,16):
        assert unrestricted_minimum(reps[i][0])==(463*128**4//256,0)
    if verbose:
        print('PASS 18900 pure <=3T-prepared input rays')
        print('PASS 10 global Clifford orbits, 58 local Clifford classes')
        print('PASS 48 exact one-CNOT R=7/4 witnesses; 10 exact R=463/256')
        print('PASS exact unrestricted minima in both exceptional full orbits')
        print('SHARP prep-T threshold for strict 2-CNOT 3T conversion gain =4')
    return reps,WORDS

if __name__=='__main__':certify()
