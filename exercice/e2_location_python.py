from src.create_connexion import get_connection
from exercice.velo_utils import print_velo


def run_e2_location(abonne_id=42, velo_id=8):
    """E2 : la location avec `with connection.transaction()`.

    Le bloc with fait le travail de E1 à notre place :
      - en entrant          -> BEGIN
      - sortie normale      -> COMMIT
      - exception levée     -> ROLLBACK automatique

    On en profite pour vérifier une règle métier : on ne loue qu'un vélo
    'disponible'. Si ce n'est pas le cas, on lève une exception nous-mêmes
    et le with annule tout.
    """
    with get_connection() as connection:
        connection.autocommit = True

        with connection.cursor() as cursor:
            print_velo(cursor, velo_id, "avant")

        try:
            with connection.transaction():  # BEGIN
                with connection.cursor() as cursor:
                    # On lit la station du vélo AVANT de la mettre à NULL
                    cursor.execute(
                        "SELECT station_id, etat FROM velo WHERE id = %s;",
                        (velo_id,),
                    )
                    station_depart_id, etat = cursor.fetchone()
                    if etat != "disponible":
                        raise ValueError(
                            f"vélo {velo_id} non disponible (état : {etat})"
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
            print("  COMMIT automatique (sortie du with sans erreur)")
        except ValueError as error:
            print(f"  ROLLBACK automatique : {error}")

        with connection.cursor() as cursor:
            print_velo(cursor, velo_id, "après")
