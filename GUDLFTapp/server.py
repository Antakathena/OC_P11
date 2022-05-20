import os
import json
from flask import (
    current_app,
    Blueprint,
    flash,
    Flask,
    g,
    redirect,
    render_template,
    request,
    url_for
)

bp = Blueprint('bp', __name__, url_prefix='/')


@bp.before_request
def get_clubs_and_competitions():
    g.competitions = current_app.config['competitions']
    g.clubs = current_app.config['clubs']


@bp.route('/')
# au lieu de @app.route('/'), changé pour tout
def index():
    """accueil et invitation à se logger"""
    return render_template('/index.html')
    # return render_template(current_app.config['index.html'])
    # current app sert à y acceder malgré la app factory


@bp.route('/show-summary', methods=['POST'])
def show_summary():
    club = [club for club in g.clubs if club['email'] == request.form['email']][0]
    return render_template('/welcome.html', club=club, competitions=g.competitions)
    # return render_template(current_app.config['welcome.html'], club=club, competitions=competitions)


@bp.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = [c for c in g.clubs if c['name'] == club][0]
    found_competition = [c for c in g.competitions if c['name'] == competition][0]
    if found_club and found_competition:
        return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('/welcome.html', club=club, competitions=g.competitions)
        # return render_template(current_app.config['welcome.html'], club=club, competitions=competitions)


@bp.route('/purchase-places', methods=['POST'])
def purchase_places():
    competition = [c for c in g.competitions if c['name'] == request.form['competition']][0]
    club = [c for c in g.clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
    flash('Great-booking complete!')
    return render_template('/welcome.html', club=club, competitions=g.competitions)
    # return render_template(current_app.config['welcome.html'], club=club, competitions=competitions)


#@bp.route('/show-points-board', defaults={'clubs': clubs}, methods=['GET'])
@bp.route('/show-points-board', methods=['GET'])
# TODO: Add route for points display
# CORRECTIF >>> FEATURE : implement points board display -> vue ci-dessous + template (points.html)
def show_points_board():
    return render_template('/points.html', clubs=g.clubs)
    # return render_template(current_app.config['points.html'], clubs=clubs)


@bp.route('/logout')
def logout():
    return redirect(url_for('.index'))

# fin de l'app factory :
# return app
