#!/usr/bin/env python3
"""
THE VOID · testes de aceite do lockup.html (plano de construção, seção 4, linha lockup.html).

Critérios: botão Copiar em cada trecho; cada trecho renderiza igual ao copiado; nenhum
logotipo em texto. Mais o gate geral que se aplica a esta página: sem rolagem horizontal
em 320, 390 e 1440 px, zero travessão, nenhum TATOO, HEX só de tokens.json, mínimos de
logotipo e selo respeitados, data URI idêntico ao arquivo oficial, movimento reduzido.

Uso: python3 tools/teste_lockup.py [--capturas PASTA]
Sai com código 0 só quando tudo passa. Requer playwright (chromium) e Pillow.
"""
import io
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent
PAGINA = RAIZ / "lockup.html"
URL = PAGINA.as_uri()
FONTES = ('<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900'
          '&family=Newsreader:ital,opsz,wght@1,6..72,300&family=Nunito+Sans:wght@400;600&display=swap" rel="stylesheet">')
FUNDO = {"sala": "#181818", "tela": "#F8F9F4", "bastidor": "#212121"}

falhas, avisos, oks = [], [], []


def ok(cond, msg):
    (oks if cond else falhas).append(msg)
    return cond


def tokens_hex():
    t = json.loads((RAIZ / "tokens.json").read_text(encoding="utf-8"))
    achados = set()

    def anda(n):
        if isinstance(n, dict):
            for v in n.values():
                anda(v)
        elif isinstance(n, str):
            achados.update(h.upper() for h in re.findall(r"#[0-9A-Fa-f]{6}\b", n))
    anda(t)
    return achados


def estatico():
    s = PAGINA.read_text(encoding="utf-8")
    ok(not re.search("[—–]", s), "zero travessão (U+2014 e U+2013) no arquivo inteiro")
    ok("TATOO" not in s.upper().replace("TATTOO", ""), "nenhum TATOO")
    sem_json = re.sub(r'<script type="application/json" id="lk-datauri">.*?</script>', "", s, flags=re.S)
    hexes = {h.upper() for h in re.findall(r"#[0-9A-Fa-f]{6}\b", sem_json)}
    fora = hexes - tokens_hex() - {"#21130C"}
    ok(not fora, "todo HEX pertence a tokens.json" + (" (fora: %s)" % sorted(fora) if fora else ""))
    ok(not re.search(r'(fill|stroke|stop-color)="var\(', s), "nenhum var() em atributo de SVG")
    ok("mask:url(#" not in s, "nenhum mask:url(#")
    ok(len(re.findall(r"<h1\b", s)) == 1, "um único h1")
    ids = re.findall(r'\sid="([^"]+)"', s)
    rep = sorted({i for i in ids if ids.count(i) > 1})
    ok(not rep, "ids únicos" + (" (repetidos: %s)" % rep if rep else ""))
    for alvo in set(re.findall(r'href="#([^"]+)"', s)):
        ok(alvo in ids, "link interno #%s resolve" % alvo)
    locais = Path(__file__).resolve().parent / "claims-locais.txt"
    extras = [l.split("\t", 1)[0].strip() for l in (locais.read_text(encoding="utf-8").splitlines() if locais.exists() else [])
              if l.strip() and not l.lstrip().startswith("#") and "\t" in l]
    proib = re.compile("|".join([r"maior escola|maior mercado|#1\b|nº ?1\b|\bmec\b|\+\d[\d.]*\s?(?:mil\s)?alunos|líder (?:no|do) (?:segmento|mercado)|a melhor escola|a única escola|\b(?:desde|est\.?) (?:19|20)\d\d\b"] + extras), re.I)
    texto = re.sub(r"<[^>]+>", " ", re.sub(r'<script type="application/json".*?</script>', "", s, flags=re.S))
    achados = proib.findall(texto)
    ok(not achados, "nenhum claim proibido" + (" (%s)" % achados if achados else ""))
    # data URI: idêntico ao arquivo oficial, byte a byte
    dados = json.loads(re.search(r'<script type="application/json" id="lk-datauri">(.*?)</script>', s, re.S).group(1).replace("<\\/", "</"))
    ok(len(dados) >= 10, "data URI dos 10 logotipos oficiais presentes (%d)" % len(dados))
    for nome, d in dados.items():
        corpo = unquote(d["uri"].split(",", 1)[1]).encode("utf-8")
        ok(corpo == (RAIZ / d["arquivo"]).read_bytes(), "data URI %s idêntico a %s" % (nome, d["arquivo"]))


def diff_pct(a, b):
    a = Image.open(io.BytesIO(a)).convert("RGB")
    b = Image.open(io.BytesIO(b)).convert("RGB")
    if abs(a.size[0] - b.size[0]) > 1 or abs(a.size[1] - b.size[1]) > 1:
        return None, (a.size, b.size)
    w, h = min(a.size[0], b.size[0]), min(a.size[1], b.size[1])
    a, b = a.crop((0, 0, w, h)), b.crop((0, 0, w, h))
    d = ImageChops.difference(a, b).convert("L")
    hist = d.histogram()
    ruins = sum(hist[48:])  # diferença perceptível
    return ruins / (a.size[0] * a.size[1]) * 100, a.size


def dinamico(capturas):
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for w, h in [(320, 640), (390, 844), (1440, 900)]:
            pg = nav.new_page(viewport={"width": w, "height": h}, reduced_motion="reduce")
            erros = []
            pg.on("pageerror", lambda e: erros.append(str(e)))
            pg.goto(URL)
            pg.wait_for_load_state("networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(600)
            ok(not erros, "%d px: nenhum erro de JavaScript %s" % (w, erros[:2]))
            sw = pg.evaluate("document.documentElement.scrollWidth")
            ok(sw == w, "%d px: largura do documento igual à da tela (%d)" % (w, sw))
            # nada que vaze da tela fora de rolagem local
            vaza = pg.evaluate("""(w)=>{const r=[];document.querySelectorAll('body *').forEach(e=>{
                if(e.closest('pre,.tabela-wrap,.lk-codigo,.vf-corrido,.lk-eco,.vviz-tabela-oculta,.lk-palco[data-rola],.lk-viz'))return;const b=e.getBoundingClientRect();
                if(b.width&&b.right>w+0.5)r.push((e.className||e.tagName)+' '+Math.round(b.right))});return r.slice(0,5)}""", w)
            ok(not vaza, "%d px: nenhum elemento passa da borda %s" % (w, vaza))
            # palcos: o conteúdo cabe no palco
            corte = pg.evaluate("""()=>{const r=[];document.querySelectorAll('.lk-palco').forEach(p=>{
                const pb=p.getBoundingClientRect();const host=p.querySelector('.lk-host');if(!host)return;
                if(p.hasAttribute('data-rola')){if(p.scrollWidth<=p.clientWidth)r.push(p.closest('.lk-trecho').id+' rolagem sem conteúdo');return}
                host.shadowRoot.querySelectorAll('*').forEach(e=>{const b=e.getBoundingClientRect();
                if(e.closest&&e.closest('.tv-corrido'))return;
                if(b.width&&(b.right>pb.right+1||b.left<pb.left-1))r.push(p.closest('.lk-trecho').id+' '+e.tagName)})});return r.slice(0,6)}""")
            ok(not corte, "%d px: nenhuma prévia cortada %s" % (w, corte))
            rola = pg.evaluate("()=>Array.from(document.querySelectorAll('.lk-palco[data-rola]')).map(p=>p.closest('.lk-trecho').id+': '+p.getAttribute('data-rola'))")
            for r_ in rola:
                avisos.append("%d px: rolagem local sinalizada em %s" % (w, r_))
            # mínimos dos logotipos e selos dentro das prévias
            med = pg.evaluate("""()=>{const r=[];document.querySelectorAll('.lk-host').forEach(hh=>{
                if(hh.getAttribute('data-alvo')==='amostra')return;
                hh.shadowRoot.querySelectorAll('img').forEach(i=>{const b=i.getBoundingClientRect();
                r.push({id:hh.closest('.lk-trecho').id,src:i.getAttribute('src').slice(0,80),uri:(DATA=>{for(const k in DATA){if(DATA[k].uri===i.getAttribute('src'))return k}return ''})(window.LK.dados),w:b.width,h:b.height})})});return r}""")
            for m in med:
                nome = m["uri"] or m["src"]
                if "selo-completo" in nome:
                    ok(m["w"] >= 199.5, "%d px: %s selo completo com %.0f px (mínimo 200)" % (w, m["id"], m["w"]))
                elif "selo-simples" in nome:
                    ok(m["w"] >= 95.5, "%d px: %s selo simples com %.0f px (mínimo 96)" % (w, m["id"], m["w"]))
                elif "vertical" in nome:
                    ok(m["h"] >= 79.5, "%d px: %s vertical com %.0f px de altura (mínimo 80)" % (w, m["id"], m["h"]))
                elif "void-" in nome:
                    ok(m["h"] >= 23.5, "%d px: %s logotipo com %.1f px de altura (mínimo 24)" % (w, m["id"], m["h"]))
            if w != 1440:
                pg.close()
                continue

            # ---- critérios da linha lockup.html (em 1440) ----
            pg.evaluate("""()=>{window.__copias=[];navigator.clipboard.writeText=t=>{window.__copias.push(t);return Promise.resolve()}}""")
            trechos = pg.evaluate("""()=>Array.from(document.querySelectorAll('.lk-trecho:not([data-demo])')).map(a=>({id:a.id,
                botao:!!a.querySelector('button.lk-copiar'),texto:a.getAttribute('data-formato')==='texto',head:a.getAttribute('data-alvo')==='head',
                fonte:(a.querySelector('.lk-fonte')||{}).textContent||null}))""")
            ok(len(trechos) >= 45, "trechos encontrados: %d" % len(trechos))
            for t in trechos:
                ok(t["botao"], "%s tem botão Copiar" % t["id"])
                pg.click("#%s button.lk-copiar" % t["id"])
                copiado = pg.evaluate("window.__copias[window.__copias.length-1]")
                codigo = pg.evaluate("id=>document.getElementById(id).__codigo", t["id"])
                ok(copiado == codigo, "%s: o botão copia exatamente o trecho" % t["id"])
                if t["fonte"] is not None:
                    esperado = pg.evaluate("s=>window.LK.resolve(s.replace(/^\\s+|\\s+$/g,''))", t["fonte"])
                    ok(copiado == esperado, "%s: o copiado é o texto-fonte (com data URI resolvido)" % t["id"])
                if t["texto"]:
                    vis = pg.evaluate("id=>document.querySelector('#'+id+' .lk-palco-texto').textContent", t["id"])
                    ok(vis == copiado, "%s: o texto mostrado é o texto copiado" % t["id"])
                    continue
                if t["head"]:
                    oks.append("%s: trecho de <head> (não desenha; a prévia mostra o que ele carrega)" % t["id"])
                    continue
                igual = pg.evaluate("""([id,c])=>{const h=document.querySelector('#'+id+' .lk-host');
                    const tpl=document.createElement('template');tpl.innerHTML=c;
                    const d=document.createElement('div');d.innerHTML=h.shadowRoot.innerHTML;
                    d.querySelector('style').remove();return d.innerHTML===tpl.innerHTML}""", [t["id"], copiado])
                ok(igual, "%s: a prévia é o DOM do texto copiado" % t["id"])
                # prova visual: o copiado, sozinho numa página em branco do sistema, desenha igual à prévia
                caixa = pg.evaluate("""id=>{const h=document.querySelector('#'+id+' .lk-host');const b=h.getBoundingClientRect();
                    return {w:b.width,h:b.height,fx:b.left-Math.floor(b.left),fy:b.top-Math.floor(b.top),fundo:h.getAttribute('data-fundo')}}""", t["id"])
                if caixa["w"] < 1 or caixa["h"] < 1:
                    falhas.append("%s: prévia sem tamanho" % t["id"])
                    continue
                el = pg.query_selector("#%s .lk-host" % t["id"])
                el.scroll_into_view_if_needed()
                pg.wait_for_timeout(60)
                a = el.screenshot(animations="disabled")
                cor_texto = "#181818" if caixa["fundo"] == "tela" else "#DCDDD8"
                limpa = nav.new_page(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
                html = ('<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><base href="%s">' % (RAIZ.as_uri() + "/") + FONTES +
                        '<style>body{margin:0;background:%s;color:%s;font:400 18px/1.65 "Nunito Sans",Arial,sans-serif;-webkit-font-smoothing:antialiased}'
                        '#alvo{display:flow-root;position:absolute;left:%.4fpx;top:%.4fpx;width:%.4fpx}</style></head><body><div id="alvo">%s</div></body></html>'
                        % (FUNDO.get(caixa["fundo"], "#181818"), cor_texto, 40 + caixa["fx"], 40 + caixa["fy"], caixa["w"], copiado))
                tmp = RAIZ / "tools" / "_tmp_lockup_teste.html"
                tmp.write_text(html, encoding="utf-8")
                limpa.goto(tmp.as_uri())
                limpa.wait_for_load_state("networkidle")
                limpa.evaluate("document.fonts.ready")
                limpa.wait_for_timeout(250)
                b = limpa.query_selector("#alvo").screenshot(animations="disabled")
                pct, tam = diff_pct(a, b)
                if pct is not None and pct >= 1.0:  # uma nova tentativa: fonte que ainda carregava
                    limpa.wait_for_timeout(500); pg.wait_for_timeout(300)
                    a = el.screenshot(animations="disabled")
                    b = limpa.query_selector("#alvo").screenshot(animations="disabled")
                    pct, tam = diff_pct(a, b)
                limpa.close()
                if pct is None:
                    falhas.append("%s: tamanho da prévia difere do copiado %s" % (t["id"], tam))
                else:
                    ok(pct < 1.0, "%s: prévia e copiado desenham igual (%.3f%% de pixels diferentes)" % (t["id"], pct))
                    if capturas and pct >= 1.0:
                        Image.open(io.BytesIO(a)).save(Path(capturas) / ("dif-%s-a.png" % t["id"]))
                        Image.open(io.BytesIO(b)).save(Path(capturas) / ("dif-%s-b.png" % t["id"]))
            tmp = RAIZ / "tools" / "_tmp_lockup_teste.html"
            if tmp.exists():
                tmp.unlink()

            # nenhum logotipo em texto: THE VOID nunca em título; logotipo só por <img> de arquivo oficial
            titulos = pg.evaluate("""()=>{const r=[];const ver=raiz=>raiz.querySelectorAll('h1,h2,h3,h4,.titulo-filme,.titulo-secao,.fala,.lk-trecho-t').forEach(e=>{if(/the\\s*void/i.test(e.textContent))r.push(e.textContent.trim().slice(0,40))});
                ver(document);document.querySelectorAll('.lk-host').forEach(h=>ver(h.shadowRoot));return r}""")
            ok(not titulos, "nenhum THE VOID digitado em título %s" % titulos)
            textos_logo = pg.evaluate("""()=>{const r=[];const ok=/TATTOO ACADEMY|THE VOID (START|MASTER|PRO)$|THE VOID TATTOO ACADEMY|THE VOID TATTOO ·/;
                document.querySelectorAll('.lk-host').forEach(h=>{const w=document.createTreeWalker(h.shadowRoot,NodeFilter.SHOW_TEXT);let n;
                while(n=w.nextNode()){const t=n.textContent.trim();if(/^THE\\s+VOID\\b/.test(t)&&!ok.test(t))r.push(h.closest('.lk-trecho').id+': '+t.slice(0,40))}});return r}""")
            ok(not textos_logo, "nenhum THE VOID solto no lugar do logotipo (só Rótulo, Ficha e Letreiro literais) %s" % textos_logo)
            srcs = pg.evaluate("""()=>{const r=[];document.querySelectorAll('.lk-host').forEach(h=>h.shadowRoot.querySelectorAll('img').forEach(i=>r.push(i.getAttribute('src'))));return r}""")
            oficiais = {d["uri"] for d in json.loads(pg.evaluate("document.getElementById('lk-datauri').textContent")).values()}
            for s_ in srcs:
                ok(s_.startswith("assets/brand/") or s_ in oficiais, "imagem de marca vem de arquivo oficial: %s" % s_[:60])

            # gerador do logotipo: recusa abaixo do mínimo
            pg.fill("#lk-altura", "10")
            pg.dispatch_event("#lk-altura", "input")
            ok(pg.is_visible("#lk-aviso-logo"), "gerador avisa abaixo do mínimo")
            ok('height="24"' in pg.evaluate("document.getElementById('t-gerador-logo').__codigo"), "gerador sai no mínimo de 24 px")
            pg.click('#t-gerador-logo [data-controle="versao"] button[data-v="vertical"]')
            pg.fill("#lk-altura", "40"); pg.dispatch_event("#lk-altura", "input")
            ok('height="80"' in pg.evaluate("document.getElementById('t-gerador-logo').__codigo"), "gerador sobe o vertical para 80 px")
            pg.click('#t-gerador-logo [data-controle="formato"] button[data-v="uri"]')
            cod = pg.evaluate("document.getElementById('t-gerador-logo').__codigo")
            ok("data:image/svg+xml" in cod and cod.split('src="')[1].split('"')[0] in oficiais, "gerador em data URI usa o arquivo oficial")
            for v in ["horizontal", "start", "master", "pro"]:
                for c in ["branco", "preto"]:
                    for fmt in ["svg", "png", "uri"]:
                        pg.click('#t-gerador-logo [data-controle="versao"] button[data-v="%s"]' % v)
                        pg.click('#t-gerador-logo [data-controle="cor"] button[data-v="%s"]' % c)
                        pg.click('#t-gerador-logo [data-controle="formato"] button[data-v="%s"]' % fmt)
                        pg.fill("#lk-altura", "40"); pg.dispatch_event("#lk-altura", "input")
                        pg.click("#t-gerador-logo button.lk-copiar")
                        cop = pg.evaluate("window.__copias[window.__copias.length-1]")
                        fundo = pg.evaluate("document.querySelector('#t-gerador-logo .lk-palco').getAttribute('data-fundo')")
                        nat = pg.evaluate("()=>{const i=document.querySelector('#t-gerador-logo .lk-host').shadowRoot.querySelector('img');return i.complete&&i.naturalWidth>0}")
                        ok(nat and (fundo == ("sala" if c == "branco" else "tela")) and ("void-%s-%s" % (v, c) in cop or cop.split('src="')[1].split('"')[0] in oficiais),
                           "gerador %s %s %s: carrega, fundo certo, copia o que mostra" % (v, c, fmt))

            # WhatsApp: mensagem e link coerentes
            for k in ["start", "master", "pro", "aula", "talks"]:
                pg.click('#t-whatsapp [data-controle="origem"] button[data-v="%s"]' % k)
                msg = pg.evaluate("document.getElementById('t-whatsapp').__codigo")
                link = pg.evaluate("document.getElementById('t-whatsapp-link').__codigo")
                ok(link.endswith(pg.evaluate("m=>encodeURIComponent(m)", msg)) and "{{WHATSAPP_OFICIAL}}" in link and not re.search(r"[\U0001F300-\U0001FAFF]", msg),
                   "WhatsApp %s: link leva a mesma mensagem, sem emoji, número pendente" % k)

            # vviz: dado em validação não exporta
            pg.click("#lk-viz-exportar")
            ok("recusada" in pg.inner_text("#lk-viz-msg"), "vviz recusa exportar dado em validação")
            # movimento reduzido: Letreiro Corrido parado
            anim = pg.evaluate("()=>{const h=document.querySelector('#t-corrido .lk-host');return getComputedStyle(h.shadowRoot.querySelector('.tv-corrido-trilho')).animationName}")
            ok(anim == "none", "Letreiro Corrido parado com movimento reduzido")
            pg.close()
        nav.close()


def main():
    capturas = None
    if "--capturas" in sys.argv:
        capturas = sys.argv[sys.argv.index("--capturas") + 1]
        Path(capturas).mkdir(parents=True, exist_ok=True)
    estatico()
    dinamico(capturas)
    print("aprovados: %d · reprovados: %d" % (len(oks), len(falhas)))
    for a_ in avisos:
        print("AVISO:", a_)
    for f in falhas:
        print("FALHA:", f)
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
