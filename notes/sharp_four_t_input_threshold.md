# Sharp four-T input-preparation threshold for an additional-CNOT magic advantage

**Research date:** 30 October 2026. **Status:** exact finite, computer-assisted theorem with 58 physical one-CNOT witnesses; independently checked with complex state-vector simulation. **Publication-priority claim: NOT verified.**

## Precise question and answer

For a pure two-qubit state \(|\psi\rangle\), let \(t_{\mathrm{prep}}(\psi)\) be the **minimum T count** required to prepare it **exactly** from *any pure two-qubit stabilizer input* using arbitrary **two-qubit Clifford gates** and no other non-Clifford gates; assume no ancillas, measurements or postselection. Initial stabilizer states and all Cliffords are treated as free **only in defining this source-state complexity**.

Now suppose \(\psi\) is **supplied as a fixed input**, and we wish to maximize its final second stabilizer Rényi entropy using at most **three additional T gates**, arbitrary **single-qubit Clifford gates**, and at most \(d\) physical CNOTs (either direction). No ancillas or measurements. Let
\[
R^{(3)}_d(\psi)=\min_{\mathrm{allowed}\ \le3T,\le d\mathrm{CNOT}}
\sum_{P\in\{I,X,Y,Z\}^{\otimes2}}\langle P\rangle_{\mathrm{out}}^4.
\]
The unrestricted benchmark \(R^{(3)}_\infty\) allows any two-qubit Clifford routing at zero cost; by the previously proved three-T compiler, at most two CNOTs already attain that benchmark for every two-qubit input.

**Theorem (sharp preparation-cost threshold):**
\[
\boxed{
t_{\mathrm{prep}}(\psi)\le3
\quad\Longrightarrow\quad
R^{(3)}_1(\psi)=R^{(3)}_\infty(\psi).
}
\]
Moreover there exists a pure two-qubit state \(\chi_*\) with \(t_{\mathrm{prep}}(\chi_*)=4\) for which \(R^{(3)}_1(\chi_*)>R^{(3)}_2(\chi_*)\). Thus
\[
\boxed{
\min_{\psi:R^{(3)}_1(\psi)>R^{(3)}_2(\psi)}
t_{\mathrm{prep}}(\psi)=4.
}
\]

This is an **input-conditioned obstruction** and should not be misrepresented as a minimum end-to-end number of gates to prepare maximally magical states: Liu–Low–Yin (2026) already prepare maximal two-qubit magic directly from \(|++\rangle\) with **3 T and 1 CNOT**.

## Exact low-T source-state orbit classification

Use the Clifford+Pauli normal form. Every input state with \(t_{\mathrm{prep}}\le3\) is in a full Clifford orbit of one of the \(1+15+225+3375=3616\) positive Pauli-T words
\[
T_{P_k}\cdots T_{P_1}|00\rangle,\qquad k\in\{0,1,2,3\}.
\]
All initial stabilizer Cliffords can be moved through these Pauli rotations by conjugation; \(T^\dagger\) signs can be absorbed by unrestricted Cliffords in this **input preparation** normal form. Thus this covers *any* stabilizer input and arbitrary Clifford interleaving.

Using the generators \(H_0,H_1,S_0,S_1,\mathrm{CNOT}_{0\to1}\), exact signed Pauli actions computed from **Gaussian-integer 4×4 matrices**, and the complete 16-component Pauli expectation vector as a state fingerprint, the 3,616 words generate **18,900 distinct pure input rays** grouped into ten full two-qubit Clifford orbits:

\[
(60,\ 360,\ 720,\ 720,\ 720,\ 5760,\ 1440,\ 480,\ 2880,\ 5760).
\]

The local Clifford group \(C_1\otimes C_1\) leaves the subsequent single-qubit-Clifford/CNOT/T optimization invariant. Quotienting those 18,900 states by local Cliffords yields **58 local classes**. The entire classification is reproducible in [the exact certificate](../src/three_t_prepared_threshold.py). No floating point or random-state sampling is involved in determining these cardinalities.

## Exact saturation for 48 classes

For 48 of the 58 local classes, we give one explicit **chronological ordered three-Pauli rotation word** with negative signs, which after a physically valid one-CNOT Clifford localization attains the known absolute two-qubit pure-state minimum
\[
\boxed{R_{\rm out}=7/4,\qquad M_2=\log_2(16/7).}
\]
This is necessarily equal to the unrestricted optimal output magic. The 48 witnesses and the exact resulting Pauli moments are embedded in [src/three_t_prepared_threshold.py](../src/three_t_prepared_threshold.py).

The initial input vectors are algebraic with all Pauli expectations of the form
\[
r_P=\frac{a_P+b_P\sqrt2}{16},\quad a_P,b_P\in\mathbb Z.
\]
After exactly three signed Pauli T rotations, they have denominator 128. Hence their fourth moments have the exact form
\[
R=\frac{A+B\sqrt2}{128^4},\qquad A,B\in\mathbb Z.
\]
For every one of the 48 witnesses, the certificate checks the exact pair
\[
(A,B)=(7\cdot128^4/4,\ 0)=(469762048,0).
\]
Each witness's **physical one-CNOT compatibility** is checked by enumerating all six signed-axis-free local Clifford permutations per qubit, both CNOT directions, and all possible positions of the single entangling gate. The resulting physical circuit is independently simulated with dense 4×4 matrices.

**Important T-sign convention:** a negative weight-two Pauli rotation need not differ from its positive counterpart by a *local* Clifford before localization. Our compiler first maps the relevant axes to weight-one Paulis using at most one physical CNOT, and only **then** implements signed \(T^\dagger=S^\dagger T\) via local Clifford corrections.

## The 10 exceptional local classes: exact restricted AND unrestricted optimum

The remaining ten local classes belong to **two distinct full Clifford orbits**, each of size 720. For each of those ten representatives, we produce an explicit one-CNOT-compatible signed three-T word with
\[
\boxed{R_{\le1\mathrm{CNOT}}^{(3)}=463/256=1.80859375.}
\]
The exact common numerator over \(128^4\) is \((485490688,0)\).

But attaining \(463/256\) alone would **not** prove that two CNOTs cannot do better. Therefore we separately enumerate **all 3,616 unrestricted zero/one/two/three-T Pauli words** for one representative from **each** exceptional full Clifford orbit, using exact \(\mathbb Z[\sqrt2]\) arithmetic and integer square comparisons for ordering. For each orbit the absolute optimum is exactly
\[
\boxed{R_\infty^{(3)}=463/256.}
\]
Full global Clifford invariance extends this minimum across every state in the corresponding full orbit. Thus the ten exceptional classes have **no strict second-CNOT advantage either**, despite failing to reach the absolute two-qubit maximum under three additional T.

This completes the proof for **all 18,900** input rays, not just the 48 saturation classes.

## Sharpness: a previously certified four-T-prepared input

The input
\[
|\chi_*\rangle=(R_x(\pi/4)\otimes I)(A|00\rangle+B|11\rangle),
\quad
A=\frac{1-\sqrt2+i(1+2\sqrt2)}4,\quad
B=\frac{1-\sqrt2+i}4
\]
was proved [exactly four-T-preparable from a stabilizer](end_to_end_preparation_cost.md), with a constructive 4T/1CNOT circuit.

The independent [exact CNOT-gap certificate](exact_maximal_magic_two_cnot_threshold.md) establishes
\[
R_1^{(3)}(\chi_*)-R_2^{(3)}(\chi_*)
=\frac{1097-648\sqrt2}{4096}>0,
\]
with \(R_2^{(3)}(\chi_*)=7/4\). Hence four preparation T gates suffice, and the no-go for at most three proves four are **necessary** for the existence of such a strict gap.

## Reproduction

\`\`\`bash
python -m src.one_t_natural_input_theorem
python -m src.two_t_prepared_no_go
python -m src.three_t_prepared_threshold
python -m unittest discover -s tests -p 'test_three_t_prepared_threshold.py' -v
\`\`\`

The independent 4×4 state-vector test [test_three_t_prepared_threshold.py](../tests/test_three_t_prepared_threshold.py) reconstructs **all 58** input representatives from their exact Pauli expectation vectors, checks purity, explicitly compiles each witness to a circuit with at most one physical CNOT, and verifies its exact predicted fourth moment numerically. Exact orbit enumeration and unrestricted lower-bound checks remain integer/symbolic.

## Scientific interpretation and limits

This identifies a sharp **preparation complexity threshold for the *possibility* of an input-conditioned second-CNOT magic advantage**, under the exact fixed model. It does **not** prove:
- that every state with input T-preparation count \(\ge4\) has an advantage;
- that two CNOTs improve resource conversion when input preparation cost is charged end-to-end;
- any result for mixed/noisy states, larger systems, multi-copy conversion, adaptive injection, catalysis or measurement;
- that the theorem is unpublished or constitutes a new general stabilizer resource monotone.

The two-qubit absolute magic value, Clifford orbit techniques, two-qubit Clifford+T normal form, and existing direct stabilizer-to-magic preparation circuits are known prior art. Nearby references include Liu–Low–Yin (2026), Roman et al. (2026), Bian–Selinger (2023), Zhu et al. (2024), Leone–Bittel (2024), and Hou–Cao–Yang (2026). **Publication novelty and independent proof audit remain open.** A compelling next step is a short invariant-based explanation for this T-count-four threshold that avoids finite exhaustive enumeration, or a natural externally supplied \(\ge4T\)-resource-state conversion protocol that exhibits it.
