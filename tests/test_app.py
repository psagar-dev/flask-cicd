import pytest
from app import app

@pytest.fixture
def client():
    # flask provides a test client for your app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_status_code(client):
    """GET / should return HTTP 200."""
    response = client.get('/')
    assert response.status_code == 200

def test_home_content(client):
    """GET / should include our greeting."""
    response = client.get('/')
    assert b"Hello, Flask!" in response.data

def test_404(client):
    """Unknown routes should return 404."""
    resp = client.get('/does-not-exist')
    assert resp.status_code == 404