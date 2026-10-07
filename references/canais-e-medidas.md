# Medidas, utilitários e motores

Medidas de cada peça e plataforma, utilitários do `tokens.css` e a interface dos motores `vforms.js` e `vviz.js`. Manual: seções 34 a 36.

Parte da skill [`branding-the-void`](../SKILL.md). Os valores batem com [`tokens.json`](../tokens.json) (conferido por `tools/conferir_skill.py`).

## Medidas de cada peça e plataforma

As medidas de plataforma mudam: confira na véspera de cada campanha. As de marca (grade, piso, margens) não mudam.

| Peça | Produção | Áreas seguras e regra | Arquivo |
|---|---|---|---|
| Feed e carrossel | 1080 por 1350 (4:5) | Margem 72 u; miolo 3:4 protegido; título, rosto e CTA longe dos 10% de cima e de baixo | `kit-social.html` |
| Story, Reels, capa de Reels | 1080 por 1920 | Conteúdo entre y = 270 e y = 1500; 120 u livres à direita nos Reels; título da capa no miolo 3:4 | `kit-social.html` |
| TikTok | 1080 por 1920 | Livres cerca de 150 px em cima, 450 embaixo, 140 à direita | `kit-social.html` |
| Capas de destaque | 1080 por 1920 | Símbolo do selo em linha ou Esfera sobre Sala; START, MASTER, PRO, AULA, TALKS, VOIDERS, LOCAL | manual 35.1 (ainda sem modelo no kit nem arquivo pronto) |
| Peça 16:9, VSL, YouTube longo | 1920 por 1080, 24 quadros no vídeo | 120 px laterais, 96 px vertical; legenda 46 a 54 px, base a 110 px | `kit-social.html`, `vsl-kit.html` |
| Thumbnail e capa de VSL | 1280 por 720 (também 1080 por 1920 e 1080 por 1350) | Canto inferior direito livre; sem valor em reais | `vsl-kit.html` |
| LinkedIn | 1080 por 1350 (o 1200 por 627 ainda não tem modelo) | Carrossel em PDF: o kit exporta um cartão por vez em PNG; junte os PNG em ordem num PDF | `kit-social.html` (4:5) |
| Cartões de Conversa | 1080 por 1350 | Até 5 palavras de título, 4 linhas de dado em 40 u | `comunicacao-m1-m8.html` |
| Prévia de link | 1200 por 630 | Sala, título da página, selo ou logotipo | `assets/brand/social/`, `assets/seo/og-artigo.html` |
| Avatar e favicon | 1080; 16 a 512 e SVG | O do VOID em Tela sobre Sala [P 12] | `assets/brand/social/`, `favicon/` |
| E-mail | 600 px | Cabeçalho até 64 px; logotipo branco 2x com 200 px | `email-template.html` |
| Landing page | 320 a 1440 px | Dobra do celular em 640 px; margem 16 px | `lp-template.html` |
| Deck | 1440 por 900 | 12 colunas, margem 96 px | `deck-template.html` |
| Certificado e PDF | A4 | Modo Leitura; Ficha Técnica no topo | `membros-ui.html`, `exportar_pdf.py` |
| Impresso | mm | Mínimos da seção A marca | `assets/brand/png/alta/` |

PNG exportado pelo kit social: `thevoid_<rN-modelo>_<produto>_<LxA>_<aaaa-mm-dd>.png`.

## Componentes canônicos por canal

Os nomes são a interface do sistema: **nunca renomeie**. Cada canal tem um arquivo modelo que já cumpre as leis; parta dele.

### Utilitários do `tokens.css`

`.titulo-filme` (com `data-largura="92"` ou `"85"`) · `.titulo-secao` · `.fala` · `.credito` · `.numeral-prova` · `.off` (voz em off) · `.botao` (Letreiro Aceso) · `.grao` · `.janela-luz` · `.veu-esquerda` · `.veu-base` · `.campo-produto` · `.fio-produto` · `.modo-leitura` · `[data-estacao]`. Variáveis: cores, `--font-*`, `--e-1` a `--e-11`, `--t-*`, `--estacao-*`.

### Motores

| Motor | Chamada | O que guarda |
|---|---|---|
| `vforms.js` | `data-vforms`, `VForms.render`, `VForms.svg`, `VForms.montar(raiz)`, `VForms.redesenhar()` | `grao`, `esfera`, `eco`, `janela`, `veu`, `cinemascope`, `corte-logo`, `orbita`, `mapa-trilha`, `marcador-estacao`, `marcador-capitulo`, `anel`, `selo`, `logotipo`, `area-protecao`, `rodape`; lê `data-estacao` e `.modo-leitura`; recusa logotipo em texto e selo abaixo de 96 px. Opções: `logotipo {versao: horizontal\|vertical\|start\|master\|pro, cor: branco\|preto, altura}`, `selo {produto, tamanho, tipo: completo\|simples}`. Carregado por `src` do repositório, acha `assets/` sozinho; **colado num `<script>` ou fora do repositório, passe `base: "<caminho do repositório>/"`** (ou `VForms.config.base`), ou use os data URI do `lockup.html`: sem isso, logotipo e selo saem quebrados sem aviso |
| `vviz.js` | `data-vviz`, `VViz.render`, `VViz.svg`, `VViz.valida` | `barras`, `barras-horizontais`, `linha`, `coluna-empilhada`, `numeral`, `comparativo-traco`; sem `titulo`, `mede`, `periodo`, `base`, `fonte` e `origem` não desenha; `em-validacao` **não exporta** |
