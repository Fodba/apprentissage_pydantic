from rich import print
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from models.releve import Releve
from models.ville import Ville

def compter_releves(session: Session, ville):
    requete = select(func.count(Releve.id)).where(Releve.ville_id == ville.id)
    result = session.scalar(requete)
    print(f"nombre de relevé: {result}")
    return result


def temperature_min(session: Session, ville):
    requete = select(func.min(Releve.temperature)).where(Releve.ville_id == ville.id)
    result = session.scalar(requete)
    print(f"température min: {result}")
    return result


def temperature_max(session: Session, ville):
    requete = select(func.max(Releve.temperature)).where(Releve.ville_id == ville.id)
    result = session.scalar(requete)
    print(f"température max: {result}")
    return result


def temperature_moyenne(session: Session, ville):
    requete = select(func.avg(Releve.temperature)).where(Releve.ville_id == ville.id)
    result = session.scalar(requete)
    print(f"température moyenne: {result}")
    return result


def stats_temperature(session: Session):
    requete = select(
        Ville.nom,
        func.count(Releve.id),
        func.min(Releve.temperature),
        func.max(Releve.temperature),
        func.avg(Releve.temperature)
    ).group_by(Ville.nom).join(Ville)
    result = session.execute(requete).all()
    # print(f"stats temperature: {result}")
    return result

def afficher_stats(stats):
    for ligne in stats:
        print(
            f"Ville: {ligne[0]}\n"
            f"nombre de relevé(s): {ligne[1]}\n"
            f"Température minimale: {ligne[2]}\n"
            f"Température maximale: {ligne[3]}\n"
            f"température moyenne: {ligne[4]}\n"
        )
