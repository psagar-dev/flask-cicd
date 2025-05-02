from app import app

def test_home_route():
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200
    assert b"Hello, Flask CI/CD!" in response.data