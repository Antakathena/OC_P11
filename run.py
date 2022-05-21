import json
from GUDLFTapp import create_app

if __name__ == "__main__":

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

    app = create_app(clubs, competitions)
    print(app.url_map)
    print(competitions)
    print(clubs)  # a retirer à la fin
    app.run(debug=True)  # change when debug is done


