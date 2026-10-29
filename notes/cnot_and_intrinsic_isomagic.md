# One-CNOT saturation and intrinsically magical isomagic states

**29 October 2026. Research status:** exact for the scoped two-qubit models below; checked with symbolic identities, rational intervals and independent dense state vectors. **Literature priority and paper novelty unverified.**

## Model and exact entangling-depth-one result

Input: |psi(theta,phi)>=cos(theta)|00>+exp(i phi)sin(theta)|11>. Allowed gates: arbitrary 1-qubit Cliffords H,S, at most two 1-qubit T gates, and at most d physical CNOT gates (d=0 or 1); no ancillas or measurements. Count every physical CNOT, but allow a *final* CNOT when d=1. Objective is to maximize M2 of the final state, **not** synthesize a particular unitary exactly. For two qubits, at most one CNOT is also at most one entangling-gate layer. Single-qubit Cliffords have no depth constraint.

The established full-phase theorem in [general_phase_frontier.md](general_phase_frontier.md) proves that **unrestricted** global two-qubit Cliffords and at most two T gates achieve minimum Pauli fourth moment min{A,B,C} with representative ordered Pauli-axis words:

| Branch | Pauli word | Actual H/S/T/CNOT template | Physical CNOT count |
|---|---|---|---:|
| A | (IX,YI) | T_YI T_IX | 0 |
| B | (IX,ZY) | T_IY CNOT T_IX | 1 |
| C | (IX,ZX) | T_IX CZ T_IX, with CZ=(I tensor H)CNOT(I tensor H) | 1 |

Here T_P=exp(-i pi P/8), implemented by **one ordinary T** conjugated by single-qubit Cliffords whenever P has weight one; in the table operations act right-to-left.

The circuit identities are **exact state-vector identities**, for every input (not only the Schmidt family):

T_IY CNOT T_IX = CNOT T_ZY T_IX,
T_IX CZ T_IX = CZ T_ZX T_IX.

Because M2 is Clifford-invariant, the final CNOT/CZ on the right-hand sides does not affect the objective. Hence every branch of the proven global two-T frontier has a physical realization with at most one CNOT. The global theorem supplies an upper bound for *all* <=1-CNOT circuits, and the templates attain it. Therefore

\[
\boxed{R_{\min,\le1\mathrm{CNOT},\le2T}(\psi_{\theta,\phi})
=R_{\min,\mathrm{unrestricted\,Clifford},\le2T}
=\min\{A(t,x),B(t,x),C(t,x)\}.}
\]

**Sharpness of the CNOT budget for some inputs:** The proved local-only theorem [extension_corollaries.md](extension_corollaries.md) gives the exact d=0 frontier \(\min\{A,D,3R_{\rm in}/4\}\). At theta=pi/8 and phi=pi/4, R_in=11/4, d=0 optimum=129/64 while d=1 optimum=121/64. Thus one CNOT is necessary and sufficient to achieve the global optimum for that intrinsically magical input, with a gain advantage log2(129/121) bits. For other inputs, zero CNOTs may already suffice.

**Important:** this does not say the desired *specific* Pauli-word unitary can be synthesized with only one CNOT: the two circuits differ by a final entangling Clifford. Nor does it settle n>2, arbitrary input orientations, or a clock-cycle depth model that charges H/S/T layers or noisy gates.

**Reproduce:** python -m src.one_cnot_saturation; python -m unittest tests/test_one_cnot_saturation.py -v

## A strict separation for *intrinsic* pre-existing magic

The earlier two-T isomagic counterexample used maximally entangled Bell-derived states; those can be locally unitarily disentangled from stabilizer magic. The following construction is strictly stronger.

Let theta=pi/6 and define

\[
|\psi_A\rangle=\cos\theta|00\rangle+e^{i\phi_A}\sin\theta|11\rangle,
\qquad \sin^2(2\phi_A)=13/18,
\]
\[
|\psi_B\rangle=(R_x(\pi/8)\otimes I)
\big(\cos\theta|00\rangle+\sin\theta|11\rangle\big),
\quad R_x(\alpha)=e^{-i\alpha X/2}.
\]

Both have concurrence sqrt(3)/2 and initial fourth moment **exactly 91/32**, hence same M2=log2(128/91). Because their concurrence is strictly between 0 and 1, neither is locally unitarily equivalent to any two-qubit stabilizer state: pre-existing magic is unavoidable under local unitaries.

For A, t=3/4, x=sin²(phi_A)=(6-sqrt(10))/12. The full-phase theorem shows its exact optimum is branch A:

\[
R_{A,\mathrm{optimal}}=\frac{1167}{512}-\frac{27\sqrt{10}}{256}
\approx1.945775403029116.
\]

For B, merely applying the *single explicit* two-T Pauli word (ZX,IZ) gives

\[
R_{B,\mathrm{witness}}=
\frac{1223}{512}-\frac{87\sqrt2}{256}
-\frac{3\sqrt{6-3\sqrt2}}{32}
+\frac{\sqrt{12-6\sqrt2}}{64}
\approx1.813073242596151.
\]

**A rigorous inequality, without having to certify B's optimum:** the proof uses exact rational enclosures q=sin(2theta)=sqrt3/2 in (866/1000,867/1000), c=cos(pi/8) in (923/1000,925/1000), s=sin(pi/8) in (382/1000,384/1000). Expanding the witness as a polynomial in these *positive* variables and bounding each monomial with the appropriate interval endpoint yields R_B(witness)<1.819237<1.9. Separately sqrt(10)<16/5 implies R_A(optimum)>1.941796>1.9. The interval signs are checked by exact algebraic inequalities.

Therefore \(F_2(\psi_B)\ge\log_2[(91/32)/R_{B,\mathrm{witness}}] >
F_2(\psi_A)=\log_2[(91/32)/R_{A,\mathrm{optimal}}]\).
Numerically the witness gains are at least 0.649357 versus A's optimum 0.547449 bits. **This proves that initial concurrence and scalar M2 do not determine optimal two-T magic growth, even when pre-existing magic cannot be removed by local unitaries.** It does **not** prove the displayed B witness is itself the global B optimum.

**Reproduce:** python -m src.intrinsic_isomagic_separation; python -m unittest tests/test_intrinsic_isomagic.py -v

## Arbitrary local orientations: a correct finite optimizer

For *any* normalized pure two-qubit input (not necessarily Schmidt-aligned), the generic exact finite reduction is

\[
R_{\min}^{(\le2T)}(\psi)=
\min\left\{R(\psi),\min_{P\ne II}R(T_P\psi),
\min_{P,Q\ne II}R(T_QT_P\psi)\right\}.
\]

This comprises 1+15+225 candidate words and is an exact finite combinatorial formula, with the entries evaluated numerically via the 16 real Pauli expectations in [arbitrary_input_oracle.py](../src/arbitrary_input_oracle.py). The Pauli transform is explicit and tests compare every axis against independent state-vector evolution. **It is not a new analytic universal closed form.** The one-T term must be retained: for generic orientations the optimum among exactly two gates need not equal the at-most-two-gate optimum.

This oracle lets us search orientation-dependent chamber structure without conflating numerical observations with proofs; producing a tractable analytic full-orientation classification remains **open**.

## Priority audit and limits

- Zhu et al. (2024) prove the universal amortized single-T SRE bound, even with magical inputs; we do not claim it.
- Roman et al. (2026) prove static magic/entanglement frontiers, not the fixed-input routing statements as reviewed.
- Hou et al. (2026) treat non-stabilizer entanglement and magic injection; we do not claim first dynamical analysis of such states.
- Webster, Koutsioumpas and Browne, *Quantum* 10, 2212 (21 Sep 2026), https://doi.org/10.22331/q-2026-09-21-2212, establish optimal/heuristic Clifford and CNOT circuit synthesis. Our objective and input conditioning differ, but their synthesis catalog is particularly important prior art when discussing gate budgets.

**No first-discovery/publishability claim is made.** Next: comprehensive forward-citation/supplement audit, full arbitrary orientation classification, physically timed hardware depth, and independent external review.
