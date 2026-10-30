"""Exact signed Clifford orbit of all one-T-prepared two-qubit states.

360 nonstabilizer state rays, four local Clifford classes. Each class
reaches the global two-qubit maximum magic R=7/4 using <=3 additional
T rotations and <=1 CNOT. The initial state is supplied; its preparation
cost is tracked separately. No ancillas, measurements or postselection.
"""
from collections import deque
from itertools import product
import numpy as np

ALL=tuple(''.join(p) for p in product('IXYZ',repeat=2))
AXES=ALL[1:]
LOCAL=tuple(p for p in AXES if p.count('I')==1)
INDEX={p:i for i,p in enumerate(ALL)}
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1,-1]).astype(complex)
M={'I':I,'X':X,'Y':Y,'Z':Z}
P={p:np.kron(M[p[0]],M[p[1]]) for p in ALL}
HNUM=X+Z
S=np.diag([1,1j]).astype(complex)
CNOT=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],complex)
GATES=((np.kron(HNUM,I),2),(np.kron(I,HNUM),2),
       (np.kron(S,I),1),(np.kron(I,S),1),(CNOT,1))

def signed_clifford_action(U,scale):
    result=[]
    for p in ALL:
        actual=U@P[p]@U.conj().T
        matches=[(INDEX[q],s) for q in ALL for s in (-1,1)
                 if np.array_equal(actual,scale*s*P[q])]
        assert len(matches)==1,(p,matches)
        result.append(matches[0])
    return result

ACTIONS=tuple(signed_clifford_action(*gate) for gate in GATES)
# r_P=(a+b sqrt(2))/2, for (T|+>) tensor |0>.
START=tuple((2,0) if p in ('II','IZ') else
            (0,1) if p in ('XI','XZ','YI','YZ') else (0,0) for p in ALL)

def act(state,generator):
    result=[None]*16
    for val,(idx,s) in zip(state,ACTIONS[generator]):
        result[idx]=(val[0]*s,val[1]*s)
    return tuple(result)

def orbit(initial,local_only=False):
    generators=range(4) if local_only else range(5)
    seen={initial}; queue=deque([initial])
    while queue:
        state=queue.popleft()
        for g in generators:
            other=act(state,g)
            if other not in seen:
                seen.add(other);queue.append(other)
    return seen

def local_classes():
    all_states=orbit(START)
    assert len(all_states)==360
    seen=set(); representatives=[]
    for state in sorted(all_states):
        if state in seen:continue
        suborbit=orbit(state,local_only=True)
        assert suborbit<=all_states
        seen.update(suborbit)
        representatives.append((state,len(suborbit)))
    assert seen==all_states
    assert [size for _,size in representatives]==[72,72,144,72]
    return representatives

WITNESSES=(
   (('IX','IY','ZY'),(-1,-1,-1)),
   (('XI','YI','YZ'),(-1,-1,-1)),
   (('IY','IX','ZX'),(-1,-1,-1)),
   (('IY','YX','ZZ'),(-1,-1,-1)),
)

def product_paulis(a,b):
    phase=0;label=[]
    for ca,cb in zip(a,b):
        if ca=='I':label.append(cb)
        elif cb=='I':label.append(ca)
        elif ca==cb:label.append('I')
        else:
            options={'XY':('Z',1),'YZ':('X',1),'ZX':('Y',1),
                     'YX':('Z',3),'ZY':('X',3),'XZ':('Y',3)}
            c,k=options[ca+cb];label.append(c);phase+=k
    return phase%4,''.join(label)

MIX=tuple(tuple((INDEX[product_paulis(a,p)[1]],
                1 if product_paulis(a,p)[0]==3 else
                -1 if product_paulis(a,p)[0]==1 else 0)
                for p in ALL) for a in AXES)

def rotate(state,axis,sgn):
    """For denominator 2**(k+2), update to denominator 2**(k+3)."""
    result=[]
    for (a,b),(j,eps) in zip(state,MIX[AXES.index(axis)]):
        if eps:
            c,d=state[j]
            result.append((2*(b+sgn*eps*d),a+sgn*eps*c))
        else:
            result.append((2*a,2*b))
    return tuple(result)

def fourth_numerator(state):
    """Numerator of R over denominator 32**4 after three T gates."""
    a=b=0
    for x,y in state:
        a+=x**4+12*x*x*y*y+4*y**4
        b+=4*x*y*(x*x+2*y*y)
    return a,b

def cnot_compatible_word(word):
    """One-CNOT physical circuit has local prefix and conjugated-local suffix."""
    from src.one_cnot_universality import PERMS,label_under_local,cnot_label
    allowed=set(LOCAL)
    for k in (0,1,2,3):
        for p0,_,_ in PERMS:
            for p1,_,_ in PERMS:
                for control in (0,1):
                    images={label_under_local(cnot_label(p,control),(p0,p1))
                            for p in LOCAL}
                    if all(p in allowed for p in word[:k]) and all(
                        p in images for p in word[k:]):
                        return True
    return False

def certify(verbose=True):
    classes=local_classes()
    for (state,size),(word,signs) in zip(classes,WITNESSES):
        vec=tuple((2*a,2*b) for a,b in state) # initial denominator 4
        for p,sgn in zip(word,signs):vec=rotate(vec,p,sgn)
        assert vec[0]==(32,0)
        assert fourth_numerator(vec)==(7*32**4//4,0)
        assert cnot_compatible_word(word),(word,size)
    if verbose:
        print('PASS 360 distinct one-T input rays; 4 local orbits')
        print('PASS 4 exact signed three-T witnesses R=7/4 with <=1 CNOT')
    return classes,WITNESSES

if __name__=='__main__':certify()
