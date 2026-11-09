import requests
from rich import print
from core.utils import sep
from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas.ville_schema import VilleSchema
from models.ville import Ville

def print_ville(ville):
    if ville is not None:
        print(
            f"{ville.nom} ({ville.id})"
        )

def coordonnees_ville(http_session,nom:str):
    """Permet de récupérer les coordonnées d'un ville

    Args:
        nom (str): nom de la ville
    """
    try:
        geo = http_session.get("https://geocoding-api.open-meteo.com/v1/search",
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


def localise_villes(http_session, villes):
    with http_session:
        http_session.headers.update({
            "User-Agent": "api_meteo/1.0",
            "Accept": "application/json",
        })

        liste_coordonnes = []
        for ville in villes:
            sep()
            print(f"Ville: {ville}")
            sep()

            coords = coordonnees_ville(http_session,ville)
            if coords is None:
                # print("Une erreur s'est produite")
                continue
            else:
                liste_coordonnes.append(coords)
        return liste_coordonnes


def chercher_ville(session: Session, ville):
    requete = select(Ville).where(Ville.nom == ville.nom)
    ville_recu = session.scalar(requete)
    print_ville(ville_recu)
    return ville_recu

def inserer_ville(session: Session, ville):
    coordonnees = VilleSchema.model_validate(ville)
    
    result = chercher_ville(session,coordonnees)

    if result is None:
        coor = coordonnees.model_dump()
        ville_actuelle = Ville(**coor)
        session.add(ville_actuelle)
        session.commit()
        print_ville(ville_actuelle)
        return ville_actuelle
    else:
        print_ville(result)
        return result
