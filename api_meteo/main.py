# https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&current_weather=true


from pydantic import ValidationError
import requests
from weather_response import WeatherResponseModel

from rich import print




def sep(nombre=50):
    """ajoute une ligne permettant de séparer les sorties console

    Args:
        nombre (int, optional): nombre de "=" à afficher. Defaults to 50.
    """
    print("=" * nombre)



def afficher_erreurs(erreur,nombre=50):
    """Résume une ValidationError : une ligne par problème."""
    print(f"{erreur.error_count()} erreur(s) pour le modèle {erreur.title}")
    for err in erreur.errors():
        # loc est un tuple : on le transforme en chemin lisible
        champ = " → ".join(str(element) for element in err["loc"]) or "(modèle entier)"
        print(f"  ❌ {champ} : {err['msg']} [reçu : {err['input']!r}]")
    sep(nombre)

def coordonnees_villes(session,nom:str):
    """Permet de récupérer les coordonnées d'un ville

    Args:
        nom (str): nom de la ville
    """
    try:
        geo = session.get("https://geocoding-api.open-meteo.com/v1/search",
                params={"name": nom, "count": 1, "language": "fr"},
                timeout=(3, 10))
        geo.raise_for_status()
        geolocalisation = geo.json()
        if geolocalisation.get("results"):
            loc = geolocalisation["results"][0]
            return loc
        else:
            print(f"La ville '{nom}' n'est pas référencée")
            return None
    except requests.exceptions.Timeout as te:
        print(f"ville: {nom} - {te}")
        return None
    except requests.exceptions.ConnectionError as ce:
        print(f"ville: {nom} - {ce}")
        return None
    except requests.exceptions.HTTPError as he:
        print(f"ville: {nom} - {he}")
        return None
    except requests.exceptions.RequestException as re:
        print(f"ville: {nom} - {re}")
        return None

def donnes_meteo(session,parametres):
    """Permet de récupérer des données météo

    Args:
        parametres (dict): dictionnaire des paramètres à envoyer avec la requête
    """
    try:
        link = "https://api.open-meteo.com/v1/forecast"
        response = session.get(link, params=parametres, timeout=(3,15))
        response.raise_for_status()
        return response.text
    except requests.exceptions.Timeout as te:
        print(te)
        return None
    except requests.exceptions.ConnectionError as ce:
        print(ce)
        return None
    except requests.exceptions.HTTPError as he:
        print(he)
        return None
    except requests.exceptions.RequestException as re:
        print(re)
        return None










if __name__ == "__main__":
    villes = ["Paris","Lilltftre","Saint-Quentin","Amiens"]

    with requests.Session() as session:
        session.headers.update({
            "User-Agent": "api_meteo/1.0",
            "Accept": "application/json",
        })

        for ville in villes:
            sep()
            print(f"Ville: {ville}")
            sep()

            coords = coordonnees_villes(session,ville)
            if coords is None:
                # print("Une erreur s'est produite")
                continue
            
            params = {
                "latitude": coords['latitude'],
                "longitude": coords['longitude'],
                "current_weather": True
            }
            data = donnes_meteo(session,params)
            if data is None:
                continue

            try:
                new_response = WeatherResponseModel.model_validate_json(data)
                print(new_response.model_dump_json())
            except ValidationError as ve:
                afficher_erreurs(ve)




    # link = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"

    # response = requests.get(link)
    # print(response.text)



    # ma_connection = Connection_bdd("ma_bdd.db")
    # # connecter_bdd("ma_bdd.db")

    # # conn = sqlite3.connect("ma_base.db")
    # # cursor = conn.cursor()
    # sep()

    # tables = ma_connection.execute_requete(
    #     # "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    #     "SELECT name FROM sqlite_master;"
    # )
    # # tables = ma_connection.cursor.fetchall()

    # print(tables)
    # # for table in tables:
    # #   print(table[0])
    # sep()
    # ma_connection.connection.close()

