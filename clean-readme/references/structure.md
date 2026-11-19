# Structure du README et des fichiers annexes

Les titres exacts et leur traduction sont dans `titres.md`. Une section sans contenu réel est omise. Les sections sont dans l'ordre indiqué.

## Début commun (tous les types)

1. Commentaire `clean-readme` en première ligne.
2. Titre de niveau 1 : nom lisible du projet. S'il n'est pas évident, le demander.
3. Description : 2 à 4 phrases. Ce qu'est le projet, avec quoi il est fait, à quoi il sert. Pour la recherche : l'objectif et l'avancement en bref.
4. Bloc d'état (format dans `titres.md`).
5. Avertissement : facultatif, pour un projet de sécurité, de rétro-ingénierie ou qui touche un produit commercial. Usage éducatif, non-affiliation avec la marque étudiée, risques éventuels. Deux ou trois phrases.
6. Sommaire : liens vers les titres de niveau 2, seulement s'il y a au moins 5 autres sections de niveau 2.
7. Contexte : seulement si le projet a besoin d'une mise en situation (cadre, motivation, contraintes).
8. Différences avec le projet d'origine : seulement pour un fork.

## Corps selon le type

### Réalisation

- Aperçu : images, schéma, routage, vidéo de démonstration. Pour un site : lien vers la version en ligne et captures d'écran.
- Fonctionnalités : liste courte.
- Points techniques : facultatif. Les notions techniques mises en œuvre et ce que le projet montre (sockets UDP, threads POSIX, chargement dynamique de bibliothèques...). Liste courte, un élément par ligne.
- Avancement : seulement si le projet n'est pas terminé. Tableau de 10 lignes au maximum, colonne État en texte. Au-delà, proposer ROADMAP.md et ne garder qu'un résumé avec un lien.
- Structure du dépôt.
- Matériel : si le projet en utilise.
- Compilation et lancement : commence par `### Prérequis` (système, versions, dépendances, matériel, "testé sur").
- Utilisation.
- Déploiement : pour un site ou un service.
- Fonctionnement interne : bref, sinon déplacé dans `docs/FONCTIONNEMENT.md`.

### Outil

- Installation : commence par `### Prérequis` (système, versions, dépendances, "testé sur").
- Usage minimal : un exemple qui marche, copiable tel quel.
- Fonctionnalités.
- Configuration et options : courtes, sinon déplacées dans `docs/GUIDE.md`.
- Structure du dépôt : facultative.
- Contribuer : facultatif, comment signaler un problème ou proposer une modification.

### Recherche

- Question de recherche : ce qu'on cherche à savoir.
- Avancement : résumé en 3 à 8 lignes (étape en cours, ce qui bloque), lien vers ROADMAP.md s'il existe.
- Résultats principaux : 1 à 6 résultats numérotés (R1, R2...), une ou deux phrases chacun, avec un lien vers `RESULTATS.md#r1`.
- Méthode : quelques phrases (outils, données, protocole).
- Reproduire : commence par `### Prérequis`, puis uniquement les commandes qui reproduisent les résultats principaux. Signaler une commande qui demande un matériel particulier ou une longue durée.
- Structure du dépôt.
- Matériel : si le projet en utilise.
- Questions ouvertes : ce qui reste à chercher et la suite prévue.

### Recueil

- Organisation du dépôt : la forme commune de chaque entrée (arborescence type).
- Index : tableau des entrées avec lien, thème et état (valeurs de `titres.md`).
- Modèle : lien vers le modèle vierge s'il existe.
- Outils utilisés : ils servent aussi de prérequis.

## Sections libres

- Au plus 2 sections de niveau 2 hors des tableaux de `titres.md`, quand le contenu le justifie (un protocole maison, un jeu d'instructions, les règles d'un jeu).
- Les annoncer dans le plan.
- Les placer à côté de la section fixe la plus proche par son sujet, toujours avant la fin commune.

## Fin commune (tous les types)

1. Limites : ce qui ne marche pas ou est restreint aujourd'hui. Pour la recherche, ce qui reste à chercher va dans Questions ouvertes.
2. Crédits : auteurs, équipe, projets réutilisés. Tout code tiers inclus est cité avec sa licence.
3. Références : articles, documentation, projets liés. Pour une recherche académique, `### Citer ce travail` facultatif, avec une entrée BibTeX ou un fichier `CITATION.cff`.
4. Licence : celle du dépôt. Si elle manque et que le commentaire ne contient pas `licence=non`, proposer d'en ajouter une (par exemple MIT), compatible avec le code tiers inclus. Créer `LICENSE` seulement après accord.

## Structure du dépôt (arborescence)

- Dans un bloc `text`, en ASCII : indentation de 4 espaces, pas de caractères de dessin.
- 2 niveaux au maximum.
- Sans les fichiers générés ni ignorés par git.
- Un commentaire court après `#` pour chaque dossier ou fichier important.

```text
src/             # code du serveur
    main.c       # point d'entrée
docs/            # documentation et images
Makefile         # compilation
```

## ROADMAP.md

- Titre de niveau 1, puis `## Légende` avec les trois emojis : ⬜ à faire, 🟡 en cours, ✅ fait. Aucun autre emoji.
- Un seul grand tableau, colonnes : Phase, Étape, Description, État.
- La cellule État contient seulement l'emoji.
- Chaque étape est une action vérifiable, pas un thème vague.
- Le README garde seulement un résumé de l'avancement et un lien.

## RESULTATS.md

- Pas d'emoji. Phrases claires et précises.
- Une partie sans contenu est omise.

1. Titre de niveau 1.
2. Sommaire : liens vers les titres de niveau 2 et 3.
3. Résumé : ce qu'on sait aujourd'hui, en quelques phrases.
4. Méthode : outils, matériel, données, protocole.
5. Résultats : `### R1`, `### R2`... Pour chacun : l'énoncé en gras sur la première ligne, les preuves (chiffres, captures, fichiers), la date, la commande ou le fichier qui le produit.
6. Essais : tableau numéroté, colonnes #, Date, Essai, Résultat, Conclusion.
7. Pistes écartées : ce qui a été essayé sans succès, avec la raison en une ou deux phrases.
8. Questions ouvertes : ce qui reste à comprendre, avec l'essai prévu pour y répondre.

Règles de mise à jour :

- La numérotation des résultats et des essais ne change jamais.
- On réécrit, on ne barre pas. Un résultat invalidé passe dans Pistes écartées avec la raison.

## Dépassement des 200 lignes

Déplacer les sections longues et les remplacer par un résumé de 2 ou 3 phrases avec un lien, dans cet ordre :

1. Fonctionnement interne -> `docs/FONCTIONNEMENT.md`.
2. Installation détaillée -> `docs/GUIDE.md`.
3. Configuration et options -> `docs/GUIDE.md`.
4. Matériel détaillé -> `docs/GUIDE.md`.

Selon le type :

- Recueil : un index trop long part dans `docs/INDEX.md`. Le README garde le nombre d'entrées, les thèmes et les 5 à 10 entrées les plus récentes ou les plus importantes.
- Recherche : la méthode détaillée part dans la partie Méthode de RESULTATS.md. Le README en garde 3 ou 4 phrases.

Si le README dépasse encore 200 lignes : raccourcir les résumés et les listes (Fonctionnalités, Points techniques, Structure du dépôt), puis en dernier recours demander à l'utilisateur quelle section sortir.

## Correspondances fréquentes en refonte

Titres courants d'anciens README et leur destination habituelle. À confirmer dans le plan.

| Ancien titre | Destination |
|---|---|
| About, Présentation, Introduction, Vue d'ensemble | Description ou Contexte |
| Demo, Screenshots, Captures | Aperçu |
| Getting started, Quick start, Démarrage | Usage minimal (Outil) ou Compilation et lancement (Réalisation) |
| Build, Compilation, Lancement, Running | Compilation et lancement |
| Requirements, Dépendances | `### Prérequis` |
| Architecture, Fonctionnement, Internals | Fonctionnement interne |
| Structure du projet, Architecture du dépôt, Layout | Structure du dépôt |
| Roadmap, TODO, Feuille de route | Avancement et ROADMAP.md |
| Résultats, Benchmarks, Expériences, Essais réalisés | Résultats principaux et RESULTATS.md |
| Suite du projet, Future work, Next steps | Questions ouvertes (Recherche) ou Avancement |
| Équipe, Auteurs, Remerciements, Acknowledgements | Crédits |
| Known issues, Limitations, Caveats | Limites |
