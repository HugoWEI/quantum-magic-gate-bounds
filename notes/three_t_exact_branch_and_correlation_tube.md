# Exact optimal three-T branches and a Pauli-correlation neighborhood

**Research date:** 30 October 2026. **Status:** exact finite theorem, two independent computational implementations (the original polynomial generator and an independently rewritten integer-polynomial enumerator), complex-matrix checks. **Literature novelty unverified.**

## Input and model

For \(-1/8\le s\le 1/4\), set
\[
v(s)=(-1+3i,\,-7-i,\,-1+i,\,-1+(4+s)i)^T,\quad
N(s)=v^\dagger v=s^2+8s+79,\quad
|\psi_s\rangle=v(s)/\sqrt{N(s)}.
\]
We permit at most **three single-qubit T gates** and arbitrary 1-qubit Cliffords, with either 0/1 or 0/1/2 physical CNOT gates, no ancillas or measurement. The objective is the final Pauli fourth moment
\[
R(\psi)=\sum_{P\in\{I,X,Y,Z\}^{\otimes2}}\langle P\rangle_\psi^4,
\]
equivalently the second stabilizer Rényi entropy \(M_2=-\log_2(R/4)\) for pure states.

The preceding exact [three-T proof](three_t_two_cnot_threshold.md) established a strictly positive 2-CNOT gain for one state, and the earlier [uniform interval certificate](three_t_parametric_and_symplectic.md) established a >0.01 fourth-moment gap across the full interval. Here we **identify both globally optimal branches throughout the interval**.

## Theorem: exactly two fixed optimal circuits and rational functions

Define polynomials in increasing powers \(s^0,\ldots,s^8\):

\[
\begin{split}
P_*(s)={}&1103764401+435414168s+145739564s^2+27589704s^3\\
&+3664950s^4+349032s^5+24908s^6+1080s^7+33s^8,\\
P_1(s)={}&69521131+28084688s+9917468s^2+1747712s^3\\
&+162570s^4+11856s^5+1388s^6+96s^7+3s^8.
\end{split}
\]

**Exact sharp envelopes** for every \(-1/8\le s\le1/4\):
\[
\boxed{R_{\min,\le2\mathrm{CNOT},\le3T}(\psi_s)=\frac{P_*(s)}{16N(s)^4}}
\]
attained by chronological Pauli-T word **(YY, XI, XY)**, and
\[
\boxed{R_{\min,\le1\mathrm{CNOT},\le3T}(\psi_s)=\frac{P_1(s)}{N(s)^4}}
\]
attained already by the **two-T** Pauli word **(ZI, ZY)** (known from the 2T one-CNOT localization compiler). As already proved, at most two CNOTs suffice for every three-T word up to a final Clifford.

Thus the exact moment advantage and magic-bit advantage are
\[
G(s)=\frac{H(s)}{16N(s)^4},\qquad
\Delta_{\mathrm{CNOT}}M_2(s)=\log_2\frac{16P_1(s)}{P_*(s)},
\]
where
\[
\boxed{\begin{split}
H(s)={}&8573695+13940840s+12939924s^2+373688s^3\\
&-1063830s^4-159336s^5-2700s^6+456s^7+15s^8.
\end{split}}
\]
The gap G(-1/8) ≈ 0.011864529, G(0) ≈ 0.013757505, G(1/4) ≈ 0.018627339, in fourth-moment units. Additional M2 gains are ≈0.009616, 0.011163, 0.015112 bits at the respective points. The previously proved bound **G(s)>0.01** holds on the whole interval.

## Finite exact proof of the *optimizers*, not just the gap

An independent polynomial enumerator uses direct 4x4 Pauli expectation matrices for the unnormalized input, exact integer polynomial updates for the \(\pi/4\) rotation of Pauli expectations, and exact \(\mathbb Q(\sqrt2)\) arithmetic. It confirms the old 1-CNOT word-set cardinality **2,457** independently.

Each circuit produces a degree-8 numerator in \(\mathbb Z[\sqrt2][s]\) after normalizing by \((8N(s))^4\). For this fixed input family:
- all 1+15+225+3375 = **3616** unrestricted zero/one/two/three-T words collapse to **1,876 distinct polynomial classes**;
- the overcomplete **19,897** zero/one/two/three-T <=1-CNOT candidate words collapse to **1,258 distinct polynomial classes**, with all T-inverse sign assignments included.

For every unrestricted class W, the polynomial \(R_W-R_{YY,XI,XY}\), after clearing the common positive denominator, has **nine nonnegative degree-8 Bernstein coefficients** on \(s=(3t-1)/8\), \(0\le t\le1\). Likewise every restricted class minus \(R_{ZI,ZY}\). This certifies **all 1,876+1,258=3,134 class inequalities**, exactly, including ties. No numerical sampling or real-root estimates enter the proof. The independent integer polynomial implementation found **zero Bernstein failures** in either family.

**Short separate positivity certificate for the resulting gap:** The degree-eight Bernstein coefficients of \(H((3t-1)/8)\), in increasing Bernstein index, when multiplied by \(35\cdot8^8\), are the following nine **strictly positive integers**:
\[
\begin{gathered}
4129379619051085,\ 4424765246189470,\ 4757614012979860,\\
5128412975487160,\ 5537489122997200,\ 5984997157020640,\\
6470907089945920,\ 6994991697097600,\ 7556813859400960.
\end{gathered}
\]
Since the Bernstein basis is nonnegative and sums to 1, \(H(s)>0\) everywhere on the interval. Note that proving this *alone* does not establish that these two circuits are optimal; the **3,134 dominance certificates** are essential for that.

**Reproduction:** Run [three_t_exact_branch_frontier.py](../src/three_t_exact_branch_frontier.py) and [test_three_t_exact_branch_frontier.py](../tests/test_three_t_exact_branch_frontier.py). An additional **standalone independently constructed enumerator** (integer polynomials, separate Pauli expectation construction and Bernstein transform) was used to cross-check the polynomial-class counts and every dominance sign. The standalone code is a supplementary verification, not a formal proof in another programming language.

## Correlation-space robust tube: physically interpretable sufficient condition

Write the input's measurable 15-component Pauli correlation vector as
\[
\mathbf r(\psi)=\big(\langle P\rangle_\psi\big)_{P\in\{I,X,Y,Z\}^{\otimes2}\setminus\{II\}}.
\]
At each \(\psi_s\) in the interval, the vector is the explicit rational curve \(\mathbf r(s)=\mathbf m(s)/N(s)\), with the 15 numerator components, in order
IX,IY,IZ,XI,XX,XY,XZ,YI,YX,YY,YZ,ZI,ZX,ZY,ZZ,
\[
(18+2s,\ 38-2s,\ -55-8s-s^2,\ 14-2s,\ 38+6s,\ 14-2s,\ 2+2s,
-54-14s,\ -18-2s,\ -14-6s,\ 62+14s,\ 41-8s-s^2,\ -2-2s,\ 50+2s,\ -25+8s+s^2).
\]

For any fixed two-qubit unitary U, \(R(U\psi)=1+\sum_{j=1}^{15}v_j^4\), where the traceless Pauli coordinates v are obtained from input r by an orthogonal real transform (unitary conjugation preserves the Hilbert-Schmidt inner product). For any state, \(|v_j|\le1\) and \(\|\mathbf v\|_2^2=4\mathrm{Tr}(\rho^2)-1\le3\). On a straight segment between two state vectors, \(\|\nabla_\mathbf v R\|_2=4\sqrt{\sum v_j^6}\le 4\sqrt3\). Therefore for any two input states and any unitary U,
\[
|R(U\rho)-R(U\sigma)|\le4\sqrt3\,\|\mathbf r(\rho)-\mathbf r(\sigma)\|_2.
\]
Taking minima over the fixed <=1-CNOT and <=2-CNOT circuit sets preserves this Lipschitz constant, so the **gap function** G satisfies
\[
|G(\rho)-G(\sigma)|\le8\sqrt3\,\|\mathbf r(\rho)-\mathbf r(\sigma)\|_2.
\]
Since **G(\psi_s)>1/100** throughout the interval, any pure two-qubit input \(\varphi\) satisfying
\[
\boxed{\min_{s\in[-1/8,1/4]}
\|\mathbf r(\varphi)-\mathbf r(\psi_s)\|_2
<\frac{1}{800\sqrt3}}
\]
**must also require exactly two CNOTs** to reach its unrestricted at-most-three-T magic optimum.

This gives an **explicit open neighborhood in the six-real-dimensional manifold of pure two-qubit states**, described using experimentally measurable Pauli correlations. The pure-state correlation manifold is *not* full-dimensional in the ambient 15-dimensional Euclidean space. This is a conservative sufficient condition, not a necessary or global classification. It remains a conservative sufficient condition, not a necessary one or a global characterization.

## What is and is not novel

Mathematical claims: finite computer-assisted certificate of exact optimal branches for a specified one-parameter family, a rational positive gap, and an open correlation-space sufficient condition. **No assertion is made that the Clifford normal form, Bernstein positivity method, Pauli symplectic methods, or statement itself is publication-first**. Prior-art searches and independent code review remain essential; see [literature audit](literature.md) and [Issue #7](https://github.com/HugoWEI/quantum-magic-gate-bounds/issues/7).
