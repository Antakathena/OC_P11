def test_should_status_code_ok(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/logout')
    assert response.status_code == 302  # redirection 302 FOUND
    assert response.headers['Location'] == 'http://localhost/'  # (index)

