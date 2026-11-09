from pydantic import ValidationError
import requests
from rich import print
from sqlalchemy import select
from schemas.weather_response import WeatherResponseModel
from schemas.releve_schema import ReleveSchema
from core.utils import afficher_erreurs
from sqlalchemy.orm import Session
from models.releve import Releve


def donnees_meteo(http_session, parametres):
    """Permet de récupérer des données météo

    Args:
        parametres (dict): dictionnaire des paramètres à envoyer avec la requête
    """
    try:
        link = "https://api.open-meteo.com/v1/forecast"
        response = http_session.get(link, params=parametres, timeout=(3, 15))
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


def chercher_releve_precis(session: Session, releve, ville):
    """vérifie si un relevé existe déjà en base"""
    requete = (
        select(Releve)
        .where(Releve.ville_id == ville.id)
        .where(Releve.date_heure == releve.date_heure)
    )
    releve_recu = session.scalar(requete)
    return releve_recu


def lister_releves(session: Session, ville):
    """liste les relevés d'une ville"""
    requete = (
        select(Releve).where(Releve.ville_id == ville.id).order_by(Releve.date_heure)
    )
    releve_recu = session.scalars(requete).all()
    return releve_recu


def inserer_releve(session: Session, releve, ville):
    """insère le relevé d'une ville dans la base données"""
    try:
        donnees_releve = WeatherResponseModel.model_validate_json(releve)
    except ValidationError as ve:
        afficher_erreurs(ve)
        return None

    releve_actuel = donnees_releve.model_dump()["current_weather"]
    releve_temp = ReleveSchema.model_validate(releve_actuel)
    result = chercher_releve_precis(session, releve_temp, ville)
    if result is None:
        releve_dict = releve_temp.model_dump()
        releve_dict["ville_id"] = ville.id

        releve = Releve(**releve_dict)

        session.add(releve)
        session.commit()
        return releve
    else:
        return result
