"""Guard against CI-only module name mismatches across research certificates."""
import importlib
import unittest

MODULES = [
    "src.magic_bounds",
    "src.symbolic_verify",
    "src.exact_counterexample",
    "src.two_t_frontier_certificate",
    "src.general_phase_certificate",
    "src.two_t_isomagic_counterexample",
    "src.local_clifford_frontier",
    "src.one_cnot_saturation",
    "src.intrinsic_isomagic_separation",
    "src.arbitrary_input_oracle",
    "src.one_cnot_universality",
    "src.cnot_cost_oracle",
    "src.three_t_prelocalization",
    "src.three_t_exact_gap",
    "src.three_t_two_cnot_compiler",
    "src.three_t_symplectic_obstruction",
    "src.three_t_parametric_certificate",
    "src.three_t_exact_branch_frontier",
    "src.correlation_tube",
    "src.three_t_simple_state_certificate",
    "src.maximal_magic_orbit_certificate",
    "src.three_t_exact_maximal_magic",
    "src.input_preparation_cost",
]

class ImportContractTests(unittest.TestCase):
    def test_every_research_module_imports(self):
        for module in MODULES:
            with self.subTest(module=module):
                self.assertIsNotNone(importlib.import_module(module))

if __name__ == "__main__":
    unittest.main()
