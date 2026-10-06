#!/usr/bin/env python3
"""Gera a versão AUTOCONTIDA dos HTML da marca The VOID: um arquivo único que abre sozinho
(e-mail, WhatsApp, Drive, celular), sem a pasta assets/, sem tokens.css e sem os motores ao lado.

O que faz, em cada HTML:
1. troca <link rel="stylesheet" href="tokens.css"> pelo conteúdo do tokens.css;
2. troca <script src="vforms.js|vviz.js"> pelo código do motor, no mesmo lugar (o motor
   espera o DOMContentLoaded, então continua montando depois da página);
3. embute as fontes do link do Google Fonts da especificação (Archivo variável com os eixos
   de peso e largura, Newsreader Italic 300 e Nunito Sans 400 e 600) em woff2, alfabetos
   latin e latin-ext, preservando as faixas de peso e de largura. Os woff2 baixados ficam em
   assets/fontes/google/ e servem de reserva sem internet. Todas têm licença SIL Open Font
   License. A Alga (comercial) NUNCA entra: ela não está no link nem em assets/;
4. guarda cada imagem usada UMA vez, em data URI, num dicionário no começo do <head>. Um script
   troca todo src, href, srcset, poster e url() de style que começa com "assets/" pela imagem
   embutida, inclusive nos elementos que os motores criam depois e dentro de iframe de prévia
   (o e-mail). Os SVG oficiais de assets/brand/svg entram sempre nas páginas com motor, porque
   o vforms.js monta o caminho do selo e do logotipo na hora;
5. url(assets/...) dentro de <style> vira data URI direto;
6. link entre arquivos da marca (brand-book.html#s22, lockup.html...) passa a apontar para o
   nome que o arquivo ganha em dist/; link para outro arquivo do repositório (tokens.json,
   assets/foto/receitas.md) ganha "../", para continuar abrindo a partir de dist/.
Blocos <template>, <pre>, <script>, <textarea> e <style> não têm atributos alterados (o código
mostrado e copiado continua com os caminhos assets/...).

Uso (Python padrão; a internet só é usada na primeira vez, para baixar as fontes):
  python3 autocontido.py                     # gera dist/ com todos os HTML da marca
  python3 autocontido.py lockup.html         # só esse
"""
import base64
import hashlib
import json
import mimetypes
import os
import re
import sys
import urllib.request

RAIZ = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(RAIZ, "dist")
LIMITE = 16 * 1024 * 1024
PADRAO = {
    "index.html": "index.html",
    "brand-book.html": "brand-book-the-void.html",
    "guia-de-uso.html": "guia-de-uso-the-void.html",
    "lockup.html": "trechos-da-marca-the-void.html",
    "kit-social.html": "kit-social-the-void.html",
    "lp-template.html": "modelo-lp-the-void.html",
    "vsl-kit.html": "kit-vsl-the-void.html",
    "membros-ui.html": "area-de-membros-the-void.html",
    "comunicacao-m1-m8.html": "comunicacao-m1-m8-the-void.html",
    "email-template.html": "modelo-email-the-void.html",
    "artigo-template.html": "modelo-artigo-the-void.html",
    "deck-template.html": "apresentacao-the-void.html",
}
MOTORES = ("vforms.js", "vviz.js")
FONTES = os.path.join(RAIZ, "assets", "fontes", "google")
RE_LINK_FONTES = re.compile(r'<link\b[^>]*href="(https://fonts\.googleapis\.com/css2\?[^"]+)"[^>]*>\n?')
RE_PRECONNECT = re.compile(r'<link rel="preconnect" href="https://fonts\.(?:googleapis|gstatic)\.com"[^>]*>\n?')
RE_ASSET = re.compile(r"assets/[A-Za-z0-9_./-]+?\.(?:png|jpe?g|svg|webp|gif|ico)")
ALFABETOS = ("latin", "latin-ext")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def baixa(url, timeout=30):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=timeout).read()


def fontes_embutidas(url):
    """CSS com @font-face em data URI (woff2, latin e latin-ext), ou None se não der."""
    url = url.replace("&amp;", "&")
    if "alga" in url.lower():
        return None
    os.makedirs(FONTES, exist_ok=True)
    guardado = os.path.join(FONTES, "google-%s.css" % hashlib.sha1(url.encode()).hexdigest()[:10])
    try:
        css = baixa(url, 20).decode("utf-8")
        with open(guardado, "w", encoding="utf-8") as f:
            f.write(css)
    except Exception as erro:
        if not os.path.isfile(guardado):
            print("aviso: sem internet e sem cópia em assets/fontes/google/; as fontes continuam pelo link do Google (%s)" % erro)
            return None
        css = open(guardado, encoding="utf-8").read()
    saida, vistos = [], set()
    for alfabeto, corpo in re.findall(r"/\*\s*([a-z-]+)\s*\*/\s*@font-face\s*\{([^}]*)\}", css):
        if alfabeto not in ALFABETOS:
            continue
        prop = dict((k.strip(), v.strip()) for k, v in re.findall(r"([a-z-]+)\s*:\s*([^;]+);", corpo))
        fonte = re.search(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", prop.get("src", ""))
        if not fonte:
            continue
        chave = (prop.get("font-family"), prop.get("font-style"), prop.get("font-weight"),
                 prop.get("font-stretch"), fonte.group(1), prop.get("unicode-range"))
        if chave in vistos:
            continue
        vistos.add(chave)
        link = fonte.group(1)
        local = os.path.join(FONTES, os.path.basename(link))
        try:
            if not os.path.isfile(local):
                with open(local, "wb") as f:
                    f.write(baixa(link))
        except Exception as erro:
            print("aviso: não baixou %s (%s); as fontes continuam pelo link do Google" % (link, erro))
            return None
        dado = base64.b64encode(open(local, "rb").read()).decode()
        extra = ("font-stretch:%s;" % prop["font-stretch"]) if "font-stretch" in prop else ""
        saida.append("/* %s */\n@font-face{font-family:%s;font-style:%s;font-weight:%s;%sfont-display:swap;"
                     "src:url(data:font/woff2;base64,%s) format('woff2');unicode-range:%s;}"
                     % (alfabeto, prop.get("font-family"), prop.get("font-style", "normal"), prop.get("font-weight", "400"),
                        extra, dado, prop.get("unicode-range", "U+0000-00FF")))
    return "\n".join(saida) if saida else None


TROCA = r"""<script>/* imagens embutidas: troca assets/... pela versão em data URI */
(function(){var A=window.__VOID_ASSETS=%s;
function chave(v){return typeof v==="string"?v.replace(/^\.\//,""):v}
function url(v){return A[chave(v)]||v}
/* imagem criada por script (new Image, setAttribute, fetch) também pega a versão embutida */
try{var dSrc=Object.getOwnPropertyDescriptor(HTMLImageElement.prototype,"src");
 Object.defineProperty(HTMLImageElement.prototype,"src",{get:dSrc.get,set:function(v){dSrc.set.call(this,url(v))},configurable:true,enumerable:dSrc.enumerable});
 var sa=Element.prototype.setAttribute;Element.prototype.setAttribute=function(n,v){if(n==="src"||n==="href"||n==="xlink:href"||n==="poster")v=url(v);return sa.call(this,n,v)};
 if(window.fetch){var fe=window.fetch;window.fetch=function(u,o){return fe.call(this,url(u),o)}}
 var ash=Element.prototype.attachShadow;if(ash)Element.prototype.attachShadow=function(o){var r=ash.call(this,o);observar(r);return r}}catch(e){}
function css(v){return v.replace(/url\((['"]?)(assets\/[^'")]+)\1\)/g,function(m,q,p){return A[p]?'url("'+A[p]+'")':m})}
function set(el){if(!el||el.nodeType!==1)return;
 ["src","href","poster"].forEach(function(a){var v=chave(el.getAttribute(a));if(v&&v.indexOf("assets/")===0&&A[v])el.setAttribute(a,A[v])});
 var x=el.getAttributeNS&&el.getAttributeNS("http://www.w3.org/1999/xlink","href");
 if(x&&x.indexOf("assets/")===0&&A[x])el.setAttributeNS("http://www.w3.org/1999/xlink","xlink:href",A[x]);
 var s=el.getAttribute("srcset");if(s&&s.indexOf("assets/")>-1)el.setAttribute("srcset",s.replace(/assets\/[^\s,]+/g,url));
 var st=el.getAttribute("style");if(st&&st.indexOf("assets/")>-1){var n=css(st);if(n!==st)el.setAttribute("style",n)}
 if(el.tagName==="IFRAME"&&!el.__void){el.__void=1;var ligar=function(){try{var d=el.contentDocument;if(d&&d.documentElement){walk(d.documentElement);observar(d.documentElement)}}catch(e){}};el.addEventListener("load",ligar);ligar()}}
function walk(r){set(r);if(r.querySelectorAll)r.querySelectorAll("[src],[href],[srcset],[poster],[style],image,iframe").forEach(set)}
function observar(alvo){new MutationObserver(function(ms){ms.forEach(function(m){if(m.type==="attributes")set(m.target);else m.addedNodes.forEach(function(n){if(n.nodeType===1)walk(n)})})})
 .observe(alvo,{subtree:true,childList:true,attributes:true,attributeFilter:["src","href","srcset","poster","style","xlink:href"]})}
observar(document.documentElement);
document.addEventListener("DOMContentLoaded",function(){walk(document.documentElement)});})();
</script>"""


def aviso_ofl():
    """Aviso que acompanha as fontes embutidas: a SIL OFL 1.1 pede o copyright e a licença junto
    de toda redistribuição. Os avisos vêm de assets/fontes/google/OFL.txt."""
    avisos = []
    try:
        for ln in open(os.path.join(FONTES, "OFL.txt"), encoding="utf-8"):
            if not ln.startswith("Copyright"):
                break
            avisos.append(ln.strip())
    except OSError:
        pass
    return ("Fontes embutidas, alfabetos latin e latin-ext. Archivo, Newsreader e Nunito Sans: SIL Open Font "
            "License 1.1 (https://openfontlicense.org). %s. Texto completo em assets/fontes/google/OFL.txt"
            % ("; ".join(avisos) or "Copyright dos autores de cada projeto"))


def data_uri(caminho):
    tipo = mimetypes.guess_type(caminho)[0] or "application/octet-stream"
    if caminho.endswith(".svg"):
        tipo = "image/svg+xml"
    elif caminho.endswith(".webp"):
        tipo = "image/webp"
    with open(caminho, "rb") as f:
        return "data:%s;base64,%s" % (tipo, base64.b64encode(f.read()).decode())


RE_BLOCOS = re.compile(r"(<(template|pre|script|textarea|style)\b[\s\S]*?</\2>)")


def fora_de_codigo(html, func):
    """Aplica func só fora de template, pre, script, textarea e style (o código mostrado e o
    HTML montado pelos modelos, como o e-mail, ficam intactos). Com func=None, devolve só o
    texto de fora, para busca."""
    partes = RE_BLOCOS.split(html)
    saida, i = [], 0
    while i < len(partes):
        if i % 3 == 0:
            saida.append(partes[i] if func is None else func(partes[i]))
            i += 1
        else:
            if func is not None:
                saida.append(partes[i])
            i += 2
    return "".join(saida)


def ajusta_links(trecho, nome_origem):
    """Links <a href> para outro HTML da marca ganham o nome de dist/; outros arquivos ganham ../"""
    def troca(m):
        antes, href, depois = m.group(1), m.group(2), m.group(3)
        if re.match(r"^(?:[a-z]+:|#|//|\{\{)", href):
            return m.group(0)
        caminho, _, frag = href.partition("#")
        caminho_q, _, consulta = caminho.partition("?")
        if caminho_q in PADRAO:
            novo = PADRAO[caminho_q] + ("?" + consulta if consulta else "") + ("#" + frag if frag else "")
        elif caminho_q.startswith("dist/"):
            novo = href[len("dist/"):]
        elif caminho_q:
            novo = "../" + href
        else:
            return m.group(0)
        return antes + novo + depois
    return re.sub(r'(<a\b[^>]*?\shref=")([^"]*)(")', troca, trecho)


def autocontido(origem, destino):
    html = open(origem, encoding="utf-8").read()
    nome = os.path.basename(origem)
    # 0. tokens.css dentro do arquivo, no mesmo lugar
    tokens = open(os.path.join(RAIZ, "tokens.css"), encoding="utf-8").read()
    html = re.sub(r'<link rel="stylesheet" href="tokens\.css">', lambda m: "<style>/* tokens.css */\n%s\n</style>" % tokens, html, count=1)
    # 1. fontes do Google embutidas
    blocos, sobra = [], 0
    for link in sorted(set(RE_LINK_FONTES.findall(fora_de_codigo(html, None)))):
        css = fontes_embutidas(link)
        if css:
            blocos.append(css)
            rx = re.compile(r'<link\b[^>]*href="%s"[^>]*>\n?' % re.escape(link))
            html = fora_de_codigo(html, lambda t: rx.sub("", t))
        else:
            sobra += 1
    if blocos:
        if not sobra:
            html = fora_de_codigo(html, lambda t: re.sub(r"<noscript>\s*</noscript>\n?", "", RE_PRECONNECT.sub("", t)))
        bloco_fontes = "<style>\n/* %s */\n%s\n</style>\n" % (aviso_ofl(), "\n".join(blocos))
        html = re.sub(r"(<meta charset=[^>]*>\n?)", lambda m: m.group(1) + bloco_fontes, html, count=1)
    # 1b. o manifesto do site (JSON, não imagem) não vira data URI: aponta para o do repositório
    html = fora_de_codigo(html, lambda t: re.sub(r'(<link rel="manifest" href=")(assets/)', r"\1../\2", t))
    # 2. motores dentro do arquivo
    tem_motor = False
    for js in MOTORES:
        rx = re.compile(r'<script src="%s"(?: defer)?></script>' % re.escape(js))
        if rx.search(html):
            tem_motor = True
            codigo = open(os.path.join(RAIZ, js), encoding="utf-8").read().replace("</script", "<\\/script")
            html = rx.sub(lambda m: "<script>/* %s */\n%s\n</script>" % (js, codigo), html, count=1)
    # 3. dicionário de imagens (cada arquivo uma vez só)
    usados = set(m.group(0) for m in RE_ASSET.finditer(html))
    # caminho montado na hora pelo script ('assets/aplicacoes/selo-email-' + p + '.png'):
    # entram todos os arquivos de imagem da pasta que começam com o prefixo
    for pasta_rel, prefixo in re.findall(r"assets/([A-Za-z0-9_./-]*/)([A-Za-z0-9_.-]*)['\"]\s*\+", html):
        pasta = os.path.join(RAIZ, "assets", pasta_rel)
        if os.path.isdir(pasta):
            usados |= {"assets/" + pasta_rel + f for f in os.listdir(pasta)
                       if f.startswith(prefixo) and re.search(r"\.(?:png|jpe?g|svg|webp|gif|ico)$", f)}
    if tem_motor:
        pasta = os.path.join(RAIZ, "assets", "brand", "svg")
        usados |= {"assets/brand/svg/" + f for f in os.listdir(pasta) if f.endswith(".svg")}
    mapa, faltando = {}, []
    for p in sorted(usados):
        c = os.path.join(RAIZ, p)
        if os.path.isfile(c):
            mapa[p] = data_uri(c)
        else:
            faltando.append(p)

    # 4. CSS url(assets/...) vira data URI direto (só dentro de <style>)
    def troca_css(m):
        return re.sub(r"url\(\s*(['\"]?)(assets/[^)'\"]+)\1\s*\)",
                      lambda u: "url(%s)" % json.dumps(mapa.get(u.group(2), u.group(2))), m.group(0))
    html = re.sub(r"<style\b[\s\S]*?</style>", troca_css, html)
    # 5. atributos estáticos fora de template, pre, script, textarea e style viram data URI
    partes = re.split(r"(<(template|pre|script|textarea|style)\b[\s\S]*?</\2>)", html)
    saida, i = [], 0
    while i < len(partes):
        trecho = partes[i]
        if i % 3 == 0:
            trecho = re.sub(r'(<(?:img|source|image|link|video)\b[^>]*?\s)(src|href|poster)="(assets/[^"]*)"',
                            lambda m: '%s%s="%s"' % (m.group(1), m.group(2), mapa.get(m.group(3), m.group(3))), trecho)
            trecho = re.sub(r'(\ssrcset=")([^"]*assets/[^"]*)(")',
                            lambda m: m.group(1) + re.sub(r"assets/[^\s,]+", lambda u: mapa.get(u.group(0), u.group(0)), m.group(2)) + m.group(3), trecho)
            trecho = ajusta_links(trecho, nome)
            saida.append(trecho)
            i += 1
        else:
            saida.append(trecho)
            i += 2
    html = "".join(saida)
    # 6. o script de troca entra logo depois do <meta charset>
    bloco = TROCA % json.dumps(mapa, separators=(",", ":"))
    html = re.sub(r"(<meta charset=[^>]*>)", lambda m: m.group(1) + "\n" + bloco, html, count=1)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(html)
    tamanho = len(html.encode())
    print("ok %-40s %6d KB  imagens=%-3d fontes=%d%s" % (
        os.path.relpath(destino, RAIZ), tamanho // 1024, len(mapa), len(blocos),
        ("  sem arquivo (ficam como estão): " + ", ".join(faltando)) if faltando else ""))
    if tamanho > LIMITE:
        print("ERRO: %s passou de 16 MB" % destino)
        return False
    return True


if __name__ == "__main__":
    alvos = sys.argv[1:] or [a for a in PADRAO if os.path.isfile(os.path.join(RAIZ, a))]
    tudo_ok = True
    for a in alvos:
        o = a if os.path.isabs(a) else os.path.join(RAIZ, a)
        if not os.path.isfile(o):
            print("pulado (não existe): %s" % a)
            continue
        tudo_ok &= autocontido(o, os.path.join(DIST, PADRAO.get(os.path.basename(a), os.path.basename(a))))
    sys.exit(0 if tudo_ok else 1)
