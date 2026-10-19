# QKD Simulation: BB84, BBM92, Eavesdropping, and Channel Noise

**Problem:** Qiskit Fall Fest Hackathon, Track 5 / Problem 9 — Quantum Key Distribution.  
**Python:** 3.12.4 (tested locally by the project author).  
**Scope:** Educational simulation; not suitable for protecting real data.

## What this project does

- Simulates BB84 with basis sifting.
- Simulates BBM92 using entangled Bell pairs and basis sifting.
- Models an intercept-and-resend eavesdropper and compares QBER with the ideal reference `QBER = f/4`.
- Models a random non-identity Pauli error with probability `p`, compares the measured QBER with `2p/3`, and demonstrates an illustrative 11% abort threshold.
- Saves CSV results and figures in `results/` and `figures/`.

## Clean setup (Windows PowerShell)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, run commands with `.venv\Scripts\python.exe` instead of activating the environment.

## Reproduce the main results

From the repository root, run:

```powershell
python scripts/run_experiments.py
```

Expected output: `Experiments and figures saved.` The script writes three CSV files to `results/` and three PNG figures to `figures/`. It uses fixed per-trial seeds, runs 60 trials for each attack sweep (10 trials at each of six attack fractions), and 70 channel-noise trials (10 trials at each of seven noise probabilities). Runtime depends on hardware; on the author's setup the runner completed and saved the files.

Run tests:

```powershell
python -m pytest tests -v
```

The author observed **12 passing tests** in the development environment. Re-run tests after installation to verify your environment.

## Classical/theoretical reference and interpretation

The plotted reference curves are analytic statistical expectations: `QBER = f/4` for the idealized intercept-and-resend model and `QBER ≈ 2p/3` for the implemented random Pauli-error model. The simulations are also ordinary classical computations running quantum-circuit simulators; this project does **not** claim quantum speedup or quantum advantage. These reference curves validate expected model behavior, not a security proof.

## Limitations

This is an educational simulation, not a physical quantum communication experiment or a production QKD implementation. It studies one eavesdropping strategy and a simplified channel model. The 11% abort threshold is illustrative, not a universal security threshold. Full authenticated classical communication, error correction, privacy amplification, and finite-key security analysis are not implemented. Do not use this project to protect real data.
