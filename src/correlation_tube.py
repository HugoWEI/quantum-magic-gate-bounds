"""Measurable sufficient Pauli-correlation test for a 3T/2-CNOT magic gap.

The exact uniform gap >1/100 for s in [-1/8,1/4], with
|psi_s> proportional to [-1+3i,-7-i,-1+i,-1+(4+s)i],
plus an 8sqrt(3) Lipschitz bound in the 15 Pauli coordinates proves
a strict 2-CNOT advantage for every pure two-qubit input with distance
<1/(800sqrt(3)) from this curve.

Nearest point is computed numerically; a strict guard is used to avoid
making claims on the floating-point boundary.
"""
import numpy as np
from src.magic_bounds import normalize,paulis

LABELS=('IX','IY','IZ','XI','XX','XY','XZ','YI','YX','YY','YZ','ZI','ZX','ZY','ZZ')
COEFF=np.array([(18,2,0),(38,-2,0),(-55,-8,-1),(14,-2,0),
    (38,6,0),(14,-2,0),(2,2,0),(-54,-14,0),(-18,-2,0),(-14,-6,0),
    (62,14,0),(41,-8,-1),(-2,-2,0),(50,2,0),(-25,8,1)],float)
RADIUS=1/(800*np.sqrt(3.))
LOW,HIGH=-1/8,1/4

def curve(s):
    n=79+8*s+s*s
    return COEFF@np.array([1.,s,s*s])/n

def pauli_vector(psi):
    psi=normalize(psi)
    if psi.size!=4:raise ValueError("pure two-qubit input required")
    return np.array([np.vdot(psi,paulis(2)[p]@psi).real for p in LABELS])

def nearest_point(psi):
    """Numerically minimize squared distance to a rational curve.

    Distance squared is Q(s)/N(s)^2 with deg Q<=4, so all candidates
    occur at interval endpoints or real roots of Q' N-2 Q N' (deg<=5).
    """
    from numpy.polynomial import Polynomial as Pol
    r=pauli_vector(psi)
    n=Pol([79,8,1])
    q=[Pol(tuple(-c))+r[i]*n for i,c in enumerate(COEFF)]
    sq=sum((w*w for w in q),Pol([0]))
    derivative=sq.deriv()*n-2*sq*n.deriv()
    candidates=[LOW,HIGH]
    for root in derivative.roots():
        if abs(root.imag)<1e-9 and LOW<=root.real<=HIGH:
            candidates.append(float(root.real))
    smin=min(candidates,key=lambda s:float(sq(s)/n(s)**2))
    dist=float(np.linalg.norm(r-curve(smin)))
    return dist,smin

def certificate(psi,numerical_guard=1e-11):
    """A True value is a *sufficient*, not necessary, theoretical condition.

    Caller should use certified interval arithmetic if very close to
    threshold. The numerical_guard is a pragmatic floating-point buffer.
    """
    distance,s=nearest_point(psi)
    return {'certified':bool(distance<RADIUS-numerical_guard),
            'distance':distance,'nearest_s':s,'threshold':float(RADIUS)}

if __name__=="__main__":
    for s in (LOW,0,.1,HIGH):
        psi=normalize(np.array([-1+3j,-7-1j,-1+1j,-1+(4+s)*1j]))
        print(s,certificate(psi))
