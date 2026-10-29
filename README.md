# Quantum magic gate bounds

**Research launch:** 29 October 2026 · Fall 2027 Physics PhD research portfolio · **status: rigorously verified baseline; novelty unconfirmed**.

Study tight input-conditioned changes of the second stabilizer Rényi entropy M2 under limited-depth Clifford+T circuits, focusing on entangled inputs with prior magic. A universal one-T bound and the unconstrained two-qubit magic–entanglement frontier are already known and are **not** claimed as discoveries.

## Exact two-T input-conditioned frontier (proved 29 October 2026)

For the entangled input family **cos(theta)|00> + exp(i*pi/4)sin(theta)|11>** (phase **pi/4, not pi/2**), we have now proved a sharp **three-branch conditional two-T gain**, with transitions at squared concurrence `(3-sqrt(5))/2` and `2*(sqrt(2)-1)`. The proof classifies all **225** ordered Pauli-axis pairs into 15 exact fourth-moment classes, excludes all inactive classes using exact rational Bernstein and quartic positivity certificates, and independently checks all 225 words with dense state-vector simulation. This is **arbitrary free two-qubit Clifford routing, NOT bounded physical circuit depth**. Full statement and proof: [notes/two_t_frontier.md](notes/two_t_frontier.md). Novelty in the published literature remains unverified.

## First reproducible results

1. On |psi> = cos(theta)|00> + exp(i phi)sin(theta)|11>, exact Pauli fourth-moment expressions for local T and HTH. HTH saturates Zhu et al.'s log2(4/3) increase even with prior intrinsic magic at partial entanglement. This is a derived baseline, not a novelty claim.
2. **Exact isomagic counterexample**: two maximally entangled pure states with identical M2 = log2(64/49) have different maximal one-T gains under arbitrary Clifford routing: log2(4/3) versus log2(49/37). The latter uses an exact 15-Pauli-axis deficit certificate. Thus concurrence and scalar M2 alone do not determine fixed-input optimal gate gain.
3. Direct enumeration of up to 15^k Pauli-rotation words for very small k. The Schmidt-phase-slice two-T frontier is now proved. A generic-input or bounded-depth frontier is **not yet proved**.

## Reproduction

Python >=3.10, NumPy and SymPy; no GPU needed.

```bash
python -m pip install -r requirements.txt
python -m src.symbolic_verify
python -m src.exact_counterexample
python -m src.two_t_frontier_certificate
python -m unittest discover -s tests -v
```

See [literature exclusions](notes/literature.md) and [derivations + exact proof](notes/derivation.md).

## Distinctions

- Gate count k is not physical circuit depth; Clifford routing may increase depth. Local-only Clifford access gives fewer candidate Pauli axes than arbitrary two-qubit Cliffords.
- A Bell state's apparent magic can be removed by arbitrary local unitaries, unlike intrinsic magic of partially entangled states with non-flat Schmidt spectrum.
- No publishable novelty or peer-review claim is made; full related-work and supplementary checks remain required.

## Primary prior work

Zhu et al. (2024), https://arxiv.org/abs/2409.06659
Roman et al. (2026), https://arxiv.org/html/2603.24902v1
Hou et al. (2026), https://doi.org/10.1038/s41534-026-01265-4
Leone et al. (2022), https://doi.org/10.1103/PhysRevLett.128.050402
