import psycopg

from src.create_connexion import get_connection
from exercice.velo_utils import print_velo


def run_e0_location_sans_transaction(abonne_id=42, velo_id=2, station_id=9999):
    """E0 : louer un vélo SANS transaction... depuis une station qui n'existe pas.

    Une location = 2 requêtes qui doivent réussir ENSEMBLE :
      1. UPDATE du vélo : il passe 'en_trajet' et quitte sa station
      2. INSERT du trajet : on note qui l'a pris, d'où et quand

    autocommit = True : chaque requête est validée (enregistrée pour de bon)
    dès qu'elle s'exécute. Observez ce qui arrive au vélo quand l'INSERT
    échoue (la station 9999 n'existe pas).
    """
    with get_connection() as connection:
        connection.autocommit = True
        with connection.cursor() as cursor:
            print_velo(cursor, velo_id, "avant")

            try:
                # TODO 1 : UPDATE du vélo velo_id -> etat 'en_trajet', station_id NULL
                #          (requête paramétrée : "... WHERE id = %s;", (velo_id,))
                #          puis afficher "UPDATE du vélo OK (et déjà enregistré !)"
                # TODO 2 : INSERT d'un trajet (abonne_id, velo_id, station_depart_id,
                #          depart_le) avec depart_le = NOW()
                #          puis afficher "INSERT du trajet OK"
                raise NotImplementedError("E0 : écrire l'UPDATE et l'INSERT")
            except psycopg.Error as error:
                print(f"  ERREUR à l'INSERT : {type(error).__name__}")

            print_velo(cursor, velo_id, "après")
