# Gestion de projet augmentee

Application de suivi et pilotage de projets avec assistance IA.

---

## Fonctionnalites

### 1. Dashboard projets
- **Diagramme de Gantt interactif** avec code couleur par niveau de risque
- **Score de risque automatique** calcule en temps reel (ecart temps ecoule vs avancement)
- **Metriques cles** : projets en bonne voie, a risque, en retard, termines
- **Filtres** par statut et par responsable

### 2. Allocation des ressources
- **Charge par responsable** : nombre de projets actifs et risque moyen
- **Suggestions de reallocation** : detection automatique des surcharges et disponibilites
- **Detail** par responsable avec liste des projets assignes

### 3. Synthese status reports par IA
- **Generation automatique** de rapports de statut via LLM (LLaMA 3.3)
- **Deux formats** : resume executif (concis) ou rapport detaille (analyse des risques, recommandations)
- **Export** en markdown

### 4. Assistant IA
- Chatbot specialise en gestion de projet (Gantt, PERT, chemin critique, KPIs)
- Accessible via le bouton rouge en bas de page

---

## Demarrage rapide

1. **Charger des donnees** : utilisez le bouton "Utiliser les donnees d'exemple" dans le sidebar, ou chargez votre propre fichier CSV/Excel
2. **Explorer le dashboard** : visualisez le Gantt et les metriques
3. **Analyser les ressources** : identifiez les surcharges
4. **Generer un rapport** : obtenez une synthese IA de l'etat des projets

### Format CSV attendu

Separateur : point-virgule (`;`)

| Colonne | Type | Description |
|---------|------|-------------|
| project | texte | Nom du projet |
| start_date | date (YYYY-MM-DD) | Date de debut |
| end_date | date (YYYY-MM-DD) | Date de fin prevue |
| progress | nombre (0-100) | Avancement en % |
| responsible | texte | Responsable du projet |
| budget | nombre | Budget en euros |
