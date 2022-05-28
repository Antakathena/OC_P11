from datetime import datetime
from flask import (
    current_app,
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for
)

bp = Blueprint('bp', __name__, url_prefix='/')


@bp.before_request
def get_clubs_and_competitions():
    """Récupère dans les blueprints les competitions et clubs.
    L'app s'articule entre server.py, init (app factory) et run.py
    Hors tests, les clubs et compétitions sont récupérés au moment du lancement
    dans run.py par les fonctions load_clubs et load_competitions"""
    g.competitions = current_app.config['competitions']
    g.clubs = current_app.config['clubs']


@bp.route('/')
def index():
    """Accueil et invitation à se logger
    NB : l'email entré est traité dans show_summary"""
    return render_template('/index.html')


@bp.route('/show-summary', methods=['POST'])
def show_summary():
    """Calendrier des compétitions
    Doit afficher le calendrier des compétitions et
    le nombre de points du club connecté si l'email entré est bon.
    """
    try:
        club = [club for club in g.clubs if club['email'] == request.form['email']][0]
        return render_template('/welcome.html', club=club, competitions=g.competitions)
    except IndexError:
        flash("Unknown Club, please try again", 'error')
        return redirect(url_for('bp.index'))


@bp.route('/book/<competition>/<club>')
def book(competition, club):
    """Vérifications avant achat de places
    Vérifie que le club est bien trouvé, ainsi que la compétition
    Vérifie que la compétition choisie n'est pas passée
    """
    try:
        found_club = [c for c in g.clubs if c['name'] == club][0]
        found_competition = [c for c in g.competitions if c['name'] == competition][0]

        # On vérifie que la date de competition est à venir, sinon : message explicite
        if datetime.strptime(found_competition['date'], "%Y-%m-%d %H:%M:%S") < datetime.now():
            flash("This competition is past, you cannot book places", 'error')
            return redirect(url_for("bp.index"))
            # TODO : améliorer ou supprimer commentaire
            # index pour parer au 405 not allowed, pb = show_summary est en POST, data = email
            # on peut récupérer la data dans la session et ajouter au url_for pour rester connecté?

        if found_club and found_competition:
            return render_template('booking.html', club=found_club, competition=found_competition)

    except IndexError:
        flash("Club or competition not found. Something went wrong-please try again", 'error')
        return render_template('/welcome.html', club=club, competitions=g.competitions)
    except Exception as e:
        print(e)
        flash("Something went wrong-please try again", 'error')
        return render_template('/welcome.html', club=club, competitions=g.competitions)


@bp.route('/purchase-places', methods=['POST'])
def purchase_places():
    """Achat de places avec les points du club
    Soit 1 point = 1 place en compétition
    Doit d'abord s'assurer que les places demandées ne sont pas supérieures :
    - aux points disponibles pour le club,
    - aux places disponibles pour la compétition,
    - à 12 places par club pour une compétition
    Enfin,
    Les points et places disponibles doivent être modifiés en fonction de l'achat qui a été réalisé.
    """
    # only allow places required >= 1, except value error
    try:
        competition = [c for c in g.competitions if c['name'] == request.form['competition']][0]
        club = [c for c in g.clubs if c['name'] == request.form['club']][0]
        places_required = int(request.form['places'])
        if places_required < 1:
            raise ValueError
    except (ValueError, IndexError):
        flash("Enter a number between 1 and your allowed possibility of booking (3 club-point = 1 place)")
        return render_template('welcome.html', club=club, competitions=g.competitions)

    # clubs should not be able to book more than 12 places per competition
    if places_required > 12:
        flash("A club cannot purchase more than 12 places in a competition")
        return render_template('welcome.html', club=club, competitions=g.competitions)

    # no more places than available in this competition
    if places_required > int(competition['numberOfPlaces']):
        flash("There is not so many places available for this competition")
        return render_template('welcome.html', club=club, competitions=g.competitions)

    # clubs should not be able to book more than their allowed points
    necessary_points = places_required * 3
    club_points = int(club['points'])
    if necessary_points >= club_points:
        flash("According to your points, your club cannot book so many places")
        return render_template('welcome.html', club=club, competitions=g.competitions)

    # competition places and points update after purchase (1 place = 3 points)
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
    club['points'] = int(club['points']) - places_required * 3
    flash('Great-booking complete!')
    return render_template('/welcome.html', club=club, competitions=g.competitions)


@bp.route('/show-points-board', methods=['GET'])
def show_points_board():
    """Présente le nombre de point de chaque club sans avoir besoin d'être connecté"""
    return render_template('/points.html', clubs=g.clubs)


@bp.route('/logout')
def logout():
    """Déconnection, redirection vers l'accueil"""
    return redirect(url_for('.index'))
