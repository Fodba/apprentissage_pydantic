

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