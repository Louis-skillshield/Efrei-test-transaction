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
            with connection.transaction():
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE velo SET etat = 'disponible', station_id = %s "
                        "WHERE id = %s;",
                        (station_arrivee_id, velo_id),
                    )
                    print("  UPDATE du vélo OK (pas encore enregistré)")
                    cursor.execute(
                        "UPDATE trajet SET station_arrivee_id = %s, "
                        "arrivee_le = NOW() "
                        "WHERE velo_id = %s AND arrivee_le IS NULL;",
                        (station_arrivee_id, velo_id),
                    )
                    # rowcount = nombre de lignes modifiées par la dernière requête
                    if cursor.rowcount == 0:
                        raise ValueError(f"aucun trajet en cours pour le vélo {velo_id}")
            print("  COMMIT automatique : vélo rendu")
        except ValueError as error:
            print(f"  ROLLBACK automatique : {error}")

        with connection.cursor() as cursor:
            print_velo(cursor, velo_id, "après")
