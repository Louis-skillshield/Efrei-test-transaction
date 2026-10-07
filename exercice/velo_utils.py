def get_velo(cursor, velo_id):
    cursor.execute(
        "SELECT id, etat, station_id FROM velo WHERE id = %s;",
        (velo_id,),
    )
    return cursor.fetchone()


def get_trajet_en_cours(cursor, velo_id):
    cursor.execute(
        "SELECT id, abonne_id, station_depart_id, depart_le FROM trajet "
        "WHERE velo_id = %s AND arrivee_le IS NULL "
        "ORDER BY id DESC LIMIT 1;",
        (velo_id,),
    )
    return cursor.fetchone()


def print_velo(cursor, velo_id, moment):
    velo = get_velo(cursor, velo_id)
    trajet = get_trajet_en_cours(cursor, velo_id)
    print(f"  [{moment}] vélo (id, etat, station_id) : {velo}")
    print(f"  [{moment}] trajet en cours : {trajet}")
