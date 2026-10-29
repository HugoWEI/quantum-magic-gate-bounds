# Prior-art boundary (checked 29 October 2026)

**This is a targeted literature/theorem comparison, not an exhaustive novelty search. Do not claim publishable novelty yet.**

| Prior work | What is already established | What remains a *candidate* question |
|---|---|---|
| Zhu, Chen, Shen, Liu, Yu, Wang, **Amortized Stabilizer Rényi Entropy of Quantum Dynamics** (2024), [arXiv:2409.06659](https://arxiv.org/abs/2409.06659), Theorem 2 / Appendix C | Exact universal gain for one T: M2^A(T)=2-log2(3)=log2(4/3), valid with ancillas and initially magical pure inputs. Composition implies k log2(4/3). Their proof uses Pauli fourth moments and an exact positivity inequality. | Which **fixed inputs** can attain equality, what correlation information is needed to quantify a strict deficit, and what can shallow Clifford+T sequences reach? Algebraic rewrites of their theorem are not original discoveries. |
| Roman, Knipfer, Neto, Matchev, Matcheva, Gleyzer, **The Pareto Frontiers of Magic and Entanglement: The Case of Two Qubits** (2026), [arXiv:2603.24902](https://arxiv.org/html/2603.24902v1) | Complete two-qubit maximum and minimum static M2 at fixed concurrence, including extremizer families. Global two-qubit maximum is **ln(16/7)** using their natural-log convention, or **log2(16/7)** in our bits convention. At intermediate concurrence, magic cannot vanish. | Dynamical **reachability from a specified input** under limited T-count and Clifford routing; static Pareto frontiers alone do not characterize this reachable set. Beware: arbitrary global Clifford routing may change concurrence. |
| Hou, Cao, Yang, **Stabilizer entanglement enhances magic injection** (2026), [npj Quantum Information 12, 113](https://doi.org/10.1038/s41534-026-01265-4) (published 11 May 2026; version of record 20 July 2026; [arXiv precursor 2503.20873](https://arxiv.org/abs/2503.20873) titled *Stabilizer Entanglement as a Magic Highway*) | Entanglement-enhanced injection on stabilizer inputs under Haar-local U and unitary SRE; also numerical explorations of non-stabilizer entanglement and shallow brickwork circuits. Explicitly raises systematic intrinsic magic capacity as an open direction. | Deterministic, fixed-input structured Clifford+T reachability and exact orientation-dependent capacities. **Do not claim** first treatment of initial non-stabilizer entanglement or shallow circuits; inspect their supplement fully. |
| Leone, Oliviero, Hamma, **Stabilizer Rényi Entropy** (2022), [PRL 128, 050402](https://doi.org/10.1103/PhysRevLett.128.050402) | The SRE definition and properties. | Baseline conventions only. |
| Liu, Low, Yin, **Maximal magic for two-qubit states** (2026) | Earlier two-qubit maximal magic results/bounds; cited by Roman. | Prior-art chronology when using a global magic cap. |

## The working research gap (hypothesis, not novelty verification)

For a **fixed entangled magic input** psi, define F_k(psi) as the maximum M2 increase from Clifford+T circuits with k T gates (specifying whether Cliffords are globally available or locality/depth-limited). Is there a certified, state-dependent analytic frontier strictly finer than the Zhu count bound and Roman's static state bound? Which Pauli correlation invariants distinguish states at the same initial concurrence and M2? Our exact counterexample confirms the latter distinction is necessary, but **does not establish that the insight is new**.

## Required novelty checks before paper claims

1. Read all of Zhu Appendix C and references on single-T equality/saturation input classifications.
2. Read all of Roman's 34 pages, including explicit extremal state families, and Hou's supplement on non-stabilizer inputs and brickwork.
3. Forward-citation search through 29 Oct 2026: "fixed-input magic capacity", "T gate stabilizer Rényi saturation", "Pauli rotation fourth moments", "amortized SRE equality", "two T gates magic growth".
4. Check whether arbitrary global Clifford interleaving or strictly local Clifford gates are allowed in every claimed theorem; distinguish **T-count from physical depth**.
5. Independently certify all candidate piecewise two-T frontiers over **225 Pauli-axis words**; simulations alone cannot prove a sharp bound.

## Update: exact finite two-T slice theorem (29 October 2026)

An exact 225-word, 15-class three-branch fixed-input theorem for |psi>=cos(theta)|00>+exp(i*pi/4)sin(theta)|11> was independently certified; details in [two_t_frontier.md](two_t_frontier.md). This is a **restricted-input theorem** allowing unrestricted global Clifford routing, not a physical-depth-constrained or arbitrary-input theorem, and must **not** be advertised as literature-novel yet.

Additional relevant work: Szombathy, Valli, Moca, Asbóth, Farkas, Rakovszky and Zaránd, [*Spectral properties versus magic generation in T-doped random Clifford circuits*](https://doi.org/10.1103/557f-6tpb), *Physical Review Research* **7**, 043080 (2025), studies the distribution and nonstabilizing power of T-doped random Clifford circuits, including low-T behavior. Their random-ensemble statements are not the same optimization, but inspect their appendices and citing papers before novelty claims. The already established Zhu Theorem 2, Roman static Pareto boundary, and Hou non-stabilizer-input magic injection remain excluded from originality claims.

## 29 Oct 2026: extension to all Schmidt relative phases

We derived and algebraically proved the full two-parameter at-most-two-T gate-count frontier over arbitrary free two-qubit Cliffords: [complete theorem](general_phase_frontier.md). It is a minimum of three explicitly attainable polynomials, with 225 axis pairs grouped into 21 exact classes and 18 inactive classes excluded via 42 exact algebraic Bernstein rectangles. **A rigorous theorem within our model is not evidence of publication novelty.** The targeted abstracts/sections of Zhu, Roman, Hou and Szombathy establish nearby but not identical results, and a full supplementary/forward-citation review remains outstanding. Roman's 2026 arXiv HTML version displays August 24, 2026 in its body while its arXiv v1 label dates March 26; cite explicit version/date carefully.

## 29 Oct 2026: actual CNOT-count and intrinsic-magic input-orientation theorem

The new [CNOT and intrinsic-magic note](cnot_and_intrinsic_isomagic.md) gives explicit 0/1/1-CNOT circuits attaining the three sharp Schmidt two-T branches (magic objective only), and a partially entangled equal-(concurrence,M2) pair with a certified strict capacity separation. The original Bell-state example was less compelling because its magic can be removed by suitable local unitaries. The stronger pair avoids this weakness.

**Additional relevant recent synthesis prior art:** Webster, Koutsioumpas, Browne, [*Heuristic and Optimal Synthesis of CNOT and Clifford Circuits*](https://doi.org/10.22331/q-2026-09-21-2212), *Quantum* 10, 2212 (21 September 2026), provides optimal CNOT-count and depth synthesis of Clifford unitaries for small circuits. Their target is *unitary synthesis*; our target is *fixed-input output M2*, where a trailing entangling Clifford is irrelevant to the objective. Cite this distinction, never claim first optimization of two-qubit CNOT circuits.

## Additional close papers identified on 29 October 2026

- Alejandro Borda Kuhlmann and Julian Rincon, [*Magic-protected entanglement and Clifford-irreducible structure in magic state space*](https://arxiv.org/abs/2607.18400) (20 July 2026): develops a **Clifford-orbit framework** for magical entanglement and protected entanglement. Our use of the informal phrase "intrinsic magic" must not imply their stronger definition of Clifford-irreducible entanglement or originality for orbit ideas. Our exact two-T fixed-input separation is distinct as phrased, but compare their canonical state representatives and examples before publication.
- Tanner Jackson and Alexey Milekhin, [*Pauli instability in arbitrary states: detecting magic in physical correlators*](https://arxiv.org/abs/2609.40032) (30 September 2026): state-dependent correlator diagnostics of non-Clifford dynamics and architecture-independent **T-count lower bounds**, not the same fixed-input upper-reachability optimization. Important counterpoint for any proposed general information-theoretic significance of conditional magic capacity.
- Webster, Koutsioumpas and Browne [Quantum 10, 2212 (2026)](https://doi.org/10.22331/q-2026-09-21-2212) optimize general Clifford synthesis by CNOT count/depth; do not conflate this with the new magic-objective-specific one-CNOT witness. Check their optimal two-qubit tables for simpler circuit identities.

**Priority gap remains unverified:** abstracts/targeted sections alone cannot rule out matching earlier finite two-T enumerations or unpublished equivalent identities. An exhaustive reverse/forward citation graph and direct reading of supplements are required.

## New priority audit: universal one-CNOT two-T normal form

On 29 Oct 2026 we proved, for **any** pure two-qubit input and any **Clifford-invariant** output objective, that the unrestricted at-most-two-T optimum is achievable with **at most one CNOT** plus single-qubit Cliffords. Full [constructive proof and test](universal_one_cnot.md). The localization is elementary, and originality is **not claimed**.

**Must compare foundational exact synthesis literature:** Xiaoning Bian and Peter Selinger, [*Generators and Relations for 2-Qubit Clifford+T Operators*](https://arxiv.org/abs/2204.02217) (submitted April 2022; QPL 2022 proceedings published 2023), already develop and formally verify Clifford+T presentations and Pauli rotation normal forms. This representation is known prior art. Clifford/CNOT optimization is separately addressed by [Webster et al. (2026)](https://doi.org/10.22331/q-2026-09-21-2212), and worst-case exact **unitary** CNOT requirements were established by [Shende, Markov, Bullock (2004)](https://www.nist.gov/publications/minimal-universal-two-qubit-controlled-not-based-circuits).

**Next nontrivial research question:** conditioned three-T magic capacity and minimal entangling budget. Failure to simultaneously localize three axes with one *initial* Clifford is **not** evidence that a one-CNOT circuit cannot attain the same magic objective using interleaving or other identities.

## 29 Oct 2026: exact gate-budgeted three-T state-specific CNOT separation

New **reproducible exact result**: [three-T two-CNOT threshold theorem](three_t_two_cnot_threshold.md), for an explicit partially entangled magic input, exhibits a **strict positive rational gap** between <=1-CNOT and arbitrary Clifford routing with <=3 Ts, while a constructed 2-CNOT circuit saturates the latter. Unlike the elementary 2-T Clifford localization theorem, this is a **strict fixed-input entangling-cost separation**. The exhaustive finite proof uses exact Q(sqrt2) arithmetic and explicitly covers signed gates and all CNOT placements. **Mathematical theorem != verified publication novelty.**

**Important nomenclature overlap discovered:** Poetri Sonya Tarabunga and Tobias Haug, [*Efficient mutual magic and magic capacity with matrix product states*](https://doi.org/10.21468/SciPostPhys.19.4.085), SciPost Phys. 19, 085 (2025), already introduce *magic capacity* as an anti-flatness-related quantity on a state's Pauli spectrum. Use **"input-conditioned, gate-budgeted magic-gain frontier"** instead of unqualified "magic capacity" in our paper draft.

Related open work includes [Haug & Tarabunga (2026), *Efficient witnessing and testing of magic in mixed quantum states*](https://doi.org/10.1038/s41534-026-01189-z); it examines noisy-T witnessing, not the fixed pure-input exact Clifford+CNOT output-M2 optimum. Recent [Jackson & Milekhin (2026)](https://arxiv.org/abs/2609.40032) give physical-correlator T-count lower bounds (different task). [Borda Kuhlmann & Rincon (2026)](https://arxiv.org/abs/2607.18400) give Clifford-irreducible orbit structure, relevant for the phrase "intrinsic nonlocal magic". **Full supplement / citation-forward priority search remains to be done.**

## 29 Oct 2026: parametric 3T/2-CNOT magic separation

We have proved a **uniform strict Pauli-fourth-moment gap >1/100** for an entire explicit one-parameter family of partially entangled magical pure inputs, not just the isolated three-T counterexample; the [certificate](three_t_parametric_and_symplectic.md) checks 179,073 exact Bernstein coefficients (19,897 competitors x 9) across -1/8<=s<=1/4. We also give an elementary binary symplectic rank/anticommutation graph classification of simultaneous Pauli triple localization; **standard symplectic extension and Clifford/stabilizer diagonalization are established tools, not an originality claim**.

Added potentially relevant background: [*Hardware-tailored diagonalization circuits*](https://doi.org/10.1038/s41534-024-00901-1) (2024) explains simultaneous commuting-Pauli diagonalization using graph states and Clifford frames; [*Limits of Clifford disentangling in tensor network states*](https://doi.org/10.1103/5g5b-5rrz) (2026) treats limitations on Clifford disentanglement of arbitrary nonstabilizer states. Neither source as checked directly establishes the particular input-conditioned three-T/CNOT gap; **full priority still unverified**.

## Additional publication-priority boundary checked 30 October 2026

Gosset, Kothari and Wu, [*Quantum state preparation with optimal T-count*](https://quantum-journal.org/papers/q-2026-07-22-2168/), *Quantum* **10**, 2168 (22 July 2026), prove optimal asymptotic T-count for arbitrary approximate state preparation (with ancillas) and diagonal unitary synthesis. This is an important quantum-resource synthesis result but distinct from our **fixed pure two-qubit input, exact low-T, CNOT-budget-constrained maximization of second stabilizer Rényi entropy**. This contrast concerns their published abstract and should not substitute for a thorough appendix/citation review.

Also note the contemporary [*Local spreading of stabilizer Rényi entropy in a brickwork random Clifford circuit*](https://journals.aps.org/prresearch/abstract/10.1103/68g7-8pdc) (2026), which addresses dynamical spreading in random circuits, not the exact fixed-input two-qubit low-gate circuit optimization in our theorem.

The newly identified exact [3T parametric envelopes](three_t_exact_branch_and_correlation_tube.md) reduce a large computational gap proof to two rational-polynomial optimal branches and a small positive gap polynomial; **novelty is still not independently verified**.

## Exact fiducial-orbit comparison (30 Oct 2026)

Our clean 3T/2-CNOT output is proved to be uniquely closest among the **480 known maximally magical Clifford-orbit states** to `(I⊗S)(H⊗H)|f>`, where `|f>=(1,i,i,i)/2`, with exact squared fidelity `(17+3sqrt(3)+4sqrt(6))/32`. See [proof and exact signed Pauli orbit program](exact_maximal_magic_orbit_proximity.md). **These 480 maximum-magic states and their Clifford-orbit property are prior art:** Liu, Low and Yin, [*Maximal magic for two-qubit states*](https://doi.org/10.1088/2058-9565/ae3028), *Quantum Science and Technology* **11** 015035, published **7 January 2026**, arXiv preprint first submitted February 2025; Roman et al. (2026) subsequently gave analytic Pareto frontiers. Do not call the orbit or its static fidelity geometry a newly discovered physical phenomenon. The possible contribution is its dynamical connection to sharply gate-constrained input-conditioned magic generation.
