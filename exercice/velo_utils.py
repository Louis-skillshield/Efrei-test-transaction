"""Outils d'affichage fournis : vous n'avez rien à modifier ici.

print_velo affiche l'état d'un vélo et un verdict de cohérence :
c'est lui qui vous dira si la base est restée propre ou non.
"""


def get_velo(cursor, velo_id):
    cursor.execute(
        "SELECT id, etat, station_id FROM velo WHERE id = %s;",
        (velo_id,),
    )
    return cursor.fetchone()


def get_trajet_ouvert_list(cursor, velo_id):
    """Trajets commencés mais pas encore terminés (arrivee_le IS NULL)."""
    cursor.execute(
        "SELECT id FROM trajet "
        "WHERE velo_id = %s AND arrivee_le IS NULL ORDER BY id;",
        (velo_id,),
    )
    return [row[0] for row in cursor.fetchall()]


def get_coherence_problem_list(etat, station_id, trajet_ouvert_list):
    """Liste les règles métier violées par un vélo (liste vide = tout va bien)."""
    problem_list = []
    trajet_ouvert_count = len(trajet_ouvert_list)

    if etat == "en_trajet" and trajet_ouvert_count == 0:
        problem_list.append("vélo 'en_trajet' mais aucun trajet ouvert (vélo fantôme)")
    if etat != "en_trajet" and trajet_ouvert_count > 0:
        problem_list.append(f"vélo '{etat}' mais un trajet est encore ouvert")
    if trajet_ouvert_count > 1:
        problem_list.append(
            f"{trajet_ouvert_count} trajets ouverts en même temps pour un seul vélo"
        )
    if etat == "en_trajet" and station_id is not None:
        problem_list.append("vélo 'en_trajet' mais toujours garé en station")
    if etat == "disponible" and station_id is None:
        problem_list.append("vélo 'disponible' mais garé nulle part")
    return problem_list


def print_velo(cursor, velo_id, moment):
    velo = get_velo(cursor, velo_id)
    if velo is None:
        print(f"  [{moment}] vélo {velo_id} introuvable")
        return

    _, etat, station_id = velo
    trajet_ouvert_list = get_trajet_ouvert_list(cursor, velo_id)
    print(
        f"  [{moment}] vélo {velo_id} : etat={etat}, station={station_id}, "
        f"trajets ouverts={trajet_ouvert_list}"
    )

    problem_list = get_coherence_problem_list(etat, station_id, trajet_ouvert_list)
    if problem_list:
        for problem in problem_list:
            print(f"  [{moment}] ❌ INCOHÉRENT : {problem}")
    else:
        print(f"  [{moment}] ✅ cohérent")
