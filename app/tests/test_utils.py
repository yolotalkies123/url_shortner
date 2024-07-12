# tests/test_utils.py
from app.utils import generate_short_key

def test_generate_short_key():
    short_key = generate_short_key()
    assert len(short_key) == 6
    assert all(char.isalnum() for char in short_key)

    short_key = generate_short_key(length=8)
    assert len(short_key) == 8
    assert all(char.isalnum() for char in short_key)
