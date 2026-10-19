import pytest
from src.noise_model import simulate_qkd

def test_noise_free_channel():
    r = simulate_qkd(1000, 0.0, 0.0, 0.20, 0.11, 301)
    assert r["estimated_qber"] == 0.0 and r["accepted"] and r["candidate_keys_match"]

def test_invalid_eve_fraction():
    with pytest.raises(ValueError): simulate_qkd(eve_fraction=1.5)

def test_invalid_noise_probability():
    with pytest.raises(ValueError): simulate_qkd(pauli_error_probability=-0.1)

def test_high_sample_qber_aborts():
    r = simulate_qkd(3000, 0.0, 1.0, 0.50, 0.05, 302)
    assert r["estimated_qber"] > 0.05 and r["accepted"] is False
