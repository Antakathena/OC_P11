import json
from GUDLFTapp import create_app

if __name__ == "__main__":

    # On récupère les clubs et compétitions fournis dans les json (pas de db pour l'instant):
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

    # On utilise l'app factory qui se trouve dans le "__init__" du dossier GUDLFTapp :
    app = create_app(clubs, competitions)
    # (Si besoin de mapper les urls : print(app.url_map))

    # On lance :
    app.run(debug=True)  # change when debug is done


