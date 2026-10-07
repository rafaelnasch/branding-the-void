#!/usr/bin/env python3
"""Exporta HTML da marca The VOID em PDF, na pasta dist/.

Uso, na pasta do repositório (precisa de Playwright com Chromium):
  python3 exportar_pdf.py                    # brand-book.html (A4) e deck-template.html (1440 por 900)
  python3 exportar_pdf.py brand-book.html    # só o manual -> dist/brand-book.pdf
  python3 exportar_pdf.py deck-template.html # só o deck   -> dist/apresentacao-the-void.pdf
  python3 exportar_pdf.py dist/x.html        # qualquer HTML (o autocontido também serve)

O PDF usa a folha de impressão do próprio arquivo: A4 no manual (seção em página nova, sumário,
botões e seletores escondidos), 1440 por 900 no deck (um slide por página). Movimento desligado,
fontes carregadas e formas dos motores montadas antes de imprimir. Foto com miniatura no
srcset imprime a miniatura de 640 px (o manual fica bem abaixo de 60 MB). Depois confere: número de
páginas, página sem texto nem imagem (em branco) e link file:// (caminho do computador), que
apaga o PDF e falha.
"""
import functools
import http.server
import io
import re
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

PASTA = Path(__file__).resolve().parent
NOMES = {"brand-book.html": "brand-book.pdf",
         "brand-book-the-void.html": "brand-book.pdf",
         "deck-template.html": "apresentacao-the-void.pdf",
         "apresentacao-the-void.html": "apresentacao-the-void.pdf",
         "guia-de-uso.html": "guia-de-uso-the-void.pdf",
         "membros-ui.html": "area-de-membros-the-void.pdf"}
DECK = {"deck-template.html", "apresentacao-the-void.html"}
# fotos do acervo, mockups e demonstrações: no PDF entram como JPEG de até 1000 px (o Chromium
# embute JPEG como está; WebP ele descompacta e o PDF passa de 100 MB)
RE_FOTO = re.compile(r"^/assets/(?:foto/(?:acervo|personas|demo)|aplicacoes/(?:mockups|email-foto)|video/canal)/[^/]+\.(?:webp|png|jpe?g)$")
LADO_PDF = 1000


class Servidor(http.server.SimpleHTTPRequestHandler):
    """Serve a pasta do repositório; foto vira JPEG leve na hora (o arquivo não muda)."""
    def log_message(self, *a):
        pass

    def do_GET(self):
        caminho = self.path.split("?")[0]
        if RE_FOTO.match(caminho):
            from PIL import Image
            arq = PASTA / caminho.lstrip("/")
            if arq.is_file():
                im = Image.open(arq)
                if im.mode in ("RGBA", "LA", "P") and "A" in im.getbands() or (im.mode == "P" and "transparency" in im.info):
                    return super().do_GET()
                im = im.convert("RGB")
                im.thumbnail((LADO_PDF, LADO_PDF), Image.LANCZOS)
                buf = io.BytesIO()
                im.save(buf, "JPEG", quality=72, optimize=True, progressive=False)
                dados = buf.getvalue()
                self.send_response(200)
                self.send_header("Content-Type", "image/jpeg")
                self.send_header("Content-Length", str(len(dados)))
                self.end_headers()
                self.wfile.write(dados)
                return
        return super().do_GET()


def exportar(arquivo):
    saida = PASTA / "dist" / NOMES.get(arquivo.name, arquivo.with_suffix(".pdf").name)
    saida.parent.mkdir(exist_ok=True)
    deck = arquivo.name in DECK
    largura, altura = (1440, 900) if deck else (1200, 900)
    dentro = PASTA in arquivo.resolve().parents
    srv = None
    if dentro:
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Servidor, directory=str(PASTA)))
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        endereco = "http://127.0.0.1:%d/%s" % (srv.server_address[1], arquivo.resolve().relative_to(PASTA).as_posix())
    else:
        endereco = arquivo.as_uri()
    with sync_playwright() as p:
        nav = p.chromium.launch()
        ctx = nav.new_context(viewport={"width": largura, "height": altura}, reduced_motion="reduce")
        pag = ctx.new_page()
        pag.goto(endereco, wait_until="networkidle", timeout=120000)
        pag.evaluate("""() => {
          document.querySelectorAll('img[loading=lazy]').forEach(i => { i.loading = 'eager'; });
          // impressão leve: foto com miniatura no srcset (mesma proporção) imprime a miniatura
          // de 640 px; o PDF do manual fica bem abaixo de 60 MB.
          document.querySelectorAll('img[srcset*="_thumb."], source[srcset*="_thumb."]').forEach(i => {
            i.setAttribute('sizes', '600px');
          });
          // link relativo para arquivo vira file:///caminho/do/computador dentro do PDF:
          // no PDF ele fica como texto, sem link (as âncoras internas continuam).
          document.querySelectorAll('a[href]').forEach(a => {
            const h = a.getAttribute('href');
            if ((a.href.startsWith('file:') || a.origin === location.origin) && !h.startsWith('#')) a.removeAttribute('href');
          });
        }""")
        pag.wait_for_function("Array.from(document.images).every(i => i.complete)", timeout=120000)
        pag.evaluate("document.fonts.ready.then(() => true)")
        pag.wait_for_timeout(1500)
        pag.emulate_media(media="print", reduced_motion="reduce")
        pag.wait_for_timeout(500)
        # print_background é obrigatório: sem ele a Sala some e o texto claro fica invisível.
        pag.pdf(path=str(saida), print_background=True, prefer_css_page_size=True)
        nav.close()
    if srv:
        srv.shutdown()
    bruto = saida.read_bytes()
    if b"file://" in bruto or b"127.0.0.1" in bruto:
        saida.unlink()
        sys.exit("ERRO: o PDF de %s continha link file:// (caminho local) e foi apagado." % arquivo.name)
    conferir(saida)
    return saida


def conferir(saida):
    try:
        from pypdf import PdfReader
    except ImportError:
        print("PDF gravado em %s (pypdf ausente: páginas não conferidas)" % saida)
        return
    leitor = PdfReader(str(saida))
    vazias = []
    for i, pg in enumerate(leitor.pages, 1):
        texto = (pg.extract_text() or "").strip()
        recursos = pg.get("/Resources") or {}
        tem_imagem = bool(recursos.get("/XObject")) if hasattr(recursos, "get") else False
        if not texto and not tem_imagem:
            vazias.append(i)
    tam = leitor.pages[0].mediabox
    print("PDF gravado em %s: %d páginas de %.0f por %.0f pt, %d KB%s" % (
        saida.relative_to(PASTA), len(leitor.pages), float(tam.width), float(tam.height),
        saida.stat().st_size // 1024, ("; páginas sem conteúdo: %s" % vazias) if vazias else "; nenhuma página em branco"))
    if vazias:
        sys.exit("ERRO: página em branco no PDF")


if __name__ == "__main__":
    nomes = sys.argv[1:] or ["brand-book.html", "deck-template.html"]
    for nome in nomes:
        arquivo = Path(nome) if Path(nome).is_absolute() else PASTA / nome
        if not arquivo.is_file():
            sys.exit("arquivo não existe: %s" % arquivo)
        exportar(arquivo)
