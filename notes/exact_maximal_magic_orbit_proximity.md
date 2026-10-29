# Exact Clifford-orbit proximity of the clean 3T/2-CNOT optimum

**Research date:** 30 October 2026. **Status:** exact algebraic overlap, 480-state orbit exhaustion, separate 4x4 state-vector check. **Originality unverified.** This note concerns a *known* set of maximally magical two-qubit states, not a new discovery of their existence.

## A stronger physical interpretation of the near-maximal output

Take the input and output-optimal three-T Pauli word from [the clean threshold theorem](simple_state_three_t_threshold.md):
\[
|\chi\rangle=(R_x(\pi/4)\otimes I)(\cos(\pi/12)|00\rangle+e^{i\pi/12}\sin(\pi/12)|11\rangle),
\quad
|\psi_{\rm out}\rangle=T_{IY}T_{IZ}T_{XX}|\chi\rangle,
\]
where \(T_P=e^{-i\pi P/8}\). Output magic is \(M_2(\psi_{\rm out})\simeq1.1923192554\) bits, close to the established two-qubit maximum \(\log_2(16/7)\simeq1.192645\).

Liu, Low and Yin (2025), and later Roman et al. (2026), identify a **480-element pure-state Clifford orbit of maximally magical states**, generated from the fiducial
\[
|f\rangle=(|00\rangle+i|01\rangle+i|10\rangle+i|11\rangle)/2.
\]
The exact **closest orbit representative** to our output is
\[
|f_*\rangle=(I\otimes S)(H\otimes H)|f\rangle
=\frac{(1+3i)|00\rangle+(1+i)|01\rangle+(1-i)|10\rangle+(1+i)|11\rangle}{4}.
\]

**Theorem (exact unique orbit nearest neighbor):**
\[
\boxed{
\max_{\Phi\in{\rm Cliff}_2\cdot f}
|\langle\Phi|\psi_{\rm out}\rangle|^2
=\frac{17+3\sqrt3+4\sqrt6}{32}
\simeq0.9998159810574795.
}
\]
The maximizer is unique up to global phase in the 480-state Clifford orbit. The **second-highest** fidelity is exactly
\[
F_{\rm next}=
\frac{228+14\sqrt2+28\sqrt3+50\sqrt6}{512}
\simeq0.817911913329.
\]
Thus the winning state is **99.9816% faithful** to a known maximal-magic fiducial. Its pure-state trace distance to that fiducial is
\[
\sqrt{1-F_{\max}}\simeq0.01356536.
\]
The fiducial has concurrence \(1/\sqrt2\), while the output state has \(C\simeq0.7103201\). That matches the known fact that maximally magical two-qubit pure states occur at intermediate, not maximal, entanglement. **This is a state-property comparison, not a hardware error or fault-tolerance fidelity claim.**

For context, the **magic-optimal output from the one-CNOT-restricted circuit**, obtained with signed axes (-ZX,-IY,-ZI), has maximal fidelity with this same 480-state orbit equal to
\[
\frac{156+66\sqrt2+52\sqrt3+62\sqrt6}{512}
\simeq0.959517775709.
\]
This does *not* establish the maximum possible orbit fidelity over **all** restricted circuits; it only describes their final-M2-optimal output.

## Why the orbit comparison can be checked *exactly*

For any pure two-qubit states,
\[
F(\psi,\phi)=\operatorname{Tr}(\rho_\psi\rho_\phi)
=\frac14\left(1+\sum_{P\ne II}r_\psi(P)r_\phi(P)\right),
\qquad r_\psi(P)=\langle\psi|P|\psi\rangle.
\]
Each maximally magical fiducial-orbit state has **twelve nonzero traceless Pauli expectations equal to \(\pm1/2\)** and three zero. Since its Clifford transformations simply permute Pauli labels with signs, each orbit member is an **integer signed 15-component vector** \(v_P=2r_\phi(P)\in\{-1,0,1\}\).

For the fixed output \(\psi_{\rm out}\), all 15 Pauli expectations are exactly
\[
r_{\rm out}(P)=
\frac{a_P+b_P\sqrt2+c_P\sqrt3+d_P\sqrt6}{64}
\quad(a_P,b_P,c_P,d_P\in\mathbb Z).
\]
Therefore each possible orbit overlap is exactly
\[
\boxed{F=\frac{128+\sum_{P\ne II}v_P(a_P+b_P\sqrt2+c_P\sqrt3+d_P\sqrt6)}{512}}.
\]

The [executable orbit certificate](../src/maximal_magic_orbit_certificate.py) proceeds as follows:
1. Construct H, S, CNOT Clifford generators using **Gaussian-integer 4x4 matrices**, representing Hadamards by their integer numerator \(H_{\rm num}=\sqrt2H\), and verify the induced **signed Pauli permutations by exact matrix equality**.
2. Start from the exact signed Pauli signature of \(|f\rangle\) and exhaust the orbit under the five generators H0,H1,S0,S1,CNOT, deduplicating by the **exact integer 15-vector signature**. Exactly **480 distinct signatures** arise.
3. Obtain \(r_{\rm out}(P)\) exactly using the previously checked integer-\(\mathbb Q(\sqrt2,\sqrt3)\) Pauli rotation engine.
4. Compare all 480 candidate fidelities **exactly** using integer-square-root enclosures for \(\sqrt2,\sqrt3,\sqrt6\) (no floating-point ranking or ties). The unique maximum has numerator \((272,0,48,64)\) over 512, and the runner-up \((228,14,28,50)\).
5. Independently evolve the actual complex input through the three Pauli rotations and compute overlap with the explicit \(|f_*\rangle\) vector.

This demonstrates a genuine quantitative link between **low-T, CNOT-budgeted magic optimization** and the **known static maximal-magic Clifford orbit**, without conflating the two problems.

**Reproduction:**
\`\`\`bash
python -m src.maximal_magic_orbit_certificate
python -m unittest discover -s tests -p 'test_maximal_magic_orbit.py' -v
\`\`\`

**Prior art boundary:** The 480-state orbit and its maximum \(M_2\) were already studied by [Liu, Low and Yin, *Maximal Magic for Two-qubit States* (2025)](https://arxiv.org/abs/2502.17550); Roman et al., [*The Pareto Frontiers of Magic and Entanglement* (2026)](https://arxiv.org/abs/2603.24902), prove static magic–concurrence frontier formulas. Our fixed-input **gate-budget optimality** is a different problem, but the exact overlap observation does not by itself establish an original publication-level contribution.
