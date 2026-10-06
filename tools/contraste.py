#!/usr/bin/env python3
"""Contraste WCAG 2 dos tokens do sistema Sala Escura (The VOID).

Origem: contraste_spec.py da especificação (06/10/2026), com a mesma lista de
pares da tabela 3.4. Acrescenta o modo --check, que serve de gate:

  python3 tools/contraste.py            tabelas em Markdown
  python3 tools/contraste.py --json     saída completa em JSON
  python3 tools/contraste.py --check    sai com código 1 se:
      - algum par "livre" ficar abaixo de 4,5:1;
      - algum par "condicionado" ficar abaixo de 3:1;
      - algum HEX daqui divergir do tokens.json do repositório.

Véu: mistura sRGB de Sala (#181818) com a opacidade indicada sobre o pior
pixel, branco puro (#FFFFFF). Para acrescentar um par, edite a lista P, rode
de novo e copie a linha para a tabela 3.4 da especificação.
"""
import json
import os
import sys

T = {
    'nanquim': '#000000', 'sala': '#181818', 'bastidor': '#212121', 'coxia': '#2B2B2B', 'fio': '#363636',
    'chumbo': '#474747', 'penumbra': '#5F5F5C', 'fumaca': '#898989', 'po': '#B4B5B0', 'cal': '#DCDDD8',
    'cinza-100': '#ECEDE7', 'tela': '#F8F9F4', 'branco': '#FFFFFF', 'nevoa': '#C9D0D8', 'ardosia': '#3F4E4F',
    'terracota': '#B25A32', 'terracota-viva': '#C46039', 'terracota-funda': '#8C4529', 'terracota-luz': '#DE8C66',
    'terracota-noite': '#4A2416', 'areia': '#DBC5A3', 'campo-start': '#B5966B', 'caramelo': '#AE8A64',
    'ouro-velho': '#93693B', 'ouro-fundo': '#734120', 'campo-master': '#76432B', 'couro': '#6C4327', 'cafe': '#412919',
    'sucesso': '#9DB79B', 'sucesso-claro': '#3E6A4B', 'atencao-claro': '#7A5418', 'erro': '#EF8A80', 'erro-claro': '#A8322C',
}


def rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hexs(c):
    return '#%02X%02X%02X' % tuple(int(round(v)) for v in c)


def lin(v):
    v /= 255
    return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4


def L(h):
    r, g, b = rgb(h)
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def cr(a, b):
    la, lb = L(a), L(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def mix(top, a, base='#FFFFFF'):
    t = rgb(top)
    b = rgb(base)
    return hexs(tuple(a * t[i] + (1 - a) * b[i] for i in range(3)))


# véus (pior pixel = branco puro)
for _a in (48, 55, 62, 70, 75):
    T['veu-%d' % _a] = mix(T['sala'], _a / 100)

# (texto, fundo, categoria declarada, condição)
P = [
    # liberados para qualquer texto
    ('tela', 'nanquim', 'livre', ''), ('tela', 'sala', 'livre', ''), ('sala', 'tela', 'livre', ''), ('branco', 'sala', 'livre', ''),
    ('cal', 'sala', 'livre', 'corpo longo no escuro'), ('po', 'sala', 'livre', 'apoio, legenda, crédito de prova'),
    ('tela', 'bastidor', 'livre', ''), ('cal', 'bastidor', 'livre', ''), ('po', 'bastidor', 'livre', ''),
    ('tela', 'coxia', 'livre', ''), ('po', 'coxia', 'livre', ''),
    ('nevoa', 'sala', 'livre', 'acento do Pro e informação'), ('areia', 'sala', 'livre', 'destaque Start e institucional'),
    ('areia', 'bastidor', 'livre', ''), ('terracota-luz', 'sala', 'livre', 'destaque Master em texto pequeno'),
    ('terracota-luz', 'bastidor', 'livre', ''), ('fumaca', 'sala', 'livre', 'só 14 px ou mais por escolha'),
    ('sala', 'cinza-100', 'livre', 'zebra do Modo Leitura'), ('ardosia', 'tela', 'livre', 'apoio no Modo Leitura'),
    ('penumbra', 'tela', 'livre', 'legenda no Modo Leitura'), ('terracota-funda', 'tela', 'livre', 'link e filete no claro'),
    ('chumbo', 'tela', 'livre', ''), ('tela', 'campo-master', 'livre', 'texto no Campo Master'),
    ('sala', 'campo-start', 'livre', 'texto no Campo Start'), ('tela', 'cafe', 'livre', ''), ('tela', 'terracota-noite', 'livre', ''),
    ('tela', 'couro', 'livre', ''), ('tela', 'ouro-fundo', 'livre', ''), ('sala', 'areia', 'livre', ''), ('sala', 'nevoa', 'livre', ''),
    ('caramelo', 'sala', 'livre', 'destaque Start sobre Sala'), ('sucesso', 'sala', 'livre', 'com ícone e palavra'), ('erro', 'sala', 'livre', 'com ícone e palavra'),
    ('sucesso-claro', 'tela', 'livre', 'com ícone e palavra'), ('erro-claro', 'tela', 'livre', 'com ícone e palavra'),
    ('atencao-claro', 'tela', 'livre', 'com ícone e palavra'),
    ('tela', 'veu-62', 'livre', 'mínimo sob qualquer texto abaixo de 24 px'), ('tela', 'veu-70', 'livre', 'véu padrão'),
    ('tela', 'veu-75', 'livre', 'caixa de legenda de vídeo'), ('areia', 'veu-75', 'livre', 'palavra de destaque na legenda'),
    # condicionados
    ('tela', 'terracota', 'cond', 'só 19 px em 700 ou 24 px ou mais'), ('terracota', 'tela', 'cond', 'título e numeral, nunca corpo'),
    ('tela', 'ouro-velho', 'cond', 'só 19 px em 700 ou 24 px ou mais'), ('ouro-velho', 'tela', 'cond', 'título ou rótulo em 600+, nunca corpo'),
    ('terracota', 'sala', 'cond', 'só título de 24 px ou mais, numeral e grafismo'), ('terracota-viva', 'sala', 'cond', 'só texto grande e ícone'),
    ('ouro-velho', 'sala', 'cond', 'só grafismo e texto de 24 px ou mais'),
    ('tela', 'veu-48', 'cond', 'só título de 24 px ou mais sobre foto já escura'), ('tela', 'veu-55', 'cond', 'só título de 24 px ou mais'),
    ('areia', 'veu-70', 'cond', 'só palavra de destaque em título de 24 px ou mais'),
    # proibidos como texto
    ('fumaca', 'tela', 'proib', 'só linha e divisória no claro'), ('caramelo', 'tela', 'proib', 'só campo'),
    ('tela', 'campo-start', 'proib', 'no Campo Start o texto é Sala'), ('penumbra', 'sala', 'proib', 'decoração'),
    ('ardosia', 'sala', 'proib', 'só campo e miolo do selo'), ('chumbo', 'sala', 'proib', 'só fio decorativo'),
    ('fio', 'sala', 'proib', 'só linha'), ('nanquim', 'sala', 'proib', 'base do selo Pro some na Sala: selo simples Pro exige disco Coxia'),
    ('coxia', 'sala', 'proib', 'disco de assentamento: só superfície'), ('tela', 'veu-48', 'proib-pequeno', 'texto abaixo de 24 px'),
]

def faixa(r):
    return 'AAA' if r >= 7 else ('AA' if r >= 4.5 else ('AA grande' if r >= 3 else 'reprova'))


def calcular():
    rows = []
    for t, f, cat, cond in P:
        r = cr(T[t], T[f])
        rows.append(dict(texto=t, hex_texto=T[t], fundo=f, hex_fundo=T[f], razao=round(r, 2),
                         nivel=faixa(r), categoria=cat, condicao=cond))
    erros = [x for x in rows if (x['categoria'] == 'livre' and x['razao'] < 4.5)
             or (x['categoria'] == 'cond' and x['razao'] < 3)]
    return rows, erros


def tokens_do_repositorio():
    """Lê tokens.json (raiz do repositório) e devolve {nome: HEX} das cores sólidas."""
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho = os.path.join(raiz, 'tokens.json')
    if not os.path.exists(caminho):
        return None
    dados = json.load(open(caminho, encoding='utf-8'))
    saida = {}

    def andar(o, nome=None):
        if isinstance(o, dict):
            if '$value' in o:
                v = o['$value']
                if o.get('$type') == 'color' and isinstance(v, str) and v.startswith('#'):
                    saida[nome] = v.upper()
                return
            for k, v in o.items():
                andar(v, k)
    andar(dados)
    return saida


def divergencias_de_tokens():
    repo = tokens_do_repositorio()
    if repo is None:
        return ['tokens.json não encontrado na raiz do repositório']
    erros = []
    for nome, hexa in T.items():
        if nome.startswith('veu-'):
            continue
        if nome not in repo:
            erros.append('%s ausente no tokens.json' % nome)
        elif repo[nome] != hexa.upper():
            erros.append('%s: script %s, tokens.json %s' % (nome, hexa, repo[nome]))
    return erros


def main():
    rows, erros = calcular()
    if '--json' in sys.argv:
        print(json.dumps(dict(tokens=T, pares=rows, erros=erros), ensure_ascii=False, indent=1))
        return 0
    if '--check' in sys.argv:
        div = divergencias_de_tokens()
        livres = sum(1 for r in rows if r['categoria'] == 'livre')
        cond = sum(1 for r in rows if r['categoria'] == 'cond')
        for x in erros:
            minimo = '4,5' if x['categoria'] == 'livre' else '3'
            print('FALHA par %s sobre %s: %s (mínimo %s)' % (x['texto'], x['fundo'],
                                                           str(x['razao']).replace('.', ','), minimo))
        for d in div:
            print('FALHA token: %s' % d)
        if erros or div:
            return 1
        print('OK: %d pares livres com 4,5:1 ou mais, %d condicionados com 3:1 ou mais; '
              '%d HEX iguais ao tokens.json.' % (livres, cond, len([k for k in T if not k.startswith('veu-')])))
        return 0
    nome = {'livre': 'Liberados para qualquer texto (4,5:1 ou mais)',
            'cond': 'Liberados com condição (abaixo de 4,5:1, ou no limite e restritos por decisão de marca)',
            'proib': 'Proibidos como texto'}
    for cat in ('livre', 'cond', 'proib'):
        print('\n**%s**\n' % nome[cat])
        print('| Texto | Fundo | Razão | Nível | Uso |')
        print('|---|---|---|---|---|')
        for x in sorted([r for r in rows if r['categoria'].startswith(cat)], key=lambda r: -r['razao']):
            print('| %s `%s` | %s `%s` | %s | %s | %s |' % (x['texto'], x['hex_texto'], x['fundo'], x['hex_fundo'],
                                                         str(x['razao']).replace('.', ','), x['nivel'], x['condicao']))
    print('\nVéus calculados sobre #FFFFFF:', ', '.join('%s=%s' % (k, v) for k, v in T.items() if k.startswith('veu')))
    print('Erros de categoria:', erros if erros else 'nenhum')
    return 0


if __name__ == '__main__':
    sys.exit(main())
