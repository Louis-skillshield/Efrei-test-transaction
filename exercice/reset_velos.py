from src.create_connexion import get_connection

# Station où chaque vélo d'exercice est garé lors de la remise à zéro
STATION_PAR_DEFAUT = {2: 20, 3: 2, 8: 5, 9: 2}


def run_reset_velos(velo_id_list=(2, 3, 8, 9)):
    """Remet les vélos des exercices en état 'disponible'.

    Les trajets encore ouverts sont clôturés à leur station de départ,
    pour pouvoir rejouer les exercices autant de fois qu'on veut.
    """
    with get_connection() as connection:
        with connection.transaction():
            with connection.cursor() as cursor:
                for velo_id in velo_id_list:
                    station_id = STATION_PAR_DEFAUT[velo_id]
                    cursor.execute(
                        "UPDATE trajet SET arrivee_le = NOW(), "
                        "station_arrivee_id = station_depart_id "
                        "WHERE velo_id = %s AND arrivee_le IS NULL;",
                        (velo_id,),
                    )
                    closed_count = cursor.rowcount
                    cursor.execute(
                        "UPDATE velo SET etat = 'disponible', "
                        "station_id = %s WHERE id = %s;",
                        (station_id, velo_id),
                    )
                    print(
                        f"  Vélo {velo_id} : disponible en station "
                        f"{station_id} ({closed_count} trajet(s) clôturé(s))"
                    )
