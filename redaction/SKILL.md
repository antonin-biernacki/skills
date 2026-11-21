---
name: redaction
description: Corrige la façon dont un texte français est rédigé - aucune tournure qui sonne IA, bonnes formulations, zéro faute, uniquement des caractères du clavier, phrases de longueurs variées - sans rien inventer ni rien perdre du fond. Réécrit un texte existant ou rédige à partir de documents ou de notes. Traite le texte collé et les fichiers .md, .txt, .tex, .odt et .docx. Uniquement sur appel explicite de /redaction.
disable-model-invocation: true
---

# redaction

Le skill corrige la façon dont un texte est rédigé. Le texte rendu ne sonne pas comme un texte généré par une IA, il est bien formulé, sans faute, et n'utilise que des caractères du clavier. Il est prêt à être utilisé tel quel, pour que l'utilisateur se concentre sur le contenu.

Le skill ne s'occupe que de la rédaction. Le fond, la structure, le genre du document et le ton viennent du contexte de la demande et du jugement du modèle. Les conventions évidentes d'un document restent (l'annonce du plan et la conclusion d'un rapport, la formule de politesse d'une lettre).

Le skill écrit uniquement en français. Pour un texte en anglais, le signaler et proposer le skill humanizer.

Fichier de référence, à lire avant d'écrire : `references/catalogue.md`, les tournures qui sonnent IA et leur correction.

## Entrée

Le texte, les documents ou les notes suivent l'appel, collés dans le message ou en fichier.

| Après `/redaction` | Travail |
|---|---|
| Un texte rédigé | Le réécrire |
| Une demande avec des documents, ou un texte à transformer (un mail à partir d'un rapport) | Écrire le texte demandé à partir des documents |
| Des notes (titres, puces, mots-clés) | Les rédiger en texte suivi |

Le skill pose au plus un message de questions avant d'écrire, et seulement si une information bloque. Sinon il écrit et signale les manques à la fin.

## Ordre de priorité

Quand deux règles se contredisent, la première de cette liste l'emporte :

1. ne rien inventer et ne rien perdre ;
2. orthographe, caractères et ponctuation ;
3. longueur des phrases ;
4. réécriture minimale ;
5. le reste du catalogue.

## Ne rien inventer, ne rien perdre

Simplifier se fait comme en mathématiques. Une expression simplifiée garde exactement la même valeur, elle est seulement écrite pour être plus facile à comprendre. Parfois la forme la plus claire n'est pas la plus courte.

- Aucun fait, chiffre, date, source, citation, personne, exemple ou anecdote absent de la source.
- Aucune cause, intention, priorité, opinion ou conséquence ajoutée. Reformuler, ordonner et relier deux faits de la source reste permis.
- Aucune information de la source perdue. En réécriture, chaque fait, chaque idée et chaque nuance de l'original se retrouve dans le texte rendu, éventuellement reformulé.
- Seul le pur remplissage disparaît (une formule qui ne porte aucune information, comme "il est important de noter que"). Ce qui suit la formule reste.
- Une affirmation vague mais porteuse d'une intention (un éloge de l'entreprise dans une lettre) est reformulée sobrement, pas supprimée.
- Une attribution vague ("des experts estiment") n'est jamais remplacée par une source précise.
- Si une information manque pour qu'une phrase tienne, la signaler au lieu de la compléter.

## Bien formuler

- Le mot simple plutôt que le mot recherché ("utiliser" plutôt que "tirer parti de", "est" plutôt que "constitue").
- Le fait précis de la source plutôt qu'une formule vague.
- Reformuler avant de supprimer. Une phrase maladroite, trop longue ou trop chargée est reformulée, découpée ou réordonnée. Elle n'est jamais supprimée si elle porte une information.
- Un verbe plutôt qu'une suite de noms. "La mise en place de la réalisation du prototype a permis la réduction des erreurs" devient "Le prototype, une fois réalisé, a réduit les erreurs".
- La forme active quand on sait qui agit. "Il a été décidé par l'équipe de reporter la réunion" devient "L'équipe a décidé de reporter la réunion". Si la source ne dit pas qui agit, la forme passive reste, car nommer quelqu'un serait inventer.
- Pas le même mot répété dans des phrases voisines ("permet", "ensuite", "notamment"). Le remplacer par un synonyme juste ou fusionner les phrases, sans tomber dans la variation de synonymes.
- Une proposition compacte plutôt qu'une suite de "et". Deux verbes presque synonymes coordonnés peuvent être fusionnés.
- Les phrases restent reliées entre elles. Un connecteur qui porte un vrai lien logique est gardé ("en effet", "cependant", "donc", "de plus" pour un vrai ajout). Jamais deux fois le même connecteur dans un paragraphe.
- La longueur du texte suit le contenu. Le texte n'est jamais raccourci pour lui-même, et il peut être plus long que l'original si c'est plus clair.

## Réécriture minimale

En réécriture, ne toucher que ce qui pose problème. Une phrase déjà claire est gardée mot pour mot. Le texte garde la voix de son auteur, et la structure qu'il a voulue (titres, tableaux, plan).

## Orthographe et grammaire

Corriger toujours les fautes de frappe, d'orthographe, de grammaire et de conjugaison. Le texte rendu ne perdrait aucun point en dictée, sans que le style de l'auteur change.

- Accords (participes passés, pluriels, genre), conjugaison, homophones (a / à, ou / où, ces / ses, leur / leurs).
- Accents oubliés, y compris sur les majuscules (`Etablissement` devient `Établissement`).
- Mots mal orthographiés et fautes de frappe.
- Espaces en trop ou manquants autour de la ponctuation.
- Une citation reste exacte, fautes comprises.

## Aucune trace d'IA

- Ne jamais ajouter de mention d'IA, de Claude, d'Anthropic, de ChatGPT ou de contenu généré. Une mention écrite par l'auteur (une déclaration d'usage de l'IA exigée par une consigne) fait partie de la source et reste.
- Aucun reste de conversation ("Voici une version réécrite", "J'espère que cela vous aidera").
- Aucune note du modèle dans le texte ("[à compléter]", "Note : j'ai supposé que..."). Les champs à remplir laissés par l'auteur restent.
- Aucun marqueur technique laissé par un outil (`contentReference[oaicite:2]{index=2}`, `?utm_source=chatgpt.com`).

## Longueur des phrases

Les phrases ont des longueurs variées, sans alternance mécanique. La plupart restent courtes ou moyennes, et certaines peuvent s'allonger quand l'idée le demande, tant qu'elles restent faciles à suivre.

- Aucun segment de plus de 35 mots.
- Pas de longue suite de phrases toutes courtes, ni de longue suite de phrases toutes longues.
- Les paragraphes ne font pas tous la même longueur.

Pour compter, un mot vaut 1. La virgule ne remet pas le compteur à zéro. Le point, le point d'interrogation, le point d'exclamation, le deux-points et une nouvelle puce le remettent à zéro. Le code, les commandes, les noms de fichier et les nombres ne comptent pas, ni les mots entre parenthèses. Une parenthèse reste courte (une dizaine de mots), sinon elle devient une phrase à part.

## Deux-points

Le deux-points sert seulement à annoncer une courte énumération ou quelques exemples brefs en fin de phrase, ou à introduire une liste à puces. Au milieu d'une phrase, il est remplacé :

| Usage à corriger | Remplacement | Exemple |
|---|---|---|
| Précision ou exemple | Parenthèses | "les informations périmées : contredites par le code" -> "les informations périmées (contredites par le code)" |
| Explication ou conséquence | Point et nouvelle phrase | "Pas de script : tout repose sur le modèle" -> "Pas de script. Tout repose sur le modèle." |
| Annonce d'un élément unique | Reformulation directe | "Point de départ : le skill actuel" -> "Le point de départ est le skill actuel" |
| Libellé suivi de sa valeur | Reformulation ou parenthèses | "Type : Recherche. Indices : dossier runs/" -> "Type : Recherche (dossier runs/...)" |

Exceptions : les libellés courts d'une fiche ou d'un tableau ("État : En cours"), l'objet d'un courriel, l'heure, les citations.

## Ponctuation et caractères

- Tiret long : remplacé par une virgule, des parenthèses ou un point. Jamais par un deux-points ni par `--`.
- Point-virgule : remplacé par un point ou une conjonction. Gardé seulement dans une liste à puces où chaque élément est un morceau de phrase.
- Pas de virgule avant "et" dans une énumération.
- Seuls les caractères tapables sur un clavier AZERTY sont permis, plus `œ` et les majuscules accentuées (`É`, `À`, `Ç`...).
- Interdits : guillemets français et typographiques, apostrophe courbe, tirets longs et demi-longs, points de suspension en un seul caractère, flèches, symboles mathématiques hors clavier, emojis, espaces insécables et caractères de largeur nulle.
- Remplacements : guillemets par `"`, apostrophe courbe par `'`, points de suspension par `...`, flèche par `->`, inférieur ou égal par `<=`, signe multiplié par `x`.
- Cette règle prime sur les conventions typographiques françaises (guillemets français, espace insécable avant `%` ou `€`).

## Ce qui ne change pas

- Le code, les commandes, les sorties recopiées, les formules.
- Les citations entre guillemets, fautes comprises.
- Les noms propres, chiffres, dates, liens et références.

## Fichiers

| Format | Traitement |
|---|---|
| `.md`, `.txt` | Modifié en place. Le Markdown (titres, listes, liens, blocs de code) est gardé |
| `.tex` | Modifié en place, en suivant les `\input` et `\include` |
| `.odt`, `.docx` | Copie `<nom>_redaction.<ext>` écrite avec `scripts/office.py`. L'original n'est jamais modifié |

### LaTeX

- Seul le texte rédigé change, y compris dans les arguments de commandes (`\section{...}`, `\caption{...}`, `\textbf{...}`, `\item`).
- Les commandes, environnements, formules, `\cite`, `\ref`, `\label`, chemins de figures et commentaires `%` restent tels quels.
- `---` est traité comme un tiret long. Les caractères spéciaux restent échappés (`\%`, `\&`, `\_`). Les choix de l'auteur restent (`\og`/`\fg`, `\\`, `\bigskip`).
- Une section encore vide ("À rédiger") n'est pas écrite sans demande.
- Après modification, compiler si `latexmk` ou un `Makefile` est disponible, et signaler une erreur causée par la modification.

### `.odt` et `.docx`

1. `python3 <dossier du skill>/scripts/office.py extraire <fichier> > paragraphes.json` (dans un dossier temporaire).
2. Réécrire le champ `texte` de chaque paragraphe modifiable. Garder les balises `{1}...{/1}` autour des mots dont elles portent la mise en forme (gras, italique). Garder `\t`, `\n` et `\f` là où ils ont un sens. Ne pas changer les `id`, et retirer du JSON les paragraphes inchangés.
3. `python3 <dossier du skill>/scripts/office.py appliquer <fichier> paragraphes.json` écrit la copie `<nom>_redaction.<ext>`.
4. Signaler les paragraphes non modifiables (liens, notes, images, champs) et, pour un `.docx`, que les zones de texte ne sont pas traitées.

La fonction "Comparer le document" de LibreOffice ou de Word montre les changements entre l'original et la copie.

## Déroulement

1. Lire `references/catalogue.md`, puis le texte, les documents ou les notes en entier.
2. Écrire ou réécrire en suivant ces règles. Le catalogue liste des signaux faibles : une tournure est corrigée quand elle s'accumule ou sonne creux, pas à chaque occurrence.
3. Vérifier :
   - aucune information inventée, aucune information perdue (en réécriture, reprendre l'original phrase par phrase) ;
   - aucune trace d'IA, aucun motif du catalogue ;
   - aucun deux-points au milieu d'une phrase, aucun caractère hors clavier, aucune faute ;
   - aucun segment de plus de 35 mots, des longueurs de phrases variées ;
   - jamais deux fois le même connecteur dans un paragraphe ;
   - pas de style nominal, pas de voix passive quand on sait qui agit, pas de mot répété dans des phrases voisines ;
   - le texte n'a pas été raccourci au-delà du remplissage retiré.
4. Relire une dernière fois en se demandant ce qui sonne encore IA, et le corriger, toujours sans rien inventer ni perdre.

## Sortie

1. Le texte final, complet et prêt à être utilisé, ou le chemin du fichier modifié. Pas de brouillon ni d'audit.
2. Après le texte, et seulement s'il y en a, quelques lignes sur le fond, jamais sur la forme :
   - les informations manquantes ou les passages impossibles à écrire sans inventer ;
   - une information qu'il a fallu retirer (rare).

Les corrections de forme ne sont pas listées. Les remarques sont dans la réponse, jamais dans le texte rendu.

## Apprendre des corrections

Quand l'utilisateur renvoie sa version corrigée d'un texte produit par le skill, comparer les deux versions. Les écarts qui reviennent ou qui traduisent un choix de formulation sont proposés comme règle à ajouter dans la partie "Appris des corrections" de `references/catalogue.md`, après accord de l'utilisateur. Les fautes de frappe ou d'orthographe de sa version sont corrigées et ne deviennent jamais une règle.
