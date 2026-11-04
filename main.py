from datetime import timedelta

from pydantic import ValidationError
from ligne_commande import LigneCommande
from contact import Contact
from commande import Commande
from produit import Produit


def sep(nombre=50):
    print("=" * nombre)


def afficher_erreurs(erreur,nombre=50):
    """Résume une ValidationError : une ligne par problème."""
    print(f"{erreur.error_count()} erreur(s) pour le modèle {erreur.title}")
    for err in erreur.errors():
        # loc est un tuple : on le transforme en chemin lisible
        champ = " → ".join(str(element) for element in err["loc"]) or "(modèle entier)"
        print(f"  ❌ {champ} : {err['msg']} [reçu : {err['input']!r}]")
    sep(nombre)


produit = Produit(reference="PX-55QT",nom="Clavier mécanique K70", prix="89.90", stock="34")
# produit = Produit(nom="Clavier mécanique K70", prix="89.90", stock="34")
try:
    produit2 = Produit(nom="Clavier simple", prix='9.90', stock="324")
    Produit(nom="Souris gamer RX-500", prix="gratuit", stock="41,6")
    # produit3 = Produit("Clavier simple", 9.90, 324)
except ValidationError as e:
    # print(e)
    afficher_erreurs(e)
    # for erreur in e.errors():
        # print(f"loc   : {erreur['loc']}")
        # print(f"msg   : {erreur['msg']}")
        # print(f"type  : {erreur['type']}")
        # print(f"input : {erreur['input']!r}")
        # print("="*50)
except TypeError as e:
    # print(e)
    afficher_erreurs(e)

print(produit)
sep()

try:
    Produit(prix="35,2", stock="41,6")
except ValidationError as e:
    afficher_erreurs(e)
except TypeError as e:
    afficher_erreurs(e)

sep()

try:
    Produit(prix=None, stock="41,6")
except ValidationError as e:
    afficher_erreurs(e)
except TypeError as e:
    afficher_erreurs(e)

sep()

try:
    Produit(prix=None, stock="23,18")
except ValidationError as e:
    afficher_erreurs(e)
except TypeError as e:
    afficher_erreurs(e)

sep()

# Les champs sont des attributs ordinaires
print(f"Nom : {produit.nom} | Prix : {produit.prix} € | Stock : {produit.stock} unités")
print(f"Valeur du stock : {produit.prix * produit.stock:.2f} €")


sep()

# Un dictionnaire comme on pourrait en recevoir d'un formulaire : le nom a été oublié
donnees_recues = {"prix": "cinquante-neuf", "stock": "beaucoup"}

try:
    Produit.model_validate(donnees_recues)
except ValidationError as e:
    # print(e)
    afficher_erreurs(e)
    # for erreur in e.errors():
    #     print(f"loc   : {erreur['loc']}")
    #     print(f"msg   : {erreur['msg']}")
    #     print(f"type  : {erreur['type']}")
    #     print(f"input : {erreur['input']!r}")
    #     print("=" * 50)

sep()

try:
    commande = Commande(
        id=91, 
        client={
            "prenom": "alice",
            "nom": "MARTIN",
            "email": "Alice.Martin@Example.com",
            "telephone": "0613454138",
            "ville": " lille ",
        }, 
        date_commande="2026-06-15", 
        enregistree_le="2026-06-15T14:32:00"
    )
    print(repr(commande.date_commande))
    # Ce sont de vraies dates : on peut en extraire des morceaux et faire des calculs
    print(f"Mois de la commande : {commande.date_commande.month}")
    print(f"Livraison prévue le : {commande.date_commande + timedelta(days=3)}")
    sep()
except ValidationError as e:
    afficher_erreurs(e)
except TypeError as e:
    afficher_erreurs(e)

# print(repr(commande.enregistree_le))


for texte in ["2026-02-30", "15/06/2026", "hier"]:
    try:
        Commande(id=92, date_commande=texte, enregistree_le="2026-06-15T14:32:00")
    except ValidationError as e:
        print(f"{texte!r:>13} → ❌ {e.errors()[0]['msg']}")
sep()


try:
    print(Commande(id=91, date_commande="2026-06-15"))
except ValidationError as e:
    afficher_erreurs(e)
except TypeError as e:
    afficher_erreurs(e)

try:
    print(Commande(id=92, date_commande="2026-06-16", statut="expédiée"))
    # print(Commande(id=93, statut="livrée"))
except ValidationError as e:
    afficher_erreurs(e)
except TypeError as e:
    afficher_erreurs(e)

try:
    Commande(id=93, statut="livrée")
except ValidationError as e:
    afficher_erreurs(e)
except TypeError as e:
    afficher_erreurs(e)

try:
    Commande(id=93, date_commande="2026-06-17", statut="perdue")
except ValidationError as e:
    afficher_erreurs(e)
try:
    Commande(id=93, statut="perdue")
except ValidationError as e:
    afficher_erreurs(e)


for adresse in [
    "alice.martin@example.com",
    "alice.martin@example",
    "alice.martin.example.com",
    "alice@@example.com",
]:
    try:
        contact = Contact(email=adresse)
        print(f"✅ {adresse}")
    except ValidationError as e:
        # print(f"❌ {adresse} → {e.errors()[0]['msg']}")
        afficher_erreurs(e)
# sep()

print(LigneCommande(produit_id=3, quantite=2, prix_unitaire="49.90"))

try:
    LigneCommande(produit_id=3, quantite=0, prix_unitaire="-49.90")
except ValidationError as e:
    afficher_erreurs(e)


try:
    Produit(nom="a", prix=None, stock="23,18")
except ValidationError as e:
    afficher_erreurs(e)
except TypeError as e:
    afficher_erreurs(e)


try:
    # Produit(nom="a", prix=None, stock="23,18")
    produit = Produit(reference="PX-55QT",nom="Clavier mécanique K70", prix="89.90", remise=100, stock="34")
except ValidationError as e:
    afficher_erreurs(e)
except TypeError as e:
    afficher_erreurs(e)

try:
    # Produit(nom="a", prix=None, stock="23,18")
    produit = Produit(reference="PX-55QT",nom="Clavier mécanique K70", prix="89.90", remise=100, stock="-34")
except ValidationError as e:
    afficher_erreurs(e)
except TypeError as e:
    afficher_erreurs(e)

try:
    # Produit(nom="a", prix=None, stock="23,18")
    produit = Produit(reference="PX-55QT",nom="Clavier mécanique K70", prix="89.90", remise=80, stock="34", nouveau_champ="azerty")
    print("Tout s'est bien passé")
    sep()
except ValidationError as e:
    afficher_erreurs(e)
except TypeError as e:
    afficher_erreurs(e)


try:
    Commande(id=93, statut="livrée", date_livraison="16/06/2026")
except ValidationError as e:
    afficher_erreurs(e)
except ValueError as e:
    afficher_erreurs(e)
except TypeError as e:
    afficher_erreurs(e)


ligne = LigneCommande(produit_id=5, quantite=3, prix_unitaire="19.90")
print(ligne)
print(f"Montant : {ligne.montant} €")

sep()


donnees_commande = {
    "id": 91,
    "client": {
        "prenom": "alice",
        "nom": "MARTIN",
        "email": "Alice.Martin@Example.com",
        "telephone": "0613454138",
        "ville": " lille ",
    },
    "date_commande": "2026-06-15",
    "lignes": [
        {"produit_id": 1, "quantite": 1, "prix_unitaire": "89.90"},
        {"produit_id": 5, "quantite": 2, "prix_unitaire": "19.90"},
    ],
}

commande = Commande.model_validate(donnees_commande)

print(f"Client  : {commande.client.prenom} {commande.client.nom} ({commande.client.ville})")
print(f"Contact : {commande.client.email} | {commande.client.telephone}")
sep(25)
for ligne in commande.lignes:
    print(f"  - produit n°{ligne.produit_id} : {ligne.quantite} x {ligne.prix_unitaire} € = {ligne.montant} €")
print(f"Total   : {commande.total} €")
sep(25)
print(commande)

sep()
sep()

donnees_invalides = {
    "id": 92,
    "client": {
        "prenom": "Bastien", 
        "nom": "Dupont", 
        "email": "bastien.dupont[at]example.com", 
        "ville": "Paris"
    },
    "date_commande": "2026-06-16",
    "statut": "en préparation",
    "lignes": [
        {"produit_id": 3, "quantite": 1, "prix_unitaire": "49.90"},
        {"produit_id": 12, "quantite": 0, "prix_unitaire": "79.90"},
        {"produit_id": 17, "quantite": 1},
    ],
}

try:
    Commande.model_validate(donnees_invalides)
except ValidationError as e:
    afficher_erreurs(e,25)
    print("loc brut de la dernière erreur :", e.errors()[-1]["loc"])

sep()
sep()

donnees_plates = commande.model_dump(mode="json")
print(donnees_plates)
sep()
donnees_json = commande.model_dump_json(indent=2)
print(donnees_json)
sep()

# Écriture...
with open("pydantic_commande.json", "w", encoding="utf-8") as fichier:
    fichier.write(donnees_json)

with open("pydantic_commande.json", encoding="utf-8") as fichier:
    try:
        commande_relue = Commande.model_validate_json(fichier.read())
    except ValidationError as e:
        afficher_erreurs(e)
    except ValueError as e:
        afficher_erreurs(e)
    except TypeError as e:
        afficher_erreurs(e)

print(type(commande_relue.date_commande), type(commande_relue.lignes[0].prix_unitaire))
print(f"Identique à l'originale ? {commande_relue == commande}")