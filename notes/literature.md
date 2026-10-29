# Prior-art boundary (checked 29 October 2026)

**This is a targeted literature/theorem comparison, not an exhaustive novelty search. Do not claim publishable novelty yet.**

| Prior work | What is already established | What remains a *candidate* question |
|---|---|---|
| Zhu, Chen, Shen, Liu, Yu, Wang, **Amortized Stabilizer Rényi Entropy of Quantum Dynamics** (2024), [arXiv:2409.06659](https://arxiv.org/abs/2409.06659), Theorem 2 / Appendix C | Exact universal gain for one T: M2^A(T)=2-log2(3)=log2(4/3), valid with ancillas and initially magical pure inputs. Composition implies k log2(4/3). Their proof uses Pauli fourth moments and an exact positivity inequality. | Which **fixed inputs** can attain equality, what correlation information is needed to quantify a strict deficit, and what can shallow Clifford+T sequences reach? Algebraic rewrites of their theorem are not original discoveries. |
| Roman, Knipfer, Neto, Matchev, Matcheva, Gleyzer, **The Pareto Frontiers of Magic and Entanglement: The Case of Two Qubits** (2026), [arXiv:2603.24902](https://arxiv.org/html/2603.24902v1) | Complete two-qubit maximum and minimum static M2 at fixed concurrence, including extremizer families. Global two-qubit maximum is **ln(16/7)** using their natural-log convention, or **log2(16/7)** in our bits convention. At intermediate concurrence, magic cannot vanish. | Dynamical **reachability from a specified input** under limited T-count and Clifford routing; static Pareto frontiers alone do not characterize this reachable set. Beware: arbitrary global Clifford routing may change concurrence. |
| Hou, Cao, Yang, **Stabilizer entanglement enhances magic injection** (2026), [npj Quantum Information 12, 113](https://doi.org/10.1038/s41534-026-01265-4) (published 11 May 2026; version of record 20 July 2026; [arXiv precursor 2503.20873](https://arxiv.org/abs/2503.20873) titled *Stabilizer Entanglement as a Magic Highway*) | Entanglement-enhanced injection on stabilizer inputs under Haar-local U and unitary SRE; also numerical explorations of non-stabilizer entanglement and shallow brickwork circuits. Explicitly raises systematic intrinsic magic capacity as an open direction. | Deterministic, fixed-input structured Clifford+T reachability and exact orientation-dependent capacities. **Do not claim** first treatment of initial non-stabilizer entanglement or shallow circuits; inspect their supplement fully. |
| Leone, Oliviero, Hamma, **Stabilizer Rényi Entropy** (2022), [PRL 128, 050402](https://doi.org/10.1103/PhysRevLett.128.050402) | The SRE definition and properties. | Baseline conventions only. |
| Liu, Low, Yin, **Maximal magic for two-qubit states** (2026) | Earlier two-qubit maximal magic results/bounds; cited by Roman. | Prior-art chronology when using a global magic cap. |

## The working research gap (hypothesis, not novelty verification)

For a **fixed entangled magic input** psi, define F_k(psi) as the maximum M2 increase from Clifford+T circuits with k T gates (specifying whether Cliffords are globally available or locality/depth-limited). Is there a certified, state-dependent analytic frontier strictly finer than the Zhu count bound and Roman's static state bound? Which Pauli correlation invariants distinguish states at the same initial concurrence and M2? Our exact counterexample confirms the latter distinction is necessary, but **does not establish that the insight is new**.

## Required novelty checks before paper claims

1. Read all of Zhu Appendix C and references on single-T equality/saturation input classifications.
2. Read all of Roman's 34 pages, including explicit extremal state families, and Hou's supplement on non-stabilizer inputs and brickwork.
3. Forward-citation search through 29 Oct 2026: "fixed-input magic capacity", "T gate stabilizer Rényi saturation", "Pauli rotation fourth moments", "amortized SRE equality", "two T gates magic growth".
4. Check whether arbitrary global Clifford interleaving or strictly local Clifford gates are allowed in every claimed theorem; distinguish **T-count from physical depth**.
5. Independently certify all candidate piecewise two-T frontiers over **225 Pauli-axis words**; simulations alone cannot prove a sharp bound.
