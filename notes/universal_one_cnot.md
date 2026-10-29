# Universal one-CNOT magic-capacity theorem for any two-qubit input

**Research date:** 2026-10-29. **Mathematical status:** elementary constructive Pauli/Clifford proof, exhaustive 225-pair symplectic check, independent dense 4x4 matrix checks, 29 passing tests across research repository. **Originality status: UNVERIFIED; this is likely an elementary consequence of established Clifford synthesis principles and is NOT claimed as first discovery.**

## Definitions and scope

For a pure two-qubit state \(\psi\), let
\[
R(\psi)=\sum_{K\in\{I,X,Y,Z\}^{\otimes2}}\langle K\rangle_\psi^4,\quad
M_2(\psi)=-\log_2(R(\psi)/4).
\]
Permitted gates: any one-qubit Clifford (H,S), any two-qubit Clifford when defining the unrestricted benchmark, at most two ordinary local T gates, and either orientation of the **physical CNOT** with a specified budget. Ancillas, measurement and feedforward are disallowed. The final Clifford's action on the state is relevant for exact unitary synthesis but **irrelevant to M2**. We count CNOTs, **not clock-cycle circuit depth**; local gates are free in this budget.

Let \(F_{2,\mathrm{Cliff}}(\psi)\) maximize the M2 gain over unrestricted Clifford+at-most-two-T circuits and \(F_{2,\le1\mathrm{CNOT}}(\psi)\) maximize with local Cliffords and **at most one physical CNOT**.

**Theorem (all pure 2-qubit inputs):**
\[
\boxed{F_{2,\le1\mathrm{CNOT}}(\psi)=F_{2,\mathrm{Cliff}}(\psi).}
\]
Indeed the statement holds for *any Clifford-invariant state functional* that is optimized over such circuits, not just M2.

## Proof: canonical Pauli-pair localization with 0 or 1 CNOT

Every Clifford+two-T circuit has, up to a **final Clifford**, the action \(T_Q T_P\), where \(P,Q\in \{I,X,Y,Z\}^{\otimes2}\setminus\{II\}\), and \(T_P=e^{-i\pi P/8}\).

**Localization lemma.** For any two nonidentity two-qubit Hermitian Pauli axes \(P,Q\), there exists a two-qubit Clifford
\[
U=\mathrm{CNOT}_{c\to t}\,(L_0\otimes L_1)
\]
with local Cliffords \(L_0,L_1\), or \(U=I\) when both axes are local, such that \(UPU^\dagger=\pm P'\), \(UQU^\dagger=\pm Q'\), and each of \(P',Q'\) has weight 1.

Prove by cases, using local Clifford axis permutations and optionally exchanging the **case labels** of the two physical qubits (no physical SWAP is needed). All cases of the two axes are exhausted:

| Axes type | Representative (P,Q) | Physical CNOT used | Images (ignoring signs) |
|---|---|---|---|
| Both weight 1 | (ZI, IZ) or on same qubit | None | Already local |
| Weight 1 + weight 2, commuting | (ZI, ZZ) | 0→1 | (ZI, IZ) |
| Weight 1 + weight 2, anticommuting | (XI, ZZ) | 1→0 | (XI, ZI) |
| Both weight 2 and equal | (XX, XX) | 0→1 | (XI, XI) |
| Both weight 2, distinct commuting | (XX, ZZ) | 0→1 | (XI, IZ) |
| Both weight 2, anticommuting | (XX, XY) | 1→0 | (IX, IY) |

Why complete: two nonidentity local axes need no entangling action. With one local and one weight-two axis, the sole overlapping Pauli factor either commutes or anticommutes. With two weight-two axes they are either equal, anticommute at exactly one site, or anticommute at both sites and commute globally. Every Pauli-pair type is locally equivalent to the representative listed. Both CNOT directions count as a single physical CNOT; if only one orientation is native, H on both qubits reverses it with no additional CNOT.

Since \(U T_Q T_P\psi=T_{\pm Q'}T_{\pm P'}U\psi\), the two non-Clifford gates after U are local. Negative axes are harmless: \(T_{-P'}=e^{+i\pi P'/8}=e^{+i\pi P'/4} T_{P'}\), i.e. one T followed by a **local Clifford**. Dropping the final \(U^\dagger\) preserves M2. A single T is handled by the same localization lemma with \(Q=P\); zero T produces no M2 gain. Thus the theorem holds for **at most two**, including zero and one T, not only exactly two T.

**Sharp CNOT threshold:** zero CNOT is insufficient at some inputs: the earlier exact Schmidt-family result at \(\theta=\pi/8,\phi=\pi/4\) gives \(R_{\min,0\,\mathrm{CNOT}}=129/64>121/64=R_{\min,1\,\mathrm{CNOT}}\). So the worst-case optimal budget is **exactly one** CNOT.

## Independent exhaustive verification

The code in [one_cnot_universality.py](../src/one_cnot_universality.py) enumerates every ordered pair of 15 nonidentity two-qubit axes (**225**), tries the six local Pauli-axis permutations on each qubit followed by both oriented CNOTs, and explicitly returns H/S generators and signed local-axis images. Exactly **36** pairs are already local and all **189** others admit a one-CNOT witness. A *separate* 4x4 dense-matrix check verifies, on four Haar-distributed complex inputs, every equation
\[
T_{\pm Q'}T_{\pm P'} U\psi=U T_QT_P\psi.
\]
This tests signs, ordering and all 225 cases, not only entropy values.

## Exact minimum-CNOT classifier for an arbitrary input

The **zero-CNOT** candidate set consists of 1 zero-T word, 6 local-axis one-T words, and 36 ordered local-axis two-T words: **43 possibilities**. The unrestricted benchmark is 1+15+225=**241 possibilities**. Define the minima of R over each set as \(R_0(\psi)\) and \(R_*(\psi)\) respectively.

The theorem implies the **exact decision**:
\[
\boxed{d_{\min}(\psi)=
\begin{cases}0,&R_0(\psi)=R_*(\psi),\\1,&R_0(\psi)>R_*(\psi).\end{cases}}
\]
The entangling-routing advantage is \(\log_2(R_0/R_*)\) bits. All values are explicit quartic polynomials in the 16 real Pauli expectations, so this is an **exact finite semialgebraic characterization**, numerically evaluated in [cnot_cost_oracle.py](../src/cnot_cost_oracle.py). It is **not** a simplified symbolic decomposition into all algebraic orientation chambers. Numerical equality uses a floating-point tolerance; claims near ties require exact arithmetic or certified intervals.

A reproducible **exploratory** Haar sample of 200 pure states (seed 20261029) found strictly positive one-CNOT advantage in **168/200**, median 0.04280358036 bits, mean 0.05544728704 bits, and maximum 0.30603307254 bits. This is not a theorem or a population estimate with characterized measurement error.

## Where the hard research question moves: >=3 T gates

Three Pauli rotations require simultaneous localization of three axes if **one shared Clifford** acts before all three Ts. We enumerated the **entire** two-qubit Clifford symplectic group \(\mathrm{Sp}(4,2)\), of order **720**, and all \(15^3=3375\) ordered triples. Exactly 216 are already local, 1629 become local with one CNOT and local gates, and **1530 cannot be simultaneously localized by any Clifford at all**, regardless of its CNOT count. The executable 720-element group certificate is [three_t_prelocalization.py](../src/three_t_prelocalization.py).

The obstruction is structural, not merely a synthesis cost: take \((IX,IY,XX)\). Its first two axes anticommute, forcing their two weight-one Clifford images to occupy the same qubit. The third commutes with the first but anticommutes with the second. A third weight-one axis that has these commutation properties must equal the first up to sign; yet \(XX\) is independent of \(IX\). Thus no Clifford simultaneously localizes the triple.

**Critical caution:** this does **not** prove that a three-T *output magic optimum* requires more than one CNOT, since a CNOT interleaved between Ts, an alternative Pauli decomposition, or a nontrivial Clifford+T identity might reproduce the same M2.

Research target: prove or disprove universal one-CNOT sufficiency at T-count 3, identify explicit input witnesses and exact 0/1/2-CNOT magic-capacity separations, and establish minimal physical timed depth under stated hardware assumptions.

## Literature-priority boundary

- **Bian & Selinger**, [*Generators and Relations for 2-Qubit Clifford+T Operators*](https://arxiv.org/abs/2204.02217) (arXiv 2022, QPL proceedings 2023): an established formally verified two-qubit Clifford+T presentation, including the Pauli-rotation representation. Our finite Pauli normal form is **not new**.
- **Webster, Koutsioumpas & Browne**, [*Heuristic and Optimal Synthesis of CNOT and Clifford Circuits*](https://doi.org/10.22331/q-2026-09-21-2212), *Quantum* **10**, 2212 (2026): a modern optimal Clifford/CNOT synthesis reference. Different target from magic-optimized circuits but potential overlap in 1-CNOT pair-localization.
- **Shende, Markov & Bullock**, [*Minimal Universal Two-Qubit Controlled-NOT-Based Circuits*](https://www.nist.gov/publications/minimal-universal-two-qubit-controlled-not-based-circuits) (2004): three-CNOT **worst-case exact SU(4) unitary synthesis** bound. It is not contradicted by optimizing a Clifford-invariant state functional with only two T gates.
- **Zhu et al.** (2024) prove the amortized universal one-T SRE gain; **Roman et al.** (2026) the static 2q magic–entanglement frontier; **Hou et al.** (2026) magic injection, including entangled and non-stabilizer inputs.

**Originality is not demonstrated.** In particular, the localization lemma is simple enough to be implicit in known stabilizer/Clifford synthesis, so do not market it alone as a new physics paper. The natural research contribution is *input-conditioned sharp frontiers and nontrivial minimal entangling budgets for 3+ T*.
