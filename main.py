from src.create_connexion import get_connection


def run_start_trajet(abonne_id, velo_id):

    with get_connection() as connection:
        connection.autocommit = True  # indispensable !

        with connection.transaction():  # BEGIN
            with connection.cursor() as cursor:
                # On récupère la station du vélo AVANT de la mettre à NULL
                # (FOR UPDATE verrouille la ligne pendant la transaction)
                cursor.execute(
                    "SELECT station_id, etat FROM velo "
                    "WHERE id = %s FOR UPDATE;",
                    (velo_id,),
                )
                row = cursor.fetchone()
                if row is None:
                    raise ValueError(f"Vélo {velo_id} introuvable")
                station_depart_id, etat = row
                # Un vélo déjà en trajet n'a plus de station : on refuse
                if etat != "disponible":
                    raise ValueError(
                        f"Vélo {velo_id} non disponible (état : {etat})"
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


def main():

    run_start_trajet(abonne_id=1, velo_id=1)


if __name__ == "__main__":

    main()
