# Correlation-sensitive two-T capacities and restricted Clifford routing

**Status: 29 October 2026.** Exact within specified models; **publication novelty is unverified**.

## Proposition 1: concurrence and initial magic do not determine optimal two-T gain

Let \(|\Phi^+\rangle=(|00\rangle+|11\rangle)/\sqrt2\), and \(R_j(\alpha)=e^{-i\alpha\sigma_j/2}\). Define
\[
|\psi_A\rangle=(|00\rangle+e^{i\phi}|11\rangle)/\sqrt2,\quad
\cos(2\phi)=\frac14,
\]
\[
|\psi_B\rangle=(R_x(\pi/8)R_y(\pi/8)\otimes I)|\Phi^+\rangle.
\]
Their concurrences both equal 1 and initial fourth moments both equal \(49/16\), so \(M_2(\psi_A)=M_2(\psi_B)=\log_2(64/49)\).

With **arbitrary two-qubit Clifford routing and at most two T gates**, the general-phase theorem gives
\[
\min_{\le2T}R(\psi_A)=57/32,\qquad
F_2(\psi_A)=\log_2(98/57)\approx0.781819830.
\]
For \(\psi_B\), an exhaustive exact 225-word certificate yields
\[
\min_{\le2T}R(\psi_B)=
\frac{597-70\sqrt2+(32\sqrt2-56)\sqrt{2+\sqrt2}}{256}
\approx1.867775674784,
\]
\[
F_2(\psi_B)\approx0.713388650476.
\]
Thus the gap is \(\approx0.068431179475\) bits at *identical* input concurrence and \(M_2\). The full exact algebraic minimizer for state B is attained by chronological Pauli-axis word (IZ,ZX). This is a **pointwise** separation, not a proof that no envelope function of (C,M2) can exist.

**Exact proof for state B:** The Bell correlation tensor after \(R_x(\pi/8)R_y(\pi/8)\) has nonzero Pauli moments
\(II=1\), \(XX=c\), \(XZ=s\), \(YX=s^2\), \(YY=-c\), \(YZ=ZX=-cs\), \(ZY=-s\), \(ZZ=c^2\),
with \(c=\cos(\pi/8)\), \(s=\sin(\pi/8)\).
All 225 Pauli rotations collapse into 70 symbolic polynomial classes.
The source [two_t_isomagic_counterexample.py](../src/two_t_isomagic_counterexample.py) proposes 18-digit rational intervals for \(c,s,\sqrt2\), **proves their validity by rational squaring inequalities**, then certifies all 69 inactive classes above the exact minimum through rational monomial interval bounds. This is a rigorous rational sign certificate, not a numerical minimization.

**Interpretation caveat:** Both \(\psi_A\) and \(\psi_B\) are maximally entangled states obtained from Bell pairs by local unitaries; the magic can be removed by local unitaries. For unavoidable pre-existing magic, use \(0<\theta<\pi/4\) in the main Schmidt-family theorem.

## Proposition 2: exact two-T frontier with local-only Clifford access

Now **forbid all entangling Clifford gates**: arbitrary *single-qubit* Cliffords and at most two local T gates are allowed. The input family remains \(|\psi_{\theta,\phi}\rangle=\cos\theta|00\rangle+e^{i\phi}\sin\theta|11\rangle\). After phase symmetry reduction \(0\le\phi\le\pi/4\), set \(t=\sin^2(2\theta), x=\sin^2\phi\), and
\[
K=1-t+t^2(1-x+x^2),\quad R_{\rm in}=4K,
\]
\[
A=\frac{9-8t+8t^2+6tx-8t^2x+9t^2x^2}{4},\quad
D=\frac{11-11t+(9+5x-5x^2)t^2}{4}.
\]
Only six Pauli axes XI,YI,ZI,IX,IY,IZ are available. All **36** ordered two-T words form **five exact symbolic moment classes**. The optimum with exactly two T gates is
\[
R_{\min,\mathrm{local}}^{(2T)}=\min\{A,D\},
\]
achieved by chronological axes (IX,YI) and (IX,IY), respectively. The three other classes are **globally dominated by A**, proved by positive tensor Bernstein coefficients in \(\mathbb Q(\sqrt2)\) on the whole rational parameter square without subdivision.

Since the best one-T output moment is exactly \(3R_{\rm in}/4=3K\), the sharp **at-most-two-T local Clifford** answer is
\[
\boxed{R_{\min,\mathrm{local}}^{(\le2T)}=\min\{A,D,3K\}},
\quad
F_{2,\mathrm{local}}=\log_2\frac{4K}{\min\{A,D,3K\}}.
\]
This is a **local-gate-access** theorem, NOT a general constant-depth or limited-CNOT-layer theorem.

### Strict advantage from entangling Clifford routing

At \(\theta=\pi/8,\phi=\pi/4\), the input is partially entangled with \(C=1/\sqrt2\) and *intrinsic* magic. Exact values:
\[
R_{\rm in}=11/4,\qquad
R_{\min,\mathrm{local}}^{(\le2T)}=129/64,\qquad
R_{\min,\mathrm{global}}^{(\le2T)}=121/64.
\]
Thus global two-qubit Clifford routing gives a strictly greater optimal magic gain by
\[
F_{2,\mathrm{global}}-F_{2,\mathrm{local}}
=\log_2(129/121)\approx0.092364018149\ \mathrm{bits}.
\]
This illustrates the impact of routing restrictions **without claiming any particular minimal physical circuit depth**.

## Reproduction

\`\`\`bash
pip install -r requirements.txt
python -m src.general_phase_certificate
python -m src.two_t_isomagic_counterexample
python -m src.local_clifford_frontier
python -m unittest discover -s tests -v
\`\`\`

Sources and prior-art caveats: [general-phase theorem](general_phase_frontier.md), [literature audit](literature.md). The extra 2026 Liu–Low–Yin static magic bounds, Zhu amortized SRE, Roman two-qubit static Pareto, Hou magic injection, and Szombathy random doped circuits must all be explicitly kept separate from any future originality claim.
