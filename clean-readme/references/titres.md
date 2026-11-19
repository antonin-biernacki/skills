# Titres, états et libellés de référence

Textes exacts à utiliser. Les titres de niveau 2 du README sont pris uniquement dans ces tableaux, sauf au plus 2 sections libres. Les titres de niveau 3 sont libres, sauf ceux indiqués ici.

## Commentaire en tête du README

Première ligne du README, toujours en ASCII et en français, quelle que soit la langue du README :

```markdown
<!-- clean-readme: type=recherche; langue=fr; v=2 -->
```

| Clé | Valeurs | Rôle |
|---|---|---|
| `type` | `realisation`, `outil`, `recherche`, `recueil` | Type retenu |
| `langue` | `fr`, `en` | Langue de tous les fichiers du dépôt |
| `v` | entier, actuellement `2` | Version des règles. Plus ancienne que celle du skill : proposer une refonte |

## Bloc d'état

Une citation, juste après la description.

```markdown
> **État** : En pause. La communication avec le capteur fonctionne, mais les mesures ne sont pas encore enregistrées. Reprise à la réception d'une nouvelle carte.
```

Avec une version :

```markdown
> **État** : Terminé (version 1.2.0 du 2026-01-10).
```

En anglais :

```markdown
> **Status**: Paused. Sensor communication works, but measurements are not recorded yet. Work resumes when a new board arrives.
> **Status**: Done (version 1.2.0 of 2026-01-10).
```

- Pas de date de mise à jour : l'historique git la donne déjà, et elle se périme.
- La version et sa date viennent des tags git ou des releases, jamais d'une estimation.

## États

| État | En anglais | Sens | Précision obligatoire après la parenthèse |
|---|---|---|---|
| En cours | In progress | Développement actif | Aucune |
| Expérimental | Experimental | Fonctionne en partie, peut changer ou casser | Ce qui marche et ce qui ne marche pas, en une phrase |
| En pause | Paused | Arrêté temporairement | La raison et ce qui permettra de reprendre |
| Arrêté | Stopped | Abandonné ou non mené à terme | La raison, et le point où le projet s'est arrêté |
| Terminé | Done | Fini et fonctionnel | Aucune |

Dans un tableau d'avancement du README, la colonne État utilise du texte : Fait, En cours, À faire (Done, In progress, To do).

## README : titres communs

| Niveau | Français | Anglais | Types |
|---|---|---|---|
| 1 | (nom lisible du projet) | (project name) | Tous |
| 2 | Avertissement | Disclaimer | Tous, facultatif |
| 2 | Sommaire | Contents | Tous, à partir de 5 autres sections de niveau 2 |
| 2 | Contexte | Context | Tous, facultatif |
| 2 | Différences avec le projet d'origine | Differences from upstream | Fork |
| 2 | Structure du dépôt | Repository structure | Réalisation, Outil, Recherche |
| 2 | Matériel | Hardware | Réalisation, Recherche |
| 2 | Fonctionnalités | Features | Réalisation, Outil |
| 2 | Avancement | Progress | Réalisation, Recherche |
| 2 | Limites | Limitations | Tous |
| 2 | Crédits | Credits | Tous, seulement si l'utilisateur l'écrit |
| 2 | Références | References | Tous |
| 3 | Citer ce travail | Citation | Sous Références, recherche académique |
| 2 | Licence | License | Tous, seulement si le dépôt a un fichier de licence |

## README : titres propres à un type

| Niveau | Français | Anglais | Type |
|---|---|---|---|
| 2 | Aperçu | Overview | Réalisation |
| 2 | Points techniques | Technical highlights | Réalisation, facultatif |
| 2 | Compilation et lancement | Build and run | Réalisation |
| 3 | Prérequis | Prerequisites | Sous Compilation et lancement, Installation ou Reproduire |
| 2 | Utilisation | Usage | Réalisation |
| 2 | Déploiement | Deployment | Réalisation |
| 2 | Fonctionnement interne | How it works | Réalisation |
| 2 | Installation | Installation | Outil |
| 2 | Usage minimal | Quick start | Outil |
| 2 | Configuration et options | Configuration and options | Outil |
| 2 | Contribuer | Contributing | Outil |
| 2 | Question de recherche | Research question | Recherche |
| 2 | Résultats principaux | Key results | Recherche |
| 2 | Méthode | Method | Recherche |
| 2 | Reproduire | Reproduce | Recherche |
| 2 | Questions ouvertes | Open questions | Recherche |
| 2 | Organisation du dépôt | Repository layout | Recueil |
| 2 | Index | Index | Recueil |
| 2 | Modèle | Template | Recueil |
| 2 | Outils utilisés | Tools | Recueil |

## Fichiers annexes

| Fichier (fr / en) | Niveau 1 (fr / en) | Niveaux 2 (fr / en) |
|---|---|---|
| `ROADMAP.md` / `ROADMAP.md` | Feuille de route / Roadmap | Légende / Legend |
| `RESULTATS.md` / `RESULTS.md` | Résultats de recherche / Research results | Sommaire / Contents, Résumé / Summary, Méthode / Method, Résultats / Results, Essais / Trials, Pistes écartées / Discarded leads, Questions ouvertes / Open questions |
| `docs/GUIDE.md` / `docs/GUIDE.md` | Guide / Guide | Titres repris du README : Installation, Configuration et options, Matériel |
| `docs/FONCTIONNEMENT.md` / `docs/HOW-IT-WORKS.md` | Fonctionnement interne / How it works | Libres |
| `docs/INDEX.md` / `docs/INDEX.md` | Index / Index | Libres, par exemple un niveau 2 par thème |

- Le titre de niveau 1 de RESULTATS.md diffère du niveau 2 "Résultats", sinon GitHub donne deux fois la même ancre.
- Chaque résultat de RESULTATS.md a un titre de niveau 3 réduit à son numéro (`### R1`), et son énoncé en gras sur la ligne suivante. L'ancre `#r1` reste stable si l'énoncé est reformulé.

## Ancres

Le skill et le script calculent les ancres comme GitHub :

1. retirer la mise en forme (liens, code, HTML) ;
2. passer en minuscules, garder les accents ;
3. retirer la ponctuation sauf `-` et `_` ;
4. remplacer les espaces par des tirets ;
5. pour un titre en double, ajouter `-1`, `-2`...

Exemple : `## Structure du dépôt` donne `#structure-du-dépôt`.
