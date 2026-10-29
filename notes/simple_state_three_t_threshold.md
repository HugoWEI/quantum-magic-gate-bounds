# A clean, high-contrast three-T / two-CNOT magic witness

**Date:** 30 October 2026. **Status:** exact finite arithmetic certificate, independently checked by dense matrices; **literature originality NOT established**.

## Elementary input with intrinsic magic

Let
\[
|\chi\rangle=(R_x(\pi/4)\otimes I)
\bigl(\cos(\pi/12)|00\rangle+
e^{i\pi/12}\sin(\pi/12)|11\rangle\bigr),
\qquad R_x(\alpha)=e^{-i\alpha X/2}.
\]
This is a **fixed given input**, not a promise that preparing it costs no non-Clifford gates. Its concurrence is \(C=\sin(\pi/6)=1/2\), and its initial Pauli fourth moment and second stabilizer Rényi entropy are
\[
R_{\rm in}=\frac{621}{256},\qquad
M_{2,\rm in}=\log_2\frac{1024}{621}\approx0.72155054 \ \mathrm{bits}.
\]
Because the concurrence is strictly between 0 and 1, this state is not locally unitarily equivalent to any stabilizer pure state; pre-existing magic cannot be removed with local unitaries.

The gate model is **at most three ordinary T gates, arbitrary one-qubit Clifford gates, and either orientation of CNOT**, with a 0/1/2-CNOT budget. No ancillas, measurements or extra entangling gates. The objective is final \(M_2\), which is unchanged by a trailing Clifford. We do **not** claim the exact target unitary has a minimal CNOT count of two, nor count the cost of preparing the fixed input.

## Exact optimum and an exact strict resource separation

The exact best unrestricted fourth moment with at most three T gates is
\[
\boxed{R_{\rm unrestricted}(\chi)
=\frac{32607-756\sqrt2-1764\sqrt3+80\sqrt6}{16384}
\approx1.750395269880194,}
\]
attained by chronological Pauli rotations \( (XX,IZ,IY)\).

The exact best fourth moment with **at most one physical CNOT** and the same three-T budget is
\[
\boxed{R_{\le1\mathrm{CNOT}}(\chi)
=\frac{29903-260\sqrt3}{16384}
\approx1.797648119508795,}
\]
attained by signed chronological rotations \((-ZX,-IY,-ZI)\); the ordered-axis pattern is in the rigorously enumerated one-CNOT-compatible set.

Thus
\[
\boxed{R_{\le1\mathrm{CNOT}}-R_{\rm unrestricted}
=\frac{-676+189\sqrt2+376\sqrt3-20\sqrt6}{4096}
\approx0.047252849629>\frac1{25}.}
\]
Since an independently verified compiler realizes **any** three-T Pauli word, up to a final Clifford, using at most **two CNOTs**, the optimal magic output for this fixed input requires **exactly two CNOTs**.

In terms of actual stabilizer Rényi entropy:
\[
M_{2,\rm unrestricted}\approx1.1923192554,\quad
M_{2,\le1\mathrm{CNOT}}\approx1.1538893517,\quad
\Delta M_2\approx0.0384299036\ \mathrm{bits}.
\]
This gives more than three times the magic-bit separation of the earlier Gaussian-integer input. Moreover the two-CNOT state lies only **0.000325823 bits** below the known global two-qubit pure-state magic maximum \(\log_2(16/7)\) (see Liu–Low–Yin and Roman et al.). This makes the operational significance clearer: the extra entangling gate enables **near-maximal two-qubit magic** under the imposed non-Clifford gate budget.

## Small exact field and verification

Unlike the earlier Gaussian-integer witness, the input correlations belong to the degree-four field \(\mathbb Q(\sqrt2,\sqrt3)\). In the standard Pauli basis, the only nonzero expectation values, each represented as an integer expression divided by 8, are:
\[
\begin{array}{lll}
II:8,&IZ:4\sqrt3,&ZI:2\sqrt6,\\
YI:-2\sqrt6,&XX:\sqrt2+\sqrt6,&XY:-\sqrt2+\sqrt6,\\
YX:-1+\sqrt3,&YY:-1-\sqrt3,&YZ:-4\sqrt2,\\
ZX:-1+\sqrt3,&ZY:-1-\sqrt3,&ZZ:4\sqrt2 .
\end{array}
\]
All other expectations vanish. An anticommuting Pauli pair rotates by \(1/\sqrt2\) under each T, so coefficients remain in this field and can be propagated *exactly*, without floats.

[Executable exact certificate](../src/three_t_simple_state_certificate.py):
1. Generates all \(1+15+225+3375=3616\) unrestricted zero/one/two/three-T Pauli words.
2. Includes all 241 unrestricted shorter words (a safe superset for the one-CNOT comparison), and all \(2457\times8\) signed three-T words compatible with **zero or one CNOT placed at any cut**, totaling **19,897** conservatively exhaustive restricted candidates.
3. Computes all fourth moments as integer quadruples \(a+b\sqrt2+c\sqrt3+d\sqrt6\) over common denominator \(64^4\).
4. Compares signs rigorously using integer-square-root enclosures of \(\sqrt2,\sqrt3,\sqrt6\) scaled by \(10^{40}\); enclosure endpoints are certified by squaring integers. Asserts exact optimal numerators and verifies \(25(R_{\le1\mathrm{CNOT}}-R_*)>1\) using only integer signs.
5. [Independent matrix tests](../tests/test_three_t_simple_state.py) evolve the explicit input under the winning \(T_P\) rotations using complex NumPy matrices and independently check the moments, concurrence, and comparison with the two-qubit global magic ceiling.

Reproduce from the repository root:
\`\`\`bash
python -m src.three_t_simple_state_certificate
python -m unittest discover -s tests -p 'test_three_t_simple_state.py' -v
\`\`\`

## Interpretation and open research question

A small *exploratory* grid of 81 **Schmidt-aligned** inputs showed no 3T two-CNOT advantage, but a single non-Clifford local rotation of the Schmidt basis produced the strict separation above. The grid does **not** prove that aligned inputs never require two CNOTs. The current evidence suggests **Pauli-correlation orientation**, beyond concurrence and scalar initial magic, controls the architecture-dependent resource threshold.

Investigate whether an analytic symmetry or invariant characterizes such a high-contrast region around this elementary example. The existing phase-family theorem for a different input has already established a broad region and an exact correlator-distance sufficient condition; it does not yet yield a global orientation-space classification.

**Priority:** our exact input-conditioned low-T/CNOT-output-magic theorem is distinct in *objective* from the static two-qubit magic–entanglement frontier (Roman et al., 2026), synthesis of Clifford/CNOT unitaries (Webster et al., 2026), and entanglement-enhanced injection (Hou et al., 2026). A targeted comparison is not a comprehensive novelty audit; do not claim first publication, theorem priority, or applicability to arbitrary larger architectures.
