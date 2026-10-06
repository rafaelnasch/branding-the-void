#!/usr/bin/env python3
"""Gera as texturas do sistema Sala Escura (spec 6.1 e 6.2).

Saídas em assets/textura/:
  grao-240.webp         ladrilho de grão para campo escuro (mix-blend-mode: screen, 6%)
  grao-240-claro.webp   ladrilho de grão para o Modo Leitura (mix-blend-mode: multiply, 4%)
  esfera-3000.png       Esfera do Vazio, tinta Nanquim sobre fundo transparente (impressão e vídeo)
  esfera-1080.webp      a mesma Esfera desenhada em 1080 px (web e redes)

Tudo é determinístico: semente fixa, nenhuma data e nenhum metadado variável.
Duas execuções produzem arquivos idênticos byte a byte (confira com --verificar).

Uso:
  python3 tools/gerar_texturas.py              gera os quatro arquivos
  python3 tools/gerar_texturas.py --verificar  gera duas vezes em pasta temporária e compara os hashes
Precisa de numpy e Pillow (com suporte a WebP).
"""
import hashlib
import io
import os
import sys
import tempfile

import numpy as np
from PIL import Image, ImageFilter

SEMENTE = 20261006
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, 'assets', 'textura')
LIMITE_LADRILHO = 25 * 1024  # critério de aceite: até 25 KB


# ---------------------------------------------------------------- grão

def _ruido_ciclico(lado, rng, sigma):
    """Ruído gaussiano desfocado por convolução circular (FFT): as bordas se
    encontram sem emenda porque o desfoque dá a volta no ladrilho."""
    branco = rng.standard_normal((lado, lado))
    f = np.fft.fftfreq(lado)
    fx, fy = np.meshgrid(f, f)
    nucleo = np.exp(-2 * (np.pi ** 2) * (sigma ** 2) * (fx ** 2 + fy ** 2))
    suave = np.real(np.fft.ifft2(np.fft.fft2(branco) * nucleo))
    # mistura um pouco do ruído de pixel isolado para o grão não ficar borrado
    campo = 0.75 * suave / suave.std() + 0.25 * branco / branco.std()
    return campo / campo.std()


def _ladrilho(claro, rng):
    n = _ruido_ciclico(240, rng, sigma=0.65)
    if claro:
        # Modo Leitura: quase branco com pontos escuros (multiply só escurece)
        v = 0.80 - 0.19 * n
    else:
        # Campo escuro: quase preto com pontos claros (screen só clareia).
        # Média baixa para a Sala continuar perto de #181818 sob o grão.
        v = 0.20 + 0.19 * n
    v = np.clip(v, 0, 1)
    return Image.fromarray((v * 255 + 0.5).astype(np.uint8))


def _webp_ate(img, limite, qualidades=(86, 82, 78, 74, 70, 66, 62, 58)):
    """Maior qualidade WebP que cabe no limite (busca determinística)."""
    for q in qualidades:
        buf = io.BytesIO()
        img.save(buf, 'WEBP', quality=q, method=6)
        if buf.tell() <= limite:
            return buf.getvalue(), q
    raise SystemExit('ladrilho não coube em %d bytes' % limite)


# ---------------------------------------------------------------- esfera

def _campo_suave(lado, rng, grade):
    """Ruído de baixa frequência (grade x grade valores ampliados em bicúbico)."""
    base = rng.random((grade, grade)).astype(np.float32)
    img = Image.fromarray(base).resize((lado, lado), Image.BICUBIC)
    a = np.asarray(img, dtype=np.float32)
    return (a - a.mean()) / (a.std() + 1e-9)


def _camada(lado, rng, passo):
    """Ruído uniforme em blocos de `passo` px: vira gotas de tinta maiores."""
    m = int(np.ceil(lado / passo))
    base = rng.random((m, m)).astype(np.float32)
    return np.kron(base, np.ones((passo, passo), dtype=np.float32))[:lado, :lado]


def esfera(lado, rng):
    """Esfera do Vazio: núcleo sólido, borda de aerógrafo granulada e difusa.
    Referência visual: slides 16 e 48 da apresentação de rebranding."""
    escala = lado / 3000.0
    y, x = np.mgrid[0:lado, 0:lado].astype(np.float32)
    c = (lado - 1) / 2.0
    dx, dy = x - c, y - c
    r = np.sqrt(dx * dx + dy * dy) / (lado / 2.0)  # 0 no centro, 1 na borda do quadro

    # contorno quase circular: o raio respira menos de 1%, como num jato firme
    r = r * (1 + 0.006 * _campo_suave(lado, rng, 7) + 0.004 * _campo_suave(lado, rng, 29))

    # densidade de tinta: cheia até o miolo (0,49), metade em cerca de 0,62, cauda longa
    # de pontos soltos até cerca de 0,95 do raio do quadro (perfil do slide 16)
    nucleo, largura = 0.49, 0.17
    x = np.maximum(r - nucleo, 0) / largura
    densidade = np.exp(-(x ** 1.45))
    # a névoa morre antes da borda do arquivo: nenhum ponto toca o quadro,
    # então a Esfera pode ser posta em qualquer fundo sem aparecer recorte
    janela = np.clip((0.97 - r) / 0.12, 0, 1)
    densidade = densidade * janela * janela * (3 - 2 * janela)

    # gotas de vários tamanhos: pó fino, gota média e alguns respingos
    p1 = 1
    p2 = max(1, int(round(2 * escala)))
    p3 = max(1, int(round(3 * escala)))
    mistura = (0.70 * _camada(lado, rng, p1) + 0.20 * _camada(lado, rng, p2)
               + 0.10 * _camada(lado, rng, p3))
    # converte a mistura em distribuição uniforme (posição no ranking), para
    # que a cobertura de tinta seja exatamente a densidade pedida
    ordem = np.argsort(mistura, axis=None, kind='stable')
    uniforme = np.empty(lado * lado, dtype=np.float32)
    uniforme[ordem] = (np.arange(lado * lado, dtype=np.float32) + 0.5) / (lado * lado)
    uniforme = uniforme.reshape(lado, lado)

    pontos = (uniforme < densidade).astype(np.float32)
    # um terço de tom contínuo (a névoa do aerógrafo), o resto em ponto (o grão)
    continuo = densidade ** 1.25
    tinta = 0.3 * continuo + 0.7 * pontos
    alfa = Image.fromarray((np.clip(tinta, 0, 1) * 255 + 0.5).astype(np.uint8))
    alfa = alfa.filter(ImageFilter.GaussianBlur(0.5))
    preto = Image.new('L', (lado, lado), 0)
    return Image.merge('RGBA', (preto, preto, preto, alfa))


# ---------------------------------------------------------------- saída

def gerar(destino):
    os.makedirs(destino, exist_ok=True)
    rng = np.random.default_rng(SEMENTE)
    rel = {}

    escuro, q1 = _webp_ate(_ladrilho(False, rng), LIMITE_LADRILHO)
    claro, q2 = _webp_ate(_ladrilho(True, rng), LIMITE_LADRILHO)
    with open(os.path.join(destino, 'grao-240.webp'), 'wb') as f:
        f.write(escuro)
    with open(os.path.join(destino, 'grao-240-claro.webp'), 'wb') as f:
        f.write(claro)
    rel['grao-240.webp'] = 'qualidade %d' % q1
    rel['grao-240-claro.webp'] = 'qualidade %d' % q2

    rng_e = np.random.default_rng(SEMENTE + 1)
    grande = esfera(3000, rng_e)
    grande.save(os.path.join(destino, 'esfera-3000.png'), 'PNG', optimize=True)
    rng_w = np.random.default_rng(SEMENTE + 2)
    web = esfera(1080, rng_w)
    web.save(os.path.join(destino, 'esfera-1080.webp'), 'WEBP', quality=88, alpha_quality=100, method=6)
    rel['esfera-3000.png'] = 'PNG RGBA'
    rel['esfera-1080.webp'] = 'WebP RGBA'
    return rel


def hashes(pasta):
    out = {}
    for nome in sorted(os.listdir(pasta)):
        caminho = os.path.join(pasta, nome)
        out[nome] = (hashlib.sha256(open(caminho, 'rb').read()).hexdigest(), os.path.getsize(caminho))
    return out


def main():
    if '--verificar' in sys.argv:
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            gerar(a)
            gerar(b)
            ha, hb = hashes(a), hashes(b)
        falhou = False
        for nome in ha:
            igual = ha[nome][0] == hb[nome][0]
            print('%-22s %9d bytes  %s  %s' % (nome, ha[nome][1], ha[nome][0][:16], 'igual' if igual else 'DIFERENTE'))
            falhou |= not igual
            if nome.startswith('grao') and ha[nome][1] > LIMITE_LADRILHO:
                print('  FALHA: ladrilho acima de 25 KB')
                falhou = True
        return 1 if falhou else 0
    rel = gerar(DESTINO)
    for nome, info in sorted(rel.items()):
        caminho = os.path.join(DESTINO, nome)
        print('%-22s %9d bytes  %s' % (nome, os.path.getsize(caminho), info))
    return 0


if __name__ == '__main__':
    sys.exit(main())
