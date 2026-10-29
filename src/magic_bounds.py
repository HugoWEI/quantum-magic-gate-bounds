"""Exact n-qubit Pauli fourth-moment evaluators for Clifford+T research.

Qubits ordered left-to-right; log base 2. T_P=exp(-i*pi*P/8)
differs from a Clifford-conjugated T only by an irrelevant global phase.
"""
from __future__ import annotations
from functools import lru_cache
from itertools import product
import numpy as np

ONE = np.eye(2, dtype=np.complex128)
X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
Z = np.diag([1, -1]).astype(np.complex128)
LOCAL = {"I": ONE, "X": X, "Y": Y, "Z": Z}

@lru_cache(None)
def paulis(n: int) -> dict[str, np.ndarray]:
    out = {}
    for labels in product("IXYZ", repeat=n):
        mat = np.array([[1]], dtype=np.complex128)
        for label in labels:
            mat = np.kron(mat, LOCAL[label])
        out["".join(labels)] = mat
    return out

def normalize(psi: np.ndarray) -> np.ndarray:
    psi = np.asarray(psi, dtype=np.complex128).reshape(-1)
    n = int(round(np.log2(psi.size)))
    if 2**n != psi.size:
        raise ValueError("State dimension must be a power of two")
    norm = np.linalg.norm(psi)
    if not norm:
        raise ValueError("Zero state")
    return psi / norm

def expectations(psi: np.ndarray) -> dict[str, float]:
    psi = normalize(psi)
    return {k: float(np.real(np.vdot(psi, p @ psi)))
            for k, p in paulis(int(round(np.log2(psi.size)))).items()}

def fourth_moment(psi: np.ndarray) -> float:
    return float(sum(v**4 for v in expectations(psi).values()))

def m2(psi: np.ndarray) -> float:
    psi = normalize(psi)
    n = int(round(np.log2(psi.size)))
    return float(-np.log2(fourth_moment(psi) / 2**n))

def t_pauli(psi: np.ndarray, label: str) -> np.ndarray:
    psi = normalize(psi)
    matrix = paulis(int(round(np.log2(psi.size))))[label]
    return np.cos(np.pi/8)*psi-1j*np.sin(np.pi/8)*(matrix@psi)

def gain(psi: np.ndarray, axis: str) -> float:
    return m2(t_pauli(psi, axis))-m2(psi)

def concurrence(psi: np.ndarray) -> float:
    a, b, c, d = normalize(psi)
    return float(2 * abs(a*d-b*c))

def schmidt_phase(theta: float, phi: float) -> np.ndarray:
    return normalize(np.array([np.cos(theta),0,0,
                               np.exp(1j*phi)*np.sin(theta)]))

def schmidt_moment(theta: float, phi: float) -> tuple[float,float,float]:
    """Analytic R2 before, after local T_Z, after local T_X=HTH."""
    c = np.sin(2*theta)
    base = 4-4*c*c+4*c**4
    s = np.sin(2*phi)**2
    return base-c**4*s, base-c**4*(1-s), 0.75*(base-c**4*s)

def best_axis(psi: np.ndarray, local_only: bool=False) -> tuple[str,float]:
    n = int(round(np.log2(normalize(psi).size)))
    p = paulis(n)
    axes = [x for x in p if x.count("I")==n-1] if local_only else [
        x for x in p if x != "I"*n]
    return max(((axis, gain(psi, axis)) for axis in axes),
               key=lambda z:z[1])

def zhu_deficit(psi: np.ndarray, axis: str) -> float:
    """Established nonnegative identity: 4R2(T_P psi)-3R2(psi)."""
    psi = normalize(psi)
    return 4*fourth_moment(t_pauli(psi,axis))-3*fourth_moment(psi)

def best_sequence(psi: np.ndarray, k: int) -> tuple[tuple[str,...],float]:
    """Exhaust 15^k Pauli words for n=2 (general n: (4^n-1)^k).

    Equivalent to k T gates with arbitrary free Clifford routing.
    Chronological axis sequence; exponential, for very small k only.
    """
    if k<0:
        raise ValueError("k must be nonnegative")
    psi=normalize(psi)
    n=int(round(np.log2(psi.size)))
    axes=[p for p in paulis(n) if p!="I"*n]
    initial=m2(psi)
    best=((),0.0)
    for word in product(axes, repeat=k):
        v=psi
        for p in word:
            v=t_pauli(v,p)
        delta=m2(v)-initial
        if delta>best[1]:
            best=(word,float(delta))
    return best
