from src.create_connexion import get_connection
from exercice.velo_utils import print_velo


def run_t1_location(abonne_id=42, velo_id=1, station_id=5):
    """T1 : location en SQL "brut" avec BEGIN / COMMIT écrits à la main."""
    with get_connection() as connection:
        # autocommit = True : psycopg n'ouvre pas de transaction tout seul,
        # c'est nous qui écrivons BEGIN et COMMIT
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
                print(f"  ROLLBACK : {error}")

            print_velo(cursor, velo_id, "après")
