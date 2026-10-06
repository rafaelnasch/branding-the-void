#!/usr/bin/env python3
"""Gera as LUTs de fotografia e vídeo do sistema Sala Escura (spec 8.3).

Saídas em assets/foto/ (formato .cube, 33 pontos por eixo, 35.937 linhas de dados):
  void-ritual.cube           P&B padrão
  void-vazio.cube            P&B dramático (capa e topo de funil)
  void-terra.cube            cor natural aquecida e dessaturada (depoimento e comunidade)
  void-duotom-start.cube     Café #412919 para Areia #DBC5A3
  void-duotom-master.cube    #21130C para Terracota Viva #C46039
  void-duotom-pro.cube       Sala #181818 para Névoa #C9D0D8

Números da especificação 8.3:
  Entrada Rec.709 com gama 2,4. O grão nunca vai dentro da LUT.
  Matriz P&B Ritual: luminância = 0,36 R + 0,50 G + 0,14 B (também usada no Vazio).
  Curva Ritual: 0,00>0,03 · 0,15>0,10 · 0,50>0,50 · 0,80>0,85 · 1,00>0,96.
  Curva Vazio:  0>0 · 0,235>0,137 · 0,50>0,47 · 1,00>0,98.
  Terra: saturação -20%; sombras +0,012 R e -0,010 B; altas luzes +0,008 R, +0,004 G e -0,012 B.
  Duotons: luminância 0 para a sombra e 1 para a alta luz do produto, interpolação linear em RGB linear.

Uso:
  python3 tools/gerar_luts.py             gera as seis LUTs
  python3 tools/gerar_luts.py --testar    gera e confere cabeçalho, linhas e extremos
"""
import os
import sys

import numpy as np

N = 33
GAMA = 2.4
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, 'assets', 'foto')

PESOS_RITUAL = np.array([0.36, 0.50, 0.14])
PESOS_709 = np.array([0.2126, 0.7152, 0.0722])

CURVA_RITUAL = [(0.00, 0.03), (0.15, 0.10), (0.50, 0.50), (0.80, 0.85), (1.00, 0.96)]
CURVA_VAZIO = [(0.00, 0.00), (0.235, 0.137), (0.50, 0.47), (1.00, 0.98)]

DUOTONS = {
    'start': ('#412919', '#DBC5A3'),
    'master': ('#21130C', '#C46039'),
    'pro': ('#181818', '#C9D0D8'),
}


def hex01(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)])


def decodificar(v):
    """Valor codificado (gama 2,4) para luz linear."""
    return np.power(np.clip(v, 0, 1), GAMA)


def codificar(v):
    """Luz linear para valor codificado (gama 2,4)."""
    return np.power(np.clip(v, 0, 1), 1.0 / GAMA)


def curva_monotona(pontos):
    """Interpolação cúbica monótona (Fritsch e Carlson): passa exatamente pelos
    pontos da especificação e nunca cria ondulação que inverta tons."""
    x = np.array([p[0] for p in pontos], dtype=float)
    y = np.array([p[1] for p in pontos], dtype=float)
    h = np.diff(x)
    d = np.diff(y) / h
    m = np.zeros_like(x)
    m[0], m[-1] = d[0], d[-1]
    for k in range(1, len(x) - 1):
        if d[k - 1] * d[k] <= 0:
            m[k] = 0.0
        else:
            w1 = 2 * h[k] + h[k - 1]
            w2 = h[k] + 2 * h[k - 1]
            m[k] = (w1 + w2) / (w1 / d[k - 1] + w2 / d[k])

    def f(v):
        v = np.clip(v, x[0], x[-1])
        k = np.clip(np.searchsorted(x, v, side='right') - 1, 0, len(x) - 2)
        t = (v - x[k]) / h[k]
        t2, t3 = t * t, t * t * t
        return ((2 * t3 - 3 * t2 + 1) * y[k] + (t3 - 2 * t2 + t) * h[k] * m[k]
                + (-2 * t3 + 3 * t2) * y[k + 1] + (t3 - t2) * h[k] * m[k + 1])
    return f


def ponderar(rgb, pesos):
    """Soma ponderada dos canais (evita o produto matricial, que emite avisos
    falsos no numpy do macOS)."""
    return rgb[:, 0] * pesos[0] + rgb[:, 1] * pesos[1] + rgb[:, 2] * pesos[2]


def grade():
    """Pontos da grade na ordem do .cube: vermelho varia mais rápido."""
    a = np.linspace(0, 1, N)
    b, g, r = np.meshgrid(a, a, a, indexing='ij')
    return np.stack([r.ravel(), g.ravel(), b.ravel()], axis=1)


def pb(rgb, pontos):
    lum = ponderar(rgb, PESOS_RITUAL)
    s = curva_monotona(pontos)(lum)
    return np.repeat(s[:, None], 3, axis=1)


def terra(rgb):
    luma = ponderar(rgb, PESOS_709)[:, None]
    out = luma + (rgb - luma) * 0.80                      # saturação -20%
    lum = np.clip(luma[:, 0], 0, 1)
    sombra = ((1 - lum) ** 2)[:, None]                    # peso 1 no preto, 0 no branco
    luz = (lum ** 2)[:, None]                             # peso 0 no preto, 1 no branco
    out = out + sombra * np.array([0.012, 0.0, -0.010]) + luz * np.array([0.008, 0.004, -0.012])
    return np.clip(out, 0, 1)


def duotom(rgb, sombra_hex, luz_hex):
    # luminância linear (Rec.709) de 0 a 1 é o peso da mistura em luz linear:
    # o preto da foto fica na sombra do produto e o cinza médio fica no meio
    # perceptivo, sem clarear as sombras
    t = ponderar(decodificar(rgb), PESOS_709)[:, None]
    a = decodificar(hex01(sombra_hex))
    b = decodificar(hex01(luz_hex))
    return codificar(a + (b - a) * t)                      # mistura em RGB linear


def escrever(nome, titulo, dados):
    caminho = os.path.join(DESTINO, nome)
    with open(caminho, 'w', encoding='ascii', newline='\n') as f:
        f.write('# The VOID Tattoo Academy, sistema Sala Escura\n')
        f.write('# Entrada Rec.709 gama 2.4. Grao nao incluido: aplicar depois.\n')
        f.write('TITLE "%s"\n' % titulo)
        f.write('LUT_3D_SIZE %d\n' % N)
        f.write('DOMAIN_MIN 0.0 0.0 0.0\n')
        f.write('DOMAIN_MAX 1.0 1.0 1.0\n')
        for r, g, b in np.clip(dados, 0, 1):
            f.write('%.6f %.6f %.6f\n' % (r, g, b))
    return caminho


def gerar():
    os.makedirs(DESTINO, exist_ok=True)
    rgb = grade()
    feitos = [
        escrever('void-ritual.cube', 'VOID Ritual', pb(rgb, CURVA_RITUAL)),
        escrever('void-vazio.cube', 'VOID Vazio', pb(rgb, CURVA_VAZIO)),
        escrever('void-terra.cube', 'VOID Terra', terra(rgb)),
    ]
    for produto, (s, l) in DUOTONS.items():
        feitos.append(escrever('void-duotom-%s.cube' % produto, 'VOID Duotom %s' % produto.capitalize(),
                               duotom(rgb, s, l)))
    return feitos


# ---------------------------------------------------------------- testes

def ler_cube(caminho):
    linhas = open(caminho, encoding='ascii').read().splitlines()
    tamanho = None
    dados = []
    for ln in linhas:
        if ln.startswith('LUT_3D_SIZE'):
            tamanho = int(ln.split()[1])
        elif ln and (ln[0].isdigit() or ln[0] == '-'):
            dados.append([float(v) for v in ln.split()])
    return tamanho, np.array(dados)


def no_cubo(dados, r, g, b):
    """Valor da LUT num canto da grade (índices 0 ou N-1)."""
    return dados[r + g * N + b * N * N]


def testar(arquivos):
    erros = []
    tol = 1 / 255.0
    esperado = {
        'void-ritual.cube': ([0.03] * 3, [0.96] * 3),
        'void-vazio.cube': ([0.00] * 3, [0.98] * 3),
        'void-terra.cube': ([0.012, 0.0, 0.0], [1.0, 1.0, 0.988]),
    }
    for produto, (s, l) in DUOTONS.items():
        esperado['void-duotom-%s.cube' % produto] = (list(hex01(s)), list(hex01(l)))
    for caminho in arquivos:
        nome = os.path.basename(caminho)
        tamanho, dados = ler_cube(caminho)
        ok_tam = tamanho == N
        ok_lin = len(dados) == N ** 3
        preto = no_cubo(dados, 0, 0, 0)
        branco = no_cubo(dados, N - 1, N - 1, N - 1)
        ep, eb = esperado[nome]
        ok_p = np.all(np.abs(preto - ep) <= tol)
        ok_b = np.all(np.abs(branco - eb) <= tol)
        print('%-26s tamanho %s · %d linhas de dados · preto %s · branco %s  %s' % (
            nome, tamanho, len(dados), ' '.join('%.4f' % v for v in preto),
            ' '.join('%.4f' % v for v in branco), 'ok' if (ok_tam and ok_lin and ok_p and ok_b) else 'FALHA'))
        if not (ok_tam and ok_lin and ok_p and ok_b):
            erros.append(nome)
        # monotonia da curva P&B no eixo cinza
        if nome in ('void-ritual.cube', 'void-vazio.cube'):
            cinza = np.array([no_cubo(dados, i, i, i)[0] for i in range(N)])
            if np.any(np.diff(cinza) < -1e-9):
                erros.append(nome + ' (curva não monótona)')
    # pontos intermediários da curva Ritual (0,50 > 0,50) pela função, sem a grade
    f = curva_monotona(CURVA_RITUAL)
    for x, y in CURVA_RITUAL:
        if abs(float(f(np.array([x]))[0]) - y) > 1e-9:
            erros.append('curva Ritual não passa em %.2f' % x)
    return erros


def main():
    feitos = gerar()
    if '--testar' in sys.argv:
        erros = testar(feitos)
        print('Erros:', ', '.join(erros) if erros else 'nenhum')
        return 1 if erros else 0
    for c in feitos:
        print(os.path.relpath(c, RAIZ))
    return 0


if __name__ == '__main__':
    sys.exit(main())
