import sys

from exercice.reset_velos import run_reset_velos
from exercice.t1_location import run_t1_location
from exercice.t2_station_inexistante import run_t2_station_inexistante
from exercice.t3_retour import run_t3_retour
from exercice.t4_location_python import run_t4_location
from exercice.t5_concurrence import run_t5_concurrence

EXERCICE_LIST = [
    ("T1 - L'abonné 42 loue le vélo 1 (station 5)", run_t1_location),
    ("T2 - Vélo 2 depuis la station 9999", run_t2_station_inexistante),
    ("T3 - Retour du vélo 1 à la station 12", run_t3_retour),
    ("T4 - Location en Python avec connection.transaction()", run_t4_location),
]


def run_exercice_list():
    print("\n=== Remise à zéro des vélos 1, 2 et 8 ===")
    run_reset_velos()

    for titre, run_exercice in EXERCICE_LIST:
        input(f"\nEntrée pour lancer : {titre}")
        print(f"\n=== {titre} ===")
        run_exercice()

    print("\nT1 à T4 terminés. Pour T5, ouvre deux terminaux et lance dans chacun :")
    print("  uv run python main.py t5")
    print("(lance d'abord `uv run python main.py reset` pour libérer le vélo 8)")


def main():
    commande = sys.argv[1] if len(sys.argv) > 1 else "all"

    if commande == "t5":
        print("\n=== T5 - Deux terminaux, un seul vélo 8 ===")
        run_t5_concurrence()
    elif commande == "reset":
        run_reset_velos()
    else:
        run_exercice_list()


if __name__ == "__main__":

    main()
