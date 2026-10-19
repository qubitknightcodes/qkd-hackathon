import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def run_bb84(n_qubits=1000, seed=42):
    if n_qubits < 1: raise ValueError("n_qubits must be positive")
    rng = np.random.default_rng(seed)
    sim = AerSimulator()
    a_bits = rng.integers(0, 2, n_qubits)
    a_basis = rng.integers(0, 2, n_qubits)
    b_basis = rng.integers(0, 2, n_qubits)
    circuits = []
    for i in range(n_qubits):
        qc = QuantumCircuit(1, 1)
        if a_bits[i]: qc.x(0)
        if a_basis[i]: qc.h(0)
        if b_basis[i]: qc.h(0)
        qc.measure(0, 0)
        circuits.append(qc)
    res = sim.run(circuits, shots=1, seed_simulator=seed).result()
    b_bits = np.array([int(res.get_counts(i).most_frequent()) for i in range(n_qubits)])
    keep = a_basis == b_basis
    ak, bk = a_bits[keep], b_bits[keep]
    qber = float(np.mean(ak != bk)) if len(ak) else 0.0
    print(f"BB84: transmitted={n_qubits}, sifted={len(ak)}, rate={np.mean(keep):.3f}, QBER={qber:.3%}")
    assert np.array_equal(ak, bk)
    return {"alice_key": ak, "bob_key": bk, "sifted_key_rate": float(np.mean(keep)),
            "qber": qber, "sifted_key_length": len(ak)}

if __name__ == "__main__":
    run_bb84()
