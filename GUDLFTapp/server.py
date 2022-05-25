from datetime import datetime
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
    """récupère dans les blueprints les competitions et clubs.
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
    """calendrier des compétitions
    Doit afficher le calendrier des compétitions et
    le nombre de points du club connecté si l'email entré est bon
    """
    try:
        club = [club for club in g.clubs if club['email'] == request.form['email']][0]
        return render_template('/welcome.html', club=club, competitions=g.competitions)
    except IndexError:
        flash("Unknown Club, please try again", 'error')
        return redirect(url_for('bp.index'))


@bp.route('/book/<competition>/<club>')
# CORRECT >>> BUG : Booking places in past competitions -> don't allow
def book(competition, club):
    """Vérifications avant achat de places
    Vérifie que le club est bien trouvé, ainsi que la compétition
    Vérifie que la compétition choisie n'est pas passée
    Pourrait vérifier que la compétition a encore des places disponibles
    ou que le club a des points
    """
    found_club = [c for c in g.clubs if c['name'] == club][0]
    found_competition = [c for c in g.competitions if c['name'] == competition][0]

    # if date de la competition < now : message d'erreur explicite
    try:
        # on vérifie que la date de compet est à venir
        if datetime.strptime(found_competition['date'], "%Y-%m-%d %H:%M:%S") < datetime.now():
            flash("This competition is past, you cannot book places", 'error')
            return redirect(url_for("bp.index"))
            # index pour parer au 405 not allowed, pb = show_summary est en POST, data = email
            # on peut récupérer la data dans la session et ajouter au url_for pour rester connecté?
    except Exception as e:
        print(e)

    if found_club and found_competition:
        return render_template('booking.html', club=found_club, competition=found_competition)
    else:
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
    competition = [c for c in g.competitions if c['name'] == request.form['competition']][0]
    club = [c for c in g.clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
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
