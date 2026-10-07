#!/usr/bin/env python3
"""Confere a skill (SKILL.md + references/*.md) contra tokens.json, a especificação Agent Skills
e, se o caminho for passado, a especificação Sala Escura.

Limites (Agent Skills, agentskills.io/specification, e Claude):
  0. frontmatter só com campos da especificação; name = nome da pasta, minúsculas e hífen, até 64;
     description de 1 a 1.024 caracteres (meta 600 a 900) começando pelo caso de uso e com os gatilhos;
     SKILL.md com menos de 500 linhas; toda referência em references/ citada no SKILL.md; todo link
     relativo de SKILL.md e references/ aponta para arquivo que existe; nenhum travessão.

O que compara (no texto somado de SKILL.md e references/):
  1. todo HEX citado existe no tokens.json (ou é um véu calculado da tabela de contraste);
  2. todo par "Nome `#HEX`" e toda linha "`--token` Nome | `#HEX`" bate com o token de mesmo nome;
  3. os registros do Archivo (peso, largura, entreletra, entrelinha);
  4. a escala de documento (computador e celular);
  5. mínimos da marca, proteção, grão, véus, durações e curvas de movimento, escala de espaço,
     trilha (raios, tangência, ângulo do Pro), link do Google Fonts e tema por produto;
  6. as razões de contraste (pares por nome) contra a tabela 3.4 da especificação, quando o
     caminho dela é passado em --spec.

Uso:
  python3 tools/conferir_skill.py [--spec caminho/da/spec.md]
Sai com 1 se encontrar qualquer divergência.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SKILL_MD = (RAIZ / "SKILL.md").read_text(encoding="utf-8")
REFS = sorted((RAIZ / "references").glob("*.md"))
# o texto conferido é o SKILL.md seguido das referências (a ordem importa só para achar blocos)
SKILL = SKILL_MD + "\n" + "\n".join(r.read_text(encoding="utf-8") for r in REFS)
TOK = json.loads((RAIZ / "tokens.json").read_text(encoding="utf-8"))
falhas, ok = [], 0


def conf(cond, msg):
    global ok
    if cond:
        ok += 1
    else:
        falhas.append(msg)


def val(o):
    return o["$value"] if isinstance(o, dict) and "$value" in o else o


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn").lower()


# ---------- 0. limites da especificação Agent Skills ----------
CAMPOS_SPEC = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
fm = re.match(r"^---\n(.*?)\n---\n", SKILL_MD, re.S)
conf(bool(fm), "SKILL.md sem frontmatter YAML no topo")
campos = {}
if fm:
    for linha in fm.group(1).split("\n"):
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", linha)
        if m:
            campos[m.group(1)] = m.group(2).strip()
for c in campos:
    conf(c in CAMPOS_SPEC, f"frontmatter: campo '{c}' fora da especificação")
nome = campos.get("name", "").strip('"\'')
conf(nome == "branding-the-void", f"name '{nome}' diferente de branding-the-void")
conf(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", nome or "-") is not None and len(nome) <= 64, "name fora do padrão (minúsculas, hífen, até 64)")
desc = campos.get("description", "")
if desc[:1] in "\"'" and desc[-1:] == desc[:1]:
    desc = desc[1:-1]
DESC_LEN = len(desc)
conf(1 <= DESC_LEN <= 1024, f"description com {DESC_LEN} caracteres (limite 1.024)")
conf(600 <= DESC_LEN <= 900, f"description com {DESC_LEN} caracteres (meta 600 a 900)")
conf(desc.startswith("Identidade da The VOID") and "Use em todo material" in desc[:400] and "Gatilhos:" in desc[:600],
     "description deve abrir com o caso de uso e trazer os gatilhos nos primeiros 600 caracteres")
LINHAS = SKILL_MD.count("\n") + (0 if SKILL_MD.endswith("\n") else 1)
conf(LINHAS < 500, f"SKILL.md com {LINHAS} linhas (limite: menos de 500)")
for r in REFS:
    conf(f"references/{r.name}" in SKILL_MD, f"references/{r.name} não é citada no SKILL.md")
for arq, texto in [(RAIZ / "SKILL.md", SKILL_MD)] + [(r, r.read_text(encoding="utf-8")) for r in REFS]:
    for alvo in re.findall(r"\]\(([^)\s]+)\)", texto):
        if re.match(r"(https?:|mailto:|#)", alvo):
            continue
        destino = (arq.parent / alvo.split("#")[0]).resolve()
        conf(destino.exists(), f"{arq.name}: link relativo para arquivo ausente: {alvo}")
    conf(chr(0x2014) not in texto and chr(0x2013) not in texto, f"{arq.name}: travessão")

# ---------- nome visível -> HEX ----------
NOMES = {}
for grupo in ("neutro", "terracota", "terra"):
    for k, v in TOK["cor"][grupo].items():
        if k.startswith("$"):
            continue
        NOMES[k] = val(v).upper()
EST = {k: val(v).upper() for k, v in TOK["cor"]["estado"].items() if not k.startswith("$")}
VISIVEL = {
    "Nanquim": "nanquim", "Sala": "sala", "Bastidor": "bastidor", "Coxia": "coxia", "Fio": "fio",
    "Chumbo": "chumbo", "Penumbra": "penumbra", "Fumaça": "fumaca", "Pó": "po", "Cal": "cal",
    "Cinza 100": "cinza-100", "Tela": "tela", "Branco": "branco", "Névoa": "nevoa", "Ardósia": "ardosia",
    "Terracota": "terracota", "Terracota Viva": "terracota-viva", "Terracota Funda": "terracota-funda",
    "Terracota Luz": "terracota-luz", "Terracota Noite": "terracota-noite", "Areia": "areia",
    "Campo Start": "campo-start", "Caramelo": "caramelo", "Ouro Velho": "ouro-velho", "Ouro Fundo": "ouro-fundo",
    "Campo Master": "campo-master", "Couro": "couro", "Café": "cafe",
}
HEX_DE = {n: NOMES[t] for n, t in VISIVEL.items()}
HEX_DE.update({"Musgo Luz": EST["sucesso"], "Musgo": EST["sucesso-claro"], "Âmbar Fundo": EST["atencao-claro"],
               "Ferrugem Luz": EST["erro"], "Ferrugem": EST["erro-claro"]})
VEUS = {"véu 75%": "#525252", "véu 70%": "#5D5D5D", "véu 62%": "#707070", "véu 55%": "#808080", "véu 48%": "#909090"}

# 1. todo HEX conhecido
conhecidos = set(NOMES.values()) | set(EST.values()) | set(VEUS.values())
for h in sorted(set(x.upper() for x in re.findall(r"#[0-9A-Fa-f]{6}\b", SKILL))):
    conf(h in conhecidos, f"HEX {h} não está no tokens.json nem nos véus")

# 2. nome + HEX
nomes_ord = sorted(list(HEX_DE) + list(VEUS), key=len, reverse=True)
padrao = re.compile(r"(" + "|".join(re.escape(n) for n in nomes_ord) + r")\s+`(#[0-9A-Fa-f]{6})`")
for m in padrao.finditer(SKILL):
    nome, hx = m.group(1), m.group(2).upper()
    esperado = VEUS.get(nome) or HEX_DE[nome]
    conf(hx == esperado, f"{nome} citado como {hx}, token é {esperado}")
for m in re.finditer(r"`--([a-z0-9-]+)` [^|]+\| `(#[0-9A-Fa-f]{6})`", SKILL):
    t, hx = m.group(1), m.group(2).upper()
    conf(NOMES.get(t) == hx, f"--{t} citado como {hx}, token é {NOMES.get(t)}")
conf(len(set(re.findall(r"`--([a-z0-9-]+)` [^|]+\| `#", SKILL))) == 28, "as tabelas de tokens não cobrem as 28 cores de interface")

# 3. registros
REG = {"Título de Filme": "titulo-filme", "Título de Seção": "titulo-secao", "Fala": "fala", "Crédito": "credito",
       "Estreito": "estreito", "Numeral de Prova": "numeral-prova", "Numeral de Data": "numeral-data", "Botão": "botao"}


def num(t):
    t = t.strip().replace("+", "").replace(",", ".")
    try:
        return float(t.replace("em", ""))
    except ValueError:
        return t


for nome, chave in REG.items():
    m = re.search(r"^\| \*\*" + re.escape(nome) + r"\*\*[^|]*\| (\d+) \| (\d+) \| [^|]+ \| ([^|]+) \| ([^|]+) \|", SKILL, re.M)
    conf(bool(m), f"registro {nome} não encontrado")
    if not m:
        continue
    r = TOK["registro"][chave]
    conf(int(m.group(1)) == r["wght"], f"{nome}: peso {m.group(1)} != {r['wght']}")
    conf(int(m.group(2)) == r["wdth"], f"{nome}: largura {m.group(2)} != {r['wdth']}")
    if "entreletra" in r:
        conf(num(m.group(3)) == num(r["entreletra"]), f"{nome}: entreletra {m.group(3)} != {r['entreletra']}")
    conf(num(m.group(4)) == float(r["entrelinha"]), f"{nome}: entrelinha {m.group(4)} != {r['entrelinha']}")

# 4. escala de documento
DOC = {"Título de Filme": "titulo-filme", "Título de Seção": "titulo-secao", "Subtítulo": "subtitulo",
       "Intertítulo": "intertitulo", "Voz em off isolada": "off", "Chamada": "chamada", "Corpo": "corpo",
       "Apoio": "apoio", "Legenda e Crédito de Prova": "legenda", "Crédito em caixa alta": "credito",
       "Numeral de Prova": "numeral-prova", "Botão": "botao"}
bloco = SKILL[SKILL.find("**Documento e site**"):SKILL.find("**Peça de 1080 px**")]
for nome, chave in DOC.items():
    m = re.search(r"(?:^|· |\): )\**" + re.escape(nome) + r" (\d+) / (\d+)", bloco)
    conf(bool(m), f"escala de documento: {nome} não encontrado")
    if m:
        e = TOK["escala"]["documento"][chave]
        conf((int(m.group(1)), int(m.group(2))) == (e["computador"], e["celular"]),
             f"escala {nome}: {m.group(1)}/{m.group(2)} != {e['computador']}/{e['celular']}")

# 5. demais números
M = TOK["marca"]
for trecho in [f"mínimo **{M['min-horizontal-px']} px** de altura", f"mínimo **{M['min-vertical-px']} px** de altura",
               f"mínimo **{M['min-selo-completo-px']} px** de diâmetro", f"mínimo **{M['min-selo-simples-px']} px**",
               "0,352 H", "12,5% do diâmetro"]:
    conf(trecho in SKILL, f"marca: falta '{trecho}'")
G = TOK["grao"]
conf(f"**{round(G['opacidade-escuro']*100)}% no escuro" in SKILL and f"{round(G['opacidade-claro']*100)}% no claro" in SKILL, "grão: opacidades")
for chave, pct in (("veu", 70), ("veu-minimo", 62), ("veu-titulo", 55), ("veu-legenda", 75)):
    conf(f".{pct:02d}" in TOK["veu"][chave] if isinstance(TOK["veu"][chave], str) else f".{pct}" in val(TOK["veu"][chave]),
         f"véu {chave} no tokens não é {pct}%")
    conf(f"{pct}%" in SKILL, f"véu {pct}% não citado")
for k, ms in TOK["movimento"]["duracao"].items():
    conf(re.search(r"`--t-" + k + r"` " + str(ms) + r" ms", SKILL) is not None, f"movimento --t-{k} {ms} ms")
for k, c in TOK["movimento"]["curva"].items():
    conf(f"`{c}`" in SKILL, f"curva {k} {c} não citada")
esc = " · ".join(re.sub(r"px$", "", val(v)) for k, v in TOK["espaco"].items() if not k.startswith("$"))
conf(f"`{esc}`" in SKILL, f"escala de espaço {esc}")
T = TOK["trilha"]
conf("raios 65, 150, 232" in SKILL or "raios 65, 150 e 232" in SKILL, "trilha: raios")
conf(T["raios-svg"] == [65, 150, 232] and T["tangente-x"] == 250 and "x = 250" in SKILL, "trilha: tangência x = 250")
conf(f"±{T['orbita-pro-graus-da-vertical']}°" in SKILL, "órbita do Pro")
conf(T["proporcao"] in SKILL, "proporção da trilha")
conf(val(TOK["fonte"]["google-fonts"]) in SKILL, "link do Google Fonts diferente")
for k, v in TOK["grade"].items():
    if k.startswith("$"):
        continue
    v = str(val(v)).replace("px", "")
    conf(v in SKILL, f"grade {k} = {v} não citado")
# tema por produto: seta do botão
linha = re.search(r"^\| Seta do botão[^\n]+", SKILL, re.M).group(0)
cel = [c.strip() for c in linha.strip("|").split("|")][1:]
INV = {v: k for k, v in VISIVEL.items()}
for prod, c in zip(("chamado", "start", "master", "pro", "voiders"), cel):
    ref = val(TOK["estacao"][prod]["seta"]).strip("{}").split(".")[-1]
    conf(c.startswith(INV[ref]), f"seta do botão em {prod}: '{c}' != {INV[ref]}")

# 6. contraste contra a especificação
args = sys.argv[1:]
if "--spec" in args:
    spec = Path(args[args.index("--spec") + 1]).read_text(encoding="utf-8")
    sec = spec[spec.find("### 3.4"):spec.find("### 3.5")]
    REF = {}
    for m in re.finditer(r"^\| ([^`|]+?) `#[0-9A-Fa-f]{6}` \| ([^`|]+?) `#[0-9A-Fa-f]{6}` \| (\d+,\d+) \|", sec, re.M):
        REF[(m.group(1).strip(), m.group(2).strip())] = m.group(3)
    usados = 0
    for m in re.finditer(r"([A-ZÁÂÉÍÓÚÃÕÇ][A-Za-zÀ-ÿ0-9 ]*?|véu \d+%) / ([A-ZÁÂÉÍÓÚÃÕÇ][A-Za-zÀ-ÿ0-9 ]*?|véu \d+%)(?: \| | )(\d+,\d+)", SKILL):
        a, b, r = m.group(1).strip(), m.group(2).strip(), m.group(3)
        if (a, b) in REF:
            usados += 1
            conf(REF[(a, b)] == r, f"contraste {a} / {b}: {r} != spec {REF[(a, b)]}")
    conf(usados >= len(REF) - 1, f"pares conferidos {usados} de {len(REF)} da spec")
    print(f"pares de contraste conferidos contra a spec: {usados} (spec tem {len(REF)})")
    for nivel, nome, r in (("100", "Tela", "16,78"), ("86", "Cal", "13,00"), ("68", "Pó", "8,61"), ("55", "Fumaça", "5,08")):
        conf(f"{nivel} {nome}, {r}" in SKILL, f"hierarquia de luz {nivel}")

print(f"SKILL.md: {LINHAS} linhas · description: {DESC_LEN} caracteres · referências: {len(REFS)}")
print(f"{ok} verificações certas, {len(falhas)} divergências")
for f in falhas:
    print("  DIVERGE:", f)
sys.exit(1 if falhas else 0)
