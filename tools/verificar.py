#!/usr/bin/env python3
"""Gate de aceite do repositório da The VOID (plano de construção, seção 6).

Roda sobre todo HTML do repositório, menos os rascunhos (nome que começa com "_",
pasta _fragmentos/) e a pasta dist/ (gerada; use --dist para incluí-la).

  python3 tools/verificar.py                  todos os itens (1 a 10)
  python3 tools/verificar.py --rapido         só o que se confere no arquivo (1, 2, 3, 4, 6 e 7;
                                              5, 8 e 9 precisam do navegador)
  python3 tools/verificar.py --sem-lighthouse pula o item 10
  python3 tools/verificar.py lp-template.html só esses arquivos (caminho relativo à pasta
                                              atual ou à raiz; serve para peça salva em
                                              qualquer pasta, inclusive fora do repositório)
  python3 tools/verificar.py --dist           inclui dist/*.html

Itens
  1  HTML sem erro de análise (html5lib, que segue o algoritmo do navegador), um h1 por
     página, ids únicos (no arquivo e no DOM montado), links internos resolvidos (#id na
     mesma página e arquivo.html#id entre páginas do repositório) e arquivo local existente.
  2  Nenhum travessão (U+2014, U+2013) no arquivo, nos motores .js e no texto montado
     (texto visível, alt, title, aria-label, placeholder e content de ::before/::after).
  3  Todo HEX de CSS, SVG e motor pertence ao tokens.json (exceções: #21130C do duotom
     e as cores dos SVG oficiais de assets/brand/svg).
  4  Todo .par confere com tools/contraste.py (tolerância de 0,01); toda .amostra-cor
     mostra o HEX do tokens.json.
  5  Nenhum termo do território "fora" (spec 9.2) nem claim vetado (spec 11.1) no texto
     montado fora de [data-exemplo="proibido"]. Termos de gamificação só em membros-ui.
  6  Nenhum TATOO; nenhum "The VOID" digitado em texto com classe de título.
  7  Nenhum var( em atributo de apresentação SVG; nenhum mask:url(#.
  8  Playwright em 320, 390 e 1440 px: largura do documento igual à da tela.
  9  prefers-reduced-motion emulado: nenhuma animação ou transição acima de 120 ms.
 10  Lighthouse de acessibilidade 95 ou mais em brand-book, lp-template, artigo-template e
     membros-ui (se npx lighthouse existir; senão o item é pulado com aviso).
O item 11 (olhar humano das capturas) fica registrado no README.

Sai com código 0 só quando nada falha.
"""
import argparse
import functools
import http.server
import json
import os
import re
import shutil
import socketserver
import subprocess
import sys
import tempfile
import threading
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))
import contraste  # noqa: E402

LARGURAS = (320, 390, 1440)
LIGHTHOUSE = ("brand-book.html", "lp-template.html", "artigo-template.html", "membros-ui.html")
MOTORES = ("vforms.js", "vviz.js")
# Páginas sem h1 por natureza: og-1200x630.html é só a matriz da imagem de compartilhamento
# (vira PNG em tools/build_assets.py; não é lida por pessoa nem indexada).
SEM_H1 = {"og-1200x630.html"}
# Matrizes de imagem de tamanho fixo (viram PNG de 1200 por 630): a rolagem do item 8 só vale
# a partir da largura nativa.
FIXOS = {"og-1200x630.html": 1200, "og-artigo.html": 1200}
TRAVESSOES = {"\u2014": "U+2014", "\u2013": "U+2013"}
CLASSES_TITULO = {"titulo-filme", "titulo-secao", "fala", "regra-titulo"}
VAZIOS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

# spec 9.2 (fora do território) e 11.1 (claims vetados). Regex sem distinção de caixa,
# menos onde a sigla é que importa.
FORA = [
    r"\bincr[ií]ve(?:l|is)\b", r"\bmaravilhos[oa]s?\b", r"\bsimples assim\b", r"\bem poucos cliques\b",
    r"\bsonho realizado\b", r"\bempodera\w*", r"\brevolucion[aá]ri[oa]s?\b", r"\bdisruptiv[oa]s?\b",
    r"\bcurso r[aá]pido\b", r"\bcertificado f[aá]cil\b", r"\btatuagem comercial\b", r"\binfluencer de tattoo\b",
    r"\baula online gravada\b", r"\bpre[cç]o (?:baixo|acess[ií]vel)\b", r"\blearn more\b", r"\bkeep up,? baby\b",
    r"\byour own artistic\b", r"\bself (?:hero|made)\b", r"\bsaiba mais\b", r"\bclique aqui\b", r"\bcompre agora\b",
]
CLAIMS = [
    (r"maior escola", "maior escola"), (r"\bmaior(?:es)? mercado\b", "superlativo de mercado"),
    (r"(?<![\w&#])#\s?1\b", "#1"), (r"\bN[ºo°]\.?\s?1\b", "Nº 1"), (r"\bMEC\b", "MEC"),
    (r"\+\s?\d{1,3}(?:\.\d{3}|\s?mil|K)\s+(?:alunos|formados|tatuadores)\b", "número de alunos sem método"),
    (r"\bl[ií]der(?:es)? (?:no|do) (?:segmento|mercado)\b", "liderança sem prova"),
    (r"\ba melhor escola\b", "a melhor escola"), (r"\ba [uú]nica escola\b", "a única escola"),
    (r"\b\d+ anos de (?:mercado|hist[oó]ria|estrada|tradi[cç][aã]o)\b", "tempo de mercado [P 5]"),
    (r"\b(?:desde|EST\.?|fundada em) (?:19|20)\d\d\b", "ano de fundação [P 5]"),
    (r"\b(?:o )?mercado cresce \S+ ao ano\b", "dado de mercado sem fonte"),
    (r"\binstitui[cç][aã]o parceira\b", "certificação por instituição parceira"),
    (r"\bcertifica[cç][aã]o (?:via|com|pel[ao])\b", "certificação por instituição parceira"),
    (r"\bse paga (?:com|em)\b", "promessa de retorno"), (r"\bcobr(?:ei|ou|amos) R\$", "promessa de valor cobrado"),
    (r"\bdobrar o (?:seu )?valor\b", "dobrar o valor"), (r"\b\d+(?: a \d+)?\s?x mais\b", "cobrar N vezes mais"),
    (r"\b(?:desafio|imers[aã]o|programa) [^.\n]{0,40}?\d+\s?k\b", "valor em dinheiro no nome"),
    (r"[uú]ltimas vagas", "últimas vagas"),
    (r"\bs[oó] hoje\b", "só hoje"), (r"\bdiploma\b", "diploma"), (r"\bcredenciament\w+", "credenciamento"),
]
GAMIFICACAO = [r"\bn[ií]vel\b", r"\bn[ií]veis\b", r"\bXP\b", r"\bdesbloque\w*", r"\branking\b", r"\bsequ[eê]ncia de dias\b"]


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


# --------------------------------------------------------------------------- util
class Relatorio:
    def __init__(self):
        self.falhas, self.avisos, self.ok = [], [], []

    def falha(self, item, arq, msg):
        self.falhas.append((item, arq, msg))

    def aviso(self, item, arq, msg):
        self.avisos.append((item, arq, msg))


def dentro_da_raiz(p):
    try:
        Path(p).resolve().relative_to(RAIZ)
        return True
    except ValueError:
        return False


def rel(p):
    """Caminho relativo à raiz do repositório; absoluto quando o arquivo mora fora dela
    (peça salva no workspace do cliente, por exemplo)."""
    r = Path(p).resolve()
    try:
        return str(r.relative_to(RAIZ))
    except ValueError:
        return str(r)


def alvo_local(arq, ref):
    """Arquivo local apontado por src/href, ou None quando não há o que conferir no disco:
    URL externa, data:, variável de modelo ({x} ou {{x}}) e rota do site (/caminho/), que só
    existe depois de publicada."""
    u = urlparse(ref)
    if ref.startswith(("{", "//", "data:")):
        return None
    if u.scheme == "file":
        return Path(unquote(u.path)).resolve()
    if u.scheme or ref.startswith("/"):
        return None
    return (Path(arq).parent / unquote(u.path)).resolve()


def arquivos_html(escolhidos, incluir_dist):
    if escolhidos:
        saida = []
        for a in escolhidos:
            p = Path(a).expanduser()
            if not p.is_absolute():
                # primeiro a pasta de onde o comando foi chamado; depois a raiz do repositório
                p = (Path.cwd() / a) if (Path.cwd() / a).exists() else (RAIZ / a)
            if not p.exists():
                sys.exit("verificar.py: arquivo não encontrado: %s" % a)
            saida.append(p.resolve())
        return saida
    saida = []
    for p in sorted(RAIZ.rglob("*.html")):
        r = p.relative_to(RAIZ)
        partes = r.parts
        if partes[0] in (".git", "node_modules") or any(x.startswith("_") for x in partes):
            continue
        if partes[0] == "dist" and not incluir_dist:
            continue
        if partes[0] == "assets" and partes[1:2] == ("referencia-original",):
            continue
        saida.append(p)
    return saida


def linha(texto, pos):
    return texto.count("\n", 0, pos) + 1


def hex_permitidos():
    texto = (RAIZ / "tokens.json").read_text(encoding="utf-8")
    ok = {h.upper() for h in re.findall(r"#[0-9A-Fa-f]{6}\b", texto)} | {"#21130C"}
    for svg in (RAIZ / "assets/brand/svg").rglob("*.svg"):
        for h in re.findall(r"#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b", svg.read_text(encoding="utf-8", errors="ignore")):
            ok.add(normaliza_hex(h))
    return ok


def normaliza_hex(h):
    h = h.lstrip("#").upper()
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return "#" + h


def tokens_cor():
    dados = json.loads((RAIZ / "tokens.json").read_text(encoding="utf-8"))
    saida = {}

    def andar(o, nome=None):
        if isinstance(o, dict):
            if "$value" in o:
                v = o["$value"]
                if o.get("$type") == "color" and isinstance(v, str) and v.startswith("#"):
                    saida[nome] = v.upper()
                return
            for k, v in o.items():
                andar(v, k)
    andar(dados)
    return saida


# --------------------------------------------------------------------------- análise estática
class Leitor(HTMLParser):
    """Ids, links, h1, títulos com The VOID, .par e .amostra-cor (fora de script e template)."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pilha, self.ids, self.links, self.recursos = [], [], [], []
        self.h1 = 0
        self.titulo_void = []
        self.pares, self.amostras = [], []
        self.opaco = 0  # dentro de script, style, template ou textarea

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        ln = self.getpos()[0]
        if tag in ("script", "style", "template", "textarea"):
            if tag not in VAZIOS:
                self.pilha.append((tag, False))
            self.opaco += 1
            if tag == "script" and a.get("src"):
                self.recursos.append((a["src"], ln))
            return
        if self.opaco:
            return
        if "id" in a:
            self.ids.append((a["id"], ln))
        if tag == "a" and a.get("href"):
            self.links.append((a["href"], ln))
        if tag in ("img", "source", "video", "audio") and a.get("src"):
            self.recursos.append((a["src"], ln))
        if tag == "link" and a.get("href") and (a.get("rel") or "") in ("stylesheet", "icon", "apple-touch-icon", "manifest"):
            self.recursos.append((a["href"], ln))
        if tag == "h1":
            self.h1 += 1
        classes = set((a.get("class") or "").split())
        if "par" in classes and a.get("data-texto"):
            self.pares.append((a.get("data-texto"), a.get("data-fundo"), a.get("data-razao"), ln))
        if "amostra-cor" in classes and a.get("data-token"):
            self.amostras.append([a["data-token"], None, ln])
        titulo = bool(classes & CLASSES_TITULO) or tag in ("h1", "h2")
        if tag not in VAZIOS:
            self.pilha.append((tag, titulo))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VAZIOS and self.pilha and self.pilha[-1][0] == tag:
            self.pilha.pop()
            if tag in ("script", "style", "template", "textarea"):
                self.opaco -= 1

    def handle_endtag(self, tag):
        for i in range(len(self.pilha) - 1, -1, -1):
            if self.pilha[i][0] == tag:
                fechados = self.pilha[i:]
                del self.pilha[i:]
                self.opaco -= sum(1 for t, _ in fechados if t in ("script", "style", "template", "textarea"))
                self.opaco = max(self.opaco, 0)
                break

    def handle_data(self, data):
        if self.opaco or not data.strip():
            return
        if self.amostras and self.amostras[-1][1] is None:
            m = re.search(r"#[0-9A-Fa-f]{6}\b", data)
            if m and any(t == "figure" for t, _ in self.pilha):
                self.amostras[-1][1] = m.group(0).upper()
        if any(t for _, t in self.pilha) and re.search(r"the\s+void", data, re.I):
            self.titulo_void.append((self.getpos()[0], data.strip()[:60]))


def validar_html(texto):
    import html5lib
    p = html5lib.HTMLParser(strict=False, namespaceHTMLElements=False)
    p.parse(texto)
    erros = []
    # expected-named-entity: o html5lib 1.1 acusa "&family=" do link de fontes, que o padrão
    # atual do HTML aceita (só é erro "&nome;" desconhecido terminado em ponto e vírgula).
    ignorar = {"expected-named-entity"}
    for (pos, codigo, dados) in p.errors:
        if codigo in ignorar:
            continue
        erros.append((pos[0], codigo, dados))
    return erros


def estatico(arq, texto, rep, ids_por_arquivo):
    nome = rel(arq)
    # 1. parser estrito
    for ln, codigo, dados in validar_html(texto)[:20]:
        rep.falha(1, nome, "linha %d: erro de HTML %s %s" % (ln, codigo, dados or ""))
    leitor = Leitor()
    leitor.feed(texto)
    leitor.pendentes = []  # conferidos no DOM montado quando o navegador roda
    if leitor.h1 != 1 and arq.name not in SEM_H1:
        leitor.pendentes.append(("h1", leitor.h1, 0))
    vistos = {}
    for i, ln in leitor.ids:
        vistos.setdefault(i, []).append(ln)
    for i, lns in vistos.items():
        if len(lns) > 1:
            rep.falha(1, nome, "id repetido %r nas linhas %s" % (i, ", ".join(map(str, lns))))
    ids_por_arquivo[arq.resolve()] = set(vistos)
    for alvo, ln in leitor.recursos:
        caminho = alvo_local(arq, alvo)
        if caminho is None:
            continue
        if not caminho.exists():
            rep.falha(1, nome, "linha %d: arquivo local não existe: %s" % (ln, alvo))
    # 6. títulos
    for ln, trecho in leitor.titulo_void:
        rep.falha(6, nome, "linha %d: 'The VOID' digitado em título (o logotipo é arquivo): %s" % (ln, trecho))
    # 4. pares e amostras
    for t, f, r, ln in leitor.pares:
        if t not in contraste.T or f not in contraste.T:
            rep.falha(4, nome, "linha %d: par %s sobre %s sem token no contraste.py" % (ln, t, f))
            continue
        calc = round(contraste.cr(contraste.T[t], contraste.T[f]), 2)
        try:
            impresso = float((r or "").replace(",", "."))
        except ValueError:
            rep.falha(4, nome, "linha %d: par %s sobre %s sem data-razao" % (ln, t, f))
            continue
        if abs(calc - impresso) > 0.01:
            rep.falha(4, nome, "linha %d: par %s sobre %s diz %.2f, contraste.py calcula %.2f" % (ln, t, f, impresso, calc))
    cores = tokens_cor()
    for tok, hexa, ln in leitor.amostras:
        if tok in cores and hexa and hexa != cores[tok]:
            rep.falha(4, nome, "linha %d: amostra %s mostra %s, tokens.json tem %s" % (ln, tok, hexa, cores[tok]))
    return leitor


def links_cruzados(arq, leitor, rep, ids_por_arquivo):
    nome = rel(arq)
    for href, ln in leitor.links:
        u = urlparse(href)
        if href.startswith("#"):
            alvo = unquote(href[1:])
            if alvo and alvo not in ids_por_arquivo.get(arq.resolve(), set()):
                leitor.pendentes.append(("ancora", alvo, ln))
            continue
        caminho = alvo_local(arq, href)
        if caminho is None:
            continue
        if not caminho.exists():
            rep.falha(1, nome, "linha %d: link para arquivo inexistente: %s" % (ln, href))
            continue
        if u.fragment and caminho.suffix == ".html":
            ids = ids_por_arquivo.get(caminho)
            if ids is None:
                lt = Leitor()
                lt.feed(caminho.read_text(encoding="utf-8"))
                ids = ids_por_arquivo[caminho] = {i for i, _ in lt.ids}
            if unquote(u.fragment) not in ids:
                rep.falha(1, nome, "linha %d: %s aponta para #%s, que não existe em %s" % (ln, href, u.fragment, rel(caminho)))


def texto_cru(arq, texto, rep, permitidos):
    nome = rel(arq)
    # 2. travessão em qualquer lugar do arquivo
    for ch, cod in TRAVESSOES.items():
        for m in re.finditer(ch, texto):
            rep.falha(2, nome, "linha %d: travessão %s" % (linha(texto, m.start()), cod))
    # 6. TATOO
    for m in re.finditer(r"tatoo", texto, re.I):
        rep.falha(6, nome, "linha %d: grafia TATOO" % linha(texto, m.start()))
    # 7. var() em atributo SVG e mask:url(#
    for m in re.finditer(r"\b(fill|stroke|stop-color|flood-color|lighting-color|color)\s*=\s*(\\?[\"'])\s*var\(", texto):
        rep.falha(7, nome, "linha %d: var() em atributo SVG (%s)" % (linha(texto, m.start()), m.group(1)))
    for m in re.finditer(r"mask(?:-image)?\s*:\s*url\(\s*['\"]?#", texto):
        rep.falha(7, nome, "linha %d: mask:url(#" % linha(texto, m.start()))
    # 3. HEX em CSS, SVG e scripts
    trechos = []
    if arq.suffix == ".js":
        trechos.append((0, texto, True))
    else:
        for m in re.finditer(r"<style\b[^>]*>(.*?)</style>", texto, re.S):
            trechos.append((m.start(1), m.group(1), False))
        for m in re.finditer(r'\bstyle\s*=\s*"([^"]*)"', texto):
            trechos.append((m.start(1), m.group(1), False))
        for m in re.finditer(r"<svg\b.*?</svg>", texto, re.S):
            trechos.append((m.start(), m.group(0), False))
        for m in re.finditer(r"<script\b(?![^>]*\bsrc=)[^>]*>(.*?)</script>", texto, re.S):
            trechos.append((m.start(1), m.group(1), True))
        for m in re.finditer(r'\b(?:bgcolor|color|fill|stroke|stop-color)\s*=\s*"(#[0-9A-Fa-f]{3,6})"', texto):
            trechos.append((m.start(1), m.group(1), False))
    vistos = set()
    for base, trecho, js in trechos:
        rx = r"(?:#|%23)([0-9A-Fa-f]{6})\b" if js else r"(?:#|%23)([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b(?![-\w])"
        for h in re.finditer(rx, trecho):
            antes = trecho[max(0, h.start() - 1):h.start()]
            if not js and antes in ("&",):  # entidade &#123;
                continue
            cor = normaliza_hex(h.group(1))
            pos = base + h.start()
            if cor not in permitidos and (cor, pos) not in vistos:
                vistos.add((cor, pos))
                rep.falha(3, nome, "linha %d: HEX fora dos tokens %s" % (linha(texto, pos), cor))


# --------------------------------------------------------------------------- navegador
JS_COLETA = r"""
(args) => {
  const [FORA, CLAIMS, GAMI, CLASSES] = args;
  const out = {dup: [], textos: [], titulos: [], travessao: []};
  // ids repetidos no DOM montado (fora de template)
  const cont = {};
  document.querySelectorAll('[id]').forEach(e => { if (e.closest('template')) return; cont[e.id] = (cont[e.id] || 0) + 1; });
  for (const k in cont) if (cont[k] > 1) out.dup.push(k + ' x' + cont[k]);
  // texto visível sem os exemplos proibidos e sem código
  const corpo = document.body.cloneNode(true);
  corpo.querySelectorAll('[data-exemplo="proibido"],script,style,template,noscript,pre,code,textarea').forEach(e => e.remove());
  const visivel = corpo.textContent.replace(/\s+/g, ' ');
  const atributos = [];
  document.querySelectorAll('[alt],[title],[aria-label],[placeholder]').forEach(e => {
    if (e.closest('[data-exemplo="proibido"],template')) return;
    ['alt', 'title', 'aria-label', 'placeholder'].forEach(a => { const v = e.getAttribute(a); if (v) atributos.push(v); });
  });
  const pseudo = [];
  document.querySelectorAll('body *').forEach(e => {
    ['::before', '::after'].forEach(p => { const c = getComputedStyle(e, p).content; if (c && c !== 'none' && c !== 'normal' && c.length > 2) pseudo.push(c); });
  });
  const tudo = visivel + ' \u0001 ' + atributos.join(' \u0001 ') + ' \u0001 ' + pseudo.join(' ');
  const achar = (lista, flags, tipo) => lista.forEach(([rx, nome]) => {
    const r = new RegExp(rx, flags);
    let m; while ((m = r.exec(tudo)) !== null) {
      out.textos.push([tipo, nome, tudo.slice(Math.max(0, m.index - 40), m.index + m[0].length + 40)]);
      if (out.textos.length > 200) return;
    }
  });
  achar(FORA.map(x => [x, x]), 'giu', 'fora');
  achar(CLAIMS.filter(c => c[1] === 'MEC').map(c => c), 'gu', 'claim');
  achar(CLAIMS.filter(c => c[1] !== 'MEC'), 'giu', 'claim');
  if (GAMI) achar(GAMI.map(x => [x, x]), 'giu', 'gamificação');
  for (const ch of ['\u2014', '\u2013']) {
    const i = tudo.indexOf(ch); if (i > -1) out.travessao.push(tudo.slice(Math.max(0, i - 40), i + 40));
  }
  // títulos montados com The VOID digitado
  const sel = Array.from(CLASSES).map(c => '.' + c).join(',') + ',h1,h2';
  document.querySelectorAll(sel).forEach(e => {
    if (e.closest('[data-exemplo="proibido"],template')) return;
    if (/the\s+void/i.test(e.textContent)) out.titulos.push(e.textContent.trim().slice(0, 60));
  });
  return out;
}
"""

JS_MOVIMENTO = r"""
() => {
  const seg = v => v.split(',').map(s => s.trim()).map(s => s.endsWith('ms') ? parseFloat(s) : parseFloat(s) * 1000);
  const ruins = [];
  const olhar = (e, p) => {
    const cs = getComputedStyle(e, p);
    if (cs.animationName && cs.animationName !== 'none') {
      const d = Math.max(...seg(cs.animationDuration));
      if (d > 120) ruins.push(['animação', descrever(e, p), cs.animationName, d]);
    }
    const props = cs.transitionProperty;
    if (props && props !== 'none') {
      const d = Math.max(...seg(cs.transitionDuration));
      if (d > 120) ruins.push(['transição', descrever(e, p), props, d]);
    }
  };
  const descrever = (e, p) => e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.classList.length ? '.' + Array.from(e.classList).slice(0, 2).join('.') : '') + (p || '');
  document.querySelectorAll('*').forEach(e => { olhar(e, null); olhar(e, '::before'); olhar(e, '::after'); });
  (document.getAnimations ? document.getAnimations() : []).forEach(a => {
    const t = a.effect && a.effect.getTiming ? a.effect.getTiming() : {};
    const d = typeof t.duration === 'number' ? t.duration : 0;
    if (d > 120 && a.playState === 'running') ruins.push(['animação JS', (a.effect.target ? descrever(a.effect.target, a.effect.pseudoElement) : '?'), a.animationName || a.transitionProperty || 'WAAPI', d]);
  });
  return ruins.slice(0, 30);
}
"""


class Silencioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def servidor():
    handler = functools.partial(Silencioso, directory=str(RAIZ))
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def navegador(arquivos, rep, pendentes=None, pular_movimento=False):
    pendentes = pendentes or {}
    from playwright.sync_api import sync_playwright
    srv = servidor()
    base = "http://127.0.0.1:%d/" % srv.server_address[1]
    try:
        with sync_playwright() as p:
            nav = p.chromium.launch()
            for arq in arquivos:
                nome = rel(arq)
                # arquivo do repositório vai pelo servidor local; peça salva fora dele (no
                # workspace do cliente) abre direto do disco, com os recursos file:// que usa
                url = (base + rel(arq)) if dentro_da_raiz(arq) else arq.resolve().as_uri()
                gami = arq.name.startswith("membros")
                for i, w in enumerate(LARGURAS):
                    ctx = nav.new_context(viewport={"width": w, "height": 900 if w > 500 else 844},
                                          reduced_motion="reduce" if w == 390 else "no-preference")
                    pg = ctx.new_page()
                    erros_js = []
                    pg.on("pageerror", lambda e, l=erros_js: l.append(str(e)))
                    try:
                        pg.goto(url, wait_until="networkidle", timeout=60000)
                    except Exception as e:
                        rep.falha(8, nome, "%d px: não abriu (%s)" % (w, str(e)[:80]))
                        ctx.close()
                        continue
                    pg.wait_for_timeout(600)
                    larg = pg.evaluate("[document.documentElement.scrollWidth, document.body ? document.body.scrollWidth : 0, window.innerWidth]")
                    if max(larg[0], larg[1]) > larg[2] and w >= FIXOS.get(arq.name, 0):
                        quem = pg.evaluate("""(w) => { const r = [];
                          document.querySelectorAll('body *').forEach(e => { const b = e.getBoundingClientRect();
                            if (b.width && b.right > w + 1 && getComputedStyle(e).position !== 'fixed') {
                              let a = e.parentElement, cortado = false;
                              while (a && a !== document.body) { const o = getComputedStyle(a).overflowX; if (o !== 'visible') { cortado = true; break; } a = a.parentElement; }
                              if (!cortado) r.push(e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.className && e.className.baseVal === undefined ? '.' + String(e.className).split(' ').slice(0, 2).join('.') : '') + ' ' + Math.round(b.right)); } });
                          return r.slice(0, 6); }""", larg[2])
                        rep.falha(8, nome, "%d px: documento com %d px (rolagem horizontal) %s" % (w, max(larg[0], larg[1]), "; ".join(quem)))
                    for e in erros_js[:3]:
                        rep.falha(1, nome, "%d px: erro de JavaScript: %s" % (w, e[:140]))
                    if i == 0:
                        h1 = pg.evaluate("Array.from(document.querySelectorAll('h1')).filter(e => !e.closest('template')).length")
                        if h1 != 1 and arq.name not in SEM_H1:
                            rep.falha(1, nome, "%d h1 no DOM montado (esperado 1)" % h1)
                        for tipo, v, ln in pendentes.get(arq, []):
                            if tipo == "ancora" and not pg.evaluate("(i) => !!document.getElementById(i)", v):
                                rep.falha(1, nome, "linha %d: link #%s sem destino (nem no DOM montado)" % (ln, v))
                        dados = pg.evaluate(JS_COLETA, [FORA, CLAIMS, GAMIFICACAO if gami else None, sorted(CLASSES_TITULO)])
                        for d in dados["dup"][:10]:
                            rep.falha(1, nome, "id repetido no DOM montado: %s" % d)
                        for tipo, termo, ctxo in dados["textos"][:40]:
                            rep.falha(5, nome, "%s (%s) fora de exemplo proibido: ...%s..." % (tipo, termo, ctxo.strip()))
                        for t in dados["travessao"]:
                            rep.falha(2, nome, "travessão no texto montado: ...%s..." % t.strip())
                        for t in dados["titulos"]:
                            rep.falha(6, nome, "'The VOID' digitado em título montado: %s" % t)
                    if w == 390 and not pular_movimento:
                        for tipo, alvo, prop, d in pg.evaluate(JS_MOVIMENTO):
                            rep.falha(9, nome, "%s de %d ms com movimento reduzido em %s (%s)" % (tipo, d, alvo, str(prop)[:40]))
                    ctx.close()
            nav.close()
    finally:
        srv.shutdown()


# --------------------------------------------------------------------------- Lighthouse
def achar_lighthouse():
    npx = shutil.which("npx")
    if not npx:
        return None
    for pacote in ("lighthouse@12", "lighthouse"):
        try:
            r = subprocess.run([npx, "--no-install", pacote, "--version"], capture_output=True, text=True, timeout=60)
            if r.returncode == 0 and re.match(r"\d+\.", r.stdout.strip()):
                return [npx, "--no-install", pacote]
        except Exception:
            pass
    return None


def chrome_do_playwright():
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            return p.chromium.executable_path
    except Exception:
        return None


def lighthouse(arquivos, rep):
    cmd = achar_lighthouse()
    if not cmd:
        rep.aviso(10, "-", "npx lighthouse não está disponível: item 10 pulado")
        return
    alvos = [a for a in arquivos if a.name in LIGHTHOUSE and a.parent == RAIZ]
    if not alvos:
        return
    env = dict(os.environ)
    chrome = chrome_do_playwright()
    if chrome:
        env["CHROME_PATH"] = chrome
    srv = servidor()
    base = "http://127.0.0.1:%d/" % srv.server_address[1]
    try:
        for arq in alvos:
            with tempfile.TemporaryDirectory() as tmp:
                saida = os.path.join(tmp, "lh.json")
                r = subprocess.run(cmd + [base + arq.name, "--only-categories=accessibility", "--output=json",
                                          "--output-path=" + saida, "--quiet", "--chrome-flags=--headless=new --no-sandbox"],
                                   capture_output=True, text=True, timeout=300, env=env)
                if not os.path.exists(saida):
                    rep.aviso(10, arq.name, "Lighthouse não gerou relatório (%s)" % (r.stderr.strip().splitlines() or ["?"])[-1][:120])
                    continue
                dados = json.load(open(saida))
                nota = round((dados["categories"]["accessibility"]["score"] or 0) * 100)
                if nota < 95:
                    ruins = [k for k, v in dados["audits"].items() if v.get("score") == 0 and v.get("scoreDisplayMode") == "binary"]
                    rep.falha(10, arq.name, "acessibilidade %d (mínimo 95): %s" % (nota, ", ".join(ruins)))
                else:
                    rep.ok.append("item 10 %s: acessibilidade %d" % (arq.name, nota))
    finally:
        srv.shutdown()


# --------------------------------------------------------------------------- principal
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("arquivos", nargs="*")
    ap.add_argument("--rapido", action="store_true", help="só itens estáticos (1 a 7)")
    ap.add_argument("--sem-lighthouse", action="store_true")
    ap.add_argument("--dist", action="store_true", help="inclui dist/*.html")
    args = ap.parse_args()

    rep = Relatorio()
    arquivos = arquivos_html(args.arquivos, args.dist)
    permitidos = hex_permitidos()
    ids_por_arquivo, leitores = {}, {}
    for arq in arquivos:
        texto = arq.read_text(encoding="utf-8")
        leitores[arq] = estatico(arq, texto, rep, ids_por_arquivo)
        texto_cru(arq, texto, rep, permitidos)
    for arq in arquivos:
        links_cruzados(arq, leitores[arq], rep, ids_por_arquivo)
    if not args.arquivos:
        for js in MOTORES + ("tokens.css",):
            p = RAIZ / js
            if p.exists():
                texto_cru(p, p.read_text(encoding="utf-8"), rep, permitidos)
    # contraste.py --check também é parte do item 4
    r = subprocess.run([sys.executable, str(RAIZ / "tools/contraste.py"), "--check"], capture_output=True, text=True)
    if r.returncode != 0:
        for l in r.stdout.splitlines():
            rep.falha(4, "tools/contraste.py", l)

    pendentes = {a: leitores[a].pendentes for a in arquivos if leitores[a].pendentes}
    if args.rapido:
        for a, lista in pendentes.items():
            for tipo, v, ln in lista:
                rep.aviso(1, rel(a), (("%d h1 no HTML estático" % v) if tipo == "h1" else ("linha %d: link #%s sem destino no HTML estático" % (ln, v))) + "; conferido só no DOM montado (rode sem --rapido)")
    if not args.rapido:
        navegador(arquivos, rep, pendentes)
        if not args.sem_lighthouse:
            lighthouse(arquivos, rep)
        else:
            rep.aviso(10, "-", "item 10 pulado (--sem-lighthouse)")

    print("Gate de aceite da The VOID (plano, seção 6) · %d arquivos HTML" % len(arquivos))
    for a in arquivos:
        print("  %s" % rel(a))
    for o in rep.ok:
        print("  OK     %s" % o)
    for item, arq, msg in rep.avisos:
        print("  AVISO  [%s] %s: %s" % (item, arq, msg))
    for item, arq, msg in sorted(rep.falhas, key=lambda x: (x[0], x[1])):
        print("  FALHA  [%s] %s: %s" % (item, arq, msg))
    por_item = {}
    for item, _, _ in rep.falhas:
        por_item[item] = por_item.get(item, 0) + 1
    print("Resultado: %s (%d falhas%s, %d avisos)" % (
        "aprovado" if not rep.falhas else "reprovado", len(rep.falhas),
        (": " + ", ".join("item %d=%d" % kv for kv in sorted(por_item.items()))) if por_item else "", len(rep.avisos)))
    return 0 if not rep.falhas else 1


if __name__ == "__main__":
    sys.exit(main())
