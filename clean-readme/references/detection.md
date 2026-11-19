# Détection du type et de l'état

Le skill choisit le type et l'état à partir des indices, et les annonce dans le bilan. Il ne pose la question que si le cas est ambigu.

## Les 4 types

| Type | Question à laquelle répond le README | Exemples |
|---|---|---|
| Réalisation | Qu'est-ce qui a été construit et comment ça marche ? | Jeu, carte électronique, processeur sur FPGA, serveur réseau, application, site web |
| Outil | Comment je l'installe et je m'en sers ? | Bibliothèque, outil en ligne de commande, modèle de document, thème ou modèle de site |
| Recherche | Quelle question, où en est le projet, qu'est-ce qui a été trouvé ? | Preuve de concept, rétro-ingénierie, étude expérimentale, projet d'apprentissage automatique |
| Recueil | Qu'est-ce que contient le dépôt et comment s'y retrouver ? | Rapports de TP ou de CTF, notes de cours, collection d'exercices |

## Ordre des sources

S'arrêter dès qu'une source suffit :

1. le commentaire `clean-readme` en tête du README : le type est déjà connu ;
2. ce que dit l'utilisateur ("c'est un POC", "c'est ma bibliothèque") ;
3. le README et les docs existants : vocabulaire, sections présentes ;
4. la structure du dépôt, les fichiers de configuration et l'historique git.

## Question de départage

Quand les indices ne suffisent pas : quel est le contenu principal que le lecteur vient chercher ?

| Le lecteur vient chercher... | Type |
|---|---|
| Ce qui a été construit, à voir ou à lancer | Réalisation |
| Un moyen de l'utiliser dans son propre travail | Outil |
| La réponse à une question dont on ne connaît pas encore la réponse | Recherche |
| Une collection d'éléments indépendants | Recueil |

Un projet inachevé n'est pas forcément de la recherche. Objectif connu et travail restant : Réalisation en cours. On ne sait pas encore si c'est faisable, ou comment : Recherche.

## Indices par type

- Un indice fort suffit presque à lui seul. Un indice faible ne compte que s'il s'ajoute à d'autres.
- Si deux types ont des indices forts, demander.
- Les indices qui demandent une API d'hébergement (GitHub, GitLab) ne servent que si l'information est accessible. Le skill doit fonctionner hors ligne.
- Si le dossier n'est pas un dépôt git, se passer des indices tirés de l'historique et des tags.

### Outil

- Forts :
  - paquet publiable : `pyproject.toml` ou `setup.py` avec un nom de paquet, `Cargo.toml` avec `[lib]`, `package.json` avec `bin`, `main` ou `exports` et sans `"private": true`, `go.mod` d'un module, `*.gemspec`, `pom.xml` ou `build.gradle` de bibliothèque ;
  - publication automatisée (workflow vers PyPI, npm, crates.io, Docker Hub) ;
  - modèle à réutiliser : dépôt marqué comme modèle, `cookiecutter.json`, classe ou style LaTeX (`.cls`, `.sty`), thème de site (`theme.toml` pour Hugo, `*.gemspec` de thème Jekyll) ;
  - bibliothèque d'un seul fichier d'en-tête (`.h`) pensée pour être incluse ailleurs.
- Faibles : tags de version, releases, `CHANGELOG.md`, `CONTRIBUTING.md`, dossier `examples/`, site de documentation (`mkdocs.yml`, `docs/conf.py`), tests et intégration continue, licence.

### Réalisation

- Forts :
  - matériel : KiCad (`*.kicad_pro`, `*.kicad_pcb`), Eagle (`*.sch`, `*.brd`), fichiers Gerber, modèles 3D (`*.stl`, `*.step`, FreeCAD) ;
  - FPGA : projet Vivado (`*.xpr`) ou Quartus (`*.qpf`), sources `*.vhd` ou `*.v` avec contraintes (`*.xdc`, `*.qsf`) ;
  - embarqué : `*.ino`, `platformio.ini`, Makefile visant `avr-gcc` ou `arm-none-eabi-gcc` ;
  - site web : `index.html` à la racine, configuration Hugo, Jekyll (`_config.yml`), Astro, Vite, Next, Svelte, fichier `CNAME`, workflow de déploiement GitHub Pages ;
  - application : point d'entrée unique (`main.c`, `main.py`, `src/main.rs`) sans paquet publiable, ressources (`assets/`, `sprites/`, `sounds/`), projet mobile (`AndroidManifest.xml`, `*.xcodeproj`) ;
  - service : `Dockerfile` ou `docker-compose.yml` qui lance l'application.
- Faibles : captures d'écran ou vidéo dans le dépôt, Makefile avec une cible `run`.

### Recherche

- Forts :
  - sorties d'expériences : `results/`, `runs/`, `out/`, `logs/`, `experiments/`, `outputs/`, `mlruns/`, `wandb/` ;
  - apprentissage automatique : carnets `*.ipynb`, poids de modèles (`*.pt`, `*.ckpt`, `*.h5`, `*.onnx`, `*.safetensors`), `data/` avec un jeu de données, configurations d'expériences ou de balayage de paramètres ;
  - rétro-ingénierie ou réseau : captures (`*.pcap`, `*.pcapng`), dumps de mémoire ou de firmware, projets Ghidra, IDA ou radare2, dossier `patches/` sur un projet tiers ;
  - vocabulaire dans le nom, le README ou les docs : poc, proof of concept, preuve de concept, expérimental, hypothèse, essai, benchmark, étude, investigation, reverse engineering.
- Faibles : fichiers `*.bib`, dossier `paper/` en LaTeX, scripts de mesure ou de tracé de courbes.

### Recueil

- Forts :
  - plusieurs dossiers frères de même structure interne, souvent numérotés (`session_1/`, `tp1/`, `week-01/`, `day01/`, `chapitre-3/`) ;
  - un modèle vierge à recopier (`TEMPLATE.md`, `modele.md`) ;
  - une majorité de fichiers Markdown, PDF ou de solutions indépendantes, sans point d'entrée unique ;
  - un README qui est surtout une longue liste de liens (liste "awesome").
- Faibles : vocabulaire comme writeup, solutions, notes, exercices, cours, CTF, Advent of Code, LeetCode ; un README par sous-dossier.

## Cas ambigus

| Situation | Type retenu |
|---|---|
| Site web (portfolio, site de présentation, blog, application web) | Réalisation. Le README dit ce qu'est le site, où le voir en ligne, comment le lancer en local et comment le déployer. Le contenu publié n'est pas recopié. |
| Thème ou modèle de site fait pour être réutilisé | Outil |
| Code de recherche publié pour que d'autres l'utilisent | Outil si le README sert surtout à l'utiliser, Recherche si son contenu principal est ce qui a été trouvé. |
| Preuve de concept devenue fonctionnelle et stable | Réalisation ou Outil. Proposer le changement de type. |
| Dépôt qui contient plusieurs projets indépendants | Recueil, avec un index des projets |
| Configuration personnelle (dotfiles) | Outil s'il fournit un script d'installation, Recueil sinon |
| Documentation, cours ou guide | Recueil |
| Fork modifié d'un autre projet | Même type que le projet d'origine, avec la section "Différences avec le projet d'origine" juste après le Contexte |
| Dépôt vide ou presque | Poser directement la question |

## Indices pour l'état

- ce que dit le README existant prime sur les indices suivants ;
- dépôt archivé, si l'information est accessible : Arrêté ou Terminé ;
- aucun commit depuis plus de 6 mois : En pause ou Arrêté. Demander la raison seulement si aucune source ne la donne ;
- tags de version récents et stables : Terminé ou En cours, avec la dernière version ;
- mots "WIP", "en cours", "TODO" nombreux dans le README : En cours ou Expérimental.

Commandes utiles :

```bash
git log -1 --format=%cs
git tag --sort=-creatordate | head -5
git log --oneline | wc -l
```

## Forme dans le bilan

```text
Type : Recherche (dossier runs/ avec 12 sorties d'expériences, captures .pcap, le README parle de preuve de concept).
État : En pause (dernier commit il y a 7 mois, raison donnée dans le README).
```
