#test_utils.py

import pytest
from routers.auth import verify_password, get_password_hash

def test_verify_password():
    password = "testpassword"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password) == True
    assert verify_password("wrongpassword", hashed_password) == False
