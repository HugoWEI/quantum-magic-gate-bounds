# Exact input-conditioned two-T frontier for an entangled Schmidt-phase family

**Research date:** 2026-10-29. **Mathematical status:** proved by finite symbolic exhaustion, exact Bernstein positivity certificates, and independently validated with dense state-vector calculations. **Publication novelty:** NOT verified.

## Scope and theorem

Let
\[
|\psi_\theta\rangle=\cos\theta|00\rangle+e^{i\pi/4}\sin\theta|11\rangle,\quad
0\le\theta\le\pi/4,\qquad t=\sin^2(2\theta).
\]
**Critical phase check:** the phase is \(\exp(i\pi/4)\), **not \(i=\exp(i\pi/2)\)**.

Define \(R(\psi)=\sum_{P\in\{I,X,Y,Z\}^{\otimes2}}\langle\psi|P|\psi\rangle^4\) and \(M_2(\psi)=-\log_2(R(\psi)/4)\). Consider arbitrary two-qubit Clifford gates (entangling ones allowed) and at most two ordinary \(T=\operatorname{diag}(1,e^{i\pi/4})\) gates, no ancilla or measurement. **Clifford depth is NOT constrained.**

**Theorem (exact sharp bound in this model):**
\[
\min R_{\rm out}(t)=\frac1{16}
\begin{cases}
36-20t+25t^2,&0\le t\le t_1,\\
44-44t+33t^2,&t_1\le t\le t_2,\\
64-64t+28t^2,&t_2\le t\le 1,
\end{cases}
\quad
t_1=\frac{3-\sqrt5}{2},\quad t_2=2(\sqrt2-1).
\]
Since \(R_{\rm in}(t)=4-4t+3t^2\), the maximum increase is
\[
F_2(\psi_\theta)=\log_2\frac{4-4t+3t^2}{\min R_{\rm out}(t)}.
\]
These are pointwise *attained* values, not merely upper bounds. States with \(0<t<1\) have pre-existing intrinsic (nonlocal) stabilizer magic. The result says nothing yet about arbitrary input states or restricted physical depth.

## Pauli enumeration and achieving words

Every two-T sequence \(C_2T C_1T C_0\) is equivalent for \(M_2\) to \(T_QT_P\) on the original input, \(T_P=\exp(-i\pi P/8)\), with \(P,Q\) from the 15 nonidentity Hermitian two-qubit Paulis. Conjugating a gate by a Clifford gives any such axis, and all trailing Cliffords leave \(M_2\) invariant; \(T_P^\dagger\) differs from \(T_P\) by a Clifford, so negative axes need not be added. Thus only 225 ordered words.

For \(q=\sin 2\theta\), \(z=\cos 2\theta\), initial Pauli moments are \(r_{II}=r_{ZZ}=1\), \(r_{IZ}=r_{ZI}=z\), \(r_{XX}=r_{XY}=r_{YX}=q/\sqrt2\), \(r_{YY}=-q/\sqrt2\). For anticommuting Pauli strings, \(T_P^\dagger K T_P=(K+iPK)/\sqrt2\). The vector of moments stays linear in \(1,q,z\), hence \(R_{\rm out}\) is an exact quartic over \(\mathbb Q(\sqrt2)\).

**Exactly 15 distinct moment classes** arise from 225 words. The three minimizing class representatives (axes listed in chronological order) are:

| Branch | Ordered axes | Number of equal-moment words | Fourth moment |
|---|---|---:|---|
| A | IX, XI | 16 | \((36-20t+25t^2)/16\) |
| B | IX, ZY | 16 | \((44-44t+33t^2)/16\) |
| C | IX, ZX | 8 | \((64-64t+28t^2)/16\) |

A=B at \(t_1\); B=C at \(t_2\). A=C at \(t=2/3\), where B is smaller, giving exactly the three branches.

## Exact certificate excluding all 12 other classes

Ten inactive classes have moments even in \(q,z\), so each reduces to a quadratic \(p(t)\) using \(q^2=t,z^2=1-t\). For every class we certify:
- \(p-A\ge0\) on the rational covering interval \([0,2/5]\);
- \(p-B\ge0\) on \([3/8,5/6]\);
- \(p-C\ge0\) on \([4/5,1]\).

The exact degree-two Bernstein coefficients for all 30 differences are nonnegative. The rational intervals cover the actual optimal regions because \(3/8<t_1<2/5\) and \(4/5<t_2<5/6\). See the executable certificate for the exact 30 triples.

The other **two** classes have
\[
R_\pm=\frac{44+36t-29t^2\pm(8-28t)\sqrt{2t(1-t)}}{16}.
\]
They exceed **A** over all \(t\in[0,1]\). Indeed \(N(t)=8+56t-54t^2>0\) has degree-two Bernstein coefficients \((8,36,10)\), and
\[
N(t)^2-2t(1-t)(8-28t)^2
=4(1121t^4-2128t^3+824t^2+192t+16)>0.
\]
The quartic polynomial has strictly positive degree-four Bernstein coefficients \((16,64,748/3,40,25)\). This is a complete strict radical exclusion, not a sampled inequality.

Finally, the best **one-T** output moment is exactly \(3 R_{\rm in}/4\): an input-saturating axis is explicit and Zhu et al. prove the universal inequality. Compare the three displayed quadratics branchwise to check that the two-T optimum always gives a smaller output moment; zero-T is even weaker. Therefore the theorem covers **at most two**, not just exactly two, T gates.

## Reproduction

\`\`\`bash
pip install -r requirements.txt
python -m src.two_t_frontier_certificate
python -m unittest discover -s tests -v
python -m experiments.two_t_pilot
\`\`\`

The certificate generates **all 225** Pauli words algebraically, groups the 15 distinct classes, checks 30 rational Bernstein triples, both radical cases, and exact branch crossings. A wholly separate NumPy state-vector test independently checks **every word** at eight input values, plus prior one-T regressions.

## Prior-art boundaries

- **Zhu et al. (2024), Theorem 2 and Appendix C:** established the universal one-T bound \(\log_2(4/3)\), even with magical inputs/ancillas. We do NOT claim this theorem.
- **Roman et al. (2026):** established static two-qubit magic/concurrence Pareto extremizers, not fixed-input two-gate reachability. Fixed-concurrence static bounds cannot be applied across entangling Clifford gates that alter concurrence.
- **Hou et al. (2026):** studied entanglement-enhanced magic injection with non-stabilizer initial entanglement and shallow brickwork. We do NOT claim to be first to consider those topics; their ensemble-averaged injection contrasts with pointwise optimal Pauli routing here.
- **Szombathy et al., Phys. Rev. Research 7, 043080 (2025):** analyzes T-doped Clifford random circuits including low-T magic values; must inspect relevant appendices and follow-up citations for overlap.

**Open:** full novelty audit including supplementary materials and forward citations; general phase \(\phi\); a general correlation-conditioned frontier; locality/depth-constrained Clifford+T synthesis; greater \(n\). No originality or publishability claim until those are checked.
