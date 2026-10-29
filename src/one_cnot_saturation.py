"""Constructive entangling-depth-1 saturation of the Schmidt two-T frontier.

Hardware model: at most two local T gates, arbitrary one-qubit Cliffords,
at most one two-qubit CNOT. Objective is M2, not exact unitary synthesis.
No measurements or ancillas. The proven *upper* bound uses the published
exact full-phase frontier (see notes/general_phase_frontier.md).
"""
import numpy as np
from src.magic_bounds import ONE,X,Z,t_pauli,fourth_moment,schmidt_phase

CNOT=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],complex)
H=(X+Z)/np.sqrt(2)
CZ=np.kron(ONE,H)@CNOT@np.kron(ONE,H)

def branch_circuit(state, branch):
    """Three physical H/S/T/CNOT circuit templates (T_X and T_Y are one-T local conjugations)."""
    if branch=="A": return t_pauli(t_pauli(state,"IX"),"YI")
    if branch=="B": return t_pauli(CNOT@t_pauli(state,"IX"),"IY")
    if branch=="C": return t_pauli(CZ@t_pauli(state,"IX"),"IX")
    raise ValueError(branch)

def reference_circuit(state,branch):
    first,second={"A":("IX","YI"),"B":("IX","ZY"),"C":("IX","ZX")}[branch]
    return t_pauli(t_pauli(state,first),second)

def moments(theta,phi):
    t=np.sin(2*theta)**2;x=np.sin(phi)**2
    k=1-t+t*t*(1-x+x*x)
    return {"A":(9-8*t+8*t*t+6*t*x-8*t*t*x+9*t*t*x*x)/4,
            "B":11*k/4,
            "C":(16-16*t+(9-8*x+8*x*x)*t*t)/4}

def verify_dense():
    assert np.allclose(CZ,np.diag([1,1,1,-1]))
    for theta,phi in [(0,0),(.18,.2),(.33,.5),(.5,.3),
                      (np.pi/8,np.pi/4),(np.pi/4,np.pi/4)]:
        state=schmidt_phase(theta,phi)
        for branch,target in moments(theta,phi).items():
            physical=branch_circuit(state,branch)
            ideal=reference_circuit(state,branch)
            expected={"A":ideal,"B":CNOT@ideal,"C":CZ@ideal}[branch]
            assert np.allclose(physical,expected,rtol=1e-13,atol=1e-13)
            assert abs(fourth_moment(physical)-target)<1e-11
    print("PASS: all three exact optimal branches use 0 or 1 physical CNOT")

if __name__=="__main__":verify_dense()
