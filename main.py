from datetime import timedelta

from pydantic import ValidationError
from ligne_commande import LigneCommande
from contact import Contact
from commande import Commande
from produit import Produit


def sep():
    print("=" * 50)


def afficher_erreurs(erreur):
    """Résume une ValidationError : une ligne par problème."""
    print(f"{erreur.error_count()} erreur(s) pour le modèle {erreur.title}")
    for err in erreur.errors():
        # loc est un tuple : on le transforme en chemin lisible
        champ = " → ".join(str(element) for element in err["loc"]) or "(modèle entier)"
        print(f"  ❌ {champ} : {err['msg']} [reçu : {err['input']!r}]")
    sep()


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

commande = Commande(
    id=91, date_commande="2026-06-15", enregistree_le="2026-06-15T14:32:00"
)

print(repr(commande.date_commande))
print(repr(commande.enregistree_le))

# Ce sont de vraies dates : on peut en extraire des morceaux et faire des calculs
print(f"Mois de la commande : {commande.date_commande.month}")
print(f"Livraison prévue le : {commande.date_commande + timedelta(days=3)}")
sep()

for texte in ["2026-02-30", "15/06/2026", "hier"]:
    try:
        Commande(id=92, date_commande=texte, enregistree_le="2026-06-15T14:32:00")
    except ValidationError as e:
        print(f"{texte!r:>13} → ❌ {e.errors()[0]['msg']}")
sep()


print(Commande(id=91, date_commande="2026-06-15"))
print(Commande(id=92, date_commande="2026-06-16", statut="expédiée"))
print(Commande(id=93, statut="livrée"))

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
