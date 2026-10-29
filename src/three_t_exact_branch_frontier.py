"""Exact branch identification over the whole three-T/CNOT separation interval.

For psi(s) proportional to [-1+3i,-7-i,-1+i,-1+(4+s)i],
s in [-1/8,1/4], prove BOTH exact optima:
  <=1 CNOT, <=3 T: (ZI, ZY), only two T needed;
  unrestricted, <=3 T: (YY, XI, XY), using exactly two CNOT.

All algebra over Z[s,sqrt(2)]. We group the 19,897 restricted candidate
words into 1,258 distinct output polynomials; the 3,616 unrestricted
words form 1,876 polynomial classes. Every inactive polynomial minus
the winner has nonnegative degree-8 Bernstein coefficients over the
whole rational interval, with exact integer sign tests.
"""
from collections import defaultdict
from itertools import product
import sympy as S
from src.three_t_parametric_certificate import (
    input_coefficients, rotate, fourth_moment_polynomial,
    bernstein_matrix, sign_pair, AXES, one_cnot_triples)

GLOBAL_WORD=("YY","XI","XY")
RESTRICTED_WORD=("ZI","ZY")
N_COEFF=(79,8,1)
PG=(1103764401,435414168,145739564,27589704,3664950,
    349032,24908,1080,33)
PR=(69521131,28084688,9917468,1747712,162570,
    11856,1388,96,3)
GAP_POLY=(8573695,13940840,12939924,373688,-1063830,
          -159336,-2700,456,15)

def zero():
    return ((0,)*9,(0,)*9)

def signatures():
    """Construct quartic-moment polynomial signatures without sampling s."""
    initial=input_coefficients()
    all_words={fourth_moment_polynomial(initial,0)}
    shorter={fourth_moment_polynomial(initial,0)}
    for p in AXES:
        first=rotate(initial,AXES.index(p),1)
        one=fourth_moment_polynomial(first,1)
        shorter.add(one);all_words.add(one)
        for q in AXES:
            second=rotate(first,AXES.index(q),1)
            two=fourth_moment_polynomial(second,2)
            shorter.add(two);all_words.add(two)
            for r in AXES:
                three=fourth_moment_polynomial(rotate(second,AXES.index(r),1),3)
                all_words.add(three)
    restricted=set(shorter)
    grouped=defaultdict(list)
    for p,q,r in one_cnot_triples():
        grouped[(AXES.index(p),AXES.index(q))].append(AXES.index(r))
    for signs in product((-1,1),repeat=3):
        for (p,q),thirds in grouped.items():
            first=rotate(initial,p,signs[0])
            second=rotate(first,q,signs[1])
            for r in thirds:
                restricted.add(fourth_moment_polynomial(
                    rotate(second,r,signs[2]),3))
    return all_words,restricted

def word_polynomial(word):
    state=input_coefficients()
    for axis in word:
        state=rotate(state,AXES.index(axis),1)
    return fourth_moment_polynomial(state,len(word))

def certify_lower_envelope(candidates,winner,M):
    """Nonnegative tensor Bernstein coefficients imply global dominance."""
    for candidate in candidates:
        a=[u-v for u,v in zip(candidate[0],winner[0])]
        b=[u-v for u,v in zip(candidate[1],winner[1])]
        for row in M:
            A=sum(c*d for c,d in zip(row,a))
            B=sum(c*d for c,d in zip(row,b))
            assert sign_pair(A,B)>=0,("Dominance not proved",candidate)
    return len(candidates)

def certify(verbose=True):
    all_words,restricted=signatures()
    assert (len(all_words),len(restricted))==(1876,1258)
    global_w=word_polynomial(GLOBAL_WORD)
    restricted_w=word_polynomial(RESTRICTED_WORD)
    assert global_w==(tuple(256*c for c in PG),(0,)*9)
    assert restricted_w==(tuple(4096*c for c in PR),(0,)*9)
    assert global_w in all_words and restricted_w in restricted
    M,den=bernstein_matrix()
    assert den==35
    certify_lower_envelope(all_words,global_w,M)
    certify_lower_envelope(restricted,restricted_w,M)
    assert tuple(16*r-g for g,r in zip(PG,PR))==GAP_POLY
    # The gap G(s)=H(s)/(16 N(s)^4). Prove H(s)>0 using 9 coefficients.
    coefficients=[
        sum(M[i][j]*GAP_POLY[j] for j in range(9))
        for i in range(9)
    ]
    assert all(v>0 for v in coefficients)
    if verbose:
        print("PASS: exact global 3T frontier, 1876 distinct polynomial classes")
        print("PASS: exact <=1 CNOT frontier, 1258 distinct polynomial classes")
        print("PASS: 3134 exact polynomial-class Bernstein comparisons")
        print("PASS: H(s)>0 via 9 positive Bernstein coefficients")
        print("Global R=PG(s)/(16*(79+8s+s^2)^4)")
        print("Restricted R=PR(s)/(79+8s+s^2)^4")
        print("H coefficients (ascending):",GAP_POLY)
    return all_words,restricted

if __name__=="__main__":
    certify()
