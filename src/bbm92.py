import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def run_bbm92(n_pairs=1000, eve_fraction=0.0, seed=42):
    if n_pairs < 1: raise ValueError("n_pairs must be positive")
    if not 0 <= eve_fraction <= 1: raise ValueError("eve_fraction must be between 0 and 1")
    rng = np.random.default_rng(seed); sim = AerSimulator()
    ab = rng.integers(0, 2, n_pairs); bb = rng.integers(0, 2, n_pairs)
    eb = rng.integers(0, 2, n_pairs); attacked = rng.random(n_pairs) < eve_fraction
    circuits = []
    for i in range(n_pairs):
        qc = QuantumCircuit(2, 3)  # c0 Alice, c1 Eve, c2 Bob
        qc.h(0); qc.cx(0, 1)
        if attacked[i]:
            if eb[i]: qc.h(1)
            qc.measure(1, 1); qc.reset(1)
            with qc.if_test((qc.clbits[1], 1)): qc.x(1)
            if eb[i]: qc.h(1)
        if ab[i]: qc.h(0)
        if bb[i]: qc.h(1)
        qc.measure(0, 0); qc.measure(1, 2); circuits.append(qc)
    res = sim.run(circuits, shots=1, seed_simulator=seed).result()
    a = np.zeros(n_pairs, dtype=int); b = np.zeros(n_pairs, dtype=int)
    for i in range(n_pairs):
        s = res.get_counts(i).most_frequent().replace(" ", "")
        a[i], b[i] = int(s[-1]), int(s[-3])
    keep = ab == bb; ak, bk = a[keep], b[keep]
    qber = float(np.mean(ak != bk)) if len(ak) else 0.0
    if eve_fraction == 0: assert np.array_equal(ak, bk)
    print(f"BBM92: attack={eve_fraction:.0%}, sifted={len(ak)}, QBER={qber:.3%}")
    return {"sifted_key_rate": float(np.mean(keep)), "qber": qber, "sifted_key_length": len(ak)}
