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


@bp.route('/book/<competition>/<club>')
def book(competition, club):
    """Vérifications avant achat de places
    Vérifie que le club est bien trouvé, ainsi que la compétition
    Vérifie que la compétition choisie n'est pas passée
    Pourrait vérifier que la compétition a encore des places disponibles
    ou que le club a des points
    """
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
    # return render_template(current_app.config['welcome.html'], club=club, competitions=competitions)


@bp.route('/show-points-board', methods=['GET'])
# TODO: Add route for points display
# CORRECTIF >>> FEATURE : implement points board display -> vue ci-dessous + template (points.html)
def show_points_board():
    """Présente le nombre de point de chaque club sans avoir besoin d'être connecté"""
    return render_template('/points.html', clubs=g.clubs)
    # return render_template(current_app.config['points.html'], clubs=clubs)


@bp.route('/logout')
def logout():
    """Déconnection, redirection vers l'accueil"""
    return redirect(url_for('.index'))

# fin de l'app factory :
# return app
