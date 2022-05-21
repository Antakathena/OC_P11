import pytest
from GUDLFTapp import create_app
# package = GUDLFT
# module = server
# function = create_app


@pytest.fixture
def app(clubs, competitions):
    app = create_app(clubs, competitions)
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture
def client(app):
    # with flask_app.test_client() as test_client:
    # response = test_client.get('/index')
    return app.test_client()


# ça je ne sais pas à quoi ça sert mais c'est dans la doc:
@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def good_club():
    club = {
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": "13"
    }
    yield club


@pytest.fixture
def bad_club():
    bad_club = {
        "name": "anonymus",
        "email": "noone@test.co",
        "points": "0"
    }
    yield bad_club


@pytest.fixture
def less_points_club():
    club = {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
    }
    yield club


@pytest.fixture()
def clubs():
    clubs = [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        }
    ]
    yield clubs


@pytest.fixture()
def competitions():
    competitions = [
            {
                "name": "Spring Festival",
                "date": "2023-03-27 10:00:00",
                "numberOfPlaces": "25"
            },
            {
                "name": "Fall Classic",
                "date": "2023-10-22 13:30:00",
                "numberOfPlaces": "13"
            },
            {
                "name": "Festival with few places",
                "date": "2023-03-27 10:00:00",
                "numberOfPlaces": "8"
            },
            {
                "name": "Festival fini",
                "date": "2020-03-27 10:00:00",
                "numberOfPlaces": "25"
            }
        ]
    yield competitions


@pytest.fixture()
def past_competition():
    competition = {
        "name": "Festival fini",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "25"
    }
    yield competition


@pytest.fixture()
def good_competition():
    competition = {
            "name": "Spring Festival",
            "date": "2023-03-27 10:00:00",
            "numberOfPlaces": "25"
    }
    yield competition


@pytest.fixture()
def few_places_competition():
    competition = {
        "name": "Festival with few places",
        "date": "2023-03-27 10:00:00",
        "numberOfPlaces": "8"
    }
    yield competition
