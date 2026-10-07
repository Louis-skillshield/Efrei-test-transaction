from src.create_connexion import get_connection
from exercice.velo_utils import print_velo


def run_t2_station_inexistante(abonne_id=42, velo_id=2, station_id=9999):
    """T2 : même location, mais depuis une station qui n'existe pas.

    L'INSERT viole la clé étrangère trajet -> station : la transaction
    est annulée, y compris l'UPDATE du vélo qui avait pourtant réussi.
    """
    with get_connection() as connection:
        connection.autocommit = True
        with connection.cursor() as cursor:
            print_velo(cursor, velo_id, "avant")

            cursor.execute("BEGIN;")
            try:
                cursor.execute(
                    "UPDATE velo SET etat = 'en_trajet', station_id = NULL "
                    "WHERE id = %s;",
                    (velo_id,),
                )
                print("  UPDATE du vélo OK (pas encore validé)")
                cursor.execute(
                    "INSERT INTO trajet (abonne_id, velo_id, "
                    "station_depart_id, depart_le) "
                    "VALUES (%s, %s, %s, NOW());",
                    (abonne_id, velo_id, station_id),
                )
                cursor.execute("COMMIT;")
                print("  COMMIT effectué")
            except Exception as error:
                cursor.execute("ROLLBACK;")
                print(f"  ERREUR : {type(error).__name__}")
                print(f"  {error}")
                print("  ROLLBACK effectué")

            print_velo(cursor, velo_id, "après")
