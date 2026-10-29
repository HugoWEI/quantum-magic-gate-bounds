"""Classify simultaneous Pauli localization of up to 3 axes by one pre-CNOT.

This is NOT a lower bound on CNOT for arbitrary interleaved 3-T circuits.
Run: python -m src.three_t_prelocalization
"""
from itertools import product
from src.one_cnot_universality import AXES, LOCAL, PERMS, label_under_local,cnot_label

PATTERNS=[(p0,p1,c) for p0,_,_ in PERMS for p1,_,_ in PERMS for c in (0,1)]

def classification():
    counts={'already_local':0,'one_pre_cnot':0,'no_simultaneous_one_pre_cnot':0}
    examples=[]
    for axes in product(AXES,repeat=3):
        if all(x in LOCAL for x in axes):
            counts['already_local']+=1
            continue
        possible=any(
            all(cnot_label(label_under_local(axis,(p0,p1)),ctrl) in LOCAL
                for axis in axes)
            for p0,p1,ctrl in PATTERNS)
        if possible:counts['one_pre_cnot']+=1
        else:
            counts['no_simultaneous_one_pre_cnot']+=1
            if len(examples)<10:examples.append(axes)
    assert counts=={'already_local':216,'one_pre_cnot':1629,
                    'no_simultaneous_one_pre_cnot':1530}
    return counts,examples

if __name__=='__main__':
    result,examples=classification()
    print('PASS 15^3=3375 ordered triples:',result)
    print('Examples not simultaneously localizable:',examples)
