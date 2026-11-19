---
name: clean-readme
description: Crée, refond ou met à jour le README d'un dépôt et ses fichiers annexes (ROADMAP.md, RESULTATS.md, docs/) selon des règles fixes - type de projet (réalisation, outil, recherche, recueil), bloc d'état daté, 200 lignes au maximum, titres fixes, rien d'inventé, vérification par script. À utiliser quand l'utilisateur appelle /clean-readme, demande d'écrire, refaire, nettoyer ou mettre à jour un README (write, clean up or update a README), ou donne une information à ranger dans un dépôt déjà suivi (nouvel essai, nouveau résultat, étape terminée, projet en pause).
---

# clean-readme

Le README décrit l'état actuel du projet et sert de porte d'entrée. Tout ce qui grossit avec le temps (étapes, essais, résultats détaillés, documentation longue) va dans un fichier à part, et le README en garde un résumé avec un lien.

Fichiers de référence, à lire quand ils servent :

- `references/detection.md` : reconnaître le type et l'état d'un projet ;
- `references/structure.md` : sections du README par type, ROADMAP.md, RESULTATS.md, dépassement des 200 lignes, correspondances pour une refonte ;
- `references/titres.md` : titres exacts en français et en anglais, états, bloc d'état, commentaire en tête, ancres ;
- `templates/` : un modèle de README par type, et les modèles de ROADMAP.md et RESULTATS.md ;
- `scripts/verifier.py` : vérification automatique.

## Arguments

| Argument | Effet |
|---|---|
| `creation`, `refonte`, `maj` | Force le mode |
| `type=realisation`, `type=outil`, `type=recherche`, `type=recueil` | Force le type |
| `en`, `fr` | Force la langue |
| Texte libre | Information à intégrer (nouvel essai, changement d'état...) |

## Choix du mode

| Situation | Mode |
|---|---|
| Pas de README | Création |
| README sans commentaire `clean-readme` en première ligne | Refonte |
| README avec ce commentaire | Mise à jour |

Si l'utilisateur donne une information à ranger alors que le README n'a pas le commentaire, proposer d'abord la refonte. S'il refuse, faire seulement l'ajout demandé, sans restructurer et sans ajouter le commentaire.

## Lecture du dépôt

Ne pas lire tout le code d'un gros dépôt. Lire dans l'ordre :

1. l'arborescence, sans les fichiers ignorés (`git ls-files`, ou `ls` si ce n'est pas un dépôt git) ;
2. le README et les docs existants ;
3. les fichiers de configuration et de build (Makefile, fichiers de paquet, configuration de framework) ;
4. les points d'entrée et les scripts ;
5. l'historique git et les tags, si c'est un dépôt git ;
6. le reste du code seulement si une section en a besoin.

Lire aussi la date du jour : `date +%F`. Ne jamais l'estimer.

## Mode création

1. Lire le dépôt.
2. Déterminer le type et l'état avec `references/detection.md`.
3. Envoyer **un seul message** qui regroupe :
   - le type et l'état proposés, avec les indices trouvés et l'autre possibilité s'il y en a une ;
   - les questions sur ce qui manque : raison de l'état, résultats, nom lisible du projet s'il n'est pas évident, licence si absente (sauf `licence=non`) ;
   - le plan : sections prévues, sections libres éventuelles, fichiers qui seront créés.
4. Attendre la réponse. Rédiger à partir du modèle du type dans `templates/` et de `references/structure.md`. Retirer les sections sans contenu réel, et leurs lignes dans le sommaire.
5. Lancer les vérifications.
6. Présenter le bilan des fichiers créés et de ce qui manque encore (captures à faire, informations à fournir).

## Mode refonte

1. Lire le dépôt et le README existant.
2. Associer chaque section existante à la nouvelle structure (voir les correspondances dans `references/structure.md`).
3. Repérer les informations qui semblent périmées : contredites par le code, par un autre passage ou par l'historique.
4. Envoyer **un seul message** qui regroupe :
   - le type et l'état proposés, avec les indices ;
   - le plan : pour chaque section existante, gardée, renommée, fusionnée ou déplacée, et vers quel fichier ;
   - les informations qui semblent périmées, avec pour chacune le choix : supprimer, corriger, ou déplacer dans RESULTATS.md (pistes écartées) ;
   - les questions sur ce qui manque.
5. Attendre la réponse, puis rédiger. Toute l'information encore valable est conservée, dans le README ou dans un fichier annexe.
6. Lancer les vérifications.
7. Présenter le bilan : ce qui a été déplacé et où, ce qui manque encore.

## Mode mise à jour

Lire le type, la langue et la version des règles dans le commentaire en tête. Si `v` est inférieur à 1, proposer une refonte. Sinon, ranger l'information sans plan préalable :

| Information reçue | Où elle va |
|---|---|
| Nouvel essai | RESULTATS.md, tableau des essais, avec le numéro suivant. Créer le fichier s'il n'existe pas |
| Nouveau résultat consolidé | RESULTATS.md, nouvelle section `### Rn`, et une ligne dans Résultats principaux du README s'il est important |
| Étape terminée ou commencée | ROADMAP.md, puis le résumé d'avancement du README |
| Changement d'état | Bloc d'état du README, avec la date du jour |
| Projet qui a changé de nature (preuve de concept devenue stable) | Proposer le nouveau type. Après accord, restructurer et mettre à jour le commentaire |
| Nouvelle fonctionnalité ou commande | Section correspondante du README |

Lancer quand même toutes les vérifications. Si le README a été modifié à la main et ne respecte plus les règles, signaler les écarts et proposer de les corriger. Terminer par le bilan des modifications.

## Fichiers produits

Au plus 5 fichiers de documentation créés par le skill, README compris :

| Fichier | Quand le créer |
|---|---|
| `README.md` | Toujours |
| `ROADMAP.md` | Roadmap déjà présente, demande de l'utilisateur, ou avancement de plus de 10 lignes dans le README (sur proposition) |
| `RESULTATS.md` (`RESULTS.md` en anglais) | Recherche, dès le premier résultat ou le premier essai |
| `docs/GUIDE.md` | README de plus de 200 lignes : installation détaillée, configuration, matériel |
| `docs/FONCTIONNEMENT.md` (`docs/HOW-IT-WORKS.md`) | README de plus de 200 lignes : architecture, fonctionnement interne |
| `docs/INDEX.md` | Recueil dont l'index fait dépasser 200 lignes |

- Les fichiers existants hors de cette liste (`CHANGELOG.md`, autres dossiers de `docs/`) ne sont ni renommés, ni modifiés, ni supprimés. Le README peut y renvoyer.
- Noms de fichiers sans accent ni espace. Images dans `docs/images/`.
- Seul le README racine est traité, sauf demande pour un sous-dossier.

## Règles d'écriture

### Langue

Dans l'ordre : langue demandée par l'utilisateur, langue du commentaire en tête, langue du README existant, langue dans laquelle l'utilisateur écrit. Tous les fichiers du dépôt dans la même langue. En anglais, titres, états et noms de fichiers viennent des tables de `references/titres.md`.

### Style

- Phrases claires, précises et courtes : une idée par phrase.
- Pas de ton commercial. Mots à éviter : puissant, simple, facile, simplement, il suffit de, robuste, moderne, incontournable, révolutionnaire (et leurs équivalents anglais). Acceptés pour un nom propre (Simple DirectMedia Layer) ou au sens littéral ("un simple fichier texte").
- "Je" pour un projet seul, "nous" pour une équipe, la même personne partout.

### Caractères

- Seulement les caractères d'un clavier AZERTY : lettres, accents, chiffres, ponctuation du clavier. Autorisés en plus : `œ`, `Œ` et les majuscules accentuées.
- Interdits : guillemets français et typographiques, apostrophe courbe, tirets longs, points de suspension en un caractère, flèches, symboles mathématiques hors clavier, caractères de dessin d'arborescence, espaces insécables et caractères de largeur nulle.
- Remplacer par `"`, `'`, `-` ou `:`, `...`, `->`, `<=`, `x`.
- Formules : LaTeX de GitHub (`$...$`) ou ASCII dans un bloc de code.
- Une sortie réelle recopiée dans un bloc de code reste telle quelle.

### Emojis

Interdits dans le README et RESULTATS.md. Dans ROADMAP.md, seulement ⬜, 🟡 et ✅.

### Forme Markdown

- Un seul titre de niveau 1 (nom lisible du projet). Sections en niveau 2, sous-sections en niveau 3, jamais plus profond.
- Titres de niveau 2 pris dans `references/titres.md`, plus au plus 2 sections libres justifiées par le contenu, annoncées dans le plan, placées près de la section fixe la plus proche et avant la fin commune.
- Blocs de code toujours avec un langage. Commandes copiables, sans `$` devant. Sortie dans un bloc `text` séparé.
- Images avec un texte alternatif, chemins relatifs.
- Liens relatifs pour les fichiers du dépôt.
- Pas de badges. Pas de HTML de mise en page. `<details>` et `<img>` avec une taille tolérés si nécessaire.
- Aucune mention d'IA ou d'assistant, ni de contenu généré.

### Fiabilité

- Ne jamais inventer un résultat, un chiffre, une date, une commande, une version ou un état. Demander. Une date inconnue s'écrit "inconnue".
- Les commandes du projet (cibles Makefile, scripts, points d'entrée) doivent exister dans le dépôt. Les outils externes utilisés figurent dans les prérequis.
- Les liens, ancres et images visent des fichiers qui existent et qui sont suivis par git.
- Si l'aperçu demande des captures absentes, lister celles à faire au lieu de laisser un lien vide.
- Ne rien perdre : un contenu retiré du README est déplacé dans un fichier annexe, sauf une information périmée dont l'utilisateur a validé la suppression.

### Données personnelles

Dans les sorties recopiées et les exemples, remplacer :

- les chemins absolus locaux (`/home/<utilisateur>/...`) par un chemin relatif ou `~` ;
- les secrets (jetons, mots de passe, clés, contenu de `.env`) : les retirer ;
- les adresses IP, MAC et noms de machine personnels par des valeurs d'exemple (`192.0.2.10`, `00:11:22:33:44:55`) ;
- les adresses e-mail que le dépôt ne montre pas déjà.

## Vérifications

Lancer le script depuis le dossier de ce skill :

```bash
python3 scripts/verifier.py <chemin-du-depot>
```

- `ERREUR` : règle non respectée, à corriger avant de rendre la main.
- `ALERTE` : point à juger. Corriger, ou justifier dans le bilan (mot "simple" au sens littéral, cible à commiter, sortie réelle recopiée).
- Relancer jusqu'à zéro erreur.

Le script vérifie la longueur, les caractères, les emojis, les titres et leur ordre, le sommaire, le bloc d'état, le commentaire en tête, les liens, les ancres, les images, les blocs de code, les badges, le HTML et les motifs de données personnelles.

Le skill vérifie lui-même ce que le script ne peut pas juger :

- les commandes citées existent dans le dépôt ;
- les outils externes figurent dans les prérequis ;
- aucun secret qu'un motif ne repère pas ;
- le style (phrases courtes, mots à éviter selon le contexte) ;
- l'information encore valable n'a pas été perdue.

## Ce que le skill ne fait pas

- Il ne commit pas et ne pousse pas.
- Il ne supprime pas de contenu sans le déplacer, sauf une information périmée validée par l'utilisateur.
- Il ne modifie pas le code du projet.
- Il n'exécute pas les commandes du projet, sauf demande : il vérifie seulement qu'elles existent.
- Il ne gère pas le `CHANGELOG.md`, ni les README en plusieurs langues (`README.en.md`).
- Il ne crée pas de fichier `LICENSE` sans accord.
