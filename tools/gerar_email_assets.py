#!/usr/bin/env python3
"""Gera as imagens do e-mail da The VOID (spec 12.5, 5.2, 5.6 e 6.4).

Saídas em assets/aplicacoes/:
  placa-email-600.png          cabeçalho do e-mail: faixa Sala de 600 por 64 px desenhada em 2x
                               (1200 por 128), com Janela de Luz, grão e o logotipo horizontal
                               branco oficial a 200 px de largura e 24 px da margem esquerda.
  selo-email-start.png         selo simples Start em 2x para 96 px (192 por 192), fundo transparente.
  selo-email-master.png        selo simples Master, idem.
  selo-email-pro.png           selo simples Pro assentado no disco Coxia (spec 5.6: folga de 4%
                               do diâmetro), 2x para 104 px (208 por 208).

Regras:
  · O logotipo e os selos saem dos PNG oficiais em assets/brand/png/alta (redução, nunca redesenho).
  · Janela de Luz: radial-gradient(110% 75% at 12% 0%, Tela a 9% até 0 em 62%) sobre Sala (spec 6.4).
  · Grão: ladrilho assets/textura/grao-240.webp a 6% em modo tela (spec 6.1).
  · Determinístico: nenhuma data, nenhum metadado variável. Rode duas vezes e compare (--verificar).

Uso:
  python3 tools/gerar_email_assets.py
  python3 tools/gerar_email_assets.py --verificar
Precisa de numpy e Pillow.
"""
import hashlib
import os
import sys
import tempfile

import numpy as np
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, 'assets', 'aplicacoes')
BRAND = os.path.join(RAIZ, 'assets', 'brand', 'png', 'alta')
GRAO = os.path.join(RAIZ, 'assets', 'textura', 'grao-240.webp')

SALA = (24, 24, 24)
TELA = (248, 249, 244)
COXIA = (43, 43, 43)
ESCALA = 2                      # imagens em 2x
PLACA = (600, 64)               # tamanho de exibição do cabeçalho
LOGO_LARGURA = 200              # spec 12.5: logotipo a 200 px (mínimo 158)
MARGEM = 24                     # spec 7.1: margem do e-mail
SELO = 96                       # spec 5.2: selo simples a partir de 96 px
FOLGA_DISCO = 0.04              # spec 5.6: disco Coxia com folga de 4% do diâmetro


def _png(im, caminho):
    im.save(caminho, 'PNG', optimize=True)


def placa(destino):
    w, h = PLACA[0] * ESCALA, PLACA[1] * ESCALA
    y, x = np.mgrid[0:h, 0:w].astype(np.float64)
    # elipse de 110% da largura por 75% da altura, centrada em 12% 0%
    cx, cy = 0.12 * w, 0.0
    rx, ry = 1.10 * w, 0.75 * h
    d = np.sqrt(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2)
    alfa = 0.09 * np.clip(1 - d / 0.62, 0, 1)
    base = np.empty((h, w, 3))
    for i in range(3):
        base[..., i] = SALA[i] * (1 - alfa) + TELA[i] * alfa
    # grão a 6% em modo tela
    g = Image.open(GRAO).convert('L')
    gw, gh = g.size
    lad = np.array(g, dtype=np.float64) / 255.0
    reps = (h // gh + 1, w // gw + 1)
    tile = np.tile(lad, reps)[:h, :w]
    b = base / 255.0
    tela = 1 - (1 - b) * (1 - tile[..., None])
    b = b * 0.94 + tela * 0.06
    im = Image.fromarray(np.clip(np.round(b * 255), 0, 255).astype(np.uint8))
    # logotipo oficial branco
    logo = Image.open(os.path.join(BRAND, 'void-horizontal-branco.png')).convert('RGBA')
    lw = LOGO_LARGURA * ESCALA
    lh = round(logo.size[1] * lw / logo.size[0])
    logo = logo.resize((lw, lh), Image.LANCZOS)
    im = im.convert('RGBA')
    im.alpha_composite(logo, (MARGEM * ESCALA, (h - lh) // 2))
    _png(im.convert('RGB'), os.path.join(destino, 'placa-email-600.png'))


def selo(destino, produto):
    lado = SELO * ESCALA
    s = Image.open(os.path.join(BRAND, 'selo-simples-%s.png' % produto)).convert('RGBA')
    s = s.resize((lado, lado), Image.LANCZOS)
    if produto != 'pro':
        _png(s, os.path.join(destino, 'selo-email-%s.png' % produto))
        return
    # Pro simples: base Nanquim some na Sala (1,18:1); assenta no disco Coxia sem alterar o vetor
    total = round(lado * (1 + 2 * FOLGA_DISCO))
    total += total % 2
    sup = 4  # supersampling para a borda do disco
    disco = Image.new('L', (total * sup, total * sup), 0)
    yy, xx = np.mgrid[0:total * sup, 0:total * sup]
    r = total * sup / 2
    m = ((xx + .5 - r) ** 2 + (yy + .5 - r) ** 2) <= r * r
    disco = Image.fromarray((m * 255).astype(np.uint8)).resize((total, total), Image.LANCZOS)
    tela = Image.new('RGBA', (total, total), COXIA + (0,))
    tela.putalpha(disco)
    off = (total - lado) // 2
    tela.alpha_composite(s, (off, off))
    _png(tela, os.path.join(destino, 'selo-email-pro.png'))


def gerar(destino):
    os.makedirs(destino, exist_ok=True)
    placa(destino)
    for p in ('start', 'master', 'pro'):
        selo(destino, p)
    return sorted(f for f in os.listdir(destino) if f.endswith('.png'))


def _hash(pasta, nomes):
    return {n: hashlib.sha256(open(os.path.join(pasta, n), 'rb').read()).hexdigest() for n in nomes}


if __name__ == '__main__':
    if '--verificar' in sys.argv:
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            ha, hb = _hash(a, gerar(a)), _hash(b, gerar(b))
        ok = ha == hb
        for n in ha:
            print(('igual  ' if ha[n] == hb.get(n) else 'DIFERE ') + n)
        sys.exit(0 if ok else 1)
    nomes = gerar(DESTINO)
    for n in nomes:
        im = Image.open(os.path.join(DESTINO, n))
        print('%-24s %4d x %-4d %6d bytes' % (n, im.size[0], im.size[1], os.path.getsize(os.path.join(DESTINO, n))))
