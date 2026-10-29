# Exact three-T, two-CNOT magic-gain separation

**Date:** 29 October 2026. **Status:** constructive theorem with a finite, exact integer certificate and independent dense-statevector witness. **Literature priority NOT established.**

## Model and theorem

We consider pure **two-qubit** states, zero to three standard single-qubit T gates, arbitrary single-qubit Clifford gates H/S, and up to d physical CNOTs (either orientation). No ancillas, measurement, feedforward, other non-Clifford gates, or timed single-qubit-depth restrictions. The objective is the **final second stabilizer Rényi entropy**, not exact synthesis of a target unitary:
\[
R(\psi)=\sum_{P\in\{I,X,Y,Z\}^{\otimes2}}\langle P\rangle_\psi^4,\qquad
M_2(\psi)=-\log_2(R(\psi)/4).
\]

**Theorem (strict, exact three-T entangling budget):** Define
\[
|\psi_*\rangle=\frac{(-1+3i)|00\rangle+(-7-i)|01\rangle+(-1+i)|10\rangle+(-1+4i)|11\rangle}{\sqrt{79}}.
\]
It is partially entangled, with concurrence \(2\sqrt{362}/79\in(0,1)\), and has pre-existing magic \(R_{\rm in}=85341988/38950081\), \(M_{2,\rm in}\simeq0.868371\) bits.

Under the above gate set and at most **three T**:
\[
R_{\rm unrestricted}(\psi_*)=
\frac{1103764401}{623201296}\simeq1.771120195167245,
\]
achieved by ordered (chronological) Pauli rotations **(YY, XI, XY)**, whereas with **at most one physical CNOT**,
\[
R_{\le1\,\mathrm{CNOT}}(\psi_*)=
\frac{69521131}{38950081}\simeq1.784877700254333,
\]
attained already by the two-T word **(ZI, ZY)** (implementable with one CNOT by the previously proved localization lemma). Therefore
\[
\boxed{R_{\le1\,\mathrm{CNOT}}-R_{\rm unrestricted}
=\frac{8573695}{623201296}>0}.
\]
The extra optimum magic gain from two CNOTs is
\[
\log_2\frac{R_{\le1\,\mathrm{CNOT}}}{R_{\rm unrestricted}}
\simeq0.011163101877318\ \text{bits}.
\]
A constructive two-CNOT circuit realizes (YY,XI,XY). **Exactly two physical CNOTs are necessary and sufficient** to reach the globally optimal output M2 for this fixed input with at most three Ts.

This proof concerns **magic-only optimization**. The compiled unitary differs from the Pauli-word target by a *final Clifford*, harmless for M2, but generally relevant to exact-unitary synthesis.

## Exact lower-bound certificate

The complete certificate is [src/three_t_exact_gap.py](../src/three_t_exact_gap.py).

1. **Normal form for arbitrary Cliffords.** Any Clifford+at-most-three-T circuit is, up to a final Clifford, a word in \(T_P=\exp(-i\pi P/8)\), with nonidentity Hermitian Paulis \(P\). We test 1+15+225+3375=**3616** zero/one/two/three-T positive-axis words. Inverse axes are redundant at unrestricted Clifford cost: \(T_{-P}\) differs from \(T_P\) by a Clifford, absorbable into the normal form.
2. **Complete physical one-CNOT patterns.** With one physical CNOT placed at any of the four cuts among the three Ts, commute all local Clifford frames to the final output Clifford. The resulting ordered axes are a prefix of k *local* axes (one of XI,YI,ZI,IX,IY,IZ) and a suffix of 3-k axes in a single **locally conjugated CNOT preimage of the six local axes**, for k=0,1,2,3. Enumerating six local Pauli permutations on each qubit and both CNOT orientations gives **2457 distinct ordered Pauli triples**. We allow *every one* of the eight independent sign assignments \(T_{+P}\) or \(T_{-P}\), ensuring we do not miss the physical \(T^\dagger\) possibility; this actually enlarges the admissible set. Shorter circuits are upper-covered by all 241 unrestricted 0/1/2-T words. The comparison checks **241+2457×8 = 19897** cases and includes every one-CNOT physical circuit in our model.
3. **Exact algebraic arithmetic.** The 16 initial Pauli expectations equal rational integers divided by N=79:
\[
(79,18,38,-55,14,38,14,2,-54,-18,-14,62,41,-2,50,-25)/79,
\]
ordered II,IX,IY,IZ,XI,XX,XY,XZ,YI,YX,YY,YZ,ZI,ZX,ZY,ZZ. These are recomputed by SymPy as Gaussian-integer quadratic forms. Each signed T rotates anticommuting Pauli-expectation pairs by \(\pi/4\), so after k Ts all moment coefficients have the exact form \((a+b\sqrt2)/(2^k\,79)\), \(a,b\in\mathbb Z\). Fourth moments lie in \(\mathbb Q(\sqrt2)\). The code evaluates and orders them **using only exact integer comparisons**, comparing \(a+b\sqrt2\) via integer squares; no numerical fitting, no floating-point tolerance. Using common fourth-moment denominator \((8\cdot79)^4\), the unrestricted minimum has numerator (282563686656,0), the one-CNOT minimum has (284758552576,0), and their positive difference is (2194865920,0), simplifying to the exact rational gap above.

The exhaustive enumeration is a finite computer-assisted proof with a short, checkable certificate. It is not a general closed-form input-conditioned three-T phase diagram.

## Constructive upper bound: two CNOTs always suffice for THREE T

In fact, for **any pure two-qubit input** and **any** three-Pauli word \(T_R T_Q T_P\), the output magic is realizable with at most **two** physical CNOTs.

1. By the two-axis localization lemma ([universal_one_cnot.md](universal_one_cnot.md)), find a Clifford \(U_1\), containing at most one CNOT, mapping P and Q to signed **local** axes. Apply \(U_1\), then their two local signed T rotations.
2. Compute \(R'=U_1 R U_1^\dagger\). Every nonidentity two-qubit Pauli can be mapped to a local Pauli by at most one further CNOT plus local Cliffords: choose \(U_2\). Apply \(U_2\) then its local signed T rotation.
3. The resulting state is \((U_2U_1)T_R T_Q T_P|\psi\rangle\). The leading \(U_2U_1\) is Clifford, so M2 is identical to that of the desired Pauli word. Thus **<=2 CNOTs always suffice** for <=3 Ts.

For the explicit witness triple (YY,XI,XY), [src/three_t_two_cnot_compiler.py](../src/three_t_two_cnot_compiler.py) constructs \(U_1\) with one CNOT and local images \((-YI,+XI)\), then \(U_1(XY)U_1^\dagger=-XZ\). A second CNOT Clifford \(U_2\) maps XZ to XI; its local signed T then attains the global target. The complete 4x4 statevector identity was independently verified.

This is a magic-objective two-CNOT upper bound for **any input**, not an assertion about exact unitary-synthesis cost or a physical clock-depth lower bound.

## Reproduction

\`\`\`bash
pip install -r requirements.txt
python -m src.three_t_exact_gap
python -m src.three_t_two_cnot_compiler
python -m unittest discover -s tests -v
\`\`\`

## Novelty/priority caveats

A targeted search as of 29 Oct 2026 did not identify this **specific state-conditioned three-T, two-CNOT magic-gain separation**, but this is **not** a systematic forward-citation and supplementary-material review and originality is not certified.

- [Zhu et al. (2024)](https://arxiv.org/abs/2409.06659) establish amortized universal one-T magic bounds. **Not ours.**
- [Bian & Selinger (2023)](https://arxiv.org/abs/2204.02217) establish a formally checked two-qubit Clifford+T presentation and Pauli normal form. **Not ours.**
- [Webster et al. (2026)](https://doi.org/10.22331/q-2026-09-21-2212) optimize general Clifford and CNOT circuit synthesis. **Not ours.**
- [Hou, Cao & Yang (2026)](https://doi.org/10.1038/s41534-026-01265-4) analyze magic injection into entangled, including nonstabilizer, states and identify intrinsic magic capacity as a potential direction. Different ensemble/quantity.
- [Roman et al. (2026)](https://arxiv.org/abs/2603.24902) give static two-qubit magic-entanglement frontiers, not the fixed-input routing threshold.
- **Name collision:** [Tarabunga & Haug (2025)](https://doi.org/10.21468/SciPostPhys.19.4.085) already define *magic capacity* as a state quantity related to the anti-flatness of the Pauli spectrum. Avoid using this name for gate-budgeted maximal \(\Delta M_2\) without carefully distinguishing definitions.
- [Haug & Tarabunga (2026)](https://doi.org/10.1038/s41534-026-01189-z) introduce mixed-state magic witnesses and noisy T-count certification, not our input-conditioned one/two-CNOT optimality statement.

**Next:** seek independent expert feedback, inspect full proof and supplements of the closest papers and their citations, extend the isolated exact witness to an **open set** of states with a certified positive gap, identify compact parameterized witness families, and present a short LaTeX theorem/proof note. Do NOT claim first-ever discovery or publication readiness without that.
