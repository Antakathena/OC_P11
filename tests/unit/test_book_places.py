from datetime import datetime


def test_should_status_code_ok(client, good_club, good_competition):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/book/<competition>/<club>' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get(f"/book/{good_competition['name']}/{good_club['name']}")
    assert response.status_code == 200, f"/book/{good_competition['name']}/{good_club['name']}"


def test_find_club_and_competition(client, good_club, good_competition):
    """
    GIVEN a connected user (club) and a competition
    WHEN the ''/book/<competition>/<club>' page is requested (GET)
    THEN show informations regarding this club (points)
    and this competition
    """
    club = good_club
    competition = good_competition
    response = client.get(f"/book/{good_competition['name']}/{good_club['name']}")
    # response = client.post('/show-summary', data={"email": "john@simplylift.co"})
    content = response.data.decode()
    assert club['name'] in content
    assert competition['name'] in content


def test_something_went_wrong(client, bad_club, good_competition):
    """
    GIVEN a bad piece of information
    WHEN the ''/book/<competition>/<club>' page is requested (GET)
    THEN we have a message and go back
    """
    response = client.get(f"/book/{good_competition['name']}/{bad_club['name']}")
    content = response.data.decode()
    assert "Something went wrong-please try again" in content, f'{response.status_code}, {response.headers["Location"]}'


def test_no_booking_for_past_competitions(client, good_club, past_competition):
    """
    GIVEN a connected user (club) and a competition
    WHEN the ''/book/<competition>/<club>' page is requested (GET)
    THEN show a message like "no booking for past competitions"
    """
    response = client.get(f"/book/{past_competition['name']}/{good_club['name']}")
    assert response.status_code == 302  # redirection 302 FOUND
    assert response.headers['Location'] == 'http://localhost/'  # (index)
