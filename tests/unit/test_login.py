
def test_should_status_code_ok(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/')
    assert response.status_code == 200


def test_should_invite_login(client):
    response = client.get('/')
    data = response.data.decode()
    assert "Please enter your secretary email to continue:" in data



