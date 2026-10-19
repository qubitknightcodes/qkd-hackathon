import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def simulate_qkd(n_qubits=2000, pauli_error_probability=0.03, eve_fraction=0.0,
                 sample_fraction=0.20, qber_threshold=0.11, seed=42):
    if n_qubits < 1: raise ValueError("n_qubits must be positive")
    if not 0 <= pauli_error_probability <= 1: raise ValueError("Noise probability must be between 0 and 1")
    if not 0 <= eve_fraction <= 1: raise ValueError("eve_fraction must be between 0 and 1")
    if not 0 < sample_fraction < 1: raise ValueError("sample_fraction must be between 0 and 1")
    if not 0 <= qber_threshold <= 1: raise ValueError("QBER threshold must be between 0 and 1")
    rng = np.random.default_rng(seed); sim = AerSimulator()
    a = rng.integers(0, 2, n_qubits); ab = rng.integers(0, 2, n_qubits)
    bb = rng.integers(0, 2, n_qubits); attacked = rng.random(n_qubits) < eve_fraction
    eb = rng.integers(0, 2, n_qubits); e = np.zeros(n_qubits, dtype=int)
    ids = np.flatnonzero(attacked); ec = []
    for i in ids:
        qc = QuantumCircuit(1, 1)
        if a[i]: qc.x(0)
        if ab[i]: qc.h(0)
        if eb[i]: qc.h(0)
        qc.measure(0, 0); ec.append(qc)
    if ec:
        r = sim.run(ec, shots=1, seed_simulator=seed).result()
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
        if rng.random() < pauli_error_probability: getattr(qc, rng.choice(["x","y","z"]))(0)
        if bb[i]: qc.h(0)
        qc.measure(0, 0); circuits.append(qc)
    r = sim.run(circuits, shots=1, seed_simulator=seed+1).result()
    b = np.array([int(r.get_counts(i).most_frequent()) for i in range(n_qubits)])
    keep = ab == bb; ak, bk = a[keep], b[keep]
    if len(ak) < 2: raise RuntimeError("Too few sifted bits to estimate QBER")
    size = max(1, int(sample_fraction * len(ak)))
    sample = rng.choice(len(ak), size=size, replace=False)
    qber = float(np.mean(ak[sample] != bk[sample]))
    remain = np.ones(len(ak), dtype=bool); remain[sample] = False
    ca, cb = ak[remain], bk[remain]; accepted = qber <= qber_threshold
    print(f"Noise model: p={pauli_error_probability:.3f}, sample QBER={qber:.3%}, decision={'KEEP CANDIDATE' if accepted else 'ABORT'}")
    return {"sifted_length": len(ak), "sample_size": size, "estimated_qber": qber,
            "accepted": accepted, "candidate_length": len(ca),
            "candidate_keys_match": bool(np.array_equal(ca, cb))}
