from src.bbm92 import run_bbm92

def test_bbm92_ideal_key_matches():
    assert run_bbm92(1000, 0.0, 201)["qber"] == 0.0

def test_bbm92_sifting_rate_is_approximately_half():
    assert 0.43 < run_bbm92(2000, 0.0, 202)["sifted_key_rate"] < 0.57

def test_bbm92_full_eavesdropping():
    assert 0.19 < run_bbm92(4000, 1.0, 203)["qber"] < 0.31

def test_bbm92_no_eavesdropping():
    assert run_bbm92(2000, 0.0, 204)["qber"] == 0.0
