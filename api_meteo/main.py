# https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&current_weather=true

import requests
from services.releve_service import donnees_meteo, inserer_releve
from services.ville_service import coordonnees_ville, inserer_ville
from core.database import Base, engine, SessionLocal
from core.utils import sep
from services.stats_service import (
    afficher_stats,
    stats_temperature,
)  # , compter_releves, temperature_max, temperature_min, temperature_moyenne

from rich import print

if __name__ == "__main__":

    engine.echo = True
    Base.metadata.create_all(engine)
    engine.echo = False

    villes = [
        "Paris",
        "new-yoRk",
        "Lyon",
        "Lille",
        "Marseille",
        "Aix-en-Provence",
        "Saint-Quentin",
        "Amiens",
    ]

    with SessionLocal() as ma_session_bdd:
        with requests.Session() as session:
            session.headers.update(
                {
                    "User-Agent": "api_meteo/1.0",
                    "Accept": "application/json",
                }
            )

            for ville in villes:
                sep()
                print(f"Ville: {ville}")
                sep()

                coords = coordonnees_ville(session, ville)
                if coords is None:
                    # print("Une erreur s'est produite")
                    continue
                # print(coords)

                ville_insere = inserer_ville(ma_session_bdd, coords)

                params = {
                    "latitude": ville_insere.latitude,
                    "longitude": ville_insere.longitude,
                    "current_weather": True,
                }
                data = donnees_meteo(session, params)
                # print(data)
                if data is None:
                    continue
                inserer_releve(ma_session_bdd, data, ville_insere)

                # compter_releves(ma_session_bdd,ville_insere)
                # temperature_min(ma_session_bdd,ville_insere)
                # temperature_max(ma_session_bdd,ville_insere)
                # temperature_moyenne(ma_session_bdd,ville_insere)
        stats = stats_temperature(ma_session_bdd)
        afficher_stats(stats)
