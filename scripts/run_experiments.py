import csv, io, sys
from contextlib import redirect_stdout
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from src.eavesdropper import run_bb84_with_eve
from src.bbm92 import run_bbm92
from src.noise_model import simulate_qkd
R=ROOT/"results"; F=ROOT/"figures"; R.mkdir(exist_ok=True); F.mkdir(exist_ok=True)
def quiet(fn, **kw):
    with redirect_stdout(io.StringIO()): return fn(**kw)
def save(path, rows):
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
def sweep(protocol):
    fn=run_bb84_with_eve if protocol=="BB84" else run_bbm92
    nk="n_qubits" if protocol=="BB84" else "n_pairs"
    ak="attack_fraction" if protocol=="BB84" else "eve_fraction"
    rows=[]; fs=np.linspace(0,1,6)
    for j,f in enumerate(fs):
        for t in range(10):
            seed=10000+j*10+t
            o=quiet(fn,**{nk:2000,ak:float(f),"seed":seed})
            rows.append({"protocol":protocol,"attack_fraction":float(f),"trial":t+1,"seed":seed,
                "transmissions":2000,"sifted_key_length":o["sifted_key_length"],
                "sifted_key_rate":o["sifted_key_rate"],"qber":o["qber"],"theoretical_qber":float(f/4)})
    save(R/f"{protocol.lower()}_eve_results.csv",rows)
    means=[]; stds=[]
    for f in fs:
        v=[x["qber"] for x in rows if x["attack_fraction"]==f]
        means.append(np.mean(v)); stds.append(np.std(v,ddof=1))
    plt.figure(figsize=(8,5)); plt.errorbar(fs,means,yerr=stds,fmt="o-",capsize=4,label="Simulation (mean ± SD)")
    plt.plot(fs,fs/4,"--",label="Ideal prediction: QBER = f/4")
    plt.xlabel("Fraction of transmissions attacked by Eve"); plt.ylabel("QBER")
    plt.title(f"{protocol}: Intercept-and-Resend Attack"); plt.grid(True,alpha=.3); plt.legend(); plt.tight_layout()
    plt.savefig(F/f"{protocol.lower()}_eve_comparison.png",dpi=300); plt.close()
def noise():
    rows=[]; levels=np.linspace(0,.15,7)
    for j,p in enumerate(levels):
        for t in range(10):
            seed=20000+j*10+t
            o=quiet(simulate_qkd,n_qubits=2000,pauli_error_probability=float(p),eve_fraction=0,
                    sample_fraction=.30,qber_threshold=.11,seed=seed)
            rows.append({"noise_probability":float(p),"trial":t+1,"seed":seed,"transmissions":2000,
                "sample_size":o["sample_size"],"estimated_qber":o["estimated_qber"],
                "theoretical_qber":float(2*p/3),"threshold":.11,
                "decision":"KEEP CANDIDATE" if o["accepted"] else "ABORT"})
    save(R/"channel_noise_results.csv",rows)
    means=[]; stds=[]
    for p in levels:
        v=[x["estimated_qber"] for x in rows if x["noise_probability"]==p]
        means.append(np.mean(v)); stds.append(np.std(v,ddof=1))
    plt.figure(figsize=(8,5)); plt.errorbar(levels,means,yerr=stds,fmt="o-",capsize=4,label="Estimated QBER (mean ± SD)")
    plt.plot(levels,2*levels/3,"--",label="Ideal expectation: 2p/3"); plt.axhline(.11,linestyle=":",label="Illustrative 11% threshold")
    plt.xlabel("Probability of a non-identity Pauli error"); plt.ylabel("Estimated QBER")
    plt.title("BB84: Channel Noise and Parameter Estimation"); plt.grid(True,alpha=.3); plt.legend(); plt.tight_layout()
    plt.savefig(F/"channel_noise_comparison.png",dpi=300); plt.close()
if __name__=="__main__":
    sweep("BB84"); sweep("BBM92"); noise(); print("Experiments and figures saved.")
