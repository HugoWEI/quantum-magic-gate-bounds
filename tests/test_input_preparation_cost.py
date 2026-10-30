"""Independent dense-state verification of exact input-preparation costs."""
import unittest
import numpy as np
from math import pi,sqrt,log2
from src.magic_bounds import ONE,X,Z,paulis,fourth_moment,concurrence,normalize
from src.one_cnot_universality import signed_t
from src.input_preparation_cost import verify,WORD,FINAL_CLIFFORD
from src.three_t_exact_maximal_magic import INIT

H=(X+Z)/sqrt(2)
CNOT=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],complex)
S=np.diag([1,1j])
GATES={"H0":np.kron(H,ONE),"H1":np.kron(ONE,H),"CNOT":CNOT}

def target():
    A=(1-sqrt(2)+1j*(1+2*sqrt(2)))/4
    B=(1-sqrt(2)+1j)/4
    Rx=np.cos(pi/8)*ONE-1j*np.sin(pi/8)*X
    return np.kron(Rx,ONE)@np.array([A,0,0,B],complex)

class PreparationCostTests(unittest.TestCase):
    def test_exact_integer_certificate(self):
        spectrum,word,clifford=verify(False)
        self.assertEqual(len(spectrum),9)
        self.assertNotIn(153/64,spectrum)
        self.assertEqual(len(word),4)
        self.assertEqual(sum(g=="CNOT" for g in clifford),1)

    def test_independent_dense_prep_and_target_signature(self):
        output=np.array([1,0,0,0],complex)
        for p in WORD:output=signed_t(output,p,1)
        for gate in FINAL_CLIFFORD:output=GATES[gate]@output
        chi=target()
        self.assertAlmostEqual(abs(np.vdot(chi,output))**2,1.,places=12)
        self.assertAlmostEqual(fourth_moment(output),153/64,places=12)
        self.assertGreater(concurrence(output),.5)
        for p,mat in paulis(2).items():
            a,b=INIT.get(p,(0,0))
            self.assertAlmostEqual(float(np.vdot(output,mat@output).real),
                                   (a+b*sqrt(2))/4,places=12)

    def test_direct_stabilizer_to_max_magic_3t_one_cnot(self):
        T=np.diag([1,np.exp(1j*pi/4)])
        plus=np.ones(4,complex)/2
        out=np.kron(ONE,T)@CNOT@np.kron(T,T)@plus
        fid=np.array([1,1j,1j,1j],complex)/2
        self.assertAlmostEqual(abs(np.vdot(out,fid))**2,1,places=12)
        self.assertAlmostEqual(fourth_moment(out),7/4,places=12)
        self.assertAlmostEqual(concurrence(out),1/sqrt(2),places=12)

if __name__=="__main__":unittest.main()
