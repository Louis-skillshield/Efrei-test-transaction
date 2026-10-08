# TP Transactions — location de vélos

## Le problème

Louer un vélo, c'est **deux** requêtes :

1. `UPDATE velo` : le vélo passe `en_trajet` et quitte sa station (`station_id = NULL`)
2. `INSERT INTO trajet` : on note qui l'a pris, d'où et quand

Si la 1ʳᵉ réussit et que la 2ᵉ plante, la base contient un **vélo fantôme** :
il est marqué en trajet, mais personne ne l'a loué. Une **transaction** sert à
dire « ces requêtes réussissent toutes ensemble, ou aucune ne compte ».

> Analogie : un virement bancaire. Débiter un compte sans créditer l'autre,
> c'est de l'argent qui disparaît. Les deux opérations vont ensemble.

Après chaque étape, le programme affiche un verdict :
`✅ cohérent` ou `❌ INCOHÉRENT : ...`. Votre objectif : obtenir des ✅.

## Lancer le TP

```bash
uv run python main.py        # toutes les étapes E0 à E3, une par une
uv run python main.py e1     # une seule étape (e0, e1, e2 ou e3)
uv run python main.py reset  # remet les vélos 2, 3, 8 et 9 à zéro
```

Les fichiers à compléter sont dans `exercice/` (cherchez les `TODO`).
Tant qu'une étape n'est pas codée, elle affiche `⚠️ À compléter`.

## Les étapes

| Étape | Fichier | Ce que vous codez | Résultat attendu |
|---|---|---|---|
| **E0** | `e0_sans_transaction.py` | L'`UPDATE` et l'`INSERT` d'une location, **sans** transaction | ❌ vélo fantôme (c'est voulu !) |
| **E1** | `e1_transaction_sql.py` | La même location avec `BEGIN` / `COMMIT` / `ROLLBACK` écrits à la main | E1a : ROLLBACK ✅ — E1b : COMMIT ✅ |
| **E2** | `e2_location_python.py` | La location avec `with connection.transaction()` + refus si le vélo n'est pas `disponible` | E2a : COMMIT ✅ — E2b : ROLLBACK ✅ |
| **E3** | `e3_retour.py` | Le retour d'un vélo (2 `UPDATE`) + annulation si aucun trajet n'est en cours | E3a : COMMIT ✅ — E3b : ROLLBACK ✅ |
| **E4** | `e4_concurrence.py` | Deux abonnés louent le même vélo en même temps | sans verrou ❌ — avec verrou ✅ |

### E4 — deux terminaux

1. `uv run python main.py reset`
2. Ouvrez **deux** terminaux et lancez dans chacun : `uv run python main.py e4`
3. Quand les deux affichent `>>> ... appuie sur Entrée`, appuyez sur Entrée dans l'un, puis dans l'autre.
4. Regardez le verdict. Recommencez (reset compris) avec `uv run python main.py e4-verrou`.

Question : pourquoi la transaction seule ne suffit-elle pas en E4 ?

## Aide-mémoire

- `connection.autocommit = True` : chaque requête est enregistrée **dès** qu'elle s'exécute.
  Pour regrouper plusieurs requêtes, il faut donc ouvrir une transaction soi-même.
- `cursor.execute("BEGIN;")`, `cursor.execute("COMMIT;")`, `cursor.execute("ROLLBACK;")`
- `with connection.transaction():` → BEGIN en entrant, COMMIT en sortant,
  ROLLBACK automatique si une exception est levée dedans.
- `cursor.rowcount` : nombre de lignes touchées par la dernière requête.
- `SELECT ... FOR UPDATE` : verrouille les lignes lues jusqu'à la fin de la transaction.
- Requêtes paramétrées : `cursor.execute("... WHERE id = %s;", (velo_id,))`.

## Tables utiles

- `velo(id, etat, station_id, ...)` — `etat` ∈ `disponible`, `en_trajet`, `maintenance`, `hors_service`
- `trajet(id, abonne_id, velo_id, station_depart_id, station_arrivee_id, depart_le, arrivee_le, ...)`
  — un trajet en cours a `arrivee_le IS NULL`
- `station(id, nom, ...)`
