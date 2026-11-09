from rich import print
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from models.releve import Releve
from models.ville import Ville

def compter_releves(session: Session, ville):
    """compte le nombre de relevé d'une ville"""
    requete = select(func.count(Releve.id)).where(Releve.ville_id == ville.id)
    result = session.scalar(requete)
    print(f"nombre de relevé: {result}")
    return result


def temperature_min(session: Session, ville):
    """donne la temperature minimale relevée pour une ville"""
    requete = select(func.min(Releve.temperature)).where(Releve.ville_id == ville.id)
    result = session.scalar(requete)
    print(f"température min: {result}")
    return result


def temperature_max(session: Session, ville):
    """donne la temperature maximale relevée pour une ville"""
    requete = select(func.max(Releve.temperature)).where(Releve.ville_id == ville.id)
    result = session.scalar(requete)
    print(f"température max: {result}")
    return result


def temperature_moyenne(session: Session, ville):
    """donne la temperature moyenne relevée pour une ville"""
    requete = select(func.avg(Releve.temperature)).where(Releve.ville_id == ville.id)
    result = session.scalar(requete)
    print(f"température moyenne: {result}")
    return result


def stats_temperature(session: Session):
    """Renvoie toutes les stats des relevé, regroupées par ville"""
    requete = select(
        Ville.nom,
        func.count(Releve.id).label("releves"),
        func.min(Releve.temperature).label("minimum"),
        func.max(Releve.temperature).label("maximum"),
        func.avg(Releve.temperature).label("moyenne")
    ).group_by(Ville.nom).join(Ville)
    result = session.execute(requete).all()
    return result

def afficher_stats(stats):
    """affiche les stats dans la console"""
    for ligne in stats:
        print(
            f"Ville: {ligne.nom}\n"
            f"nombre de relevé(s): {ligne.releves}\n"
            f"Température minimale: {ligne.minimum}\n"
            f"Température maximale: {ligne.maximum}\n"
            f"température moyenne: {ligne.moyenne}\n"
        )
