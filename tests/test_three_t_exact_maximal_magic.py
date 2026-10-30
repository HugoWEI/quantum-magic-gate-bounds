"""Cross-check exact maximal-magic reachability and CNOT lower bound."""
import unittest
from math import pi,sqrt,log2
import numpy as np
from src.magic_bounds import ONE,X,paulis,concurrence,fourth_moment,m2
from src.one_cnot_universality import signed_t
from src.three_t_exact_maximal_magic import certify

def exact_input():
    A=(1-sqrt(2)+1j*(1+2*sqrt(2)))/4
    B=(1-sqrt(2)+1j)/4
    R=np.cos(pi/8)*ONE-1j*np.sin(pi/8)*X
    return np.kron(R,ONE)@np.array([A,0,0,B],complex)

def evolved(psi,word,signs):
    for p,s in zip(word,signs):psi=signed_t(psi,p,s)
    return psi

class ExactMaximalMagicTests(unittest.TestCase):
    def test_exact_enumeration(self):
        global_best,restricted,gap=certify(False)
        self.assertEqual(global_best,((1835008,0),("XX","IZ","IY")))
        self.assertEqual(restricted[0],(2115840,-165888))
        self.assertEqual(gap,(280832,-165888))

    def test_dense_statevectors_and_fiducial(self):
        psi=exact_input()
        self.assertAlmostEqual(float(np.vdot(psi,psi).real),1,places=12)
        self.assertAlmostEqual(fourth_moment(psi),153/64,places=12)
        self.assertAlmostEqual(concurrence(psi),sqrt((5-2*sqrt(2))/8),places=12)
        output=evolved(psi,("XX","IZ","IY"),(1,1,1))
        fid=np.array([1+3j,1+1j,1-1j,1+1j],complex)/4
        self.assertAlmostEqual(abs(np.vdot(output,fid))**2,1,places=12)
        self.assertAlmostEqual(fourth_moment(output),7/4,places=12)
        self.assertAlmostEqual(m2(output),log2(16/7),places=12)
        restricted=evolved(psi,("YI","XY","IX"),(-1,-1,-1))
        expect=8265/4096-81*sqrt(2)/512
        self.assertAlmostEqual(fourth_moment(restricted),expect,places=12)
        self.assertGreater(fourth_moment(restricted)-fourth_moment(output),.04)

    def test_input_schmidt_angle_formula(self):
        theta=np.arcsin(np.sqrt((2-sqrt(2))/8))
        phi=np.arctan(1-1/sqrt(2))
        self.assertAlmostEqual(theta*180/pi,15.69985740495952,places=10)
        self.assertAlmostEqual(phi*180/pi,16.32494993689524,places=10)
        A=(1-sqrt(2)+1j*(1+2*sqrt(2)))/4
        B=(1-sqrt(2)+1j)/4
        self.assertAlmostEqual(abs(A),np.cos(theta),places=12)
        self.assertAlmostEqual(abs(B),np.sin(theta),places=12)
        self.assertAlmostEqual(np.angle(B/A),phi,places=12)

if __name__=="__main__":
    unittest.main()
