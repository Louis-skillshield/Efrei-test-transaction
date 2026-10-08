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

            # TODO 1 : ouvrir la transaction (cursor.execute("BEGIN;"))
            # TODO 2 : dans un try :
            #            - l'UPDATE du vélo (comme en E0)
            #            - l'INSERT du trajet (comme en E0)
            #            - COMMIT, puis afficher "COMMIT : tout est enregistré"
            # TODO 3 : dans le except psycopg.Error :
            #            - ROLLBACK, puis afficher l'erreur et "ROLLBACK"
            raise NotImplementedError("E1 : BEGIN / COMMIT / ROLLBACK à la main")

            print_velo(cursor, velo_id, "après")
