import sys

from exercice.reset_velos import run_reset_velos
from exercice.e0_sans_transaction import run_e0_location_sans_transaction
from exercice.e1_transaction_sql import run_e1_location_transaction_sql
from exercice.e2_location_python import run_e2_location
from exercice.e3_retour import run_e3_retour
from exercice.e4_concurrence import run_e4_concurrence

# (étape, titre, fonction à lancer)
EXERCICE_LIST = [
    (
        "e0",
        "E0 - SANS transaction : vélo 2 loué depuis la station 9999 (inexistante)",
        lambda: run_e0_location_sans_transaction(velo_id=2, station_id=9999),
    ),
    (
        "e1",
        "E1a - BEGIN/COMMIT à la main : vélo 3 depuis la station 9999 (inexistante)",
        lambda: run_e1_location_transaction_sql(velo_id=3, station_id=9999),
    ),
    (
        "e1",
        "E1b - BEGIN/COMMIT à la main : vélo 3 depuis la station 2 (OK)",
        lambda: run_e1_location_transaction_sql(velo_id=3, station_id=2),
    ),
    (
        "e2",
        "E2a - with transaction() : l'abonné 42 loue le vélo 8",
        lambda: run_e2_location(velo_id=8),
    ),
    (
        "e2",
        "E2b - with transaction() : on retente de louer le vélo 8",
        lambda: run_e2_location(velo_id=8),
    ),
    (
        "e3",
        "E3a - Retour du vélo 8 à la station 12",
        lambda: run_e3_retour(velo_id=8, station_arrivee_id=12),
    ),
    (
        "e3",
        "E3b - Retour du vélo 9... qui n'a jamais été loué",
        lambda: run_e3_retour(velo_id=9, station_arrivee_id=12),
    ),
]


def run_exercice(titre, run_function):
    print(f"\n=== {titre} ===")
    try:
        run_function()
    except NotImplementedError as error:
        print(f"  ⚠️  À compléter : {error}")


def run_exercice_list(etape=None):
    should_reset = input("Remettre les vélos 2, 3, 8 et 9 à zéro ? (y/n) ")
    if should_reset == "y":
        run_reset_velos()

    for exercice_etape, titre, run_function in EXERCICE_LIST:
        if etape is not None and exercice_etape != etape:
            continue
        input(f"\nEntrée pour lancer : {titre}")
        run_exercice(titre, run_function)

    if etape is None:
        print("\nE0 à E3 terminés. Pour E4, ouvre DEUX terminaux (voir le README).")


def main():
    commande = sys.argv[1] if len(sys.argv) > 1 else "all"

    if commande == "reset":
        run_reset_velos()
    elif commande == "e4":
        run_exercice(
            "E4a - Deux terminaux, un seul vélo 9, SANS verrou",
            lambda: run_e4_concurrence(should_lock=False),
        )
    elif commande == "e4-verrou":
        run_exercice(
            "E4b - Deux terminaux, un seul vélo 9, AVEC verrou (FOR UPDATE)",
            lambda: run_e4_concurrence(should_lock=True),
        )
    elif commande in ("e0", "e1", "e2", "e3"):
        run_exercice_list(etape=commande)
    else:
        run_exercice_list()


if __name__ == "__main__":
    main()
