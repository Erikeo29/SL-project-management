# Donnees projets -- format attendu

## Format CSV

- **Separateur** : point-virgule (`;`)
- **Encodage** : UTF-8
- **Dates** : format `YYYY-MM-DD`

## Colonnes

| Colonne | Type | Obligatoire | Description | Exemple |
|---------|------|-------------|-------------|---------|
| `project` | texte | oui | Nom du projet | `Validation procede electrodepot Ni` |
| `start_date` | date | oui | Date de debut (YYYY-MM-DD) | `2025-09-01` |
| `end_date` | date | oui | Date de fin prevue (YYYY-MM-DD) | `2026-04-30` |
| `progress` | nombre | oui | Avancement en % (0 a 100) | `65` |
| `responsible` | texte | oui | Responsable du projet | `Dupont` |
| `budget` | nombre | non | Budget en euros | `45000` |

## Fichiers d'exemple

| Fichier | Description | Projets | Responsables |
|---------|-------------|---------|--------------|
| `sample_projects.csv` | Donnees realistes medical device / electrochimie | 18 | 5 (Dupont, Martin, Leroy, Bernard, Garcia) |
| `exemple_minimal.csv` | Minimum viable (3 projets, 2 personnes) | 3 | 2 (Alice, Bob) |
| `exemple_equipe_large.csv` | Equipe de 4 avec projets multi-phases | 12 | 4 (Moreau, Petit, Roux, Simon) |

## Calcul du risque

Le score de risque (0-100) est calcule automatiquement :

```
risque = (temps_ecoule_% - avancement_%) x 1.5
```

| Score | Couleur Gantt | Statut |
|-------|---------------|--------|
| 0 | vert | termine |
| 1-24 | vert | en bonne voie |
| 25-49 | orange | a risque |
| 50-100 | rouge | en retard |

## Utilisation dans l'app

1. Ouvrir le sidebar (fleche en haut a gauche)
2. Soit cliquer "Utiliser les donnees d'exemple" (charge `sample_projects.csv`)
3. Soit glisser votre propre fichier CSV/Excel dans la zone de drop
4. Naviguer vers "Dashboard projets" pour voir le Gantt
