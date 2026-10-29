# Exact derivations and research limitations (29 October 2026)

All logarithms base 2 unless stated, all states pure. **These are derivations for this research project, not verified literature-novel theorems.**

## 1. Established setting

Let P_n={I,X,Y,Z}^{tensor n}, with phase-free Hermitian Paulis. Define R(psi)=sum_{Q in P_n} <psi|Q|psi>^4 and M2(psi)=-log2[R(psi)/2^n]. T=diag(1,e^{i pi/4}) is globally phase-equivalent to exp(-i pi Z/8). Define T_P=exp(-i pi P/8).

For any one-T circuit C2 T C1 (C_i arbitrary two-qubit Cliffords), Clifford invariance of M2 reduces the gain to M2(T_P psi)-M2(psi), with P any of **15** nonidentity two-qubit Pauli axes. Signs do not matter: T_P^dagger = S_P^dagger T_P, where S_P is Clifford. The 15-axis reduction only applies if arbitrary global Cliffords are free; a strictly local Clifford-only model has fewer axes.

**Zhu et al. (2024) already prove** D_P(psi):=4R(T_P psi)-3R(psi) >=0 and universal delta M2 <= log2(4/3) for arbitrary pure inputs (and ancillas). Thus

delta_P(psi)=log2[ 4R(psi)/(3R(psi)+D_P(psi)) ].

The exact deficit can be evaluated by partitioning the eight Paulis anticommuting with P into four unordered pairs {Q,Q'} under multiplication by P (discarding phase). Write r_Q=<psi|Q|psi>, and C(P) for the commuting Paulis. Direct Pauli conjugation gives

D_P = sum_{Q in C(P)} r_Q^4 + sum_{unordered anti pairs {Q,Q'}} [12 r_Q^2 r_Q'^2-r_Q^4-r_Q'^4].

Pair rotation uses (x,y)->((x+y)/sqrt(2),(x-y)/sqrt(2)) up to signs. Positivity follows from Zhu; the displayed decomposition **is not** a new general inequality.

## 2. Schmidt-phase family: exact saturation with prior magic

Define psi(theta,phi)=cos(theta)|00>+exp(i phi) sin(theta)|11>, for 0<=theta<=pi/4.

Put C=sin(2theta) (the concurrence), s=sin^2(2phi), and A(C)=4-4C^2+4C^4. The nonzero Pauli expectations are II=ZZ=1, IZ=ZI=cos(2theta), XX=-YY=C cos(phi), XY=YX=C sin(phi), up to a harmless sign convention.

Their fourth-moment sums give the exact identities

R_in=A(C)-C^4 s,
R_after_Z=A(C)-C^4(1-s)   for local T on qubit 1,
R_after_X=(3/4) R_in     for local HTH on qubit 1.

The last expression follows by mixing the Y and Z Pauli rows by 45 degrees and summing fourth powers, as independently checked with symbolic Gröbner reduction and direct state-vector simulation. Since H is Clifford, HTH uses precisely one T. Therefore delta_X=log2(4/3) for every Schmidt-phase state, including partially entangled intrinsically magical inputs.

By contrast, delta_Z=log2[(A-C^4 s)/(A-C^4(1-s))] and for C>0 its sign is sign(1-2s).

**Concrete intrinsic-magic example:** theta=pi/8, phi=pi/4. Then C=1/sqrt(2), R_in=11/4, M2_in=log2(16/11)>0, delta_X=log2(4/3), and delta_Z=log2(11/12)<0. Magic is intrinsic at 0<C<1 because no partially entangled pure state is a stabilizer, a fact encompassed by Roman et al.'s strict minimum magic at intermediate concurrence.

## 3. Exact isomagic counterexample for one T

**Proposition.** Two maximally entangled pure two-qubit states can have the same concurrence and same M2 yet *different maximum one-T gains*, even allowing every two-qubit Clifford around the gate.

**Construction.** Phi+=(|00>+|11>)/sqrt(2). Let R_j(alpha)=exp(-i alpha sigma_j/2), and define

psi_A=(R_z(phi) tensor I) Phi+, with sin^2(2phi)=15/16;
psi_B=(R_x(pi/8) R_y(pi/8) tensor I) Phi+.

Both have concurrence 1 and **exactly** R=49/16, hence M2=log2(64/49). For psi_A, Schmidt-family saturation gives max delta=log2(4/3).

For psi_B, write u=sin^2(pi/8)=(2-sqrt(2))/4 and v=cos^2(pi/8)=(2+sqrt(2))/4. Its only nonzero squared Pauli expectations, besides r_II^2=1, are

(XX,XZ,YX,YY,YZ,ZX,ZY,ZZ) =
(v,u,u^2,v,uv,uv,u,v^2).

Evaluate D_P using the pair formula from Section 1 for all 15 nonidentity P. Complete, symbolic algebraic certificate:

| Pauli axes P | D_P = 4 R(T_P psi_B) - 3 R(psi_B) |
|---|---|
| IX, XX, YI, YY | 7/4 + 7 sqrt(2)/8 |
| IZ, XZ, ZI, ZY | 7/4 - 7 sqrt(2)/8 |
| IY, XI | 49/16 |
| XY | 1/16 |
| YX | 3/2 - sqrt(2) |
| YZ, ZX | 1/2 |
| ZZ | 3/2 + sqrt(2) |

All 15 values are strictly positive and the minimum is D_XY=1/16. Thus **exactly**

max_P delta_P(psi_B) = log2( 4*(49/16)/(3*(49/16)+1/16) )
                     = log2(49/37) < log2(4/3).

So the same input concurrence and scalar initial M2 do NOT determine the optimal one-T magic gain. Proof complete for this explicit pair. Independently validate via:

\`\`\`bash
python -m src.exact_counterexample
python -m unittest discover -s tests -v
\`\`\`

**Scope cautions:** The above exact result does not claim to classify all saturation states or disprove the existence of *envelope* bounds using (C,M2). In particular, a function of (C,M2) can upper bound all inputs in the fibre while failing to be pointwise attained. Also Bell states' apparent magic can be undone by arbitrary local unitaries; they are not an example of *intrinsic* nonlocal magic. The partially entangled Schmidt family in Section 2 is the intrinsic-magic example.

## 4. Smallest next *potentially unsolved* target: two-T conditioned frontier

For fixed two-qubit input psi and arbitrary Clifford routing,

F_2(psi) = max_{P,Q != II} [ M2(T_Q T_P psi) - M2(psi) ],

where the finite optimization has **15^2=225** Pauli-axis words. Evaluate it by exact Pauli moments where possible. Known outer bounds (not our results) include Zhu's 2 log2(4/3) and the global two-qubit state cap log2(16/7)-M2(psi), the latter from prior two-qubit SRE work including Roman et al. (convert their natural logarithm to base 2).

Our reproducible enumerator is a baseline. The research opportunity is an *analytically certified, input-correlation-resolved two-T frontier* (possibly piecewise) at fixed input family, later adding physical circuit depth and nearest-neighbor restrictions. No such new frontier is proved yet, and a fuller literature/supplement search is mandatory before a novelty claim.
