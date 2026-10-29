"""Three Pauli-axis simultaneous localization: full 2-qubit Clifford group.

Of 15^3 ordered triples, 1530 cannot be mapped to three weight-one
Pauli axes by ANY two-qubit Clifford. The other 1845 can be localized
by <=1 CNOT. This says NOTHING directly about minimal CNOT count for
an arbitrary three-T circuit, where entanglers can be interleaved.
"""
from collections import deque
from itertools import product
from src.one_cnot_universality import AXES,LOCAL,PERMS,label_under_local,cnot_label

INDEX={p:i for i,p in enumerate(AXES)}
LOCAL_INDICES=set(INDEX[p] for p in LOCAL)

def local_gate(p,qubit,gate):
    chars=list(p)
    tables={'H':{'I':'I','X':'Z','Y':'Y','Z':'X'},
            'S':{'I':'I','X':'Y','Y':'X','Z':'Z'}}
    chars[qubit]=tables[gate][chars[qubit]]
    return ''.join(chars)

def full_symplectic_cliffords():
    generators=[]
    for q in (0,1):
        for gate in ('H','S'):
            generators.append(tuple(INDEX[local_gate(p,q,gate)] for p in AXES))
    for control in (0,1):
        generators.append(tuple(INDEX[cnot_label(p,control)] for p in AXES))
    identity=tuple(range(15))
    seen={identity};queue=deque([identity])
    while queue:
        state=queue.popleft()
        for gen in generators:
            new=tuple(gen[i] for i in state)
            if new not in seen:
                seen.add(new);queue.append(new)
    assert len(seen)==720  # |Sp(4,2)|=720
    return seen

def count_classes():
    perms=full_symplectic_cliffords()
    localize=0; impossible=0
    for triple in product(range(15),repeat=3):
        if any(all(g[i] in LOCAL_INDICES for i in triple) for g in perms):
            localize+=1
        else:impossible+=1
    assert (localize,impossible)==(1845,1530)
    # Re-check those localizable triples need only <=1 *pre*-CNOT.
    candidates=[]
    for p0,_,_ in PERMS:
        for p1,_,_ in PERMS:
            for ctrl in (0,1):
                mapping=tuple(INDEX[cnot_label(label_under_local(p,(p0,p1)),ctrl)]
                              for p in AXES)
                candidates.append(mapping)
    assert len(candidates)==72
    one_cnot_count=0
    for triple in product(range(15),repeat=3):
        if all(AXES[i] in LOCAL for i in triple):
            one_cnot_count+=1;continue
        if any(all(g[i] in LOCAL_INDICES for i in triple) for g in candidates):
            one_cnot_count+=1
    assert one_cnot_count==localize
    return {'all_local':len(LOCAL)**3,'one_cnot_localizable_total':one_cnot_count,
            'no_clifford_can_simultaneously_localize':impossible,
            'symplectic_group_size':len(perms)}

if __name__=='__main__':print('PASS:',count_classes())
