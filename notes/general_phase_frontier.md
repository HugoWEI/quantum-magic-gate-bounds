# Exact two-parameter two-T magic-increase frontier

**Status, 29 October 2026:** theorem proved for the stated circuit model, checked by exact symbolic exhaustive enumeration and independent state-vector tests. **Literature novelty not yet established; not a peer-reviewed result.**

## Precise statement

Two-qubit pure input
\[
|\psi_{\theta,\phi}\rangle=\cos\theta|00\rangle+
e^{i\phi}\sin\theta|11\rangle,\quad 0\le\theta,\phi\le\pi/4.
\]
All logarithms base 2. Define \(R(\psi)=\sum_{P\in\{I,X,Y,Z\}^{\otimes2}}\langle P\rangle_\psi^4\) and \(M_2=-\log_2(R/4)\). The admissible gates are **arbitrary global two-qubit Clifford gates and at most two T gates**; we do **not** constrain physical Clifford depth, require geometric locality, allow ancillas, or permit measurements.

Set \(t=\sin^2 2\theta\), \(x=\sin^2\phi\). Define
\[
A(t,x)=\frac{9-8t+8t^2+6tx-8t^2x+9t^2x^2}{4},
\]
\[
B(t,x)=\frac{11}{4}[1-t+t^2(1-x+x^2)],
\]
\[
C(t,x)=\frac{16-16t+(9-8x+8x^2)t^2}{4}.
\]

**Theorem:** the minimum achievable output Pauli fourth moment over admissible circuits is
\[
R_{\min}^{(\le2T)}(t,x)=\min\{A(t,x),B(t,x),C(t,x)\}.
\]
The initial fourth moment is
\[
R_{\rm in}(t,x)=4[1-t+t^2(1-x+x^2)],
\]
so the **sharp input-conditioned gain** is
\[
\boxed{F_2(\psi_{\theta,\phi})=
\log_2\frac{4[1-t+t^2(1-x+x^2)]}{\min\{A,B,C\}}}.
\]
Each branch is attained by the following **chronological** ordered Pauli rotations \(T_P=\exp(-i\pi P/8)\):
- A: \((IX,YI)\);
- B: \((IX,ZY)\);
- C: \((IX,ZX)\).

For \(\phi=\pi/4\), A coincides with the \((IX,XI)\) branch in the earlier one-phase theorem. The earlier theorem is a slice of the full result, not a separate publication claim.

The restriction \(0\le\phi\le\pi/4\) loses no relevant phase orbit: an S Clifford shifts \(\phi\) by \(\pi/2\), and complex conjugation maps \(\phi\mapsto-\phi\), preserving both M2 and the allowed Clifford+T count (as \(T^\dagger\) differs from \(T\) by a Clifford). Thus any real phase can be mapped into this fundamental phase domain.

## Key corollaries

**Constant-gain plateau.** Branch B obeys \(B=(11/16)R_{\rm in}\) identically, hence wherever B is optimal:
\[
F_2=\log_2(16/11)\approx0.540568\ \text{bits}.
\]
This is also a constructive lower bound on the optimum for every input in the family. Moreover the one-T optimum has output fourth moment \(3R_{\rm in}/4\) (Zhu et al.'s inequality, attained in this family). Since \(11/16<3/4\), the two-T theorem also holds for **at most two**, not only exactly two, T gates.

**Exact triple point of the circuit phase diagram.** The equations \(A=B=C\) have the unique physically relevant solution
\[
x_*=\sqrt5-2,\quad t_*=\frac{1+\sqrt5}{4},
\]
so \(\phi_*=\arcsin\sqrt{\sqrt5-2}\approx29.0694^\circ\) and \(\theta_*=\frac12\arcsin\sqrt{(1+\sqrt5)/4}\approx32.0432^\circ\). In fact
\[
A-C=\frac{[7-t(1-x)][t(1+x)-1]}4,
\]
and the resultant of \(A-B\) and \(B-C\) is proportional to \((x^2+4x-1)(71x^2-86x+64)\); the second quadratic has negative discriminant. This establishes uniqueness of the triple meeting inside the domain.

## Proof strategy and a machine-checkable *exact* certificate

1. **Reduction to 225 words:** A two-T Clifford circuit is equivalent for M2 to \(T_QT_P\) (plus an irrelevant final Clifford), with \(P,Q\) any of 15 nonidentity two-qubit Hermitian Pauli axes. Relative signs are redundant because an inverse T is one T followed by a Clifford.
2. **Exact symbolic enumeration:** Initial nonzero Pauli expectations are II=ZZ=1, IZ=ZI=\(z=\cos 2\theta\), XX=\(q\cos\phi\), XY=YX=\(q\sin\phi\), YY=\(-q\cos\phi\), with \(q=\sin2\theta\). Clifford-conjugated T rotates each anticommuting Pauli pair by 45 degrees. Enumerating all 225 ordered words yields exactly **21 distinct quartic fourth-moment polynomials** in \(q,z,u=\cos\phi,v=\sin\phi\).
3. **Sharpness:** Three classes give exactly A, B, C; explicit word representatives achieve each class.
4. **Rigorous exclusion of all other 18 classes:** Use rational chart
\[
r=\tan\theta\in[0,1],\quad
s=\frac{\tan(\phi/2)}{\sqrt2-1}\in[0,1].
\]
For each candidate difference \(R_{\rm class}-R_{\rm branch}\), multiply by the *strictly positive*
\[
(1+r^2)^4(1+(\sqrt2-1)^2s^2)^4.
\]
The result is a polynomial of bidegree at most (8,8) with coefficients in \(\mathbb Q(\sqrt2)\). Its tensor Bernstein coefficients have an exact lower-bound property. Bisect the square \([0,1]^2\) into dyadic rectangles until **at least one** of the three branch differences has *every* Bernstein coefficient nonnegative. The exact algorithm terminates with **42 rectangles across the 18 inactive classes**, maximum recursive subdivision depth 5. All signs in \(\mathbb Q(\sqrt2)\) are certified via rational arithmetic and squared comparisons; there are **no floating-point sign tests**.
5. **At most two gates:** As shown above, branch B beats the best one-T and zero-T moments, globally.

The complete certificate is in [src/general_phase_certificate.py](../src/general_phase_certificate.py), independently checked with dense NumPy evolution of all **225 circuits for 16 inputs** plus transformed phases in [tests/test_general_phase.py](../tests/test_general_phase.py).

\`\`\`bash
pip install -r requirements.txt
python -m src.general_phase_certificate
python -m unittest discover -s tests -v
\`\`\`

## Prior-art cautions

- Zhu et al., [*Amortized Stabilizer Rényi Entropy of Quantum Dynamics*](https://arxiv.org/abs/2409.06659) (2024), establish the **universal one-T** M2 increase \(\log_2(4/3)\), including magical entangled inputs and ancillas. We do not claim this result.
- Roman et al., [*The Pareto Frontiers of Magic and Entanglement: The Case of Two Qubits*](https://arxiv.org/html/2603.24902v1) (2026), establish *static* magic/concurrence frontiers; they do not in the checked sections address fixed-input two-T reachability. Arbitrary entangling Cliffords may change concurrence; don't incorrectly apply a fixed-concurrence cap to our output.
- Hou et al., [*Stabilizer entanglement enhances magic injection*](https://www.nature.com/articles/s41534-026-01265-4) (2026), study injection, including nonstabilizer entanglement and shallow circuits. We do **not** claim first to study magic already present in entangled inputs.
- Szombathy et al., [*Spectral properties versus magic generation in T-doped random Clifford circuits*](https://doi.org/10.1103/557f-6tpb) (2025), investigate low-T and random ensemble magic distributions, a distinct but relevant dynamical setting.

These are targeted theorem contrasts, **not a conclusive priority search**. Before a paper claim, investigate all supplements, forward citations, existing two-qubit circuit synthesis classifications, and related resource-capacity bounds. The next unsolved directions are (i) arbitrary local Clifford orientation/fixed-input invariants beyond \(M_2\) and concurrence and (ii) physically depth-constrained Clifford routing.
