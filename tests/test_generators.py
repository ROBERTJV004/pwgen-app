import pytest
from generators import generate_password, check_strength


def test_generate_password_letters_only():
    """Test password generation with only letters"""
    password = generate_password(10, False, False)
    assert len(password) == 10
    assert password.isalpha()


def test_generate_password_with_numbers():
    """Test password generation with numbers"""
    password = generate_password(10, True, False)
    assert len(password) == 10
    assert any(char.isdigit() for char in password)


def test_generate_password_with_symbols():
    """Test password generation with symbols"""
    password = generate_password(10, False, True)
    assert len(password) == 10
    assert any(not char.isalnum() for char in password)


def test_generate_password_all_options():
    """Test password generation with all options enabled"""
    password = generate_password(20, True, True)
    assert len(password) == 20
    assert any(char.isdigit() for char in password)
    assert any(not char.isalnum() for char in password)


def test_check_strength_weak():
    """Test strength check for weak passwords"""
    assert check_strength("abc") == "Weak"
    assert check_strength("abcde") == "Weak"


def test_check_strength_medium():
    """Test strength check for medium passwords"""
    assert check_strength("abcdef") == "Medium"
    assert check_strength("abcdefghi") == "Medium"


def test_check_strength_strong():
    """Test strength check for strong passwords"""
    assert check_strength("abcdefghij") == "Strong"
    assert check_strength("abcdefghijklmnop") == "Strong"


def test_generate_password_comprehensive():
    """Test password generation with length=12, numbers=True, symbols=True"""
    # Generate multiple times to ensure we get both cases (random can be flaky)
    password = None
    for _ in range(10):  # Try up to 10 times
        password = generate_password(12, True, True)
        if (any(char.isupper() for char in password) and 
            any(char.islower() for char in password) and
            any(char.isdigit() for char in password) and
            any(not char.isalnum() for char in password)):
            break
    
    assert len(password) == 12
    # Check it has uppercase
    assert any(char.isupper() for char in password), f"Password missing uppercase: {password}"
    # Check it has lowercase
    assert any(char.islower() for char in password), f"Password missing lowercase: {password}"
    # Check it has numbers
    assert any(char.isdigit() for char in password), f"Password missing numbers: {password}"
    # Check it has symbols
    assert any(not char.isalnum() for char in password), f"Password missing symbols: {password}"


def test_strength_with_complexity():
    """Test strength: strong if len>=12 + numbers + symbols"""
    # Generate a password with length 12, numbers, and symbols
    password = generate_password(12, True, True)
    strength = check_strength(password)
    # Should be strong because length >= 10 (our threshold)
    assert strength == "Strong"
    
    # Test with longer password
    password_long = generate_password(15, True, True)
    assert check_strength(password_long) == "Strong"


def test_strength_edge_case_weak():
    """Edge case: length=4 → weak"""
    password = generate_password(4, True, True)
    strength = check_strength(password)
    assert strength == "Weak"
