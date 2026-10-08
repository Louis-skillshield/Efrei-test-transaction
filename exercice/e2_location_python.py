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
            # TODO 1 : ouvrir un bloc `with connection.transaction():`
            #          puis un curseur `with connection.cursor() as cursor:`
            # TODO 2 : SELECT station_id, etat du vélo
            #          (on lit la station AVANT de la mettre à NULL)
            # TODO 3 : si etat != 'disponible' -> raise ValueError("...")
            # TODO 4 : UPDATE du vélo + INSERT du trajet
            #          (station_depart_id = la station lue au TODO 2)
            raise NotImplementedError("E2 : location avec connection.transaction()")
            print("  COMMIT automatique (sortie du with sans erreur)")
        except ValueError as error:
            print(f"  ROLLBACK automatique : {error}")

        with connection.cursor() as cursor:
            print_velo(cursor, velo_id, "après")
