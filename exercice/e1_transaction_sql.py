import psycopg

from src.create_connexion import get_connection
from exercice.velo_utils import print_velo


def run_e1_location_transaction_sql(abonne_id=42, velo_id=3, station_id=2):
    """E1 : la même location, mais dans une transaction écrite à la main.

    BEGIN    -> on ouvre la transaction, rien n'est encore enregistré
    COMMIT   -> tout a marché : on enregistre TOUT d'un coup
    ROLLBACK -> une requête a planté : on annule TOUT, comme si rien n'avait eu lieu

    autocommit = True : psycopg n'ouvre aucune transaction tout seul,
    c'est donc nous qui écrivons BEGIN et COMMIT.
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
                print("  UPDATE du vélo OK (pas encore enregistré)")
                cursor.execute(
                    "INSERT INTO trajet (abonne_id, velo_id, "
                    "station_depart_id, depart_le) "
                    "VALUES (%s, %s, %s, NOW());",
                    (abonne_id, velo_id, station_id),
                )
                print("  INSERT du trajet OK (pas encore enregistré)")
                cursor.execute("COMMIT;")
                print("  COMMIT : tout est enregistré")
            except psycopg.Error as error:
                cursor.execute("ROLLBACK;")
                print(f"  ERREUR : {type(error).__name__}")
                print("  ROLLBACK : l'UPDATE du vélo est annulé lui aussi")

            print_velo(cursor, velo_id, "après")
