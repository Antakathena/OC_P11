
def test_should_status_code_ok(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/show-points-board' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/show-points-board')
    assert response.status_code == 200


def test_should_return_points_board(client, clubs):
    """
    GIVEN a connected or unconnected user and a list of clubs(name, email, points)
    WHEN the '/show-points-board' page is requested (GET)
    THEN points of each club should be shown
    """
    club = clubs[0]
    response = client.get('/show-points-board')
    data = response.data.decode()
    assert club['name'] in data
    assert club['points'] in data





