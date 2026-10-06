#!/usr/bin/env python3
"""Monta o brand-book.html da The VOID a partir dos fragmentos e roda o gate de montagem.

Uso:
  python3 tools/montar_brand_book.py                 # casca + f01..f08 -> brand-book.html
  python3 tools/montar_brand_book.py --exemplo       # inclui _fragmentos/exemplo-secao.html (prévia da casca)
  python3 tools/montar_brand_book.py --saida previa.html

O que faz:
  1. Lê _fragmentos/00-casca.html e troca o marcador <!--SECOES--> pelos fragmentos na ordem f01 a f08.
  2. Antes da primeira seção de cada parte (II a IX) insere a Cartela de Parte.
  3. Confere: seções s01 a s36 presentes, em ordem e uma vez; ids únicos; links internos resolvidos;
     nenhum travessão (U+2014, U+2013); nenhum TATOO; um h1; "Em um minuto" com 2 a 4 itens e
     "Fontes desta seção" em toda seção; claims proibidos só dentro de data-exemplo="proibido";
     nenhum "The VOID" digitado em classe de título; nenhum var() em atributo SVG; nenhum mask:url(#;
     todo HEX de CSS e SVG pertence a tokens.json; CSS de fragmento com até 120 linhas e classes fNN-.
  4. Imprime o relatório. Sai com código 0 só sem erros.
"""
import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FRAG = RAIZ / "_fragmentos"
MARCADOR = "<!--SECOES-->"
FRAGMENTOS = ["f%02d" % n for n in range(1, 9)]
SECOES = ["s%02d" % n for n in range(1, 37)]

PARTES = {
    "I": ("O que a The VOID é", ["s01", "s02", "s03", "s04", "s05"], None),
    "II": ("As leis", ["s06", "s07"], ("AS", "leis")),
    "III": ("Marca", ["s08", "s09", "s10", "s11", "s12"], ("A", "marca")),
    "IV": ("Cor", ["s13", "s14", "s15", "s16"], ("A", "cor")),
    "V": ("Tipografia", ["s17", "s18", "s19", "s20"], ("AS TRÊS", "vozes")),
    "VI": ("Recursos assinatura e sistema", ["s21", "s22", "s23", "s24", "s25", "s26", "s27", "s28"], ("RECURSOS E", "sistema")),
    "VII": ("Imagem", ["s29", "s30"], ("A", "imagem")),
    "VIII": ("Voz e conformidade", ["s31", "s32", "s33"], ("VOZ E", "conformidade")),
    "IX": ("Canais", ["s34", "s35", "s36"], ("OS", "canais")),
}
NOMES_SECAO = {
    "s01": "Capa e como usar este manual", "s02": "A plataforma", "s03": "O manifesto",
    "s04": "Para quem falamos", "s05": "A ideia: Sala Escura", "s06": "As oito leis",
    "s07": "Checklist de aprovação", "s08": "O logotipo", "s09": "Área de proteção, mínimos e fundos",
    "s10": "Usos proibidos", "s11": "Os selos", "s12": "Arquitetura de marca e co-assinatura",
    "s13": "Paleta e papéis", "s14": "Contraste calculado", "s15": "Orçamento de área e regra por produto",
    "s16": "Modo Leitura", "s17": "As três vozes", "s18": "Registros do Archivo e regra de largura",
    "s19": "Escalas: documento, peça e vídeo", "s20": "A voz em off e regras gerais",
    "s21": "Grão, Esfera, Eco e Janela de Luz", "s22": "Véu, Cinemascope, Corte do Logo e Cartela",
    "s23": "Palavra Sensível, Órbitas e Mapa da Trilha", "s24": "Marcadores, Carimbo, Ficha e Créditos",
    "s25": "Prova, Revelação, Duotom, Anel e Assinatura Pro", "s26": "Grade, espaçamento, forma e movimento",
    "s27": "Ícones", "s28": "Dados e gráficos", "s29": "Fotografia", "s30": "Vídeo e som",
    "s31": "Voz, território e tom por canal", "s32": "Comunicação M1 a M8", "s33": "Conformidade e prova",
    "s34": "Landing page e VSL", "s35": "Redes, WhatsApp, e-mail e deck",
    "s36": "Membros, artigo, entidade e pendências",
}

TRAVESSOES = {chr(0x2014): "U+2014", chr(0x2013): "U+2013"}
CLAIMS = [
    (r"maior escola", "superlativo"), (r"\bmaior(?:es)? mercado\b", "superlativo de mercado"),
    (r"(?<![\w&])#\s?1\b", "#1"), (r"\bN[ºo°]\.?\s?1\b", "Nº 1"), (r"\bMEC\b", "MEC"),
    (r"\+\s?\d{1,3}(?:\.\d{3}|\s?mil|K)\s+(?:alunos|formados|tatuadores)\b", "número de alunos sem método"),
    (r"l[ií]der(?:es)? (?:no|do) (?:segmento|mercado)", "liderança sem prova"),
    (r"a melhor escola", "a melhor"), (r"a [uú]nica escola", "a única escola"),
    (r"\b(?:desde|EST\.?|fundada em) (?:19|20)\d\d\b", "ano de fundação [P 5]"),
    (r"\binstitui[cç][aã]o parceira\b", "certificação por instituição parceira"),
]
def claims_locais(raiz):
    """Padrões extras do arquivo local tools/claims-locais.txt (fora do git).

    Uma regra por linha: expressão regular, um TAB e o nome do achado. Linha com # é
    comentário. O arquivo guarda casos concretos de quem mantém o repositório e nunca é
    publicado; sem ele, o gate roda só com as regras genéricas acima.
    """
    arq = Path(raiz) / "tools" / "claims-locais.txt"
    regras = []
    if arq.exists():
        for linha in arq.read_text(encoding="utf-8").splitlines():
            if not linha.strip() or linha.lstrip().startswith("#") or "\t" not in linha:
                continue
            rx, nome = linha.split("\t", 1)
            regras.append((rx.strip(), nome.strip()))
    return regras


CLAIMS += claims_locais(Path(__file__).resolve().parent.parent)
CLASSES_TITULO = {"titulo-filme", "titulo-secao", "fala", "regra-titulo"}
VAZIOS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
EXCECOES_HEX = {"#21130C"}


def hex_dos_tokens():
    texto = (RAIZ / "tokens.json").read_text(encoding="utf-8")
    return {h.upper() for h in re.findall(r"#[0-9A-Fa-f]{6}\b", texto)} | EXCECOES_HEX


def cartela(parte):
    nome, ids, titulo = PARTES[parte]
    antes, off = titulo
    itens = "".join(
        '<li><a href="#%s"><span>%s</span>%s</a></li>' % (i, i[1:], NOMES_SECAO[i]) for i in ids
    )
    return (
        '\n<div class="cartela-parte" id="parte-%s" data-parte="%s">\n'
        '  <div class="wrap">\n'
        '    <p class="credito"><span data-vforms="marcador-estacao"></span><span><b>Parte %s</b> · %s · seções %s a %s</span></p>\n'
        '    <p class="titulo-filme">%s <em class="off">%s</em></p>\n'
        '    <ol class="cartela-lista">%s</ol>\n'
        "  </div>\n"
        "</div>\n"
    ) % (parte.lower(), parte, parte, nome, ids[0][1:], ids[-1][1:], antes, off, itens)


def inserir_cartelas(corpo):
    vistas = set()
    saida, pos = [], 0
    for m in re.finditer(r"<section\b[^>]*>", corpo):
        tag = m.group(0)
        mp = re.search(r'data-parte="([IVX]+)"', tag)
        if not mp:
            continue
        parte = mp.group(1)
        if parte in vistas:
            continue
        vistas.add(parte)
        if parte == "I" or parte not in PARTES:
            continue
        saida.append(corpo[pos:m.start()])
        saida.append(cartela(parte))
        pos = m.start()
    saida.append(corpo[pos:])
    return "".join(saida)


class Leitor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pilha = []
        self.ids = []
        self.hrefs = []
        self.h1 = 0
        self.claims = []
        self.titulo_void = []
        self.secoes = []  # (id, parte)
        self.sec_atual = None
        self.resumo_itens = {}
        self.fontes = set()
        self.em_resumo = False
        self.em_script = 0

    def _flags(self):
        proibido = any(f.get("proibido") for _, f in self.pilha)
        titulo = any(f.get("titulo") for _, f in self.pilha)
        return proibido, titulo

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append((a["id"], self.getpos()[0]))
        if tag == "a" and a.get("href", "").startswith("#") and len(a["href"]) > 1:
            self.hrefs.append((a["href"][1:], self.getpos()[0]))
        if tag == "h1":
            self.h1 += 1
        classes = set((a.get("class") or "").split())
        if tag == "section" and re.fullmatch(r"s\d{2}", a.get("id", "")):
            self.sec_atual = a["id"]
            self.secoes.append((a["id"], a.get("data-parte")))
            self.resumo_itens[a["id"]] = None
        if self.sec_atual and "resumo" in classes:
            self.resumo_itens[self.sec_atual] = 0
            self.em_resumo = True
        if self.sec_atual and self.em_resumo and tag == "li":
            self.resumo_itens[self.sec_atual] += 1
        if self.sec_atual and "fontes" in classes:
            self.fontes.add(self.sec_atual)
        if tag in ("script", "style"):
            self.em_script += 1
        flags = {
            "proibido": a.get("data-exemplo") == "proibido",
            "titulo": bool(classes & CLASSES_TITULO) or tag in ("h1", "h2"),
            "resumo": "resumo" in classes,
        }
        if tag not in VAZIOS:
            self.pilha.append((tag, flags))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VAZIOS and self.pilha and self.pilha[-1][0] == tag:
            self.pilha.pop()

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.em_script = max(0, self.em_script - 1)
        if tag == "section":
            self.sec_atual = None
        for i in range(len(self.pilha) - 1, -1, -1):
            if self.pilha[i][0] == tag:
                if any(f.get("resumo") for _, f in self.pilha[i:]):
                    self.em_resumo = False
                del self.pilha[i:]
                break

    def handle_data(self, data):
        if self.em_script or not data.strip():
            return
        proibido, titulo = self._flags()
        linha = self.getpos()[0]
        if not proibido:
            for rx, nome in CLAIMS:
                if re.search(rx, data, re.I if nome not in ("MEC",) else 0):
                    self.claims.append((nome, linha, data.strip()[:80]))
        if titulo and re.search(r"the\s+void", data, re.I):
            self.titulo_void.append((linha, data.strip()[:60]))


def linha_de(texto, pos):
    return texto.count("\n", 0, pos) + 1


def conferir(html, exemplo, origem_por_linha):
    erros, avisos = [], []

    def onde(linha):
        return origem_por_linha(linha)

    # travessões em qualquer lugar (texto, atributos, comentários)
    for ch, nome in TRAVESSOES.items():
        for m in re.finditer(ch, html):
            erros.append("travessão %s em %s" % (nome, onde(linha_de(html, m.start()))))
    for m in re.finditer(r"tatoo", html, re.I):
        erros.append("grafia TATOO em %s" % onde(linha_de(html, m.start())))

    p = Leitor()
    p.feed(html)

    # seções
    ids_sec = [s for s, _ in p.secoes]
    faltam = [s for s in SECOES if s not in ids_sec]
    destino = avisos if exemplo else erros
    if faltam:
        destino.append("seções ausentes (%d): %s" % (len(faltam), ", ".join(faltam)))
    vistos = [s for s in ids_sec if s in SECOES]
    if vistos != sorted(vistos):
        erros.append("seções fora de ordem: %s" % ", ".join(vistos))
    for s in set(ids_sec):
        if ids_sec.count(s) > 1:
            erros.append("seção repetida: %s" % s)
    for s, parte in p.secoes:
        if s in SECOES:
            esperado = next((k for k, v in PARTES.items() if s in v[1]), None)
            if parte != esperado:
                erros.append("%s com data-parte=%r, esperado %r" % (s, parte, esperado))
        n = p.resumo_itens.get(s)
        if n is None:
            erros.append("%s sem bloco 'Em um minuto' (.resumo)" % s)
        elif not 2 <= n <= 4:
            erros.append("%s com %d itens em 'Em um minuto' (2 a 4)" % (s, n))
        if s not in p.fontes:
            erros.append("%s sem 'Fontes desta seção' (.fontes)" % s)

    # ids únicos e links internos
    contagem = {}
    for i, ln in p.ids:
        contagem.setdefault(i, []).append(ln)
    for i, lns in contagem.items():
        if len(lns) > 1:
            erros.append("id repetido %r em %s" % (i, ", ".join(onde(l) for l in lns)))
    for alvo, ln in p.hrefs:
        if alvo not in contagem:
            (avisos if exemplo and alvo in SECOES else erros).append("link #%s sem destino (%s)" % (alvo, onde(ln)))

    if p.h1 != 1:
        erros.append("o documento tem %d h1 (esperado 1)" % p.h1)
    for nome, ln, trecho in p.claims:
        erros.append("claim proibido (%s) fora de data-exemplo=\"proibido\" em %s: %s" % (nome, onde(ln), trecho))
    for ln, trecho in p.titulo_void:
        erros.append("'The VOID' digitado em título em %s (o logotipo é arquivo): %s" % (onde(ln), trecho))

    # SVG e CSS
    for m in re.finditer(r'\b(fill|stroke|stop-color|color|flood-color)\s*=\s*"var\(', html):
        erros.append("var() em atributo SVG em %s" % onde(linha_de(html, m.start())))
    for m in re.finditer(r"mask\s*:\s*url\(\s*#", html):
        erros.append("mask:url(# em %s" % onde(linha_de(html, m.start())))

    permitidos = hex_dos_tokens()
    trechos_css = []
    for m in re.finditer(r"<style\b[^>]*>(.*?)</style>", html, re.S):
        trechos_css.append((m.start(1), m.group(1)))
    for m in re.finditer(r'\bstyle="([^"]*)"', html):
        trechos_css.append((m.start(1), m.group(1)))
    for m in re.finditer(r"<svg\b.*?</svg>", html, re.S):
        trechos_css.append((m.start(), m.group(0)))
    for base, trecho in trechos_css:
        for h in re.finditer(r"(?:#|%23)([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b", trecho):
            cor = "#" + h.group(1).upper()
            if len(cor) == 4:
                cor = "#" + "".join(c * 2 for c in cor[1:])
            if cor not in permitidos:
                erros.append("HEX fora dos tokens %s em %s" % (cor, onde(linha_de(html, base + h.start()))))

    # CSS dos fragmentos
    for m in re.finditer(r'<style\b[^>]*data-fragmento="(f\d{2})"[^>]*>(.*?)</style>', html, re.S):
        frag, css = m.group(1), m.group(2)
        linhas = [l for l in css.strip().splitlines() if l.strip()]
        if len(linhas) > 120:
            erros.append("CSS do fragmento %s com %d linhas (máximo 120)" % (frag, len(linhas)))
        sem_coment = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
        for seletor in re.findall(r"([^{}]+)\{", sem_coment):
            seletor = seletor.strip()
            if not seletor or seletor.startswith(("@", "from", "to")) or re.fullmatch(r"[\d.%,\s]+", seletor):
                continue
            for parte in seletor.split(","):
                if ("." + frag + "-") not in parte:
                    erros.append("seletor sem prefixo %s- no CSS do fragmento: %s" % (frag, parte.strip()[:60]))
    return erros, avisos, p


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--exemplo", action="store_true", help="inclui _fragmentos/exemplo-secao.html antes dos fragmentos")
    ap.add_argument("--saida", default=str(RAIZ / "brand-book.html"), help="arquivo de saída")
    args = ap.parse_args()

    casca = (FRAG / "00-casca.html").read_text(encoding="utf-8")
    if casca.count(MARCADOR) != 1:
        print("ERRO: a casca precisa ter exatamente um marcador %s" % MARCADOR)
        return 1

    partes, presentes, ausentes = [], [], []
    if args.exemplo:
        modelo = FRAG / "exemplo-secao.html"
        if not modelo.exists():
            print("ERRO: --exemplo pede _fragmentos/exemplo-secao.html, modelo local de seção que fica fora do "
                  "repositório público (.gitignore). Rode sem --exemplo ou recrie o modelo localmente.")
            return 1
        partes.append(("exemplo-secao", modelo.read_text(encoding="utf-8")))
    for f in FRAGMENTOS:
        arq = FRAG / ("%s.html" % f)
        if arq.exists():
            partes.append((f, arq.read_text(encoding="utf-8")))
            presentes.append(f)
        else:
            ausentes.append(f)

    corpo = "\n".join("<!-- fragmento %s -->\n%s" % (nome, txt.strip()) for nome, txt in partes)
    corpo = inserir_cartelas(corpo)
    antes, depois = casca.split(MARCADOR)
    html = antes + corpo + depois

    # mapa de linha da saída para a origem
    inicio_corpo = antes.count("\n") + 1
    marcas = [(inicio_corpo + corpo[:m.start()].count("\n"), m.group(1))
              for m in re.finditer(r"<!-- fragmento ([\w-]+) -->", corpo)]

    def origem(linha):
        if linha < inicio_corpo:
            return "casca linha %d" % linha
        nome, base = "casca", 0
        for ln, nm in marcas:
            if ln <= linha:
                nome, base = nm, ln
        if nome == "casca":
            return "linha %d" % linha
        if linha > inicio_corpo + corpo.count("\n"):
            return "casca (rodapé) linha %d" % (linha - inicio_corpo - corpo.count("\n") + antes.count("\n") + 1)
        return "%s linha %d" % (nome, linha - base)

    saida = Path(args.saida)
    saida.write_text(html, encoding="utf-8")
    erros, avisos, leitor = conferir(html, args.exemplo, origem)

    print("Montagem do manual da The VOID")
    print("  saída: %s (%d KB)" % (saida, len(html.encode("utf-8")) // 1024))
    print("  fragmentos: %s%s" % (", ".join(presentes) or "nenhum",
                                   "  + exemplo-secao" if args.exemplo else ""))
    if ausentes:
        print("  ausentes: %s" % ", ".join(ausentes))
    print("  seções encontradas: %d de 36" % len([s for s, _ in leitor.secoes if s in SECOES]))
    print("  ids: %d · links internos: %d" % (len(leitor.ids), len(leitor.hrefs)))
    for a in avisos:
        print("  AVISO  %s" % a)
    for e in erros:
        print("  ERRO   %s" % e)
    print("Resultado: %s (%d erros, %d avisos)" % ("aprovado" if not erros else "reprovado", len(erros), len(avisos)))
    return 0 if not erros else 1


if __name__ == "__main__":
    sys.exit(main())
