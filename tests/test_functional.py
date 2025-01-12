import pytest
from main import app, db, Users
from datetime import datetime
import bcrypt

@pytest.fixture
def client():
    # Configure the app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
        db.drop_all()

def add_test_user():
    # Add a test user to the database
    hashed_password = bcrypt.hashpw(b'password123', bcrypt.gensalt()).decode('utf-8')
    user = Users(
        UserName="testuser",
        Password=hashed_password,
        Email="testuser@example.com",
        Name="Test User",
        DOB=datetime(1995, 1, 1),
        Role="Tester",
        PhoneNumber="1234567890"
    )
    db.session.add(user)
    db.session.commit()

def test_add_user(client):
    # Test adding a user
    response = client.post('/add_user', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123',
        'dob': '1995-01-01',
        'role': 'Admin',
        'phone_number': '0987654321'
    })
    assert response.status_code == 201
    assert b'User added successfully!' in response.data

def test_login_success(client):
    # Add a user for testing login
    with app.app_context():
        add_test_user()

    # Test successful login
    response = client.post('/', data={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert b'Successfully logged in to your account!' in response.data

def test_login_failure(client):
    # Test login with incorrect credentials
    response = client.post('/', data={
        'username': 'wronguser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 302  # Redirect to login
    assert b'Wrong password. Please try again.' not in response.data
