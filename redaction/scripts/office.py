#!/usr/bin/env python3
"""Lit et réécrit le texte des fichiers .odt et .docx sans toucher à la mise en page.

Usage :
    python3 office.py extraire <fichier>            # écrit les paragraphes en JSON sur la sortie standard
    python3 office.py appliquer <fichier> <json>    # écrit une copie <nom>_redaction.<ext>

Dans le texte extrait, un passage dont l'apparence diffère du reste du paragraphe
(gras, italique, police...) est entouré de balises {1}...{/1}. Pour garder cette
mise en forme, il suffit de laisser les balises autour des mots concernés dans le
nouveau texte. Les différences invisibles (langue, historique d'édition) sont ignorées.

Caractères spéciaux dans le texte : \\t tabulation, \\n retour à la ligne, \\f saut de page (.docx).

Un paragraphe qui contient un élément que l'outil ne sait pas reconstruire (lien,
note de bas de page, image, champ) est marqué "modifiable": false et n'est jamais
réécrit. Les sommaires et les zones de texte des .docx ne sont pas extraits.
L'original n'est jamais modifié.

Dépendance : lxml.
"""

import copy
import json
import re
import sys
import zipfile
from pathlib import Path

from lxml import etree

TEXT = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
OFFICE = "urn:oasis:names:tc:opendocument:xmlns:office:1.0"
STYLE = "urn:oasis:names:tc:opendocument:xmlns:style:1.0"
T = "{%s}" % TEXT
S = "{%s}" % STYLE
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"

MARQUE = re.compile(r"\{(\d+)\}(.*?)\{/\1\}", re.S)


def lire_xml(chemin, interne):
    with zipfile.ZipFile(chemin) as z:
        return etree.fromstring(z.read(interne))


def ecrire_copie(chemin, interne, racine):
    chemin = Path(chemin)
    sortie = chemin.with_name(chemin.stem + "_redaction" + chemin.suffix)
    contenu = etree.tostring(racine, xml_declaration=True, encoding="UTF-8", standalone=True)
    with zipfile.ZipFile(chemin) as zin, zipfile.ZipFile(sortie, "w") as zout:
        for item in zin.infolist():
            data = contenu if item.filename == interne else zin.read(item.filename)
            # le fichier mimetype d'un .odt doit rester non compressé
            mode = zipfile.ZIP_STORED if item.filename == "mimetype" else zipfile.ZIP_DEFLATED
            zout.writestr(item, data, compress_type=mode)
    return sortie


def decouper(segments):
    """Fusionne les segments voisins de même apparence et repère l'apparence dominante.

    segments : liste de (cle_visuelle, modele, texte). Renvoie le texte balisé,
    la liste des modèles balisés et le modèle de l'apparence dominante.
    """
    fusion = []
    for cle, modele, texte in segments:
        if fusion and fusion[-1][0] == cle:
            fusion[-1][2] += texte
        else:
            fusion.append([cle, modele, texte])
    longueurs = {}
    for cle, _, texte in fusion:
        longueurs[cle] = longueurs.get(cle, 0) + len(texte.strip())
    base = max(longueurs, key=longueurs.get) if longueurs else None
    modele_base = next((m for c, m, _ in fusion if c == base), None)
    morceaux, formats = [], []
    for cle, modele, texte in fusion:
        if cle == base or not texte.strip():
            morceaux.append(texte)
        else:
            formats.append(modele)
            n = len(formats)
            morceaux.append("{%d}%s{/%d}" % (n, texte, n))
    return "".join(morceaux), formats, modele_base


def pieces(texte, formats, modele_base):
    """Découpe le nouveau texte en (modèle, texte) selon les balises."""
    pos = 0
    for m in MARQUE.finditer(texte):
        yield modele_base, texte[pos:m.start()]
        n = int(m.group(1))
        yield (formats[n - 1] if 0 < n <= len(formats) else modele_base), m.group(2)
        pos = m.end()
    yield modele_base, texte[pos:]


# Fichiers .odt

ODT_SIMPLES = {T + "s", T + "tab", T + "line-break", T + "soft-page-break"}
ODT_ANCRES = {T + "bookmark", T + "bookmark-start", T + "bookmark-end", T + "reference-mark"}
ODT_INDEX = {T + "table-of-content", T + "alphabetical-index", T + "bibliography",
             T + "illustration-index", T + "table-index", T + "object-index", T + "user-index"}
INVISIBLES = re.compile(r"rsid|language|country|script|hyphenat|letter-kerning")


class Odt:
    interne = "content.xml"

    def __init__(self, racine):
        self.racine = racine
        self.cles = {}
        for st in racine.iter(S + "style"):
            props = st.find(S + "text-properties")
            attrs = {} if props is None else {k: v for k, v in props.attrib.items()
                                               if not INVISIBLES.search(k)}
            self.cles[st.get(S + "name")] = tuple(sorted(attrs.items()))

    def paragraphes(self):
        corps = self.racine.find("{%s}body" % OFFICE)
        for p in corps.iter(T + "p", T + "h"):
            if not any(a.tag in ODT_INDEX for a in p.iterancestors()):
                yield p

    @staticmethod
    def simple(el):
        if el.tag == T + "s":
            return " " * int(el.get(T + "c", "1"))
        return {T + "tab": "\t", T + "line-break": "\n"}.get(el.tag, "")

    def lire(self, p):
        modifiable = True
        segments = [((), None, p.text or "")]
        for enfant in p:
            if enfant.tag == T + "span":
                nom = enfant.get(T + "style-name")
                texte = [enfant.text or ""]
                for e in enfant:
                    if e.tag in ODT_SIMPLES:
                        texte.append(self.simple(e))
                    else:
                        modifiable = False
                    texte.append(e.tail or "")
                segments.append((self.cles.get(nom, ()), nom, "".join(texte)))
            elif enfant.tag in ODT_SIMPLES:
                segments.append(((), None, self.simple(enfant)))
            elif enfant.tag not in ODT_ANCRES:
                modifiable = False
            segments.append(((), None, enfant.tail or ""))
        texte, formats, base = decouper(segments)
        return texte, (formats, base), modifiable

    @staticmethod
    def ajouter(parent, texte, debut_ligne):
        """Ajoute du texte en gardant tabulations, retours à la ligne et espaces significatifs."""
        def brut(s):
            if len(parent):
                parent[-1].tail = (parent[-1].tail or "") + s
            else:
                parent.text = (parent.text or "") + s

        for m in re.finditer(r"\t|\n| +|[^\t\n ]+", texte):
            bout = m.group()
            suite = texte[m.end():m.end() + 1]
            if bout == "\t":
                etree.SubElement(parent, T + "tab")
            elif bout == "\n":
                etree.SubElement(parent, T + "line-break")
                debut_ligne = True
                continue
            elif bout[0] == " " and (len(bout) > 1 or debut_ligne or suite in ("", "\n")):
                # un espace en début de ligne, en fin de ligne ou répété serait ignoré par LibreOffice
                s = etree.SubElement(parent, T + "s")
                if len(bout) > 1:
                    s.set(T + "c", str(len(bout)))
            else:
                brut(bout)
            debut_ligne = False
        return debut_ligne

    def ecrire(self, p, texte, contexte):
        formats, base = contexte
        ancres = [copy.deepcopy(e) for e in p if e.tag in ODT_ANCRES]
        for e in list(p):
            p.remove(e)
        p.text = None
        for a in ancres:
            a.tail = None
            p.append(a)
        debut = True
        for modele, morceau in pieces(texte, formats, base):
            if not morceau:
                continue
            if modele is None:
                debut = self.ajouter(p, morceau, debut)
            else:
                span = etree.SubElement(p, T + "span")
                span.set(T + "style-name", modele)
                debut = self.ajouter(span, morceau, debut)


# Fichiers .docx

DOCX_RUN = {W + "t", W + "rPr", W + "tab", W + "br", W + "lastRenderedPageBreak"}
DOCX_PARA = {W + "pPr", W + "r", W + "proofErr", W + "bookmarkStart", W + "bookmarkEnd"}
DOCX_INVISIBLES = {W + "lang", W + "noProof", W + "rFonts", W + "szCs", W + "bCs", W + "iCs"}


class Docx:
    interne = "word/document.xml"

    def __init__(self, racine):
        self.racine = racine

    def paragraphes(self):
        corps = self.racine.find(W + "body")
        for p in corps.iter(W + "p"):
            # les sommaires (sdt) et les zones de texte (présentes en deux copies) ne sont pas traités
            if not any(a.tag in (W + "sdt", W + "txbxContent") or a.tag.endswith("}AlternateContent")
                       for a in p.iterancestors()):
                yield p

    @staticmethod
    def cle(rpr):
        if rpr is None:
            return ()
        return tuple(sorted(etree.tostring(e) for e in rpr if e.tag not in DOCX_INVISIBLES))

    @staticmethod
    def texte_run(r):
        morceaux = []
        for e in r:
            if e.tag == W + "t":
                morceaux.append(e.text or "")
            elif e.tag == W + "tab":
                morceaux.append("\t")
            elif e.tag == W + "br":
                morceaux.append("\f" if e.get(W + "type") == "page" else "\n")
        return "".join(morceaux)

    def lire(self, p):
        modifiable = all(e.tag in DOCX_PARA for e in p)
        segments = []
        for r in p.iter(W + "r"):
            if any(e.tag not in DOCX_RUN for e in r):
                modifiable = False
            rpr = r.find(W + "rPr")
            segments.append((self.cle(rpr), rpr, self.texte_run(r)))
        texte, formats, base = decouper(segments)
        return texte, (formats, base), modifiable

    @staticmethod
    def run(p, texte, rpr):
        r = etree.SubElement(p, W + "r")
        if rpr is not None:
            r.append(copy.deepcopy(rpr))
        for bout in re.split(r"(\t|\n|\f)", texte):
            if bout == "\t":
                etree.SubElement(r, W + "tab")
            elif bout == "\n":
                etree.SubElement(r, W + "br")
            elif bout == "\f":
                etree.SubElement(r, W + "br").set(W + "type", "page")
            elif bout:
                t = etree.SubElement(r, W + "t")
                t.text = bout
                t.set(XML_SPACE, "preserve")

    def ecrire(self, p, texte, contexte):
        formats, base = contexte
        for e in list(p):
            if e.tag in (W + "r", W + "proofErr"):
                p.remove(e)
        for modele, morceau in pieces(texte, formats, base):
            if morceau:
                self.run(p, morceau, modele)


def charger(chemin):
    ext = Path(chemin).suffix.lower()
    classes = {".odt": Odt, ".docx": Docx}
    if ext not in classes:
        sys.exit("Format non pris en charge : %s (attendu .odt ou .docx)" % ext)
    classe = classes[ext]
    return classe(lire_xml(chemin, classe.interne))


def extraire(chemin):
    doc = charger(chemin)
    sortie = []
    for i, p in enumerate(doc.paragraphes()):
        texte, _, modifiable = doc.lire(p)
        if texte.strip():
            sortie.append({"id": i, "texte": texte, "modifiable": modifiable})
    json.dump(sortie, sys.stdout, ensure_ascii=False, indent=1)
    print()


def appliquer(chemin, fichier_json):
    doc = charger(chemin)
    corrections = {c["id"]: c["texte"] for c in json.loads(Path(fichier_json).read_text(encoding="utf-8"))}
    ignores = []
    for i, p in enumerate(doc.paragraphes()):
        if i not in corrections:
            continue
        texte, contexte, modifiable = doc.lire(p)
        if corrections[i] == texte:
            continue
        if not modifiable:
            ignores.append(i)
            continue
        doc.ecrire(p, corrections[i], contexte)
    sortie = ecrire_copie(chemin, doc.interne, doc.racine)
    print("Copie écrite : %s" % sortie)
    if ignores:
        print("Paragraphes non modifiables, laissés tels quels : %s" % ", ".join(map(str, ignores)))


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "extraire":
        extraire(sys.argv[2])
    elif len(sys.argv) == 4 and sys.argv[1] == "appliquer":
        appliquer(sys.argv[2], sys.argv[3])
    else:
        sys.exit(__doc__)
