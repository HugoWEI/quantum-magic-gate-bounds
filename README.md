# Quantum magic gate bounds

**Research launch:** 29 October 2026 · Fall 2027 Physics PhD research portfolio · **status: rigorously verified baseline; novelty unconfirmed**.

Study tight input-conditioned changes of the second stabilizer Rényi entropy M2 under limited-depth Clifford+T circuits, focusing on entangled inputs with prior magic. A universal one-T bound and the unconstrained two-qubit magic–entanglement frontier are already known and are **not** claimed as discoveries.

## New: exact entangling-depth-one theorem and intrinsic-magic separation (29 October 2026)

- **One physical CNOT suffices** to attain the full two-T Schmidt-phase magic optimum. Three explicit H/S/T/CNOT circuit templates attain the A/B/C branches with **0/1/1 CNOT**, because they equal the Pauli-word optimum up to a final Clifford. At theta=pi/8, phi=pi/4, 0 CNOT cannot attain it (129/64 vs 121/64 fourth moments), so 1 is sometimes **necessary and sufficient**. This is a real entangling-gate-count theorem for an M2 objective, **not** an exact-unitary synthesis theorem.
- **Intrinsically magical isomagic pair:** two *partially* entangled inputs with equal concurrence sqrt(3)/2 and initial M2=log2(128/91) have different two-T optimal gain: state A's optimum is 0.547449 bits while state B has a certified **achievable** 0.649357 bits. The strict difference is proved by rational intervals, without claiming that B's full optimum is known.
- **Arbitrary-orientation oracle:** all 1+15+225 zero/one/two-T candidates can be compared from the input's 16 Pauli expectations, for any pure two-qubit input. This is an exact finite optimization evaluated numerically, not a generic closed-form analytic theorem.

See [new proofs and circuit model](notes/cnot_and_intrinsic_isomagic.md), [one-CNOT code](src/one_cnot_saturation.py), [intrinsic-magic exact certificate](src/intrinsic_isomagic_separation.py) and [generic Pauli-moment optimizer](src/arbitrary_input_oracle.py). **Publication novelty has not been established.**

## Main result: exact two-parameter two-T frontier (proved 29 October 2026)

For **every** Schmidt-phase two-qubit input `cos(theta)|00>+exp(i phi)sin(theta)|11>`, we proved the exact maximal M2 increase with **at most two T gates and arbitrary global two-qubit Clifford routing**, in a closed-form minimum of **three explicit polynomial branches**. All **225** Pauli-axis words collapse into **21** exact moment classes, and all 18 inactive classes are excluded by **42 exact Q(sqrt(2)) Bernstein rectangles**, independently cross-checked by dense matrix simulation. The sharp circuit phase diagram has a triple point at `sin²(phi)=sqrt(5)-2`, `sin²(2theta)=(1+sqrt(5))/4`; its middle branch yields a constant gain `log2(16/11)`. **No physical Clifford-depth bound. Novelty not yet verified against all published work.**

**[Complete two-parameter theorem, proof and reproduction](notes/general_phase_frontier.md)** · [symbolic certificate](src/general_phase_certificate.py) · [matrix tests](tests/test_general_phase.py)

## Further exact corollaries (proved, novelty unverified)

1. **Two-T isomagic separation:** two Bell-derived maximally entangled states with the same concurrence 1 and M2 = log2(64/49) have *different* optimal two-T gains: 0.781819829950 versus 0.713388650476 bits. All 225 words for the latter state are certified with exact rational interval signs.
2. **Local-only Clifford routing:** Restricting intermediate Cliffords to single-qubit gates gives 36 two-T Pauli words, 5 exact classes, and sharp at-most-two-T output moment `min(A,D,3R_in/4)`. At an intrinsically magical entangled input, unrestricted entangling Clifford routing improves the gain by exactly `log2(129/121)` bits over local-only gates.

See [full proofs and circuit-model cautions](notes/extension_corollaries.md), [isomagic certificate](src/two_t_isomagic_counterexample.py), [local-routing certificate](src/local_clifford_frontier.py). These are **not** yet novelty-certified or physical-depth-constrained results.

## Earlier one-phase slice (also proved 29 October 2026)

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
python -m src.general_phase_certificate
python -m src.two_t_isomagic_counterexample
python -m src.local_clifford_frontier
python -m src.one_cnot_saturation
python -m src.intrinsic_isomagic_separation
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
