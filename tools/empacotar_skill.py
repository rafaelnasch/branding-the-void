#!/usr/bin/env python3
"""Gera dist-skill/branding-the-void.zip, o pacote da skill para claude.ai e ChatGPT (Release).

O ZIP tem a pasta branding-the-void/ no topo e só o que a skill precisa para operar:
  SKILL.md, references/, agents/openai.yaml, tokens.css, tokens.json, vforms.js, vviz.js,
  os nove modelos HTML de canal, a marca (svg, png web, favicon, social, marca.json),
  texturas web, LUTs .cube, presets .xmp e receitas, o kit de SEO, o catálogo do acervo
  REESCRITO para as URLs públicas do Pages e, se o orçamento permitir, as miniaturas do acervo.

Dentro do pacote (nunca no repositório), todo caminho relativo de HTML para um arquivo de
assets/ que não viaja no ZIP (fotos do acervo, mockups, e-mail, legenda) vira URL absoluta do
GitHub Pages. O catalogo.json do pacote aponta todas as fotos para o Pages.

Falha (código 1) se: ZIP > 30 MB, soma descompactada > 25 MB, mais de 400 arquivos, algum
arquivo > 10 MB, description > 1.024 caracteres, SKILL.md com 500 linhas ou mais, nome
divergente, SKILL.md ausente no topo da pasta, mais de um SKILL.md, link relativo de SKILL.md
ou references/ para arquivo ausente no pacote. Meta: ZIP abaixo de 10 MB.

Uso:
  python3 tools/empacotar_skill.py            # gera e confere
  python3 tools/empacotar_skill.py --sem-miniaturas
"""
import argparse
import io
import json
import re
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
NOME = "branding-the-void"
PAGES = "https://rafaelnasch.github.io/branding-the-void/"
SAIDA = RAIZ / "dist-skill" / f"{NOME}.zip"
MB = 1024 * 1024
LIM_ZIP, LIM_SOMA, LIM_ARQ, LIM_N, META_ZIP = 30 * MB, 25 * MB, 10 * MB, 400, 10 * MB
ORCAMENTO_MINIATURAS = 9 * MB  # só entram se o ZIP sem elas ficar abaixo disto

KITS = ["lockup.html", "lp-template.html", "kit-social.html", "vsl-kit.html", "membros-ui.html",
        "comunicacao-m1-m8.html", "email-template.html", "artigo-template.html", "deck-template.html"]
RAIZ_ARQS = ["SKILL.md", "tokens.css", "tokens.json", "vforms.js", "vviz.js", "agents/openai.yaml"] + KITS


def lista_base():
    arqs = list(RAIZ_ARQS)
    arqs += sorted(str(p.relative_to(RAIZ)) for p in (RAIZ / "references").glob("*.md"))
    marca = RAIZ / "assets" / "brand"
    for padrao in ("svg/*.svg", "svg/cor/*.svg", "png/web/*.png", "favicon/*", "social/*.png", "social/*.svg", "marca.json"):
        arqs += sorted(str(p.relative_to(RAIZ)) for p in marca.glob(padrao) if p.is_file())
    for p in ("assets/textura/grao-240.webp", "assets/textura/grao-240-claro.webp", "assets/textura/esfera-1080.webp"):
        arqs.append(p)
    foto = RAIZ / "assets" / "foto"
    arqs += sorted(str(p.relative_to(RAIZ)) for p in foto.glob("*.cube"))
    arqs += sorted(str(p.relative_to(RAIZ)) for p in foto.glob("*.xmp"))
    arqs.append("assets/foto/receitas.md")
    arqs += sorted(str(p.relative_to(RAIZ)) for p in (RAIZ / "assets" / "seo").rglob("*") if p.is_file() and p.name != ".DS_Store")
    arqs += ["assets/foto/acervo/catalogo.json", "assets/foto/acervo/LEIA-ME.md"]
    faltam = [a for a in arqs if not (RAIZ / a).is_file()]
    if faltam:
        sys.exit("arquivos esperados que não existem: " + ", ".join(faltam))
    return list(dict.fromkeys(arqs))


def miniaturas():
    return sorted(str(p.relative_to(RAIZ)) for p in (RAIZ / "assets/foto/acervo").glob("*_thumb.webp"))


REF_ASSET = re.compile(r"(?<![\w/.:-])assets/[A-Za-z0-9_./-]*")


def reescreve_html(texto, no_pacote):
    """Caminho relativo para algo de assets/ que não está no pacote vira URL absoluta do Pages."""
    trocas = 0

    def troca(m):
        nonlocal trocas
        cam = m.group(0)
        if cam.startswith("assets/foto/acervo/"):
            fica = False  # fotos do acervo sempre pelo Pages (o pacote leva só o catálogo e miniaturas)
        else:
            # arquivo do pacote, pasta do pacote ou prefixo montado no código ('.../void-' + cor + '.svg')
            limpo = cam.rstrip(".,")
            fica = limpo in no_pacote or any(a.startswith(limpo) for a in no_pacote)
        if fica:
            return cam
        trocas += 1
        return PAGES + cam

    texto = REF_ASSET.sub(troca, texto)
    # kit-social e vsl-kit montam a pasta do acervo por partes (para o autocontido.py não embutir tudo)
    junta = "['assets', 'foto', 'acervo', ''].join('/')"
    if junta in texto:
        trocas += texto.count(junta)
        texto = texto.replace(junta, "'" + PAGES + "assets/foto/acervo/'")
    return texto, trocas


def catalogo_absoluto(texto):
    dados = json.loads(texto)

    def anda(o):
        if isinstance(o, dict):
            return {k: anda(v) for k, v in o.items()}
        if isinstance(o, list):
            return [anda(v) for v in o]
        if isinstance(o, str) and o.startswith("assets/"):
            return PAGES + o
        return o

    dados = anda(dados)
    dados["_pacote"] = ("Catálogo do pacote da skill: as fotos não viajam no ZIP e são servidas pelo GitHub Pages "
                        "nas URLs absolutas abaixo. No repositório, o mesmo catálogo usa caminhos relativos.")
    return json.dumps(dados, ensure_ascii=False, indent=2) + "\n"


def monta(arqs):
    conteudo = {}
    trocas = {}
    for a in arqs:
        b = (RAIZ / a).read_bytes()
        if a.endswith(".html"):
            t, n = reescreve_html(b.decode("utf-8"), set(arqs))
            b, trocas[a] = t.encode("utf-8"), n
        elif a == "assets/foto/acervo/catalogo.json":
            b = catalogo_absoluto(b.decode("utf-8")).encode("utf-8")
        conteudo[a] = b
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for a, b in conteudo.items():
            info = zipfile.ZipInfo(f"{NOME}/{a}", date_time=(2026, 10, 6, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, b, compresslevel=9)
    return buf.getvalue(), conteudo, trocas


def confere(zip_bytes, conteudo):
    erros = []
    soma = sum(len(b) for b in conteudo.values())
    if len(zip_bytes) > LIM_ZIP:
        erros.append(f"ZIP com {len(zip_bytes)/MB:.2f} MB (limite 30 MB)")
    if soma > LIM_SOMA:
        erros.append(f"descompactado com {soma/MB:.2f} MB (limite 25 MB)")
    if len(conteudo) > LIM_N:
        erros.append(f"{len(conteudo)} arquivos (limite 400)")
    for a, b in conteudo.items():
        if len(b) > LIM_ARQ:
            erros.append(f"{a} com {len(b)/MB:.2f} MB (limite 10 MB por arquivo)")
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
        nomes = z.namelist()
    topos = {n.split("/")[0] for n in nomes}
    if topos != {NOME}:
        erros.append(f"pasta de topo diferente de {NOME}: {sorted(topos)}")
    skills = [n for n in nomes if n.endswith("SKILL.md")]
    if len(skills) != 1:
        erros.append(f"{len(skills)} arquivos SKILL.md no pacote (tem de ser um)")
    if f"{NOME}/SKILL.md" not in nomes:
        erros.append("SKILL.md ausente no topo da pasta")
    skill = conteudo.get("SKILL.md", b"").decode("utf-8")
    fm = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
    nome = desc = ""
    if fm:
        m = re.search(r"^name:\s*(.+)$", fm.group(1), re.M)
        nome = m.group(1).strip().strip("\"'") if m else ""
        m = re.search(r"^description:\s*(.+)$", fm.group(1), re.M)
        desc = m.group(1).strip() if m else ""
        if desc[:1] in "\"'" and desc[-1:] == desc[:1]:
            desc = desc[1:-1]
    if nome != NOME:
        erros.append(f"name '{nome}' diferente de {NOME}")
    if not 1 <= len(desc) <= 1024:
        erros.append(f"description com {len(desc)} caracteres (limite 1.024)")
    linhas = skill.count("\n") + (0 if skill.endswith("\n") else 1)
    if linhas >= 500:
        erros.append(f"SKILL.md com {linhas} linhas (limite: menos de 500)")
    for a, b in conteudo.items():
        if not (a == "SKILL.md" or (a.startswith("references/") and a.endswith(".md"))):
            continue
        base = Path(a).parent
        for alvo in re.findall(r"\]\(([^)\s]+)\)", b.decode("utf-8")):
            if re.match(r"(https?:|mailto:|#)", alvo):
                continue
            destino = (base / alvo.split("#")[0]).as_posix()
            partes = []
            for p in destino.split("/"):
                if p == "..":
                    if partes:
                        partes.pop()
                    else:
                        partes.append("..")
                elif p not in ("", "."):
                    partes.append(p)
            if "/".join(partes) not in conteudo:
                erros.append(f"{a}: link relativo para arquivo ausente no pacote: {alvo}")
    return erros, soma, linhas, len(desc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sem-miniaturas", action="store_true")
    args = ap.parse_args()
    arqs = lista_base()
    zip_bytes, conteudo, trocas = monta(arqs)
    com_mini = False
    if not args.sem_miniaturas and len(zip_bytes) < ORCAMENTO_MINIATURAS:
        teste = monta(arqs + miniaturas())
        if len(teste[0]) < META_ZIP and len(teste[1]) <= LIM_N:
            zip_bytes, conteudo, trocas = teste
            com_mini = True
    erros, soma, linhas, ndesc = confere(zip_bytes, conteudo)
    SAIDA.parent.mkdir(exist_ok=True)
    SAIDA.write_bytes(zip_bytes)
    maior = max(conteudo.items(), key=lambda kv: len(kv[1]))
    print(f"pacote: {SAIDA.relative_to(RAIZ)}")
    print(f"ZIP {len(zip_bytes)/MB:.2f} MB · descompactado {soma/MB:.2f} MB · {len(conteudo)} arquivos · "
          f"maior arquivo {maior[0]} ({len(maior[1])/MB:.2f} MB)")
    print(f"SKILL.md {linhas} linhas · description {ndesc} caracteres · miniaturas do acervo: {'sim' if com_mini else 'não'}")
    print("caminhos de HTML reescritos para o Pages: " + ", ".join(f"{k} {v}" for k, v in trocas.items() if v))
    if len(zip_bytes) >= META_ZIP:
        print(f"aviso: ZIP acima da meta de 10 MB")
    if erros:
        for e in erros:
            print("  FALHA:", e)
        sys.exit(1)
    print("limites atendidos")


if __name__ == "__main__":
    main()
