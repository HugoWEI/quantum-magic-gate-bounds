"""Deterministic two-T word enumeration, not a proof of a frontier."""
import numpy as np
from src.magic_bounds import schmidt_phase,concurrence,m2,best_sequence

def main():
    zhu=2*np.log2(4/3)
    state_max=np.log2(16/7)
    print("Case | C | M2(input) | best 1T | best 2T | 2T axes | Zhu 2T | state cap")
    for name,theta,phi in [
        ("partial phi=pi/4",np.pi/8,np.pi/4),
        ("partial phi=pi/8",np.pi/8,np.pi/8),
        ("Bell phi=pi/4",np.pi/4,np.pi/4),
        ("Bell phi=pi/8",np.pi/4,np.pi/8),
    ]:
        psi=schmidt_phase(theta,phi)
        _,b1=best_sequence(psi,1)
        word,b2=best_sequence(psi,2)
        print(f"{name:20} | {concurrence(psi):.6f} | {m2(psi):.9f} | "
              f"{b1:.9f} | {b2:.9f} | {word!s:14} | {zhu:.9f} | "
              f"{state_max-m2(psi):.9f}")

if __name__=="__main__":
    main()
