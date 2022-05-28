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
            'places': '1',
        }
    )
    content = response.data.decode()
    assert 'Great-booking complete!' in content, content
    assert response.status_code == 200, content


def test_limit_purchase_to_12places(client, many_points_club, good_competition):
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
            'club': many_points_club['name'],
            "places": "13"
        }
    )
    content = response.data.decode()  # on retire ".decode()" si on utilise b'(b' = octets')
    assert 'A club cannot purchase more than 12 places in a competition' in content


def test_limit_value(client, good_club, good_competition):
    """
    GIVEN a connected user (club) and a booking just made
    WHEN the user tries to purchase 0 or fewer places
    THEN an error message appears
    """
    response = client.post(
        '/purchase-places',
        data={
            'competition': good_competition['name'],
            'club': good_club['name'],
            "places": "0"
        }
    )
    content = response.data.decode()  # on retire ".decode()" si on utilise b'(b' = octets')
    assert 'Enter a number between 1 and your allowed possibility of booking (3 club-point = 1 place)' in content


def test_limit_purchase_to_available_places(client, good_club, few_places_competition):
    """clubs should not be able to book more than remaining places"""
    response = client.post(
        '/purchase-places', data={
            'competition': few_places_competition['name'], 'club': good_club['name'], "places": "10"})
    places_required = "3"
    available_places = few_places_competition['numberOfPlaces']
    total = int(available_places) - int(places_required)
    content = response.data.decode()
    assert available_places < places_required, f'places disponibles :{available_places},demandées :{places_required},' \
                                               f' number of places - required places would be = {total}'
    assert 'There is not so many places available for this competition' in content,\
        f'message given: impossible to book.'


def test_limit_purchase_according_to_points(client, less_points_club, good_competition):
    """1 place = 3 points; clubs should not be able to book more than their allowed points"""
    response = client.post(
        '/purchase-places',
        data={
            'competition': good_competition['name'],
            'club': less_points_club['name'],
            'places': '2'
        }
    )
    club_points = less_points_club['points']
    places_required = "2"
    total = int(club_points) - int(places_required)*3
    content = response.data.decode()
    assert 'According to your points, your club cannot book so many places' in content, \
        f'message given: impossible to book, {total} points more needed than possessed.'


def test_reflect_purchase_on_points(client, good_club, good_competition):
    """club_points - purchased places
    1 place = 3 points. After purchasing places,
    the club points should be diminished by the required places * 3
     """
    response = client.post(
        '/purchase-places',
        data={
            'competition': good_competition['name'],
            'club': good_club['name'],
            'places': '2'
        }
    )
    content = response.data.decode()

    # 2 places = 6 points donc 13 (good club points) - 6 : club['points'] == "7"
    assert "Points available for Simply Lift: 7" in content

    # good_competition has 25 places available - 2 : competition['numberOfPlaces']== "23"
    assert "Number of Places: 23" in content
