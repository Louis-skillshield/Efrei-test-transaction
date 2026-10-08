from src.create_connexion import get_connection
from exercice.velo_utils import print_velo


def run_e4_concurrence(should_lock, abonne_id=42, velo_id=9):
    """E4 : deux abonnés veulent le même vélo au même moment.

    À lancer dans DEUX terminaux en même temps (voir le README).

    Sans verrou : que se passe-t-il si les deux terminaux lisent
    'disponible' avant que l'un des deux ait loué ?

    Avec verrou (SELECT ... FOR UPDATE) : le premier terminal "réserve" la
    ligne du vélo jusqu'à la fin de sa transaction.
    """
    with get_connection() as connection:
        connection.autocommit = True
        try:
            # TODO 1 : ouvrir la transaction et un curseur
            # TODO 2 : SELECT station_id, etat du vélo
            #          -> ajouter " FOR UPDATE" à la requête si should_lock est vrai
            #          puis afficher ce qui a été lu
            # TODO 3 : faire une pause pour laisser l'autre terminal arriver ici :
            #          input("  >>> Fais pareil dans l'autre terminal, "
            #                "puis appuie sur Entrée ici...")
            # TODO 4 : si etat != 'disponible' -> raise ValueError("trop tard ...")
            # TODO 5 : UPDATE du vélo + INSERT du trajet (comme en E2)
            raise NotImplementedError("E4 : location concurrente")
            print(f"  COMMIT : vous avez le vélo {velo_id} !")
        except ValueError as error:
            print(f"  ROLLBACK : {error}")

        with connection.cursor() as cursor:
            print_velo(cursor, velo_id, "après")
