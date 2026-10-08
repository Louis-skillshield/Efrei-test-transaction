from src.create_connexion import get_connection
from exercice.velo_utils import print_velo


def run_e3_retour(velo_id=8, station_arrivee_id=12):
    """E3 : rendre un vélo = 2 requêtes, dans une transaction.

      1. UPDATE du vélo : il redevient 'disponible' dans la station d'arrivée
      2. UPDATE du trajet en cours : on note la station et l'heure d'arrivée

    Si aucun trajet n'était en cours (cursor.rowcount == 0), le retour n'a
    aucun sens : on lève une exception pour annuler aussi l'UPDATE du vélo.
    """
    with get_connection() as connection:
        connection.autocommit = True

        with connection.cursor() as cursor:
            print_velo(cursor, velo_id, "avant")

        try:
            # TODO 1 : ouvrir la transaction et un curseur (comme en E2)
            # TODO 2 : UPDATE du vélo -> etat 'disponible', station_id = station_arrivee_id
            #          puis afficher "UPDATE du vélo OK (pas encore enregistré)"
            # TODO 3 : UPDATE du trajet en cours de ce vélo (arrivee_le IS NULL)
            #          -> station_arrivee_id et arrivee_le = NOW()
            # TODO 4 : si cursor.rowcount == 0 -> raise ValueError("...")
            raise NotImplementedError("E3 : retour du vélo")
            print("  COMMIT automatique : vélo rendu")
        except ValueError as error:
            print(f"  ROLLBACK automatique : {error}")

        with connection.cursor() as cursor:
            print_velo(cursor, velo_id, "après")
