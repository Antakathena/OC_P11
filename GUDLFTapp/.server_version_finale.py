import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

def page_not_found(e):
    return render_template('404.html'), 404

def create_app(config_filename):
    """Facilite les tests. App factory qui englobe toute l'app :
     https://flask.palletsprojects.com/en/2.1.x/patterns/appfactories/"""
    app = Flask(__name__)
    app.secret_key = 'something_special'
    app.config.from_pyfile('config_filename')
    app.register_error_handler(404, page_not_found)
    # impl when app factory is used : https://flask.palletsprojects.com/en/1.0.x/patterns/errorpages/

    def load_clubs():
        with open('GUDLFTapp/clubs.json') as c:
            list_of_clubs = json.load(c)['clubs']
            return list_of_clubs


    def load_competitions():
        with open('GUDLFTapp/competitions.json') as comps:
            list_of_competitions = json.load(comps)['competitions']
            return list_of_competitions


    competitions = load_competitions()
    clubs = load_clubs()

    @bp.route('/')
    # au lieu de @app.route('/'), changé pour tout
    def index():
        """Accueil et invitation à se logger
        NB : l'email entré est traité dans show_summary"""
        return render_template('/index.html')

    @bp.route('/show-summary', methods=['POST'])
    # BUGFIX >>> ERROR : entering an unknown email crashes the app -> add try except
    def show_summary():
        """calendrier des compétitions
        Doit afficher le calendrier des compétitions et
        le nombre de points du club connecté si l'email entré est bon
        """
        try:
            club = [club for club in g.clubs if club['email'] == request.form['email']][0]
            return render_template('/welcome.html', club=club, competitions=g.competitions)
        except IndexError:
            flash("Unknown Club, please try again")
            return redirect(url_for(index.__name__))


    @app.route('/book/<competition>/<club>')
    # CORRECTIF A FAIRE >>> BUG : Booking places in past competitions -> don't allow
    def book(competition, club):
        found_club = [c for c in clubs if c['name'] == club][0]
        found_competition = [c for c in competitions if c['name'] == competition][0]

        # if date de la competition < now : message d'erreur explicite-------------------------------------------------
        if found_competition['date'] < datetime.today():
            flash("This competition is past")
            return redirect(url_for("bp.show_summary"))
        elif found_club and found_competition:
            return render_template('booking.html', club=found_club, competition=found_competition)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions)
      # -----------------------------------------------------------------------------------------------------------


    @app.route('/purchase-places', methods=['POST'])
    def purchase_places():
        # bug en plus si on ne saisi rien = value error--------------------------------------------------------------
        try:
            competition = [c for c in competitions if c['name'] == request.form['competition']][0]
            club = [c for c in clubs if c['name'] == request.form['club']][0]
            clubpoints = club['points']
            places_required = int(request.form['places'])
        except (ValueError, IndexError):
            flash("Enter a number between 1 and your allowed possibility of booking (1 club-point = 1 place)")
            return render_template('welcome.html', club=club, competitions=competitions)

        # CORRECTIF A FAIRE >>> BUG : clubs should not be able to book more than 12 places per competition
        # si places_required > 12 (au total) per competition : message "non pas possible"
        if places_required > 12 :
            flash("A club cannot use more than 12 points on a competition")
            return render_template('welcome.html', club=club, competitions=competitions)

        # CORRECTIF : pas plus de place que de dispos dans la compet
        if places_required > competition['numberOfPlaces']:
            flash("There is not so many places available for this competition")
            return render_template('welcome.html', club=club, competitions=competitions)

        # CORRECTIF A FAIRE >>> BUG : clubs should not be able to book more than their allowed points
        # si places_required > nbr de clubpoints : message "non pas possible"
        necessary_points = places_required * 3
        if necessary_points >= clubpoints :
            flash("According to your points, your club cannot book so many places")
            return render_template('welcome.html', club=club, competitions=competitions)

        # CORRECTIF A FAIRE >>> BUG : points update are not reflected
        # nombre de points = nombre de points - places required
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
        club['points']= int(club['points']) - places_required * 3
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)
        #----------------------------------------------------------------------------------------------------------



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

