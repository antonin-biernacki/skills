<!-- clean-readme: type=recueil; langue=fr; v=2 -->
# Bibliothèque de skills

Collection de skills au format Agent Skills. Chaque skill est un dossier autonome : un fichier `SKILL.md` qui décrit quand et comment l'utiliser, accompagné si besoin de fichiers de référence, de modèles et de scripts.

> **État** : En cours. Le skill clean-readme est terminé, le skill redaction est en test sur des textes réels.

## Organisation du dépôt

Un dossier par skill, à la racine. Le nom du dossier est le nom du skill.

```text
<nom-du-skill>/
    SKILL.md         # point d'entrée : déclenchement, déroulement, règles
    references/      # détails lus seulement quand ils servent
    templates/       # modèles de fichiers produits par le skill
    scripts/         # scripts appelés par le skill
```

Seul `SKILL.md` est obligatoire. Les autres dossiers n'existent que si le skill en a besoin.

## Index

| Skill | Rôle | État |
|---|---|---|
| [clean-readme](clean-readme/) | Crée, refond et met à jour le README d'un dépôt et ses fichiers annexes (feuille de route, résultats de recherche), avec un script de vérification | Terminé |
| [redaction](redaction/) | Corrige la rédaction d'un texte en français (formulations, fautes, tournures toutes faites, caractères du clavier) sans rien inventer ni perdre du fond. Traite le texte collé et les fichiers `.md`, `.txt`, `.tex`, `.odt` et `.docx` | Expérimental |

Pour redaction, les règles d'écriture et le traitement des fichiers `.odt` et `.docx` fonctionnent, mais le skill n'a pas encore été assez testé sur des textes réels. Il ne se lance que par la commande `/redaction`.

## Installation

Cloner le dépôt, puis copier le dossier du skill voulu dans le dossier de skills de l'outil, au niveau de l'utilisateur ou d'un seul projet :

```bash
git clone https://github.com/antonin-biernacki/skills.git
cp -r skills/clean-readme <dossier-des-skills>/
```

Le skill est reconnu par son fichier `SKILL.md`. Les scripts fournis ne demandent que Python 3 et sa bibliothèque standard, sauf `redaction/scripts/office.py`, qui demande aussi la bibliothèque lxml :

```bash
pip install lxml
```

## Modèle

Chaque nouveau skill suit la même forme :

- un nom en minuscules, avec des tirets, identique au nom du dossier et au champ `name` de `SKILL.md` ;
- une description qui dit ce que fait le skill et quand il doit se déclencher ;
- un `SKILL.md` court, les détails rangés dans `references/`.
