from src.create_connexion import get_connection


def run_t5_concurrence(abonne_id=42, velo_id=8):
    """T5 : deux terminaux veulent le même vélo en même temps.

    Lancez `uv run python main.py t5` dans deux terminaux.
    Le premier verrouille le vélo (FOR UPDATE) et attend Entrée.
    Le second reste bloqué sur son SELECT tant que le premier
    n'a pas fait COMMIT, puis voit le vélo déjà en trajet.
    """
    with get_connection() as connection:
        connection.autocommit = True
        try:
            with connection.transaction():
                with connection.cursor() as cursor:
                    print(f"  SELECT ... FOR UPDATE sur le vélo {velo_id}...")
                    print("  (si ça bloque ici, l'autre terminal a le verrou)")
                    cursor.execute(
                        "SELECT station_id, etat FROM velo "
                        "WHERE id = %s FOR UPDATE;",
                        (velo_id,),
                    )
                    station_depart_id, etat = cursor.fetchone()
                    print(f"  Verrou obtenu : etat={etat}, station={station_depart_id}")

                    if etat != "disponible":
                        raise ValueError(
                            f"Trop tard, vélo {velo_id} déjà pris (état : {etat})"
                        )

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
                    input(
                        "  Location prête, verrou tenu. "
                        "Lance l'autre terminal puis appuie sur Entrée pour COMMIT..."
                    )
            print(f"  COMMIT : vous avez le vélo {velo_id} !")
        except Exception as error:
            print(f"  ROLLBACK : {error}")
