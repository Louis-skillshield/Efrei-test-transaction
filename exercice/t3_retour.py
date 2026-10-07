from src.create_connexion import get_connection
from exercice.velo_utils import print_velo


def run_t3_retour(velo_id=1, station_arrivee_id=12):
    """T3 : retour du vélo, on termine le trajet et on gare le vélo."""
    with get_connection() as connection:
        connection.autocommit = True
        with connection.cursor() as cursor:
            print_velo(cursor, velo_id, "avant")

            cursor.execute("BEGIN;")
            try:
                cursor.execute(
                    "UPDATE trajet SET station_arrivee_id = %s, "
                    "arrivee_le = NOW() "
                    "WHERE velo_id = %s AND arrivee_le IS NULL;",
                    (station_arrivee_id, velo_id),
                )
                if cursor.rowcount == 0:
                    raise ValueError(f"Aucun trajet en cours pour le vélo {velo_id}")
                cursor.execute(
                    "UPDATE velo SET etat = 'disponible', station_id = %s "
                    "WHERE id = %s;",
                    (station_arrivee_id, velo_id),
                )
                cursor.execute("COMMIT;")
                print("  COMMIT effectué")
            except Exception as error:
                cursor.execute("ROLLBACK;")
                print(f"  ROLLBACK : {error}")

            print_velo(cursor, velo_id, "après")
