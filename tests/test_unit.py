import pytest
from main import Users
from datetime import datetime

# Unit test for the Users model
@pytest.fixture
def test_user():
    return Users(
        UserName="testuser",
        Password="hashedpassword",
        Email="testuser@example.com",
        Name="Test User",
        DOB=datetime(1995, 1, 1),
        Role="Tester",
        PhoneNumber="1234567890"
    )

def test_user_creation(test_user):
    assert test_user.UserName == "testuser"
    assert test_user.Password == "hashedpassword"
    assert test_user.Email == "testuser@example.com"
    assert test_user.Name == "Test User"
    assert test_user.DOB == datetime(1995, 1, 1)
    assert test_user.Role == "Tester"
    assert test_user.PhoneNumber == "1234567890"
