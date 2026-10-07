# Tipografia

As três vozes, o link do Google Fonts, os oito registros do Archivo, a regra de largura responsiva, as escalas (documento, peça de 1080 e vídeo), as oito regras da voz em off e as regras gerais de texto. Manual: seções 17 a 20.

Parte da skill [`branding-the-void`](../SKILL.md). Os valores batem com [`tokens.json`](../tokens.json) (conferido por `tools/conferir_skill.py`).

## Tipografia (TRAVADA)

**Três vozes:**

| Voz | Família | Papel |
|---|---|---|
| **Letreiro** (voz ativa) | **Archivo** variável, `wght` 100 a 900, `wdth` 62 a 125, só romano | Títulos em caixa alta, botões, créditos, números, rótulos, legenda de vídeo, texto curto dentro da arte |
| **Voz em off** (voz sensível) | **Alga Italic** onde houver licença; substituta livre **Newsreader Italic 300, `opsz` 72** | A palavra que sente; nomes de rito em destaque; marca d'água do nome do produto |
| **Texto** (leitura longa) | **Nunito Sans** 400 e 600 (padrão provisório [P 1]) | Corpo de LP, artigo, e-mail, membros, PDF |

**O link exato (único, igual em todo material):**

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Newsreader:ital,opsz,wght@1,6..72,300&family=Nunito+Sans:wght@400;600&display=swap" rel="stylesheet">
```

```css
--font-letreiro: "Archivo", "Arial Narrow", Arial, sans-serif;
--font-off: "Alga", "Newsreader", Georgia, serif;      /* Alga só onde a licença estiver instalada */
--font-texto: "Nunito Sans", Arial, sans-serif;
```

- **Alga é paga.** Nunca entra no repositório, no autocontido, no Canva nem em pasta de cliente (o `.gitignore` bloqueia). **Até [P 3], todo material público sai em Newsreader Italic 300.**
- **Site publicado:** servir `woff2` localmente com subconjunto latino e `font-display: swap`; pré-carregar só o Archivo. O `autocontido.py` já embute os `woff2` livres de `assets/fontes/google/`.
- **Corpo [P 1]:** Nunito Sans, irmã da Nunito pedida no Brand DNA; alternativa registrada, Archivo 400 largura 100, 18 px, entrelinha 1,7. As duas cabem na mesma escala.

### Os oito registros do Archivo

Nenhuma peça usa mais de dois registros de largura além do texto.

| Registro | `wght` | `wdth` | Caixa | Entreletra | Entrelinha | Uso |
|---|---|---|---|---|---|---|
| **Título de Filme** (`.titulo-filme`) | 800 | 112 | alta | -0,02em | 0,92 | Hero, capa, cartela, gancho |
| **Título de Seção** (`.titulo-secao`) | 700 | 100 | alta | -0,012em | 0,98 | Seção de LP, cartão de carrossel |
| **Fala** (`.fala`) | 600 | 100 | mista | -0,005em | 1,15 | Subtítulo, pergunta de FAQ, H1 e H2 de artigo, legenda de vídeo |
| **Crédito** (`.credito`) | 500 | 125 | alta | +0,18em | 1,2 | Rodapé-assinatura, sobretítulo, Ficha Técnica, rótulos, Marcadores |
| **Estreito** | 800 | 68 | alta | 0 | 0,9 | Palavra vertical ("MASTER" de pé, slide 36), título que não cabe em 320 px |
| **Numeral de Prova** (`.numeral-prova`) | 700 | 75 | n/a | -0,01em | 0,9 | Número de prova; `font-variant-numeric: lining-nums tabular-nums` |
| **Numeral de Data** | 300 | 125 | n/a | 0 | 1 | Data e horário de turma, minutagem; **nunca prova** |
| **Botão** (`.botao`) | 700 | 106 | alta | +0,06em | 1 | Todo CTA |

O "THE", o "TATTOO" e os descritores do logotipo são Archivo 400 largura 100; o VOID é letreiro ajustado à mão. **Nenhum título digitado imita o VOID**: o Título de Filme é mais largo e mais pesado de propósito.

### Regra de largura responsiva (antes de reduzir, estreite)

Se o Título de Filme passar de 3 linhas **em qualquer largura**, ou, no celular, empurrar o botão para fora da primeira dobra:

1. `wdth` 112 para **100**; ainda passa, **92**; ainda passa, **85**.
2. Só então reduza o tamanho, até o piso de 34 px.
3. Abaixo de `wdth` 85 ou do piso, **reescreva o título** (L6).

No computador o `data-largura` não age (está só no `@media` do celular): estreite com `style="font-variation-settings:'wdth' 100"` no próprio título e, se ainda passar de 3 linhas, reescreva.

```css
.titulo-filme{font:800 clamp(40px,7vw,96px)/.92 var(--font-letreiro);font-variation-settings:"wdth" 112;text-transform:uppercase;letter-spacing:-.02em;text-wrap:balance}
@media (max-width:430px){.titulo-filme{font-variation-settings:"wdth" 100}.titulo-filme[data-largura="92"]{font-variation-settings:"wdth" 92}.titulo-filme[data-largura="85"]{font-variation-settings:"wdth" 85}}
```

### Escalas

**Documento e site** (px, computador / celular): Título de Filme 96 / 48 (o `clamp` do `tokens.css` dá 40 no celular; suba para 48 só se couber em 3 linhas; piso 34) · Título de Seção 56 / 34 · Subtítulo 32 / 24 (Fala) · Intertítulo 22 / 20 (Fala) · Voz em off isolada 44 / 30 · Chamada 22 / 19 (Nunito Sans, entrelinha 1,5) · **Corpo 18 / 17** (Nunito Sans 400, entrelinha 1,65, 60 a 72 caracteres, coluna de 680 px) · Apoio 15 / 15 (entrelinha 1,5) · Legenda e Crédito de Prova 13 / 13 (piso de leitura) · Crédito em caixa alta 12 / 12 (contraste 7:1 ou mais: Tela, Cal, Pó ou Areia) · Numeral de Prova 80 / 56 · Botão 16 / 17, altura 56 (computador) e 52 (celular), largura total no celular.

**Peça de 1080 px** (feed 1080 por 1350, story 1080 por 1920, quadrado 1080 por 1080; `--u: calc(100cqw / 1080)`): Título de Filme 96 a 140 u, padrão 120, até 3 linhas e 6 palavras; **nenhuma palavra passa de 936 u** (largura útil): palavra de 11 letras ou mais começa em 100 u e `wdth` 100, de 14 ou mais em `wdth` 92; se passar, `wdth` 100, 92, 85, depois reduza até 96 u e, por fim, reescreva · voz em off no título 1,2 vez o Archivo, uma linha · subtítulo e citação 48 a 56 u (Fala) · texto curto 34 a 38 u em Archivo 400 largura 100 (Nunito Sans não entra na peça) · botão desenhado 30 u · Crédito, rodapé-assinatura e Crédito de Prova **26 u, piso absoluto** · Numeral de Prova 160 a 220 u · margens 72 u; story e Reels com conteúdo entre y = 270 e y = 1500 e 120 u livres à direita nos Reels.

**Vídeo** (vertical 1080 por 1920 / horizontal 1920 por 1080): gancho dos 2 s iniciais em Título de Filme 96 a 120 / 110 a 150, até 6 palavras · cartela 96 a 120 + voz em off 120 a 150 / 110 a 150 + 130 a 170 · legenda queimada em Archivo 600 largura 100, 60 a 68 px e 22 a 28 caracteres por linha / 46 a 54 px e 32 a 42 caracteres, 2 linhas, caixa mista, piso 60 px no vertical · lower third com nome em Archivo 600 largura 112, 40 px, caixa alta, +0,08em, e função na voz em off 34 px (a única linha em itálico do quadro) · Crédito no fecho 28 px.

### As oito regras da voz em off

1. **Uma linha por bloco** (bloco é título com subtítulo, uma tela de story ou um cartão de carrossel). No máximo duas palavras soltas na mesma linha, como "É SOBRE *continuar,* MESMO SEM *certeza*" (slide 24).
2. Só a palavra que sente; até 7 palavras.
3. Tamanho 1,2 vez o Archivo da mesma linha; entreletra 0; entrelinha 1.
4. **Caixa:** minúscula com inicial maiúscula quando abre frase. Exceções nomeadas em caixa alta: os rótulos START, MASTER e PRO dentro do Mapa da Trilha e a marca d'água do nome do produto no Campo de Produto.
5. Cor: a do título, ou o destaque do produto. Nunca terracota pura abaixo de 24 px.
6. Piso: 20 px em tela, 56 u na peça, 64 px no vídeo (o traço 300 some abaixo disso).
7. **Nunca em:** botão, número, preço, data, instrução, legenda funcional, texto legal, formulário, tabela, nome de pessoa.
8. Canva e Slides: Newsreader Italic Light. E-mail: cai para Georgia itálico, **nunca vira imagem**. Nenhuma outra serifada entra (Playfair e similares saem).

### Regras gerais de texto

Caixa alta só em título, botão, crédito e rótulo; nunca corpo, condição de oferta ou aviso legal. Itálico só na voz em off. Sublinhado só em link no Modo Leitura (1 px, afastado 3 px). Sem contorno de texto (exceção: Palavra de Produto vazada do Pro), sem sombra de texto (exceção: legenda de vídeo sobre fundo já escuro, `0 2px 8px rgb(0 0 0 / .6)`), sem degradê em texto, sem escala horizontal (largura só pelo eixo `wdth`). Números: `R$ 0.000,00` · `[N]x` · `[N] aulas` · `18h30` · `06/10/2026` · `out/2026` (preço e carga reais só do checkout [P 15]). Hifenização só em corpo de coluna estreita (`hyphens:auto`). **Zero travessão** em qualquer texto, inclusive legenda, assunto de e-mail, texto alternativo, `title` e comentário visível.
