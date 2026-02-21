# Methodologie

## Calcul du score de risque

Le score de risque de retard est calcule automatiquement pour chaque projet selon la formule :

$$\text{risque} = \min\left(\max\left((\text{temps ecoule \%} - \text{avancement \%}) \times 1.5,\ 0\right),\ 100\right)$$

Ou :
- **Temps ecoule (%)** : proportion du temps total du projet deja ecoulee a la date du jour
- **Avancement (%)** : progression declaree du projet

### Interpretation

| Score | Statut | Signification |
|-------|--------|---------------|
| 0 | Termine | Projet a 100% d'avancement |
| 1-24 | En bonne voie | L'avancement suit ou depasse le planning |
| 25-49 | A risque | Retard significatif par rapport au planning |
| 50-100 | En retard | Retard critique necessitant une action immediate |

### Limites

- Le score est base uniquement sur le ratio temps/avancement et ne prend pas en compte la complexite restante
- L'avancement est declaratif : il depend de la qualite du reporting
- Le budget n'est pas integre dans le calcul de risque (piste d'amelioration)

---

## Suggestions de reallocation

La detection de surcharge utilise un seuil a **1.4x la moyenne** du nombre de projets par responsable. Un responsable est considere comme :
- **Surcharge** : nombre de projets > 1.4x la moyenne, ou risque moyen > 50
- **Disponible** : nombre de projets < 0.6x la moyenne
- **Equilibre** : entre les deux seuils

---

## Generation de rapports IA

Les rapports sont generes via l'API Groq (modele LLaMA 3.3 70B). Le prompt inclut :
- Les donnees de suivi de tous les projets selectionnes
- Le format souhaite (resume executif ou rapport detaille)
- La langue de reponse

Les rapports detailles incluent une analyse des risques, des recommandations d'actions correctives, et une priorisation.
