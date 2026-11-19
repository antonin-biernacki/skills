#!/usr/bin/env python3
"""Vérifie le README d'un dépôt et ses fichiers annexes selon les règles de clean-readme.

Usage : python3 verifier.py [CHEMIN_DU_DEPOT]

Affiche une ligne par problème : NIVEAU fichier:ligne [règle] message.
ERREUR : règle non respectée. ALERTE : point à vérifier à la main.
Code de sortie : 1 s'il y a au moins une erreur, 0 sinon.
"""

import os
import re
import subprocess
import sys
import unicodedata

VERSION_REGLES = 1
MAX_LIGNES = 200

# Titres de niveau 2 autorisés, par langue.
UNIVERSELS = {
    "fr": ["Avertissement", "Sommaire", "Contexte", "Différences avec le projet d'origine",
           "Limites", "Crédits", "Références", "Licence"],
    "en": ["Disclaimer", "Contents", "Context", "Differences from upstream",
           "Limitations", "Credits", "References", "License"],
}
PAR_TYPE = {
    "fr": {
        "realisation": ["Aperçu", "Fonctionnalités", "Points techniques", "Avancement",
                        "Structure du dépôt", "Matériel", "Compilation et lancement",
                        "Utilisation", "Déploiement", "Fonctionnement interne"],
        "outil": ["Installation", "Usage minimal", "Fonctionnalités", "Configuration et options",
                  "Structure du dépôt", "Contribuer"],
        "recherche": ["Question de recherche", "Avancement", "Résultats principaux", "Méthode",
                      "Reproduire", "Structure du dépôt", "Matériel", "Questions ouvertes"],
        "recueil": ["Organisation du dépôt", "Index", "Modèle", "Outils utilisés"],
    },
    "en": {
        "realisation": ["Overview", "Features", "Technical highlights", "Progress",
                        "Repository structure", "Hardware", "Build and run",
                        "Usage", "Deployment", "How it works"],
        "outil": ["Installation", "Quick start", "Features", "Configuration and options",
                  "Repository structure", "Contributing"],
        "recherche": ["Research question", "Progress", "Key results", "Method",
                      "Reproduce", "Repository structure", "Hardware", "Open questions"],
        "recueil": ["Repository layout", "Index", "Template", "Tools"],
    },
}
FIN = {"fr": ["Limites", "Crédits", "Références", "Licence"],
       "en": ["Limitations", "Credits", "References", "License"]}
SOMMAIRE = {"fr": "Sommaire", "en": "Contents"}
ETATS = {"fr": ["En cours", "Expérimental", "En pause", "Arrêté", "Terminé"],
         "en": ["In progress", "Experimental", "Paused", "Stopped", "Done"]}
ETATS_A_PRECISER = {"Expérimental", "En pause", "Arrêté", "Experimental", "Paused", "Stopped"}

ANNEXES = {
    "fr": {"roadmap": "ROADMAP.md", "resultats": "RESULTATS.md", "guide": "docs/GUIDE.md",
           "fonctionnement": "docs/FONCTIONNEMENT.md", "index": "docs/INDEX.md"},
    "en": {"roadmap": "ROADMAP.md", "resultats": "RESULTS.md", "guide": "docs/GUIDE.md",
           "fonctionnement": "docs/HOW-IT-WORKS.md", "index": "docs/INDEX.md"},
}
TITRES_ANNEXES = {
    "fr": {"roadmap": ("Feuille de route", ["Légende"]),
           "resultats": ("Résultats de recherche",
                         ["Sommaire", "Résumé", "Méthode", "Résultats", "Essais",
                          "Pistes écartées", "Questions ouvertes"])},
    "en": {"roadmap": ("Roadmap", ["Legend"]),
           "resultats": ("Research results",
                         ["Contents", "Summary", "Method", "Results", "Trials",
                          "Discarded leads", "Open questions"])},
}

EMOJIS_ROADMAP = {"⬜", "\U0001f7e1", "✅"}
LETTRES_AUTORISEES = set("àâäéèêëîïôöùûüçÿœÀÂÄÉÈÊËÎÏÔÖÙÛÜÇŸŒ²°µ€£§¤¨")
INVISIBLES = {" ", " ", " ", " ", " ", "​", "‌",
              "‍", "⁠", "﻿", "­"}
REMPLACEMENTS = {"«": '"', "»": '"', "“": '"', "”": '"', "„": '"',
                 "‘": "'", "’": "'", "–": "-", "—": "-", "…": "...",
                 "→": "->", "←": "<-", "≤": "<=", "≥": ">=", "×": "x",
                 "≠": "!=", "•": "-"}

MOTS_A_EVITER = ["puissant", "puissante", "simple", "facile", "simplement", "il suffit de",
                 "robuste", "moderne", "incontournable", "révolutionnaire",
                 "powerful", "easy", "simply", "robust", "modern", "revolutionary", "seamless"]

RE_COMMENTAIRE = re.compile(r"^<!--\s*clean-readme:\s*(.*?)\s*-->\s*$")
RE_TITRE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
RE_FENCE = re.compile(r"^\s*(```+|~~~+)\s*([^\s`]*)")
RE_LIEN = re.compile(r"(!?)\[([^\]]*)\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
RE_IMG_HTML = re.compile(r"<img\b([^>]*)>", re.I)
RE_CODE_INLINE = re.compile(r"`[^`]*`")
RE_HTML_MISE_EN_PAGE = re.compile(r"<\s*(p|div|center|table|h[1-6]|br|span|font|a)\b", re.I)
RE_BADGE = re.compile(r"shields\.io|badgen\.net|badge\.svg|/badges?/", re.I)
RE_CHEMIN_ABSOLU = re.compile(r"(/home/[A-Za-z0-9._-]+|/Users/[A-Za-z0-9._-]+|[A-Za-z]:\\Users\\[A-Za-z0-9._-]+)")
RE_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
RE_IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
RE_MAC = re.compile(r"\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b")
RE_ATTRIBUTION = re.compile(
    r"(g[ée]n[ée]r[ée]e?s?|[ée]crite?s?|r[ée]dig[ée]e?s?|co-?[ée]crite?s?)\s+(par|avec)\s+(une\s+|l')?"
    r"(ia|intelligence artificielle|chatbot|assistant)\b"
    r"|\b(generated|written|co-?authored)\s+(by|with)\s+(an?\s+)?(ai|llm|assistant)\b", re.I)
RE_MARQUES_IA = re.compile(r"\b(claude|anthropic|chatgpt|openai|copilot|gemini|llm)\b", re.I)
RE_ETAT_FR = re.compile(r"^>\s*\*\*État\*\*\s*:\s*(.+?)\s*\(mis à jour le (\d{4}-\d{2}-\d{2})"
                        r"(?:,\s*version\s+\S+\s+du\s+\d{4}-\d{2}-\d{2})?\)\.?\s*(.*)$")
RE_ETAT_EN = re.compile(r"^>\s*\*\*Status\*\*\s*:\s*(.+?)\s*\(updated (\d{4}-\d{2}-\d{2})"
                        r"(?:,\s*version\s+\S+\s+of\s+\d{4}-\d{2}-\d{2})?\)\.?\s*(.*)$")

IP_EXEMPLES = ("127.", "0.0.0.0", "255.", "192.0.2.", "198.51.100.", "203.0.113.",
               "8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1")
EMAIL_EXEMPLES = ("example.com", "example.org", "example.net", "users.noreply.github.com")


class Rapport:
    def __init__(self):
        self.lignes = []
        self.erreurs = 0
        self.alertes = 0

    def erreur(self, fichier, ligne, regle, message):
        self.erreurs += 1
        self.lignes.append(f"ERREUR {fichier}:{ligne} [{regle}] {message}")

    def alerte(self, fichier, ligne, regle, message):
        self.alertes += 1
        self.lignes.append(f"ALERTE {fichier}:{ligne} [{regle}] {message}")


def ancre(texte):
    """Calcule l'ancre d'un titre comme GitHub."""
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", texte)
    t = re.sub(r"<[^>]+>", "", t)
    t = t.replace("`", "").strip().lower()
    t = re.sub(r"[^\w\- ]", "", t)
    return t.replace(" ", "-")


def nettoyer_titre(texte):
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", texte)
    return t.replace("**", "").replace("`", "").strip()


def decouper(lignes):
    """Renvoie pour chaque ligne : (numéro, texte, dans_un_bloc_de_code, langage_du_bloc)."""
    resultat = []
    dans_bloc = False
    marque = ""
    langage = ""
    for i, ligne in enumerate(lignes, 1):
        m = RE_FENCE.match(ligne)
        if m and (not dans_bloc or m.group(1)[0] == marque[0] and len(m.group(1)) >= len(marque)):
            if not dans_bloc:
                dans_bloc, marque, langage = True, m.group(1), m.group(2)
                resultat.append((i, ligne, "ouverture", langage))
            else:
                dans_bloc = False
                resultat.append((i, ligne, "fermeture", langage))
            continue
        resultat.append((i, ligne, "code" if dans_bloc else "texte", langage))
    return resultat


def titres(decoupe):
    """Liste des titres hors blocs de code : (numéro, niveau, texte)."""
    liste = []
    for num, ligne, zone, _ in decoupe:
        if zone != "texte":
            continue
        m = RE_TITRE.match(ligne)
        if m:
            liste.append((num, len(m.group(1)), nettoyer_titre(m.group(2))))
    return liste


def ancres_du_fichier(chemin):
    try:
        with open(chemin, encoding="utf-8") as f:
            decoupe = decouper(f.read().splitlines())
    except (OSError, UnicodeDecodeError):
        return set()
    vues = {}
    resultat = set()
    for _, _, texte in titres(decoupe):
        a = ancre(texte)
        n = vues.get(a, 0)
        resultat.add(a if n == 0 else f"{a}-{n}")
        vues[a] = n + 1
    return resultat


class Git:
    def __init__(self, depot):
        self.depot = depot
        self.actif = False
        self.suivis = set()
        try:
            r = subprocess.run(["git", "-C", depot, "ls-files", "-z"], capture_output=True, check=True)
            self.suivis = {p for p in r.stdout.decode("utf-8", "replace").split("\0") if p}
            self.actif = True
        except (OSError, subprocess.CalledProcessError):
            pass

    def suivi(self, chemin_relatif):
        p = chemin_relatif.rstrip("/")
        return p in self.suivis or any(s.startswith(p + "/") for s in self.suivis)

    def ignore(self, chemin_relatif):
        r = subprocess.run(["git", "-C", self.depot, "check-ignore", "-q", chemin_relatif],
                           capture_output=True)
        return r.returncode == 0


def decrire(caracteres):
    morceaux = []
    for c in sorted(caracteres):
        remplacement = REMPLACEMENTS.get(c)
        conseil = f" -> {remplacement!r}" if remplacement else ""
        morceaux.append(f"{c!r} ({unicodedata.name(c, 'inconnu').lower()}){conseil}")
    return ", ".join(morceaux)


def verifier_caracteres(rapport, nom, decoupe, emojis_permis):
    """Un message par ligne et par sorte de problème, pour ne pas noyer le rapport."""
    for num, ligne, zone, _ in decoupe:
        invisibles, emojis, dessin, autres = set(), set(), set(), set()
        for c in ligne:
            if c in INVISIBLES:
                invisibles.add(c)
            elif ord(c) < 128 or c in LETTRES_AUTORISEES or c in emojis_permis or c == "️":
                continue
            elif "─" <= c <= "╿":
                dessin.add(c)
            elif unicodedata.category(c) == "So":
                emojis.add(c)
            else:
                autres.add(c)
        if invisibles:
            codes = ", ".join(f"U+{ord(c):04X}" for c in sorted(invisibles))
            rapport.erreur(nom, num, "caracteres", f"caractère invisible : {codes}")
        if dessin:
            rapport.erreur(nom, num, "caracteres",
                           "caractères de dessin d'arborescence : utiliser une indentation en ASCII")
        if emojis:
            if zone == "texte":
                rapport.erreur(nom, num, "emojis", f"emoji ou symbole interdit : {decrire(emojis)}")
            else:
                rapport.alerte(nom, num, "emojis",
                               f"symbole dans un bloc de code : {decrire(emojis)} ; accepté seulement dans une sortie réelle")
        if autres:
            if zone == "texte":
                rapport.erreur(nom, num, "caracteres", f"caractère hors clavier : {decrire(autres)}")
            else:
                rapport.alerte(nom, num, "caracteres",
                               f"caractère hors clavier dans un bloc de code : {decrire(autres)} ; "
                               "accepté seulement dans une sortie réelle")


def verifier_forme(rapport, nom, decoupe, depot, git, dossier_fichier):
    for num, ligne, zone, langage in decoupe:
        if zone == "ouverture" and not langage:
            rapport.erreur(nom, num, "code", "bloc de code sans langage indiqué")
        if zone == "code" and langage in ("", "bash", "sh", "shell", "zsh", "console") \
                and re.match(r"^\s*\$\s", ligne):
            rapport.erreur(nom, num, "code", "commande précédée de '$'")
        if zone != "texte":
            continue
        sans_code = RE_CODE_INLINE.sub("", ligne)
        if RE_BADGE.search(sans_code):
            rapport.erreur(nom, num, "badges", "badge interdit")
        m = RE_HTML_MISE_EN_PAGE.search(sans_code)
        if m:
            rapport.erreur(nom, num, "html", f"balise HTML de mise en page <{m.group(1)}>")
        for img in RE_IMG_HTML.finditer(sans_code):
            attrs = img.group(1)
            alt = re.search(r"\balt\s*=\s*\"([^\"]*)\"", attrs)
            if not alt or not alt.group(1).strip():
                rapport.erreur(nom, num, "images", "balise <img> sans texte alternatif")
            src = re.search(r"\bsrc\s*=\s*\"([^\"]*)\"", attrs)
            if src:
                verifier_cible(rapport, nom, num, src.group(1), True, depot, git, dossier_fichier)
        for m in RE_LIEN.finditer(sans_code):
            image, texte, cible = m.group(1) == "!", m.group(2), m.group(3)
            if image and not texte.strip():
                rapport.erreur(nom, num, "images", "image sans texte alternatif")
            verifier_cible(rapport, nom, num, cible, image, depot, git, dossier_fichier)


def verifier_cible(rapport, nom, num, cible, image, depot, git, dossier_fichier):
    if re.match(r"^[a-z][a-z0-9+.-]*:", cible, re.I):
        return
    chemin, _, fragment = cible.partition("#")
    if not chemin:
        cible_abs = os.path.join(depot, nom)
    else:
        cible_abs = os.path.normpath(os.path.join(dossier_fichier, chemin))
    relatif = os.path.relpath(cible_abs, depot)
    if relatif.startswith(".."):
        rapport.erreur(nom, num, "liens", f"lien qui sort du dépôt : {cible}")
        return
    if not os.path.exists(cible_abs):
        rapport.erreur(nom, num, "liens", f"cible inexistante : {cible}")
        return
    if git.actif and chemin:
        if git.ignore(relatif):
            rapport.erreur(nom, num, "liens", f"cible ignorée par git, le lien cassera en ligne : {cible}")
        elif not git.suivi(relatif):
            rapport.alerte(nom, num, "liens", f"cible pas encore suivie par git, à commiter : {cible}")
    if image and chemin and not relatif.replace(os.sep, "/").startswith("docs/images/"):
        rapport.alerte(nom, num, "images", f"image hors de docs/images/ : {cible}")
    if fragment and cible_abs.endswith(".md"):
        if fragment not in ancres_du_fichier(cible_abs):
            rapport.erreur(nom, num, "ancres", f"ancre introuvable : #{fragment}")


def verifier_donnees(rapport, nom, decoupe):
    for num, ligne, zone, _ in decoupe:
        if zone in ("ouverture", "fermeture"):
            continue
        for m in RE_CHEMIN_ABSOLU.finditer(ligne):
            rapport.erreur(nom, num, "donnees", f"chemin absolu local : {m.group(0)}")
        for m in RE_EMAIL.finditer(ligne):
            if not m.group(0).lower().endswith(EMAIL_EXEMPLES):
                rapport.alerte(nom, num, "donnees", f"adresse e-mail à vérifier : {m.group(0)}")
        for m in RE_IPV4.finditer(ligne):
            ip = m.group(0)
            if all(0 <= int(x) <= 255 for x in ip.split(".")) and not ip.startswith(IP_EXEMPLES):
                rapport.alerte(nom, num, "donnees", f"adresse IP à vérifier : {ip}")
        for m in RE_MAC.finditer(ligne):
            mac = m.group(0).lower()
            if mac.replace("-", ":") not in ("00:00:00:00:00:00", "ff:ff:ff:ff:ff:ff"):
                rapport.alerte(nom, num, "donnees", f"adresse MAC à vérifier : {m.group(0)}")
        if RE_ATTRIBUTION.search(ligne):
            rapport.erreur(nom, num, "ia", "mention de contenu généré par une IA")
        m = RE_MARQUES_IA.search(ligne)
        if m:
            rapport.alerte(nom, num, "ia", f"mention de '{m.group(0)}' : vérifier que ce n'est pas une attribution")


def verifier_style(rapport, nom, decoupe):
    for num, ligne, zone, _ in decoupe:
        if zone != "texte":
            continue
        sans_code = RE_CODE_INLINE.sub("", ligne).lower()
        for mot in MOTS_A_EVITER:
            if re.search(r"(?<!\w)" + re.escape(mot) + r"(?!\w)", sans_code):
                rapport.alerte(nom, num, "style",
                               f"mot à éviter '{mot}' (accepté pour un nom propre ou au sens littéral)")


def lire_commentaire(rapport, lignes):
    for i, ligne in enumerate(lignes, 1):
        if not ligne.strip():
            continue
        m = RE_COMMENTAIRE.match(ligne.strip())
        if not m:
            rapport.alerte("README.md", i, "commentaire",
                           "pas de commentaire clean-readme en première ligne (README non suivi)")
            return {}
        valeurs = {}
        for morceau in m.group(1).split(";"):
            if "=" in morceau:
                cle, _, val = morceau.partition("=")
                valeurs[cle.strip()] = val.strip()
        if valeurs.get("type") not in PAR_TYPE["fr"]:
            rapport.erreur("README.md", i, "commentaire", f"type invalide : {valeurs.get('type')!r}")
        if valeurs.get("langue") not in ("fr", "en"):
            rapport.erreur("README.md", i, "commentaire", f"langue invalide : {valeurs.get('langue')!r}")
        v = valeurs.get("v", "")
        if not v.isdigit():
            rapport.erreur("README.md", i, "commentaire", f"version des règles invalide : {v!r}")
        elif int(v) < VERSION_REGLES:
            rapport.alerte("README.md", i, "commentaire",
                           f"règles en version {v}, version actuelle {VERSION_REGLES} : proposer une refonte")
        if "licence" in valeurs and valeurs["licence"] != "non":
            rapport.erreur("README.md", i, "commentaire", "la seule valeur permise pour licence est 'non'")
        return valeurs
    return {}


def detecter_langue(titres_niv2):
    fr = sum(1 for _, _, t in titres_niv2 if t in sum(PAR_TYPE["fr"].values(), UNIVERSELS["fr"]))
    en = sum(1 for _, _, t in titres_niv2 if t in sum(PAR_TYPE["en"].values(), UNIVERSELS["en"]))
    return "en" if en > fr else "fr"


def verifier_readme(rapport, depot, git):
    chemin = os.path.join(depot, "README.md")
    if not os.path.isfile(chemin):
        rapport.erreur("README.md", 0, "fichiers", "README.md introuvable à la racine")
        return None
    with open(chemin, encoding="utf-8") as f:
        lignes = f.read().splitlines()
    if len(lignes) > MAX_LIGNES:
        rapport.erreur("README.md", len(lignes), "longueur", f"{len(lignes)} lignes, maximum {MAX_LIGNES}")

    meta = lire_commentaire(rapport, lignes)
    decoupe = decouper(lignes)
    liste = titres(decoupe)
    niv2 = [t for t in liste if t[1] == 2]
    langue = meta.get("langue") if meta.get("langue") in ("fr", "en") else detecter_langue(niv2)
    type_projet = meta.get("type") if meta.get("type") in PAR_TYPE["fr"] else None

    niv1 = [t for t in liste if t[1] == 1]
    if len(niv1) != 1:
        rapport.erreur("README.md", niv1[1][0] if len(niv1) > 1 else 1, "titres",
                       f"{len(niv1)} titre(s) de niveau 1, il en faut exactement 1")
    for num, niveau, texte in liste:
        if niveau > 3:
            rapport.erreur("README.md", num, "titres", f"titre de niveau {niveau} : jamais plus profond que 3")

    if type_projet:
        permis = set(UNIVERSELS[langue]) | set(PAR_TYPE[langue][type_projet])
    else:
        permis = set(UNIVERSELS[langue]).union(*PAR_TYPE[langue].values())
    libres = [t for t in niv2 if t[2] not in permis]
    if len(libres) > 2:
        for num, _, texte in libres:
            rapport.erreur("README.md", num, "titres",
                           f"section libre '{texte}' : {len(libres)} sections libres, maximum 2")

    fin = FIN[langue]
    noms = [t[2] for t in niv2]
    premier_fin = next((i for i, n in enumerate(noms) if n in fin), None)
    if premier_fin is not None:
        apres = noms[premier_fin:]
        positions = [fin.index(n) for n in apres if n in fin]
        if any(n not in fin for n in apres) or positions != sorted(positions):
            rapport.erreur("README.md", niv2[premier_fin][0], "ordre",
                           "la fin commune doit être la dernière, dans l'ordre : " + ", ".join(fin))

    verifier_sommaire(rapport, decoupe, niv2, langue)
    verifier_etat(rapport, decoupe, langue)

    verifier_caracteres(rapport, "README.md", decoupe, set())
    verifier_forme(rapport, "README.md", decoupe, depot, git, depot)
    verifier_donnees(rapport, "README.md", decoupe)
    verifier_style(rapport, "README.md", decoupe)
    return langue


def verifier_sommaire(rapport, decoupe, niv2, langue):
    nom_sommaire = SOMMAIRE[langue]
    autres = [t for t in niv2 if t[2] != nom_sommaire]
    sommaire = next((t for t in niv2 if t[2] == nom_sommaire), None)
    if len(autres) >= 5 and not sommaire:
        rapport.erreur("README.md", 1, "sommaire", f"{len(autres)} sections de niveau 2 : un sommaire est requis")
        return
    if not sommaire:
        return
    if len(autres) < 5:
        rapport.alerte("README.md", sommaire[0], "sommaire",
                       f"sommaire présent avec seulement {len(autres)} sections : à retirer")
    fin_sommaire = next((t[0] for t in niv2 if t[0] > sommaire[0]), 10 ** 9)
    liens = set()
    for num, ligne, zone, _ in decoupe:
        if sommaire[0] < num < fin_sommaire and zone == "texte":
            liens.update(m.group(3).lstrip("#") for m in RE_LIEN.finditer(ligne) if m.group(3).startswith("#"))
    attendus = {ancre(t[2]) for t in autres}
    for a in sorted(attendus - liens):
        rapport.erreur("README.md", sommaire[0], "sommaire", f"section absente du sommaire : #{a}")
    for a in sorted(liens - attendus):
        rapport.erreur("README.md", sommaire[0], "sommaire", f"lien du sommaire sans section de niveau 2 : #{a}")


def verifier_etat(rapport, decoupe, langue):
    regex = RE_ETAT_FR if langue == "fr" else RE_ETAT_EN
    libelle = "**État**" if langue == "fr" else "**Status**"
    for num, ligne, zone, _ in decoupe:
        if zone == "texte" and ligne.lstrip().startswith(">") and libelle in ligne:
            m = regex.match(ligne.strip())
            if not m:
                rapport.erreur("README.md", num, "etat", "bloc d'état mal formé (voir references/titres.md)")
                return
            if m.group(1) not in ETATS[langue]:
                rapport.erreur("README.md", num, "etat",
                               f"état inconnu '{m.group(1)}', valeurs permises : " + ", ".join(ETATS[langue]))
            elif m.group(1) in ETATS_A_PRECISER and not m.group(3).strip():
                rapport.erreur("README.md", num, "etat", f"l'état '{m.group(1)}' demande une précision")
            return
    rapport.erreur("README.md", 1, "etat", f"bloc d'état absent (ligne commençant par '> {libelle}')")


def verifier_annexe(rapport, depot, git, relatif, langue, cle):
    chemin = os.path.join(depot, relatif)
    if not os.path.isfile(chemin):
        return
    with open(chemin, encoding="utf-8") as f:
        decoupe = decouper(f.read().splitlines())
    emojis = EMOJIS_ROADMAP if cle == "roadmap" else set()
    verifier_caracteres(rapport, relatif, decoupe, emojis)
    verifier_forme(rapport, relatif, decoupe, depot, git, os.path.dirname(chemin))
    verifier_donnees(rapport, relatif, decoupe)
    verifier_style(rapport, relatif, decoupe)
    liste = titres(decoupe)
    for num, niveau, _ in liste:
        if niveau > 3:
            rapport.erreur(relatif, num, "titres", f"titre de niveau {niveau} : jamais plus profond que 3")
    if cle in TITRES_ANNEXES[langue]:
        titre1, permis2 = TITRES_ANNEXES[langue][cle]
        niv1 = [t for t in liste if t[1] == 1]
        if len(niv1) != 1 or niv1[0][2] != titre1:
            rapport.erreur(relatif, niv1[0][0] if niv1 else 1, "titres", f"titre de niveau 1 attendu : '{titre1}'")
        for num, niveau, texte in liste:
            if niveau == 2 and texte not in permis2:
                rapport.erreur(relatif, num, "titres", f"titre de niveau 2 non prévu : '{texte}'")


def main():
    depot = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    if not os.path.isdir(depot):
        print(f"Dossier introuvable : {depot}")
        return 2
    rapport = Rapport()
    git = Git(depot)
    langue = verifier_readme(rapport, depot, git) or "fr"
    for cle, relatif in ANNEXES[langue].items():
        verifier_annexe(rapport, depot, git, relatif, langue, cle)
    autre = "en" if langue == "fr" else "fr"
    for cle in ("resultats", "fonctionnement"):
        if os.path.isfile(os.path.join(depot, ANNEXES[autre][cle])):
            rapport.erreur(ANNEXES[autre][cle], 0, "langue",
                           f"nom de fichier en {autre} alors que le README est en {langue}")
    for ligne in rapport.lignes:
        print(ligne)
    print(f"{rapport.erreurs} erreur(s), {rapport.alertes} alerte(s)")
    return 1 if rapport.erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
