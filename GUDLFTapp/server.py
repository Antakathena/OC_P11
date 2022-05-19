import os
import json
from flask import (
    current_app,
    Blueprint,
    flash,
    Flask,
    redirect,
    render_template,
    request,
    url_for
)

bp = Blueprint('bp', __name__, url_prefix='/')


@bp.route('/')
# au lieu de @app.route('/'), changé pour tout
def index():
    """accueil et invitation à se logger"""
    return render_template('/index.html')
    # return render_template(current_app.config['index.html'])
    # current app sert à y acceder malgré la app factory


@bp.route('/showSummary', methods=['POST'])
def show_summary(clubs, competitions):
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('/welcome.html', club=club, competitions=competitions)
    # return render_template(current_app.config['welcome.html'], club=club, competitions=competitions)


@bp.route('/book/<competition>/<club>')
def book(competition, club, clubs, competitions):
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]
    if found_club and found_competition:
        return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('/welcome.html', club=club, competitions=competitions)
        # return render_template(current_app.config['welcome.html'], club=club, competitions=competitions)


@bp.route('/purchasePlaces', methods=['POST'])
def purchase_places(clubs, competitions):
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
    flash('Great-booking complete!')
    return render_template('/welcome.html', club=club, competitions=competitions)
    # return render_template(current_app.config['welcome.html'], club=club, competitions=competitions)


#@bp.route('/show-points-board', defaults={'clubs': clubs}, methods=['GET'])
@bp.route('/show-points-board', methods=['GET'])
# TODO: Add route for points display
# CORRECTIF >>> FEATURE : implement points board display -> vue ci-dessous + template (points.html)
def show_points_board(clubs):
    return render_template('/points.html', clubs=clubs)
    # return render_template(current_app.config['points.html'], clubs=clubs)


@bp.route('/logout')
def logout():
    return redirect(url_for('.index'))

# fin de l'app factory :
# return app
