"""Full 720-symplectic-Clifford triple-localization checks."""
import unittest
from src.three_t_prelocalization import count_classes,full_symplectic_cliffords,INDEX,LOCAL_INDICES

class ThreeTLocalizationTests(unittest.TestCase):
    def test_group_and_class_counts(self):
        self.assertEqual(count_classes(),{
            'all_local':216,'one_cnot_localizable_total':1845,
            'no_clifford_can_simultaneously_localize':1530,
            'symplectic_group_size':720})

    def test_impossible_example_under_every_clifford(self):
        p,q,r=(INDEX[x] for x in ('IX','IY','XX'))
        for clifford in full_symplectic_cliffords():
            self.assertFalse(all(clifford[x] in LOCAL_INDICES for x in (p,q,r)))

if __name__=='__main__':unittest.main()
