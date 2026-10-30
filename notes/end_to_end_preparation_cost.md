# End-to-end resource accounting: exact preparation cost of the tuned magical input

**Research date: 30 October 2026.** **Status:** exact finite Pauli-spectrum certificate and an explicit 4T/1CNOT circuit, independently checked using complex state vectors. **Publication novelty not established.** No ancillas, measurements or postselection; ordinary 2-qubit Clifford+T gates, exact equality up to global phase.

## Question and exact preparation-cost theorem

Previously, [our fixed-input theorem](exact_maximal_magic_two_cnot_threshold.md) identified a particular partially entangled, already-magical input
\[
|\chi_*\rangle=(R_x(\pi/4)\otimes I)(A|00\rangle+B|11\rangle),
\quad A=(1-\sqrt2+i(1+2\sqrt2))/4,\quad B=(1-\sqrt2+i)/4,
\]
such that the *subsequent* operation requires three T and two CNOTs to attain the output magic \(M_2=\log_2(16/7)\) if at most three T are allowed.

Now charge **all** Clifford+T gates required to prepare \(\chi_*\) from a stabilizer state, instead of treating \(\chi_*\) as free.

**Preparation-cost theorem (two-qubit ancilla-free Clifford+T):** Starting from any **product** two-qubit stabilizer state, **at least 4 T gates and at least 1 CNOT** are necessary to prepare exactly \(\chi_*\) up to a global phase; **four T and one CNOT suffice simultaneously**. The lower bound on T count permits *unrestricted* CNOTs/Cliffords and the lower bound on CNOTs permits *unrestricted* local Clifford+T rotations. Thus both coordinates are individually sharp.

The input is entangled with concurrence
\[
C(\chi_*)=\sqrt{(5-2\sqrt2)/8}>0,
\]
so **at least one CNOT** must be used to create it from a stabilizer product input. An initially *entangled* stabilizer state would already contain entanglement, so the one-CNOT lower bound would not follow. The four-T lower bound applies to **any** stabilizer input. The joint sharp resource statement is for the product-stabilizer starting state \(|00\rangle\), or any product stabilizer state related by free local Cliffords.

## Exact four-T circuit using one CNOT

Define \(T_P=\exp(-i\pi P/8)\), each weight-one \(P\) implemented by a single ordinary T and local Clifford conjugations. The following operations act **chronologically** from right to left:
\[
\boxed{
|\chi_*\rangle\sim
(H\otimes H)\,\mathrm{CNOT}_{0\to1}\,(H\otimes I)\,
T_{XI}\,T_{IZ}\,T_{IY}\,T_{IX}\,|00\rangle.
}
\]
Only the Clifford suffix contains a CNOT. The four Pauli T rotations have weight one, and the three Hadamards are local Cliffords. No extra entangling gates are hidden in their implementation.

The [exact certificate](../src/input_preparation_cost.py) evolves all sixteen Pauli expectations as integer pairs \(a+b\sqrt2\). The start has expectation 1 on II, IZ, ZI, ZZ and zero elsewhere. Four Pauli-T rotations produce a common expectation denominator 64; applying the signed Clifford-Pauli permutations for H0, CNOT, H1, H0 results in **exactly** 16 times the target \(\chi_*\) expectation numerators stored with denominator 4. Equal Pauli expectation vectors imply equal pure density matrices, hence exact state equality up to global phase. An [independent matrix test](../tests/test_input_preparation_cost.py) verifies state fidelity one using dense complex matrices.

## Rigorous lower bound: at most three T gates from a stabilizer have a discrete magic spectrum

Any ancilla-free two-qubit Clifford+at-most-three-T circuit from any stabilizer input, up to a *final Clifford*, can be expressed as
\[
T_{P_k}\cdots T_{P_1}|00\rangle,\qquad k\le3,
\]
for nonidentity two-qubit Pauli axes \(P_j\). This follows by pushing the input-preparing and all interleaved Cliffords through the Pauli rotations and discarding the final Clifford for any Clifford-invariant resource. (Although actual state preparation requires the correct final Clifford, this reduction suffices for a T-count **lower bound**.)

Enumerating \(1+15+225+3375=3616\) possible words gives exactly **nine** possible fourth moments:
\[
\boxed{
R\in\left\{
4,\frac{51}{16},3,\frac{11}{4},\frac{41}{16},
\frac94,\frac{33}{16},\frac{31}{16},\frac74
\right\}.
}
\]
The calculation is entirely exact in \(\mathbb Z[\sqrt2]\): start with integer Pauli expectation numerators, apply signed anticommuting-pair rotations and evaluate all fourth powers with positive common denominator \(32^4\). All nine resulting fourth moments are rational, and the input has
\[
R(\chi_*)=\frac{153}{64},
\]
**absent** from the nine-value set. Hence exact preparation from a stabilizer input requires \(\boxed{T_{\rm prep}\ge4}\). Our explicit four-T circuit proves tightness.

The four-T lower bound is stronger than merely applying the universal amortized single-T \(M_2\) gain bound, which implies only \(T\ge2\). This is a **small-system Clifford-orbit enumeration**, not a new general amortized magic bound.

## The complete end-to-end resource comparison

There are now two conceptually distinct tasks.

| Task | Input | Output | T-count | CNOT count |
|---|---|---|---:|---:|
| Prepare tuned intermediate input | \(|00\rangle\) | \(\chi_*\) | **4** | **1** |
| Maximize magic from tuned input with at most 3 T | \(\chi_*\) | max-\(M_2\) state (up to Clifford) | **3** | **2** |
| Compose those particular two stages | \(|00\rangle\) | max-\(M_2\) state | **7** | **3** |
| Known direct circuit (Liu–Low–Yin) | \(|++\rangle\) (free H gates) | \((1,i,i,i)/2\) | **3** | **1** |

The **direct circuit is strictly more economical** in total gate counts than our staged construction. Written from right to left,
\[
\boxed{|f\rangle=(I\otimes T)\,\mathrm{CNOT}_{0\to1}\,(T\otimes T)\,|++\rangle
=\frac{|00\rangle+i|01\rangle+i|10\rangle+i|11\rangle}{2}.}
\]
This is Figure 1 of Liu–Low–Yin, [*Maximal magic for two-qubit states*](https://doi.org/10.1088/2058-9565/ae3028), *Quantum Science and Technology* 11, 015035 (2026). We independently verified the output via 4x4 state-vector evolution. The three-T direct cost is globally **minimal** for preparation from a stabilizer by the nine-value spectrum above (\(R=7/4\) cannot be achieved with <=2 T), while one entangling CNOT is necessary because the output is entangled and the starting product \(|++\rangle\) is not.

**Crucial inference:** The fixed-\(\chi_*\) two-CNOT theorem is an **input-conditioned reachability obstruction**; it does NOT imply any global preparation advantage or a minimal total circuit cost for reaching maximal magic. The staged resource counts \(7T+3\mathrm{CNOT}\) describe one specified two-stage implementation and do not rule out cancellations or alternative circuits under looser stage constraints. If the *intermediate state is fixed* and one additionally mandates the second stage contain at most three T, the separate exact lower bounds constrain each stage.

## What research remains useful?

The most scientifically meaningful continuation is *not* to claim our engineered two-CNOT intermediate improves the overall preparation cost (it does not). Instead:
- Analyze **state-conditioned transformations when the input is supplied externally**, as in resource-state conversion, catalytic protocols, or constrained state injection, with explicit assumptions about whether the initial magic state is freely available.
- Seek a **natural family** of already-existing magical inputs with a nontrivial CNOT/T Pareto frontier for a meaningful target or target set; avoid engineered intermediate states where the total cost trivially loses to a direct circuit.
- Investigate **magic redistribution/catalysis** or conversion efficiency rather than raw from-stabilizer synthesis; no ancillas/catalysis are permitted in our current theorem, and enabling them would change the model fundamentally.
- Fully audit the priority literature and submit the certificate for external mathematical review before claims of novelty.

**Reproduce:**
\`\`\`bash
python -m src.input_preparation_cost
python -m unittest discover -s tests -p 'test_input_preparation_cost.py' -v
\`\`\`
