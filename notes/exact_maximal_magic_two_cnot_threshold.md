# Exact maximal two-qubit magic with three T gates: a strict two-CNOT threshold

**Research date:** 30 October 2026. **Mathematical status:** explicit algebraic preparation identity, exhaustive exact gate-count certificate in \(\mathbb Q(\sqrt2)\), independent complex matrix checks. **Publication originality: NOT verified.** This is **fixed-input** output magic optimization; preparing the magical input itself is not counted.

## An elementary algebraic input

Let
\[
A=\frac{1-\sqrt2+i(1+2\sqrt2)}4,\qquad
B=\frac{1-\sqrt2+i}4,\qquad |A|^2+|B|^2=1.
\]
Define
\[
|\chi_*\rangle=(R_x(\pi/4)\otimes I)(A|00\rangle+B|11\rangle),
\quad R_x(\alpha)=e^{-i\alpha X/2}.
\]
Up to an irrelevant global phase, this is a Schmidt-phase input with
\[
\boxed{\sin^2\theta_*=\frac{2-\sqrt2}{8},\quad
\phi_*=\arg(B/A)=\arctan(1-1/\sqrt2),\quad
\alpha=\pi/4.}
\]
Thus \(\theta_*\approx15.6998574^\circ\), \(\phi_*\approx16.32494994^\circ\).
Its concurrence and initial Pauli fourth moment are exactly
\[
C(\chi_*)=\sqrt{\frac{5-2\sqrt2}{8}}\approx0.52100538,\qquad
R_{\mathrm{in}}(\chi_*)=\frac{153}{64},\qquad
M_{2,\mathrm{in}}=\log_2(256/153)\approx0.74261216 \ \text{bits}.
\]
Because \(0<C<1\), the state has nonstabilizer magic that cannot be removed using local unitaries.

## New exact gate-budget theorem

Permitted gates: **at most three standard single-qubit T gates, arbitrary single-qubit Clifford gates, CNOT gates in either direction**, with no ancillas, measurements or extra entangling gates. Count physical CNOT gates, not total clock-cycle depth. The objective is the final second stabilizer Rényi entropy \(M_2=-\log_2(R/4)\), where
\(R=\sum_{P\in\{I,X,Y,Z\}^{\otimes2}}\langle P\rangle^4\).

**Theorem:**
\[
\boxed{R_{\le2\mathrm{CNOT},\le3T}(\chi_*)=\frac74,\qquad
R_{\le1\mathrm{CNOT},\le3T}(\chi_*)
=\frac{8265}{4096}-\frac{81\sqrt2}{512}.}
\]
The unrestricted optimum \(R=7/4\), or \(M_2=\log_2(16/7)\), is the **established absolute maximum magic over all pure two-qubit states** (see Liu–Low–Yin and the analytic Pareto treatment of Roman et al.). Thus the first equality is stronger than optimality among finite gate words: it **exactly attains the known global state-magic maximum**.

The sharp positive separation is
\[
\boxed{R_{\le1\mathrm{CNOT}}-\frac74
=\frac{1097-648\sqrt2}{4096}
\simeq0.044089260640194>\frac1{25},}
\]
corresponding to a final magic-entropy advantage
\[
\boxed{\log_2\!\left(\frac{\frac{8265}{4096}-\frac{81\sqrt2}{512}}{7/4}\right)
\simeq 0.03589674784\ \text{bits}.}
\]
**Exactly two CNOTs are necessary and sufficient** for maximum final magic from this fixed input with at most three T gates.

## Explicit perfect-output circuit

Let \(T_P=e^{-i\pi P/8}\); Pauli-axis rotations implement T gates with Clifford conjugation, up to a Clifford and global phase. The three-\(T\) word in **chronological** order
\[
\boxed{(XX,\ IZ,\ IY)}
\]
maps \(|\chi_*\rangle\) to a known maximal-magic fiducial **up to global phase**:
\[
\boxed{
T_{IY}T_{IZ}T_{XX}|\chi_*\rangle\sim
|f_*\rangle=
\frac{(1+3i)|00\rangle+(1+i)|01\rangle+(1-i)|10\rangle+(1+i)|11\rangle}{4}.}
\]
The identity can be verified purely algebraically: the output's 15 Pauli expectations are twelve values \(\pm1/2\) and three zeros, with *exactly the same signs and labels* as the given \(|f_*\rangle\). Equal Pauli expectations for all sixteen Paulis imply identical pure density matrices and thus state equality up to global phase. The earlier [universal two-CNOT compiler](../src/three_t_two_cnot_compiler.py) maps any three-Pauli T word to a physical circuit with at most two CNOTs **up to a final Clifford** (which preserves M2). A one-CNOT realization attaining the same final M2 would contradict the strict lower bound.

## Exact, exhaustive lower-bound proof

A particularly convenient feature of the tuned input is that **every initial Pauli expectation** lies in the *quadratic* number field \(\mathbb Q(\sqrt2)\). All nonzero expectations are, with common denominator 4,
\[
\begin{array}{c|l}
II:(4,0)& IZ:(2,1),\quad ZI:(1,1),\quad YI:(-1,-1)\\
XX:(2,0)& XY:(2,-1),\quad YX:(-1,1),\quad YY:(0,-1)\\
YZ:(0,-2)& ZX:(-1,1),\quad ZY:(0,-1),\quad ZZ:(0,2).
\end{array}
\]
Each pair \((a,b)\) represents \(a+b\sqrt2\); omitted Paulis have expectation zero. A Pauli \(T_P\) rotates anticommuting Pauli-expectation pairs by 45 degrees, preserving \(\mathbb Q(\sqrt2)\) under the exact recurrence. After k T gates, the expectation denominator is \(4\cdot 2^k\). Normalize all fourth moments to the common positive denominator \(32^4=1\,048\,576\). The resulting fourth-moment numerator has exact form \(a+b\sqrt2\) with **integer** \(a,b\).

[Executable exact certificate](../src/three_t_exact_maximal_magic.py):
1. **All 3,616** unrestricted 0/1/2/3-T normal-form words (one sign choice is enough for unrestricted global Clifford routing);
2. The **241 unrestricted shorter words**, a conservative superset of all <=1-CNOT 0/1/2-T circuits;
3. All **2457** one-CNOT-compatible ordered three-axis patterns and all **eight** independent sign assignments to \(T\)/\(T^\dagger\), with the CNOT allowed before, between or after T gates: a total of **19,897** conservative restricted comparisons;
4. Compare all results with exact integer-square sign tests for \(a+b\sqrt2\) (no floating-point ordering).

The unrestricted winning numerator is \((1\,835\,008,0)\), attained by (XX,IZ,IY). The restricted winning numerator is \((2\,115\,840,-165\,888)\), attained, for example, by signed chronological rotations (-YI,-XY,-IX), a one-CNOT-compatible word. The exact gap numerator \((280\,832,-165\,888)\) is strictly greater than \(32^4/25\) using integer comparisons.

The [independent test](../tests/test_three_t_exact_maximal_magic.py) constructs the complex input vector using \(\sqrt2\), applies the Pauli unitaries as dense 4x4 matrices, confirms fidelity **one** to the explicit maximal-magic fiducial, and independently checks both exact fourth moments and concurrence.

## A measured Pauli-correlation sufficient neighborhood

Let \(r(\psi)\in\mathbb R^{15}\) be the vector of nonidentity Pauli expectation values. The fourth moment of any unitary output is \(4\sqrt3\)-Lipschitz in this vector, as proved in [our earlier correlation-tube note](three_t_exact_branch_and_correlation_tube.md). Taking a difference of two circuit-family minima gives an \(8\sqrt3\)-Lipschitz gap.

Since the exact CNOT gap above is **strictly greater than \(1/25\)**, any pure two-qubit input \(\varphi\) satisfying
\[
\boxed{\|r(\varphi)-r(\chi_*)\|_2<\frac{1}{200\sqrt3}\simeq0.002887}
\]
is **also guaranteed** to have a positive two-CNOT advantage when maximizing final \(M_2\) with at most three T gates. This gives an *open neighborhood* of inputs with exactly-two-CNOT resource requirement, characterized entirely by measurable input correlations. The radius is a deliberately conservative sufficient bound, not a complete classification or a realistic hardware noise tolerance.

## Reproduce

\`\`\`bash
python -m src.three_t_exact_maximal_magic
python -m unittest discover -s tests -p 'test_three_t_exact_maximal_magic.py' -v
\`\`\`

## Publication-priority and physical caveats

This theorem combines a **known maximal-magic state** and **known Clifford+T structure** with a sharp **fixed-input CNOT-count reachability separation**. The *maximal value*, *maximally magical state orbit*, and *symplectic gate structure* are all prior art; see Liu, Low and Yin, [*Maximal magic for two-qubit states*](https://doi.org/10.1088/2058-9565/ae3028) (*Quantum Science and Technology*, January 2026), Roman et al. [2026](https://arxiv.org/abs/2603.24902), Bian–Selinger (2023), and Webster et al. (2026). Our *gate-budgeted optimality statement* may be a publishable original extension, but we have **not** finished a comprehensive novelty audit or obtained independent referee-style verification.

The starting \(|\chi_*\rangle\) already contains nonstabilizer magic. Its preparation resources are **not** part of this circuit budget. The theorem is for exactly two qubits, *no ancillas or measurements*, and ideal noiseless gates. It does not claim an overall experimental fidelity, fault-tolerance advantage, absolute minimal total T-count for preparing a fiducial from a stabilizer, or anything about larger devices.
