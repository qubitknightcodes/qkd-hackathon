import numpy as np
from src.bb84 import run_bb84
from src.eavesdropper import run_bb84_with_eve

def test_bb84_ideal_key_matches():
    r = run_bb84(1000, 101)
    assert r["qber"] == 0.0 and np.array_equal(r["alice_key"], r["bob_key"])

def test_bb84_sifting_rate_is_approximately_half():
    assert 0.43 < run_bb84(2000, 102)["sifted_key_rate"] < 0.57

def test_bb84_full_eavesdropping():
    assert 0.19 < run_bb84_with_eve(4000, 1.0, 103)["qber"] < 0.31

def test_bb84_no_eavesdropping():
    assert run_bb84_with_eve(2000, 0.0, 104)["qber"] == 0.0
