#!/usr/bin/env python3
"""
THE VOID · gera os logotipos em data URI do lockup.html a partir dos SVG oficiais.

Por que existe: o logotipo é desenho, nunca texto, e nunca é digitado à mão. O data
URI de cada versão sai daqui, lido byte a byte do arquivo oficial em assets/brand/svg,
e é gravado no lockup.html entre os marcadores

    <!-- lockup-datauri:inicio -->  ...  <!-- lockup-datauri:fim -->

como um bloco <script type="application/json" id="lk-datauri">. O lockup.html troca
cada {{uri:nome}} dos trechos pelo data URI correspondente na hora de mostrar e de
copiar.

Codificação: percent-encoding (RFC 3986) do arquivo inteiro, com espaço, aspas
simples e alguns sinais mantidos legíveis. É reversível: urllib.parse.unquote(uri)
devolve exatamente os bytes do arquivo oficial (o teste --verificar confere).

Uso:
    python3 tools/gerar_lockup_datauri.py             grava o bloco no lockup.html
    python3 tools/gerar_lockup_datauri.py --verificar sai com 1 se o bloco não bater
                                                      com os arquivos oficiais
"""
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote, unquote

RAIZ = Path(__file__).resolve().parent.parent
LOCKUP = RAIZ / "lockup.html"
SVG = RAIZ / "assets" / "brand" / "svg"
FAV = RAIZ / "assets" / "brand" / "favicon"

# só os arquivos oficiais (preto e branco) e o favicon proposto [P 12]
ARQUIVOS = [
    ("void-horizontal-branco", SVG / "void-horizontal-branco.svg"),
    ("void-horizontal-preto", SVG / "void-horizontal-preto.svg"),
    ("void-vertical-branco", SVG / "void-vertical-branco.svg"),
    ("void-vertical-preto", SVG / "void-vertical-preto.svg"),
    ("void-start-branco", SVG / "void-start-branco.svg"),
    ("void-start-preto", SVG / "void-start-preto.svg"),
    ("void-master-branco", SVG / "void-master-branco.svg"),
    ("void-master-preto", SVG / "void-master-preto.svg"),
    ("void-pro-branco", SVG / "void-pro-branco.svg"),
    ("void-pro-preto", SVG / "void-pro-preto.svg"),
    ("favicon", FAV / "favicon.svg"),
]

INI = "<!-- lockup-datauri:inicio -->"
FIM = "<!-- lockup-datauri:fim -->"
SEGUROS = " '/:=;,.-_()!*~"


def codificar(dados: bytes) -> str:
    texto = dados.decode("utf-8")
    return "data:image/svg+xml;charset=utf-8," + quote(texto, safe=SEGUROS)


def viewbox(texto: str):
    m = re.search(r'viewBox="([\d.\s-]+)"', texto)
    return [float(v) if "." in v else int(v) for v in m.group(1).split()] if m else None


def montar():
    saida = {}
    for nome, caminho in ARQUIVOS:
        dados = caminho.read_bytes()
        uri = codificar(dados)
        assert unquote(uri.split(",", 1)[1]).encode("utf-8") == dados, nome
        saida[nome] = {
            "arquivo": str(caminho.relative_to(RAIZ)),
            "bytes": len(dados),
            "sha256": hashlib.sha256(dados).hexdigest(),
            "viewBox": viewbox(dados.decode("utf-8")),
            "uri": uri,
        }
    return saida


def bloco(dados) -> str:
    corpo = json.dumps(dados, ensure_ascii=False, separators=(",", ":"))
    corpo = corpo.replace("</", "<\\/")  # nunca fechar o <script> por acidente
    return INI + '\n<script type="application/json" id="lk-datauri">' + corpo + "</script>\n" + FIM


def main():
    html = LOCKUP.read_text(encoding="utf-8")
    if INI not in html or FIM not in html:
        sys.exit("lockup.html sem os marcadores " + INI + " e " + FIM)
    atual = re.search(re.escape(INI) + r".*?" + re.escape(FIM), html, re.S).group(0)
    novo = bloco(montar())
    if "--verificar" in sys.argv:
        if atual != novo:
            print("ERRO: data URI do lockup.html diverge dos SVG oficiais. Rode sem --verificar.")
            sys.exit(1)
        print("ok: %d data URI conferidos byte a byte com os arquivos oficiais" % len(ARQUIVOS))
        return
    LOCKUP.write_text(html.replace(atual, novo), encoding="utf-8")
    print("gravado: %d data URI em lockup.html" % len(ARQUIVOS))


if __name__ == "__main__":
    main()
