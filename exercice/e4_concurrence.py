from src.create_connexion import get_connection
from exercice.velo_utils import print_velo


def run_e4_concurrence(should_lock, abonne_id=42, velo_id=9):
    """E4 : deux abonnés veulent le même vélo au même moment.

    À lancer dans DEUX terminaux en même temps (voir le README).

    Sans verrou : les deux terminaux lisent 'disponible', les deux louent
    -> 2 trajets ouverts pour un seul vélo, même avec une transaction !

    Avec verrou (SELECT ... FOR UPDATE) : le premier terminal "réserve" la
    ligne du vélo. Le second reste bloqué sur son SELECT jusqu'au COMMIT du
    premier, puis lit 'en_trajet' et abandonne.
    """
    lock_clause = " FOR UPDATE" if should_lock else ""

    with get_connection() as connection:
        connection.autocommit = True
        try:
            with connection.transaction():
                with connection.cursor() as cursor:
                    print(f"  SELECT{lock_clause} sur le vélo {velo_id}...")
                    if should_lock:
                        print("  (si ça bloque ici, l'autre terminal tient le verrou)")
                    cursor.execute(
                        "SELECT station_id, etat FROM velo "
                        f"WHERE id = %s{lock_clause};",
                        (velo_id,),
                    )
                    station_depart_id, etat = cursor.fetchone()
                    print(f"  Lu : etat={etat}, station={station_depart_id}")

                    input(
                        "  >>> Fais pareil dans l'autre terminal, "
                        "puis appuie sur Entrée ici..."
                    )

                    if etat != "disponible":
                        raise ValueError(f"trop tard, vélo {velo_id} déjà pris")

                    cursor.execute(
                        "UPDATE velo SET etat = 'en_trajet', "
                        "station_id = NULL WHERE id = %s;",
                        (velo_id,),
                    )
                    cursor.execute(
                        "INSERT INTO trajet (abonne_id, velo_id, "
                        "station_depart_id, depart_le) "
                        "VALUES (%s, %s, %s, NOW());",
                        (abonne_id, velo_id, station_depart_id),
                    )
            print(f"  COMMIT : vous avez le vélo {velo_id} !")
        except ValueError as error:
            print(f"  ROLLBACK : {error}")

        with connection.cursor() as cursor:
            print_velo(cursor, velo_id, "après")
