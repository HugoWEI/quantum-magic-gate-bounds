# Quantum magic gate bounds

**Research launch:** 29 October 2026 · Fall 2027 Physics PhD research portfolio · **status: rigorously verified baseline; novelty unconfirmed**.

Study tight input-conditioned changes of the second stabilizer Rényi entropy M2 under limited-depth Clifford+T circuits, focusing on entangled inputs with prior magic. A universal one-T bound and the unconstrained two-qubit magic–entanglement frontier are already known and are **not** claimed as discoveries.

## MAIN NEW THEOREM (30 Oct 2026): sharp input-preparation T threshold = 4

We now have a fully specified **sharp resource threshold** for an input-conditioned entangling-gate advantage. Let a fixed pure two-qubit input be prepared using `t_prep` T gates and arbitrary global Cliffords from a stabilizer, **then supplied as input** to a new converter allowed **<=3 additional T**, arbitrary local Cliffords, and 1 or 2 CNOTs, without ancillas or measurements. **If `t_prep<=3`, a second CNOT can never improve the maximal final M2.** This is proved across **all 18,900** Clifford+<=3T-prepared input rays, grouped into **10 full Clifford orbits and 58 local Clifford classes**. Exactly **48 classes reach the absolute pure-state optimum R=7/4 using <=1 CNOT**; the other **10 classes** have sharp unrestricted and one-CNOT optimum `R=463/256`, proved via exact 3616-word lower-bound checks on both exceptional full Clifford orbits.

Our previous engineered fixed magical input has **exact prep T-count 4** and a strict **two-CNOT > one-CNOT** gap with three additional T, so the **minimum input T-preparation count for *existence* of a second-CNOT advantage is exactly `4`**. This is a two-qubit, pure, ideal, ancilla-free, fixed-input conditional optimization theorem, *not* an end-to-end savings or a claim of literature priority.

[**Precise theorem and complete exact proof**](notes/sharp_four_t_input_threshold.md) · [source code](src/three_t_prepared_threshold.py) · [58 independent physical-circuit tests](tests/test_three_t_prepared_threshold.py). The 2T version [covers 2,580 states](notes/low_t_prepared_no_go.md). **Publication originality unverified.**

## Earlier: exact no-go theorem for ALL naturally low-T-prepared input states (30 Oct 2026)

**Every pure two-qubit state prepared from a stabilizer using at most two T gates and arbitrary Cliffords** can reach the **absolute maximum pure two-qubit stabilizer Rényi entropy**, `M2=log2(16/7)`, using **at most three additional T gates and at most ONE CNOT** with free local Cliffords. The input family is finite: exact signed Clifford orbit enumeration yields **2,580 distinct input rays** split into four global Clifford orbits of sizes **60, 360, 720, 1,440**, and **16 local-Clifford equivalence classes**. One explicit signed three-T, <=1-CNOT word for **each** of the 16 classes is certified using integer arithmetic in `Z[sqrt2]`; independent 4x4 state-vector tests construct the physical <=1-CNOT circuits.

**Necessary condition:** any input that exhibits our strict **two-CNOT** advantage when allowed up to three *additional* T gates must have exact stabilizer-to-input **T-preparation count at least 3**. Our previous engineered input has count 4, consistent with this theorem. This is a **conditional, pure, ancilla-free** statement, not a claim of general state-preparation savings. The global bound `log2(16/7)` and the Clifford tools are known prior art; **the originality of this finite conversion theorem is not yet verified**.

[**Theorem and 16 exact circuit witnesses**](notes/low_t_prepared_no_go.md) · [one-T orbit engine](src/one_t_natural_input_theorem.py) · [2,580-state exact certificate](src/two_t_prepared_no_go.py) · [independent dense physical circuit tests](tests/test_two_t_prepared_no_go.py). **Next target:** determine whether *three*-T-prepared natural inputs already support a strict two-CNOT gain, or whether the minimum input-preparation T-count is 4.

## Earlier: exact end-to-end accounting — tuned input prep costs four T and one CNOT (30 Oct 2026)

The tuned magical input `chi*=(Rx(pi/4)⊗I)(A|00>+B|11>)` from our 3T/2CNOT fixed-input theorem is **not free** when prepared from a product stabilizer `|00>`. We have now proved its **sharp preparation cost: 4 T gates and 1 physical CNOT**. An exact normal-form enumeration of 3616 zero/one/two/three-T words shows that any two-qubit stabilizer input can produce only **nine** values of the Clifford-invariant Pauli fourth moment `R` with <=3 T; the tuned target has `R=153/64`, which is absent. A constructive 4-T local-rotation word `(IX,IY,IZ,XI)` followed by `H0,CNOT(0→1),H1,H0` reproduces every target Pauli correlation **exactly** (and the full state up to phase). Its entanglement proves one CNOT necessary from a *product* stabilizer.

**Operational conclusion:** The specific staged path (prepare input, then maximize its magic) totals **7 T + 3 CNOT**, while Liu–Low–Yin (2026) already give a direct maximal-magic preparation from `|++>` using **3 T + 1 CNOT**. We independently verified that direct circuit. Thus our strict two-CNOT threshold remains a *fixed-input reachability* theorem; it is **not** evidence of a globally more efficient way to create maximal magic. [Full exact proof and honest comparison](notes/end_to_end_preparation_cost.md) · [machine-checkable certificate](src/input_preparation_cost.py) · [independent matrix tests](tests/test_input_preparation_cost.py). **Publication originality not established.**

## Earlier: exact maximal two-qubit magic needs three T and two CNOTs (30 Oct 2026)

We now have a **perfect**, not near-perfect, resource-state preparation result for a **fixed already-magical input**:

`chi*=(Rx(pi/4)⊗I)[A|00>+B|11>]`, with `A=(1-sqrt2+i(1+2sqrt2))/4`, `B=(1-sqrt2+i)/4`. This is a rotated-Schmidt input with `sin²(theta)=(2-sqrt2)/8`, `phi=atan(1-1/sqrt2)`, concurrence ≈0.521 and initial `R=153/64`. The chronological Pauli word **(XX,IZ,IY)** gives an output **identical up to global phase** to the established maximally magical Clifford fiducial `(1+3i,1+i,1-i,1+i)/4`, hence `R=7/4` and `M2=log2(16/7)` exactly.

**Both gate budgets are sharp:** With unrestricted Clifford routing but **≤2 T**, the exact minimum moment is **463/256 > 7/4**. With **≤3 T and ≤1 physical CNOT**, the exact minimum is **8265/4096−81 sqrt2/512 ≈1.794089 >7/4**, a strict gap `(1097−648 sqrt2)/4096 >1/25`. A separate constructive Clifford compiler attains the optimum with **2 CNOTs** and three T gates. The exact certificate enumerates **3616 unrestricted** words and **19897 conservatively exhaustive restricted signed** candidates using only integer arithmetic in Q(sqrt2), with independent 4x4 matrix tests.

[**Precise theorem, proof, physical caveats**](notes/exact_maximal_magic_two_cnot_threshold.md) · [exact executable certificate](src/three_t_exact_maximal_magic.py) · [tests](tests/test_three_t_exact_maximal_magic.py). **Critical prior-art contrast:** Liu–Low–Yin (2026, Fig. 1) already prepare a maximally magical two-qubit state from the *stabilizer* `|++>` with **three T and ONE CNOT**. Our exact two-CNOT requirement is **strictly fixed-input** for the specified *already-magical* input, not an absolute resource requirement. **Input preparation resources are NOT counted; literature originality is NOT yet established.**

## Earlier: exact 99.9816% fidelity with the known maximal-magic Clifford orbit (30 Oct 2026)

Our **two-CNOT, three-T magic-optimal output** from the clean rotated-Schmidt input is **uniquely closest** among all **480** known maximally magical two-qubit Clifford fiducials to `(I⊗S)(H⊗H)(1,i,i,i)/2`. The **exact** squared overlap is `(17+3 sqrt(3)+4 sqrt(6))/32 = 0.999815981...`; the second-best among the 480 is only ≈0.817912. The final state also has concurrence ≈0.71032, close to the nearest fiducial's 1/sqrt(2). The restricted circuit's **M2-optimal** output has lower nearest-orbit fidelity ≈0.959518 (not a global fidelity optimization over restricted circuits).

A new [480-orbit exact certificate](src/maximal_magic_orbit_certificate.py) generates the orbit from signed 15-component Pauli expectation permutations using *exact Gaussian-integer Clifford matrix identities*, then compares all overlaps via exact Q(sqrt2,sqrt3) integer-square-root intervals. This connects our *gate-budget dynamical optimization* to the established *static 480-state maximal-magic geometry*. [Proof and interpretation](notes/exact_maximal_magic_orbit_proximity.md) · [independent matrix tests](tests/test_maximal_magic_orbit.py). **Novelty remains unverified; the 480-state orbit is known prior work.**

## Earlier: simple rotated-Schmidt input needs two CNOTs and reaches near-maximal magic (30 Oct 2026)

A clean input `chi=(Rx(pi/4)⊗I)[cos(pi/12)|00>+exp(i*pi/12)sin(pi/12)|11>]` has **concurrence 1/2**, initial `R=621/256` and intrinsic nonstabilizer magic. With at most **three T gates**, its unrestricted optimum is attained by `(XX,IZ,IY)`, while the best **at-most-one-CNOT** circuit uses signed `(-ZX,-IY,-ZI)`. Exact fourth moments are in the small biquadratic field `Q(sqrt2,sqrt3)` and satisfy a strict **gap > 1/25 = 0.04** (actual ≈0.04725285), corresponding to **0.03843 extra stabilizer Rényi bits**. The optimal two-CNOT output achieves M2≈1.192319, just ≈0.000326 bits below the two-qubit pure-state maximum log2(16/7).

This is fully certified by a **separate** exact algebraic-number implementation (3616 unrestricted / 19897 conservatively exhaustive restricted circuits, with integer-square-root sign certification), corroborated by dense-statevector tests. See [complete theorem and exact expressions](notes/simple_state_three_t_threshold.md), [code](src/three_t_simple_state_certificate.py) and [tests](tests/test_three_t_simple_state.py). **Publication originality remains unverified.** Schmidt alignment alone showed no two-CNOT gap on an 81-point exploratory grid (not a theorem); the local basis orientation appears crucial.

## Earlier: exact rational three-T optimal frontiers + correlation-space tube (30 Oct 2026)

For every `-1/8 <= s <= 1/4` in our explicit partially entangled magical family, the optimal unrestricted <=3T output is attained by **(YY,XI,XY)**, and the exact <=1-CNOT output by the **two-T** word **(ZI,ZY)**. We proved the exact rational formulas `R_unrestricted=PG(s)/(16*N(s)^4)` and `R_<=1CNOT=PR(s)/N(s)^4`, with `N(s)=s²+8s+79`, by grouping 3616 unrestricted circuits into **1876** exact polynomial classes and 19897 restricted candidates into **1258** classes. **All 3134 exact Bernstein class-dominance inequalities pass**, and a separate 9-coefficient positivity argument proves the difference polynomial is positive.

The uniform >0.01 gap also implies a **open neighborhood of pure two-qubit states specified by measurable Pauli correlators**: any pure input whose 15-component Pauli expectation vector lies within Euclidean distance **1/(800 sqrt(3))** of our reference correlation curve needs exactly 2 CNOTs for the <=3T magic optimum. This is a sufficient condition, not a global classification. [**Exact polynomials, certificate and correlation-tube proof**](notes/three_t_exact_branch_and_correlation_tube.md) · [code](src/three_t_exact_branch_frontier.py) · [tests](tests/test_three_t_exact_branch_frontier.py). **Publication novelty unverified.**

## Earlier: exact continuous family with a uniform three-T two-CNOT advantage

The previously isolated three-T witness is part of a provable **continuous 3/8-wide parameter interval**:
`psi(s)=[-1+3i,-7-i,-1+i,-1+(4+s)i]/sqrt(79+8s+s²)` for **`-1/8 <= s <= 1/4`**. For **every** state on this family, with <=3 T gates, the best <=1-CNOT output Pauli fourth moment is **more than 1/100 larger** than the unrestricted optimum. The certificate compares a single constructive 2-CNOT word `(YY,XI,XY)` with all **19,897** one-CNOT-or-less candidate words and verifies **179,073 exact Q(sqrt(2)) Bernstein coefficient inequalities**. Independent direct 4x4 state-vector tests match the algebra. The states remain partially entangled and inherently magical.

A compact **symplectic explanation** now classifies all 1530 three-Pauli axis triples that cannot be simultaneously localized in one Clifford frame: 1440 independent triples with >=2 anticommutations and 90 distinct mutually commuting stabilizer contexts. This structural obstruction is **not by itself a physical CNOT lower bound**; the strict polynomial certificate supplies the full result.

[Parametric theorem, proof and classification](notes/three_t_parametric_and_symplectic.md) · [uniform exact certificate](src/three_t_parametric_certificate.py) · [symplectic graph checker](src/three_t_symplectic_obstruction.py) · [independent regression tests](tests/test_three_t_parametric.py). **Publication originality unverified.**

## Earlier exact result: three-T magic needs two CNOTs for a fixed input (29 October 2026)

For the partially entangled magical input `[-1+3i, -7-i, -1+i, -1+4i] / sqrt(79)`, **at most three T gates** give a sharp entangling budget of **exactly TWO physical CNOTs** to attain the unrestricted output M2 optimum. Unrestricted minimum fourth moment: `1103764401/623201296` via axes `(YY,XI,XY)`. With at most one CNOT: `69521131/38950081`. Exact positive gap: `8573695/623201296`, equivalent to `0.011163101877318` extra bits. This is **not** a numerical estimate: a `Q(sqrt2)` integer certificate exhausts 3616 unrestricted 0/1/2/3-T words and an overcomplete 19897 one-CNOT-or-less signed circuit candidates, explicitly checking all positions of the CNOT. A constructive compiler proves any three-Pauli-T word needs at most two CNOTs **up to an irrelevant final Clifford**, and the witness achieves exactly two.

[**Precise theorem and finite proof**](notes/three_t_two_cnot_threshold.md) · [exact certificate](src/three_t_exact_gap.py) · [two-CNOT compiler](src/three_t_two_cnot_compiler.py) · [independent tests](tests/test_three_t_exact_gap.py). **Publication novelty NOT confirmed**; extensive supplemental/citation audit and expert scrutiny remain necessary.

## Earlier universal theorem: one CNOT suffices for every two-qubit input (29 October 2026)

**No Schmidt alignment assumption.** For any pure two-qubit input and at most **two T gates**, arbitrary global Clifford routing yields no greater M2 than **one physical CNOT** plus arbitrary single-qubit Cliffords. The proof simultaneously localizes *any two* nonidentity Pauli axes using local Cliffords and one oriented CNOT, then drops a final Clifford which leaves M2 invariant. All **225** ordered axis pairs are certified (36 already local; 189 with one CNOT), with signed 4×4 dense-matrix verification and a complete six-case pen-and-paper proof.

**Exact input-specific minimum CNOT cost:** compare all 43 zero-CNOT Pauli words against the 241 unrestricted zero/one/two-T words. The minimum budget is **0 or 1**, according to whether the two minimum fourth moments agree. [Theorem, proof, bibliography and limitations](notes/universal_one_cnot.md) · [Clifford witness compiler](src/one_cnot_universality.py) · [arbitrary-input cost oracle](src/cnot_cost_oracle.py). A seeded exploratory 200-state Haar sample found strict one-CNOT benefit for 168 inputs (not a theorem).

**Importantly:** this is a simple Clifford localization statement whose **literature novelty is not established**; it does not optimize exact unitary synthesis or fully timed circuit depth. A potentially richer case starts at **three T gates**, where 1530 of 3375 ordered Pauli triples **cannot be simultaneously localized by any Clifford**, verified against all 720 two-qubit Clifford symplectic transformations (this is **not** a 2-CNOT lower bound for three-T magic optimization). [Three-T exploratory classifier](src/three_t_prelocalization.py).

## Special Schmidt-family entangling-depth-one theorem and intrinsic-magic separation (29 October 2026)

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
python -m src.one_cnot_universality
python -m src.three_t_prelocalization
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
