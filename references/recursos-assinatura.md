# Recursos assinatura

Os 20 recursos assinatura com onde usar, onde nunca e a construção, mais o bloco do Crédito de Prova e as marcas de origem. Manual: seções 21 a 25.

Parte da skill [`branding-the-void`](../SKILL.md). Os valores batem com [`tokens.json`](../tokens.json) (conferido por `tools/conferir_skill.py`).

## Recursos assinatura (os 20)

**No máximo três recursos de destaque por tela** (a peça estática, cada cartão de carrossel ou tela de story, cada dobra de LP, e-mail ou membros); **o Grão conta como um**. Conta todo recurso da tabela, menos os de estrutura (a Cartela é composição: contam o Grão e a Janela que ela leva): Véu de Leitura, Palavra Sensível, Marcadores, Ficha Técnica, Créditos Finais, Crédito de Prova, Assinatura do Pro. Formas pelo `vforms.js` (`data-vforms="nome"`, `VForms.render(el,'nome',opções)`, ou `VForms.svg('nome',opções)` para Figma e Canva); utilitários no `tokens.css`. **Nunca `var()` em atributo SVG**: cor por classe ou `style`. Manual: seções 21 a 25.

| # | Recurso | Onde (e onde nunca) | Construção |
|---|---|---|---|
| 1 | **Grão do Vazio** | Todo campo escuro e foto; nunca em campo de formulário ou sobre o logotipo | `.grao`, **6% no escuro (`screen`), 4% no claro (`multiply`)**, estático no site; produção `assets/textura/grao-240.webp` |
| 2 | **Esfera do Vazio**, a única ilustração (slide 16) | Abertura de vídeo, estado vazio, obrigado, 404, manifesto; nunca atrás de rosto ou corpo, colorida, com o Eco, duas por peça | `esfera`; SVG com filtro, **nunca `mask:url(#...)` CSS**; 40% a 60% do lado menor (96 a 160 px em estado vazio); `esfera-3000.png` e `esfera-1080.webp` |
| 3 | **Eco do VOID** (slides 14 e 15) | Capa institucional, fecho de vídeo, cabeçalho do site, cartaz, fim de LP; nunca em Campo de Produto, atrás de corpo, abaixo de 600 px, com a Esfera | `eco`: `void-horizontal-branco.svg` com `blur(clamp(18px,2.6vw,40px))`, opacidade .12, `scale(1.6) translateX(18%)`, `aria-hidden` |
| 4 | **Janela de Luz** | Hero, cartela, cabeçalho de e-mail, capa de VSL, "Hoje"; nunca sobre foto, no Modo Leitura, duas por peça | `.janela-luz`: `radial-gradient(110% 75% at 12% 0%,rgb(248 249 244 / .09) 0%,rgb(248 249 244 / 0) 62%)` sobre Sala |
| 5 | **Véu de Leitura** | Todo texto sobre foto | **70% padrão**, **62%** sob texto abaixo de 24 px, **55%** sob título de 24 px ou mais, **48%** só sob título de 32 px ou mais em região escura; `.veu-esquerda`, `.veu-base`; amostre o pior pixel no `kit-social.html` |
| 6 | **Faixa Cinemascope** | Bastidor, manifesto, cabeçalho de artigo, capítulo de VSL, e-mail de marco; nunca em depoimento, story, Reels, thumbnail | 2,39 por 1 entre faixas Nanquim; em 1080 por 1350, faixa de 1080 por 452 com topo em y = 449; título em cima, Crédito embaixo |
| 7 | **Corte do Logo** | Cartaz de evento, capa, Campo de Produto, capa de carrossel, 404; nunca em anúncio de conversão, sobre rosto, em cor | `corte-logo`: SVG oficial cortado **entre letras inteiras**, nunca o ®; VOID com 70% a 110% da altura; opacidade 100% ou 8% |
| 8 | **Cartela** | Abertura, virada e fecho de carrossel, VSL, separador de LP; nunca duas seguidas, nunca com preço | Sala, grão, Janela de Luz; até 14 palavras; Título de Filme em até 3 linhas; voz em off em 1 linha; Crédito; sem foto e sem ícone |
| 9 | **Palavra Sensível** | Uma por título | `<h1 class="titulo-filme">O SEU CHAMADO PARA A ARTE <em class="off">acabou de chegar</em></h1>` |
| 10 | **Órbitas da Trilha** | Peça de produto, capa de módulo, abertura de VSL de produto; nunca no `chamado`, sobre rosto, preenchidas | `orbita`: Start 1,13 por 1; Master 0,89 por 1; Pro ±32° da vertical (razão 0,63); VOIDERS três círculos concêntricos; traço 1,5 px (2 u), Tela a 28% ou grafismo; paradas |
| 11 | **Mapa da Trilha** (slide 30): "ESSE É O VAZIO", "ESSE É O CAMINHO PARA PREENCHÊ-LO" | Trilha da LP, `/trilha/`, Minha Trilha, VSL, certificado, artigo; nunca sem nomes, fora de proporção, com mais de três círculos | `mapa-trilha` com `{"ativa":"master"}`: **1 : 2,3 : 3,6**, raios 65, 150, 232 tangentes em x = 250; vertical nativa até 430 px; frases **em HTML fora do SVG** |
| 12a | **Marcador de Estação** | Sobretítulo, e-mail, artigo, membros; uma vez por tela | `marcador-estacao` (14 px) + `START · RITUAL DO TRAÇO` em texto; nunca a palavra "estação" |
| 12b | **Marcador de Capítulo** | Só VSL (`CAPÍTULO 02 · O VAZIO`) e carrossel (`02 / 07 · A VIRADA`) | Dois dígitos, total na primeira e na última tela, fio de 24 por 1 px |
| 13a | **Selo como Carimbo** | Hero e oferta de produto, Campo de Produto, capa de VSL, certificado, marco | `{"forma":"selo","produto":"pro","tamanho":120}` |
| 13b | **Palavra de Produto** (slide 31) | Só no Campo de Produto; nunca com VOID | Voz em off em caixa alta, `calc(var(--u)*420)`, Tela a 8%; vazada só no Pro (Archivo 800 largura 125, contorno 2 u) |
| 14 | **Ficha Técnica** | Canto superior de peça premium (Pro, capa de LP, capa de VSL, convite, certificado, capa de PDF); nunca em post de conversão de topo nem na borda do rodapé | `THE VOID TATTOO ACADEMY · SÃO PAULO · BRAZIL`, Crédito 12 px (26 u), Pó; **sem "EST" ou "desde"** [P 5] |
| 15 | **Créditos Finais** | Rodapé de peça de marca, site, LP, e-mail, fecho de vídeo, PDF; nunca em anúncio 9:16 ou duas vezes | `rodape`: `TATTOO ACADEMY · ® 2025 · SÃO PAULO · BRAZIL · PREENCHA O VAZIO`, literal dos slides (2025 não é ano de fundação [P 5]), **único**, Crédito 12 px (26 u) em Pó, último termo em 700 e Tela, `·` com 0,9em, quebra depois de "BRAZIL" no celular |
| 15b | **Letreiro Corrido** | Só evento e topo de LP de evento | `THE VOID TATTOO · ® 2025 · SÃO PAULO · BRAZIL` em loop, faixa de 48 a 64 px, 40 px por segundo, pausa no `hover`, parado com movimento reduzido |
| 16 | **Crédito de Prova** | Todo número, depoimento, avaliação, dado de mercado | Bloco abaixo; `lockup.html`, grupo 08 |
| 17 | **Revelação** | Foto entrando no site (uma vez), VSL, marco validado; nunca em botão, texto, logotipo | `@keyframes revelar` de `opacity:0;filter:blur(10px) contrast(.7) brightness(.6)` a `none`, 900 ms, curva Cena |
| 18 | **Duotom de Produto** | Peça de produto; **nunca** em depoimento, rosto de aluno, Primeira Pele | Filtros `#duotom-start`, `#duotom-master`, `#duotom-pro` (manual 25.3) ou LUTs |
| 19 | **Anel de Preenchimento** | Só membros; nunca em anúncio, topo de funil, percentual de vídeo, comparação | `anel`: **enche só com marco validado pelo professor**; Start a 200°, 250° e 300°; pendente `stroke-dasharray:2 3`; 1.200 ms |
| 20 | **Assinatura de Produto do Pro**, a única pílula (slide 37) | Peças do Pro; não clicável. Start e Master: logotipo de produto e selo lado a lado | THE VOID® + pílula de 1,5 px (raio 999 px), selo simples Pro a 96 px ou mais, "SEJA UM ESTRATEGISTA DA SUA CARREIRA PROFISSIONAL." e PRO; `lockup.html`, grupo 05 |

**Crédito de Prova:**

```html
<figure class="prova" data-origem="medido">
 <data class="prova-n" value="0">[N]</data>
 <figcaption class="prova-o-que">alunos concluíram a formação Start</figcaption>
 <p class="prova-regua"><span class="origem"></span>contagem da secretaria · turmas até [mês/ano] · registro interno</p>
</figure>
```

Marca de origem (fio de 16 por 2 px): **cheio = medido** (registro da escola) · **tracejado = terceiro** (Google, imprensa; link e data da captura) · **pontilhado = mercado** (estudo externo com link) · **em validação**: "dado em validação", só no arquivo de trabalho, **bloqueia exportação e publicação**. Sem prova, o número sai; nunca vira zero, nunca vai com colchete, **nunca anima contando**.
