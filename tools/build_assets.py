#!/usr/bin/env python3
"""Gera assets/brand/ a partir de assets/referencia-original/ (exportação do Figma da aureadesign.co).

A pasta assets/referencia-original/ é LOCAL: guarda os arquivos-mestre da agência e fica fora do
repositório público (.gitignore). Os derivados oficiais já publicados estão em assets/brand/; este
script só é necessário para regenerá-los, com a exportação original copiada para essa pasta.

Regras:
- SVG oficiais sao copiados byte a byte (so o nome muda para minusculas/kebab-case).
- Variacoes de cor trocam APENAS o valor do atributo fill="black"/fill="white" por um hex exato.
  Nenhuma coordenada e alterada.
- Favicon e avatar usam paths oficiais (O e V do VOID, lockup vertical) apenas com
  transformacao (escala/translacao); a geometria de cada path fica intacta.

Uso: python3 tools/build_assets.py
Requer: playwright (chromium) e Pillow.
"""
import hashlib, io, json, re, shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ORIG = ROOT / "assets" / "referencia-original"
OUT = ROOT / "assets" / "brand"

GRAFITE = "#181818"
OFFWHITE = "#F8F9F4"

NOMES = {
    "SVG/LOGO-HORIZONTAL-PRETO.svg": "void-horizontal-preto.svg",
    "SVG/LOGO-HORIZONTAL-BRANCO.svg": "void-horizontal-branco.svg",
    "SVG/LOGO-VERTICAL-PRETO.svg": "void-vertical-preto.svg",
    "SVG/LOGO-VERTICAL-BRANCO.svg": "void-vertical-branco.svg",
    "SVG/LOGO-VOID-START-PRETO.svg": "void-start-preto.svg",
    "SVG/LOGO-VOID-START-BRANCO.svg": "void-start-branco.svg",
    "SVG/LOGO-VOID-MASTER-PRETO.svg": "void-master-preto.svg",
    "SVG/LOGO-VOID-MASTER-BRANCO.svg": "void-master-branco.svg",
    "SVG/LOGO-VOID-PRO-PRETO.svg": "void-pro-preto.svg",
    "SVG/LOGO-VOID-PRO-BRANCO.svg": "void-pro-branco.svg",
    "ICONES/SVG/ICONE-COMPLETO-START.svg": "selo-completo-start.svg",
    "ICONES/SVG/ICONE-COMPLETO-MASTER.svg": "selo-completo-master.svg",
    "ICONES/SVG/ICONE-COMPLETO-PRO.svg": "selo-completo-pro.svg",
    "ICONES/SVG/ICONE-SIMPLES-START.svg": "selo-simples-start.svg",
    "ICONES/SVG/ICONE-SIMPLES-MASTER.svg": "selo-simples-master.svg",
    "ICONES/SVG/ICONE-SIMPLES-PRO.svg": "selo-simples-pro.svg",
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def dims(svg_text):
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg_text)
    return float(m.group(1)), float(m.group(2))


def paths(svg_text):
    return re.findall(r'<path d="([^"]+)"', svg_text)


def main():
    if not (ORIG / "SVG").is_dir() or not (ORIG / "ICONES" / "SVG").is_dir():
        raise SystemExit(
            "build_assets.py: falta a pasta local assets/referencia-original/ (SVG/ e ICONES/SVG/).\n"
            "Ela guarda os arquivos-mestre da aureadesign.co e não vai para o repositório público.\n"
            "Os arquivos prontos já estão em assets/brand/. Para regenerá-los, copie a exportação do Figma\n"
            "entregue pela agência para assets/referencia-original/ e rode o script de novo.")
    for sub in ["svg", "svg/cor", "png/alta", "png/web", "webp", "favicon", "social"]:
        (OUT / sub).mkdir(parents=True, exist_ok=True)

    manifest = {"oficiais": {}, "cor": {}}
    # 1. copias oficiais
    for src, dst in NOMES.items():
        shutil.copyfile(ORIG / src, OUT / "svg" / dst)
        assert sha(ORIG / src) == sha(OUT / "svg" / dst)
        manifest["oficiais"][dst] = {"origem": src, "sha256": sha(OUT / "svg" / dst)}

    # 2. recolor exato (somente logotipos monocromaticos, a partir da versao preta)
    for dst in [d for d in NOMES.values() if d.startswith("void-") and d.endswith("-preto.svg")]:
        txt = (OUT / "svg" / dst).read_text()
        base = dst.replace("-preto.svg", "")
        for nome, hexa in [("grafite", GRAFITE), ("offwhite", OFFWHITE)]:
            novo = txt.replace('fill="black"', f'fill="{hexa}"')
            # garantia: somente o atributo fill mudou
            assert re.sub(r'fill="[^"]*"', "", novo) == re.sub(r'fill="[^"]*"', "", txt)
            out = OUT / "svg" / "cor" / f"{base}-{nome}.svg"
            out.write_text(novo)
            manifest["cor"][out.name] = {"base": dst, "fill": hexa}

    horiz = (ORIG / "SVG/LOGO-HORIZONTAL-PRETO.svg").read_text()
    vert = (ORIG / "SVG/LOGO-VERTICAL-PRETO.svg").read_text()
    void_d = paths(horiz)[0]
    subs = [s for s in re.split(r"(?=M)", void_d) if s.strip()]
    v_d = subs[0]                 # V
    o_d = subs[1] + subs[2]       # O (contorno externo + contraforma)

    # 3. favicon (PROPOSTA): O do VOID, o "vazio", em off-white sobre grafite
    # bbox do O no SVG horizontal: x 1244.73..1791.81, y 2.73..573.46
    ox0, oy0, ow, oh = 1244.73, 2.73, 547.08, 570.73
    def icon_svg(d, x0, y0, w, h, frac, fill=OFFWHITE, bg=GRAFITE, size=512):
        s = size * frac / max(w, h)
        tx = (size - w * s) / 2 - x0 * s
        ty = (size - h * s) / 2 - y0 * s
        bgrect = f'<rect width="{size}" height="{size}" fill="{bg}"/>' if bg else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">'
                f'{bgrect}<path transform="translate({tx:.3f} {ty:.3f}) scale({s:.6f})" d="{d}" fill="{fill}"/></svg>')

    fav = icon_svg(o_d, ox0, oy0, ow, oh, 0.62)
    (OUT / "favicon" / "favicon.svg").write_text(fav)
    fav_v = icon_svg(v_d, 726.4, 12.19, 536.83, 551.81, 0.60)
    (OUT / "favicon" / "favicon-alternativa-v.svg").write_text(fav_v)
    # versao adaptavel a tema escuro do navegador (sem fundo, cor por media query)
    fav_auto = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><style>path{{fill:{GRAFITE}}}'
                f'@media (prefers-color-scheme: dark){{path{{fill:{OFFWHITE}}}}}</style>'
                + re.search(r"<path[^>]+/>", icon_svg(o_d, ox0, oy0, ow, oh, 0.86, bg=None)).group(0).replace(f' fill="{OFFWHITE}"', "")
                + "</svg>")
    (OUT / "favicon" / "favicon-adaptavel.svg").write_text(fav_auto)

    # 4. avatar 1080 e imagem de compartilhamento 1200x630
    vw, vh = dims(vert)
    vpaths = "".join(f'<path d="{d}" fill="{OFFWHITE}"/>' for d in paths(vert))
    avatar_w = 1080 * 0.68
    s = avatar_w / vw
    avatar = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">'
              f'<rect width="1080" height="1080" fill="{GRAFITE}"/>'
              f'<g transform="translate({(1080 - vw * s) / 2:.3f} {(1080 - vh * s) / 2:.3f}) scale({s:.6f})">{vpaths}</g></svg>')
    (OUT / "social" / "avatar-1080.svg").write_text(avatar)

    hw, hh = dims(horiz)
    hpaths = "".join(f'<path d="{d}" fill="{OFFWHITE}"/>' for d in paths(horiz))
    og_w = 820
    s2 = og_w / hw
    og_html = f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@1,6..72,300&family=Archivo:wght@400;500&display=block" rel="stylesheet">
<style>html,body{{margin:0;width:1200px;height:630px;background:{GRAFITE};overflow:hidden}}
.w{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:44px}}
.t{{font-family:Newsreader;font-style:italic;font-weight:300;font-variation-settings:'opsz' 72;font-size:44px;color:{OFFWHITE};opacity:.88;letter-spacing:.005em}}
.f{{position:absolute;left:0;right:0;bottom:34px;display:flex;justify-content:center;gap:42px;font:400 15px Archivo;letter-spacing:.14em;color:#898989;text-transform:uppercase}}</style></head>
<body><div class="w"><svg width="{og_w}" height="{hh * s2:.1f}" viewBox="0 0 {hw:.0f} {hh:.0f}">{hpaths}</svg>
<div class="t">A arte que preenche. A carreira que liberta.</div></div>
<div class="f"><span>Tattoo Academy</span><span>Vila Madalena</span><span>São Paulo</span></div></body></html>"""
    (OUT / "social" / "og-1200x630.html").write_text(og_html)

    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()

        def render_svg(svg_text, w, h, out_png, transparent=True):
            pg.set_viewport_size({"width": int(w), "height": int(h)})
            svg_text = re.sub(r'<svg ([^>]*?)width="[^"]+" height="[^"]+"', r'<svg \1', svg_text, count=1)
            svg_text = svg_text.replace("<svg ", f'<svg width="{int(w)}" height="{int(h)}" preserveAspectRatio="xMidYMid meet" ', 1)
            pg.set_content(f"<html><body style='margin:0;background:transparent'>{svg_text}</body></html>")
            pg.screenshot(path=str(out_png), omit_background=transparent, clip={"x": 0, "y": 0, "width": int(w), "height": int(h)})

        # PNG alta (lado maior 4000 para logos, 2400 para selos) e web (1200 / 800)
        alvos = sorted((OUT / "svg").glob("*.svg")) + sorted((OUT / "svg" / "cor").glob("*.svg"))
        for f in alvos:
            txt = f.read_text()
            w, h = dims(txt)
            big = 4000 if f.name.startswith("void-") else 2400
            web = 1200 if f.name.startswith("void-") else 800
            for lado, pasta in [(big, "png/alta"), (web, "png/web")]:
                k = lado / max(w, h)
                outp = OUT / pasta / f.name.replace(".svg", ".png")
                render_svg(txt, round(w * k), round(h * k), outp)
                if pasta == "png/web":
                    Image.open(outp).save(OUT / "webp" / f.name.replace(".svg", ".webp"), "WEBP", quality=92, method=6)

        # favicons
        for n in (16, 32, 48, 180, 192, 512):
            render_svg(fav, n, n, OUT / "favicon" / f"favicon-{n}.png", transparent=False)
        shutil.copyfile(OUT / "favicon" / "favicon-180.png", OUT / "favicon" / "apple-touch-icon.png")
        render_svg(fav_v, 512, 512, OUT / "favicon" / "favicon-alternativa-v-512.png", transparent=False)
        ico_src = Image.open(OUT / "favicon" / "favicon-48.png")
        ico_src.save(OUT / "favicon" / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

        render_svg(avatar, 1080, 1080, OUT / "social" / "avatar-1080.png", transparent=False)
        pg.set_viewport_size({"width": 1200, "height": 630})
        pg.goto((OUT / "social" / "og-1200x630.html").as_uri())
        pg.wait_for_load_state("networkidle")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(600)
        pg.screenshot(path=str(OUT / "social" / "og-1200x630.png"))
        b.close()

    (OUT / "favicon" / "site.webmanifest").write_text(json.dumps({
        "name": "The Void Tattoo Academy", "short_name": "The Void",
        "icons": [{"src": "favicon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "favicon-512.png", "sizes": "512x512", "type": "image/png"}],
        "theme_color": GRAFITE, "background_color": GRAFITE, "display": "standalone"}, ensure_ascii=False, indent=2))
    (OUT / "_manifest-arquivos.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print("ok")


if __name__ == "__main__":
    main()
