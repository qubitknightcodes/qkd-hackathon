import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def run_bb84_with_eve(n_qubits=1000, attack_fraction=1.0, seed=42):
    if n_qubits < 1: raise ValueError("n_qubits must be positive")
    if not 0 <= attack_fraction <= 1: raise ValueError("attack_fraction must be between 0 and 1")
    rng = np.random.default_rng(seed); sim = AerSimulator()
    a = rng.integers(0, 2, n_qubits); ab = rng.integers(0, 2, n_qubits)
    bb = rng.integers(0, 2, n_qubits); attacked = rng.random(n_qubits) < attack_fraction
    eb = rng.integers(0, 2, n_qubits); e = np.zeros(n_qubits, dtype=int)
    ids = np.flatnonzero(attacked); circuits = []
    for i in ids:
        qc = QuantumCircuit(1, 1)
        if a[i]: qc.x(0)
        if ab[i]: qc.h(0)
        if eb[i]: qc.h(0)
        qc.measure(0, 0); circuits.append(qc)
    if circuits:
        r = sim.run(circuits, shots=1, seed_simulator=seed).result()
        e[ids] = [int(r.get_counts(j).most_frequent()) for j in range(len(ids))]
    circuits = []
    for i in range(n_qubits):
        qc = QuantumCircuit(1, 1)
        if attacked[i]:
            if e[i]: qc.x(0)
            if eb[i]: qc.h(0)
        else:
            if a[i]: qc.x(0)
            if ab[i]: qc.h(0)
        if bb[i]: qc.h(0)
        qc.measure(0, 0); circuits.append(qc)
    r = sim.run(circuits, shots=1, seed_simulator=seed+1).result()
    b = np.array([int(r.get_counts(i).most_frequent()) for i in range(n_qubits)])
    keep = ab == bb; ak, bk = a[keep], b[keep]
    qber = float(np.mean(ak != bk)) if len(ak) else 0.0
    print(f"BB84+Eve: attack={attack_fraction:.0%}, sifted={len(ak)}, QBER={qber:.3%}")
    return {"sifted_key_length": len(ak), "sifted_key_rate": float(np.mean(keep)), "qber": qber}
