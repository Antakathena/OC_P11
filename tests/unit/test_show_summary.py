import pytest


def test_should_status_code_ok(client, good_club, clubs):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/show-summary' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.post('/show-summary', data={'clubs': clubs, "email": good_club['email']})
    assert response.status_code == 200


def test_find_club(client, clubs):
    """
    GIVEN a club
    WHEN the club's email is given as input
    THEN check the email field is defined correctly,
    recognize the emails present in the json as ok,
    send an error message if the email is incorrect.
    ( show summary is an integration test)
    """
    club = clubs[0]
    response = client.post('/show-summary', data={"email": "john@simplylift.co"})
    data = response.data.decode()
    assert club['name'] in data


@pytest.mark.xfail(reason="debug not implemented")
def test_email_unknown(client):
    """
    GIVEN an unknown club
    WHEN the club's email is given as input
    THEN check the email field is defined correctly,
    send an error message if the email is incorrect.
    """
    response = client.post('/show-summary', data={"email": "unknown@test.com"})
    assert response.status_code == 301  # redirection vers template
    assert response.headers['Location'] == "/index"  # ou url_for(index)
