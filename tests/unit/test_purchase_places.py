import pytest


def test_should_status_code_ok(client, good_club, good_competition):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/purchase-places' page is requested (POST)
    THEN check that the response is valid
    """
    response = client.post(
        '/purchase-places',
        data={
            'competition': good_competition['name'],
            'club': good_club['name'],
            'places': '5',
        }
    )
    content = response.data.decode()
    assert 'Great-booking complete' in content
    assert response.status_code == 200


@pytest.mark.xfail(reason="not implemented")
def test_limit_purchase_to_12places(client, good_club, good_competition):
    """
    GIVEN a connected user (club) and a booking just made
    WHEN the '/purchase-places' page is requested (POST)
    THEN show actualised informations regarding this club (points)
    and competitions
    """
    response = client.post(
        '/purchase-places',
        data={
            'competition': good_competition['name'],
            'club': good_club['name'],
            "places": "13"
        }
    )
    data = response.data.decode()  # on retire .decode() si on utilise b'
    assert 'A club cannot use more than 12 points on a competition' in data
    # b' = octets'


@pytest.mark.xfail(reason="debug not implemented")
def test_limit_purchase_to_available_places(client, good_club, few_places_competition):
    # CORRECTIF A FAIRE >>> BUG : clubs should not be able to book more than remaining places
    response = client.post(
        '/purchase-places', data={
            'competition': few_places_competition['name'], 'club': good_club['name'], "places": "10"})
    places_required = "10"
    available_places = few_places_competition['numberOfPlaces']
    total = int(available_places) - int(places_required)
    data = response.data.decode()
    assert available_places < places_required, f'places disponibles :{available_places},demandées :{places_required},' \
                                               f' number of places - required places would be = {total}'
    assert 'There is not so many places available for this competition' in data,\
        f'message given: impossible to book.'


@pytest.mark.xfail(reason="debug not implemented")
def test_limit_purchase_according_to_points(client, less_points_club, good_competition):
    # CORRECTIF A FAIRE >>> BUG : clubs should not be able to book more than their allowed points
    response = client.post(
        '/purchase-places', data={
            'competition': good_competition['name'], 'club': less_points_club['name'], "places": "10"})
    club_points = less_points_club['points']
    places_required = "10"
    total = int(club_points) - int(places_required)
    data = response.data.decode()
    assert club_points < places_required, f'le nombre de places demandées dépasse de {total} les points disponibles'
    assert 'According to your points, your club cannot book so many places' in data, \
        f'message given: impossible to book.'


@pytest.mark.xfail(reason="debug not implemented")
def test_reflect_purchase_on_points(good_club, good_competition):
    club = good_club
    competition = good_competition
    assert club['points'] == "8"
    assert competition['numberOfPlaces'] == "20"
