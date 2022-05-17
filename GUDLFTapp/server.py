import os
import json
from flask import Flask, render_template, request, redirect, flash, url_for


def page_not_found(e):
    return render_template('404.html'), 404


def create_app(clubs_infos=None, competitions_infos=None, test_config=None):
    """Facilite les tests. App factory qui englobe toute l'app :
     https://flask.palletsprojects.com/en/2.1.x/patterns/appfactories/"""
    app = Flask(__name__)  # l'ajout de , instance_relative_config=True fait qu'il ne trouve plus config(?)
    app.config.from_pyfile('../config.py')
    app.register_error_handler(404, page_not_found)
    # impl when app factory is used : https://flask.palletsprojects.com/en/1.0.x/patterns/errorpages/
    app.secret_key = 'something_special'
    # je peux changer pour suivre : https://www.youtube.com/watch?v=6c_utRUzHG4
    # mais il faudrait mieux comprendre les concepts
    # app.config.from_mapping(
    #      SECRET_KEY='development'
    # )
    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('../config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)
    #
    # # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    def load_clubs(clubs_infos):
        if clubs_infos == None:
            with open('GUDLFTapp/clubs.json') as c:
                list_of_clubs = json.load(c)['clubs']
        else:
            list_of_clubs = clubs_infos
        return list_of_clubs

    def load_competitions(competitions_infos):
        if competitions_infos == None:
            with open('GUDLFTapp/competitions.json') as comps:
                list_of_competitions = json.load(comps)['competitions']
        else:
            list_of_competitions = competitions_infos
        return list_of_competitions

    competitions = load_competitions(competitions_infos)
    clubs = load_clubs(clubs_infos)


    @app.route('/')
    def index():
        """login"""
        # on pourrait le rebaptiser login?
        return render_template('index.html')

    @app.route('/showSummary', methods=['POST'])
    def show_summary():
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions)

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        found_club = [c for c in clubs if c['name'] == club][0]
        found_competition = [c for c in competitions if c['name'] == competition][0]
        if found_club and found_competition:
            return render_template('booking.html', club=found_club, competition=found_competition)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions)

    @app.route('/purchasePlaces', methods=['POST'])
    def purchase_places():
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        places_required = int(request.form['places'])
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)

    @app.route('/show-points-board', methods=['GET'])
    # TODO: Add route for points display
    # CORRECTIF >>> FEATURE : implement points board display -> vue ci-dessous + template (points.html)
    def show_points_board():
        return render_template('points.html', clubs=clubs)

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    # fin de l'app factory :
    return app