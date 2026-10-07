---
name: branding-the-void
description: "Identidade da The VOID Tattoo Academy (escola de tatuagem na Vila Madalena, em São Paulo), sistema Sala Escura v1. Use em todo material: post, carrossel, story, Reels, anúncio, landing page, VSL, e-mail, WhatsApp, área de membros, artigo, deck, proposta, certificado, evento e impresso. Gatilhos: the void, the void tattoo academy, padrão void, sala escura, voiders, start, master, pro, aula experimental, the void talks. Traz: Sala #181818 como campo e uma única luz por cena; Tela #F8F9F4 no título e no botão; terras como luz que se conquista; logotipo só em arquivo oficial preto ou branco; Archivo em caixa alta, Newsreader Italic 300 como voz em off e Nunito Sans no texto; oito leis; 20 recursos assinatura; tema por produto com data-estacao; Crédito de Prova em todo número; voz e comunicação M1 a M8; conformidade de escola livre; acervo de fotos reais; motores vforms.js e vviz.js."
---

# /branding-the-void · A identidade da The VOID Tattoo Academy

Um estilo de casa travado, chamado **Sala Escura** (nome de trabalho; nunca aparece em peça pública). O vazio da The VOID é a sala escura do cinema e do laboratório de revelação: o preto não é ausência, é o lugar onde a imagem ainda vai aparecer. O manifesto diz: "esse vazio não é uma fraqueza, é um chamado" (Plataforma de Branding, aureadesign, 2025, slide 10). Cada peça é uma cena em que **uma única luz** entra no escuro e revela uma mão que fica firme. A trilha Start, Master e Pro preenche esse vazio, desenhada pela agência como três círculos tangentes (slide 30).

Quatro regras de bolso: **o preto é a sala** (Sala `#181818` em pelo menos 60% de toda peça de marca), **uma luz por cena** (o botão é o ponto mais claro da tela), **a cor se conquista** (topo de funil é monocromático; a cor do produto aparece quando a pessoa entra numa formação) e **toda prova tem crédito** (nenhum número sem o que mede, recorte, data, fonte e marca de origem).

Frase-guia interna (não é copy): *No escuro, uma luz. Na luz, uma mão. Na mão, um traço.* A metáfora gera regras, não decoração.

**Abra PRIMEIRO:** o manual vivo em 36 seções e 9 partes, [brand-book.html](https://rafaelnasch.github.io/branding-the-void/brand-book.html) (cada seção abre por âncora: `brand-book.html#sNN-N`, ex.: `#s13-2`). Pedidos prontos por público: [guia-de-uso.html](https://rafaelnasch.github.io/branding-the-void/guia-de-uso.html). Trechos para copiar: [`lockup.html`](lockup.html). Motores: [`vforms.js`](vforms.js) (formas) e [`vviz.js`](vviz.js) (gráficos com régua). Valores: [`tokens.css`](tokens.css) e [`tokens.json`](tokens.json). Peça parecida com esses arquivos está certa.

**Fontes desta skill.** Tudo sai da especificação Sala Escura v1 (06/10/2026), que consolida a Plataforma de Branding (aureadesign, 2025), o Brand DNA da The VOID (set/2026), as Personas (set/2026) e o site oficial (consultado em 06/10/2026). O que depende da escola aparece como **[P n]** (lista em [`references/pendencias.md`](references/pendencias.md)) ou `{{A_CONFIRMAR}}`. Colchetes como `[ANO]` e `[N]` nunca vão ao ar.

**Como a skill está organizada.** Este arquivo traz o essencial para operar. O detalhe de cada assunto mora em `references/` e só é aberto no passo em que é necessário (mapa abaixo). Nada fica fora: todo valor citado aqui e nas referências é conferido contra o `tokens.json`.

---

## A primeira pergunta: que peça, para quem, em que momento?

Antes de cor, fonte ou formato, responda as quatro. Se o pedido não disser, **pergunte numa frase só** ou assuma o mais provável e diga o que assumiu.

1. **Que peça?** (post, carrossel, story, Reels, anúncio, LP, VSL, e-mail, WhatsApp, tela de membros, artigo, deck, impresso). Decide medida, grade, componente e arquivo modelo.
2. **Para qual etapa, M1 a M8?** Decide a crença que a peça derruba, a função, o recurso que lidera e o **único** CTA (seção M1 a M8 e [`comunicacao-m1-m8.html`](comunicacao-m1-m8.html)).
3. **Qual persona?** Gabriel, Camila ou Bruno (Sylvia, subperfil do Pro). Decide o hero, o tom e o tipo de prova (manual 04.1).
4. **Qual produto?** Vira `data-estacao` no contêiner: `chamado` (institucional, aula experimental, Talks, Convenção), `start`, `master`, `pro` ou `voiders` (comunidade e ex-alunos). Decide campo, destaque, grafismo, seta, duotom, órbita e Palavra Sensível (manual 15.3).

**Personas (Personas, set/2026).** A persona **nunca aparece escrita** na peça: está na crença que o título derruba. Faixa de renda e região são dado interno.

| Persona | Produto | Falsa convicção | Hero para teste | Tom |
|---|---|---|---|---|
| **Gabriel**, o jovem sonhador | Start | "Eu não tenho talento suficiente para viver de tatuagem." | "TALENTO É CONSEQUÊNCIA DE *treino*." | Coragem, prova de iniciantes |
| **Camila**, em transição | Start, depois Master | "Já passei da hora." | "SUA EXPERIÊNCIA É UM *diferencial*, NÃO UM ATRASO." | Recomeço; lógica antes da permissão |
| **Bruno**, tatuador em evolução | Master e Pro | "Preciso ser melhor tecnicamente antes de cobrar o que mereço." | "TÉCNICA SEM POSICIONAMENTO É *invisível*." | Posicionamento, casos de crescimento |
| Sylvia (subperfil) | Pro | "Para crescer, preciso tatuar ainda mais." (proposta GrowAI, aguarda aprovação) | o do Bruno | Estratégia de carreira |

Itálico entre asteriscos é a voz em off. "Você não precisa de talento para começar" está vetada (perto do tom condescendente). **Uma peça, uma persona, uma crença, um pedido.**

---

## Mapa: o que abrir em cada passo

Abra a referência só quando o passo pedir. Os kits HTML já cumprem as leis: parta deles.

| Passo | Referência | Kit ou arquivo modelo |
|---|---|---|
| Escolher cor, par de contraste, tema por produto, Modo Leitura | [`references/cor-e-contraste.md`](references/cor-e-contraste.md) | [`tokens.css`](tokens.css), [`tokens.json`](tokens.json) |
| Definir fonte, registro, tamanho, largura, voz em off | [`references/tipografia.md`](references/tipografia.md) | [`tokens.css`](tokens.css) |
| Pôr logotipo, selo, co-assinatura, nome de produto | [`references/marca-e-selos.md`](references/marca-e-selos.md) | [`lockup.html`](lockup.html) (grupos 03 a 06), `assets/brand/` |
| Usar Grão, Esfera, Eco, Véu, Cartela, Mapa da Trilha e os demais recursos | [`references/recursos-assinatura.md`](references/recursos-assinatura.md) | [`vforms.js`](vforms.js) |
| Montar grade, espaço, raio, movimento, ícone | [`references/grade-forma-movimento.md`](references/grade-forma-movimento.md) | [`tokens.css`](tokens.css) |
| Escolher foto, vídeo, LUT | [`references/fotografia-e-acervo.md`](references/fotografia-e-acervo.md) | `assets/foto/acervo/catalogo.json`, `assets/foto/*.cube`, `assets/foto/receitas.md` |
| Escrever a copy, o tom por canal, a mensagem por etapa M1 a M8 | [`references/voz-e-m1-m8.md`](references/voz-e-m1-m8.md) | [`comunicacao-m1-m8.html`](comunicacao-m1-m8.html) |
| Pôr número, depoimento, preço, vaga, aviso legal | [`references/conformidade.md`](references/conformidade.md) | [`lockup.html`](lockup.html) (grupo 08) |
| Saber a medida da peça e a interface dos motores | [`references/canais-e-medidas.md`](references/canais-e-medidas.md) | [`vforms.js`](vforms.js), [`vviz.js`](vviz.js) |
| Landing page | [`references/kits-por-canal.md`](references/kits-por-canal.md) | [`lp-template.html`](lp-template.html) |
| VSL, capa, cartelas, legenda | [`references/kits-por-canal.md`](references/kits-por-canal.md) | [`vsl-kit.html`](vsl-kit.html) |
| Post, carrossel, story, Reels, anúncio (R1 a R13) | [`references/kits-por-canal.md`](references/kits-por-canal.md) | [`kit-social.html`](kit-social.html) |
| Área de membros, certificado | [`references/kits-por-canal.md`](references/kits-por-canal.md) | [`membros-ui.html`](membros-ui.html) |
| E-mail | [`references/kits-por-canal.md`](references/kits-por-canal.md) | [`email-template.html`](email-template.html) |
| WhatsApp e Cartões de Conversa | [`references/kits-por-canal.md`](references/kits-por-canal.md) | [`comunicacao-m1-m8.html`](comunicacao-m1-m8.html), [`lockup.html`](lockup.html) (grupo 09) |
| Artigo do guia (SEO, GEO, AEO) | [`references/kits-por-canal.md`](references/kits-por-canal.md), [`references/seo-geo-aeo.md`](references/seo-geo-aeo.md) | [`artigo-template.html`](artigo-template.html), `assets/seo/` |
| Deck e proposta de uma página | [`references/kits-por-canal.md`](references/kits-por-canal.md) | [`deck-template.html`](deck-template.html) |
| Entidade, NAP, JSON-LD, llms.txt | [`references/seo-geo-aeo.md`](references/seo-geo-aeo.md) | `assets/seo/` |
| Gráfico, acessibilidade, celular, PDF, conferência | [`references/dados-e-acessibilidade.md`](references/dados-e-acessibilidade.md) | [`vviz.js`](vviz.js) |
| Algo depende da escola | [`references/pendencias.md`](references/pendencias.md) | |

---

## Onde a skill roda (e o que muda em cada lugar)

**Claude Code** (`~/.claude/skills/branding-the-void`) e **Codex** (`~/.agents/skills/branding-the-void` ou `~/.codex/skills/branding-the-void`), por `git clone https://github.com/rafaelnasch/branding-the-void.git`: ambiente completo, com `tools/`, `autocontido.py`, `exportar_pdf.py` e o acervo inteiro. Manual: https://rafaelnasch.github.io/branding-the-void/.

**claude.ai e ChatGPT** (ZIP `branding-the-void.zip` do Release; no claude.ai, envie em Configurações, Capacidades, Skills): o pacote leva `SKILL.md`, `references/`, tokens, motores, os nove kits HTML e a marca. **As fotos do acervo não viajam no ZIP:** o `catalogo.json` e os kits apontam para `https://rafaelnasch.github.io/branding-the-void/assets/foto/acervo/...`. Ferramentas de `tools/`, `autocontido.py` e `exportar_pdf.py` só existem no repositório. Outro caminho de `assets/` citado nas referências e ausente do pacote (por exemplo `assets/aplicacoes/email-foto/`, `assets/brand/png/alta/`, `assets/fontes/google/`, `assets/vsl/exemplo.srt`) abre pelo mesmo caminho em `https://rafaelnasch.github.io/branding-the-void/`. **O artefato é um arquivo só e não enxerga `assets/`, `tokens.css` nem os `.js`.**

**REGRA DO NAVEGADOR (claude.ai, ChatGPT):** todo HTML gerado ali é **autocontido**.

1. **Logotipo:** copie, por código, o valor `uri` do bloco `<script type="application/json" id="lk-datauri">` do [`lockup.html`](lockup.html) (entre `lockup-datauri:inicio` e `lockup-datauri:fim`; grupo 03). São os dez logotipos oficiais (horizontal, vertical, Start, Master e Pro, em preto e branco) e o favicon. **Nunca digite, resuma ou reconstrua um data URI; nunca desenhe o logotipo em `<path>` nem em texto.**
2. **Selos:** sem data URI pronto. Converta `assets/brand/svg/selo-*.svg` por código, sem alterar um byte. Sem o arquivo, use o Rótulo de Produto em texto (`THE VOID START` em Crédito com fio de 1 px) e avise.
3. **Tokens e motores:** cole `tokens.css` num `<style>` e `vforms.js` e `vviz.js` num `<script>`.
4. **Fontes:** pelo link do Google Fonts. **A Alga nunca entra.**
5. **PDF:** entregue o HTML e mande imprimir pelo Chrome com "Gráficos de segundo plano" ligado.

**Para ENVIAR um HTML** (e-mail, WhatsApp, Drive): `python3 autocontido.py <arquivo.html>` grava em `dist/` com tudo embutido; os 12 HTML da marca já estão em `dist/`. Em e-mail, data URI não funciona: vale o PNG hospedado (`lockup.html`, grupo 09).

---

## As oito leis (TRAVADAS)

**Quando duas leis brigam, vence a de número menor.** Cada uma tem um teste de menos de um minuto. Manual: seção 06.

| # | Lei e o que manda | Teste |
|---|---|---|
| L1 | **Um vazio, uma ação.** Uma crença falsa ou um fato, uma ação. Em fundo de funil, todos os botões com o mesmo destino e o mesmo rótulo. | Destinos clicáveis (sem privacidade e descadastro) = 1; a crença cabe numa linha. |
| L2 | **Toda prova tem crédito.** Número, depoimento, avaliação ou dado de mercado só com o Crédito de Prova. Superlativo conta como número sem crédito. | Leia as cinco partes de cada número. Faltou uma, a peça volta. |
| L3 | **AA ou não sai.** 4,5:1 (3:1 só a partir de 24 px, ou 19 px em 700); toque de 44 por 44 px; legenda em todo vídeo; estado com ícone e palavra; foco visível; par fora da tabela não é usado. | Cada par na tabela; texto sobre foto, amostre o pior pixel. |
| L4 | **O preto é a sala.** Campo escuro (Sala, Nanquim ou foto P&B tratada) em 60% ou mais da área; a Tela só é campo no Modo Leitura. | A peça a 64 px de largura, desfocada, é majoritariamente escura. |
| L5 | **Uma luz por cena.** Um ponto de ênfase, uma cor de acento; em campo escuro, a superfície clara mais forte da dobra é o botão (ou um rosto que olha para ele); luz de cima ou da esquerda. | Desfoque de 12 px na dobra: o primeiro ponto claro é o botão; até 1 palavra ou 1 título de acento, mais o botão. |
| L6 | **Título é letreiro.** Archivo em caixa alta, **até 6 palavras por título ou tela**; voz em off em **uma linha por bloco**, nunca em botão, número, preço, instrução, legenda funcional, texto legal. | Conte palavras e linhas em itálico. Exceções: H1 de artigo em pergunta e a tagline. |
| L7 | **Duas formas, nenhuma no meio.** Retângulo (raio 0) e círculo (50%); a única pílula é a Assinatura do Pro; nenhuma sombra decorativa. | `border-radius` só 0, 50% ou a pílula; `box-shadow` só no foco. |
| L8 | **Montagem com ritmo.** Sequências alternam **cena**, **cartela** e **documento**; nunca três iguais seguidas; o fim é **um** pedido. | Rotule cada tela; três iguais seguidas reprovam. |

**Contenção do tema:** proibido claquete, rolo de filme ilustrado, contagem regressiva de cinema, "CENA", "TAKE", "AÇÃO!", "CORTA!", créditos de filme inventados e tipografia de cartaz antigo. **Nunca dois dispositivos de cinema na mesma peça estática** (Faixa Cinemascope, Marcador de Capítulo, Corte do Logo e Revelação contam).

---

## Cores (o essencial)

O sistema é escuro por natureza: **não existe modo claro ou escuro automático**. `body` sempre com fundo explícito (`var(--sala)`); a página clara é uma **exceção nomeada** (Modo Leitura), escolhida pela peça ou pelo aluno, nunca pelo tema do aparelho. Paleta completa (28 cores), estados, orçamento de área e todos os pares: [`references/cor-e-contraste.md`](references/cor-e-contraste.md).

| Token e nome | HEX | Papel |
|---|---|---|
| `--sala` Sala | `#181818` | **O campo da marca** (site, LP, post, story, VSL, membros, cabeçalho e rodapé de e-mail); texto no Modo Leitura |
| `--bastidor` Bastidor | `#212121` | Cartão e painel sobre Sala; faixa alternada; Barra de Turma |
| `--coxia` Coxia | `#2B2B2B` | Cartão ativo, campo de formulário escuro, disco do selo Pro |
| `--tela` Tela | `#F8F9F4` | **A luz:** título e botão no escuro; campo do Modo Leitura |
| `--cal` Cal | `#DCDDD8` | **Corpo longo no escuro**; botão pressionado |
| `--po` Pó | `#B4B5B0` | Apoio no escuro: Crédito de Prova, legenda, microcopy do botão |
| `--fumaca` Fumaça | `#898989` | Texto auxiliar de 14 px ou mais e borda de campo no escuro; linha no claro |
| `--nanquim` Nanquim | `#000000` | Preto dos SVG oficiais e base do selo Pro; barras de vídeo. **Nunca campo de página** |
| `--branco` Branco | `#FFFFFF` | Só o logotipo branco oficial e as linhas dos selos |
| `--areia` Areia | `#DBC5A3` | Luz quente de texto no escuro (Start e institucional); palavra de destaque; **anel de foco** |
| `--terracota-luz` Terracota Luz | `#DE8C66` | **A única terracota de texto pequeno no escuro** |
| `--terracota` Terracota | `#B25A32` | Acento quente; base do selo Master; grafismo e título grande do Master |
| `--campo-start` Campo Start | `#B5966B` | **Campo do Start** (texto Sala; logotipo branco, como no slide 31) |
| `--campo-master` Campo Master | `#76432B` | **Campo do Master** (texto Tela; logotipo branco) |
| `--nevoa` Névoa | `#C9D0D8` | Acento frio do Pro e estado informativo no escuro |
| `--ardosia` Ardósia | `#3F4E4F` | Miolo do selo Pro; apoio e informação no claro. Nunca texto sobre Sala |

**Hierarquia de luz no escuro** (sólidas, servem em e-mail, PDF e vídeo): nível 100 Tela, 16,78 sobre Sala, título, botão, número de prova · 86 Cal, 13,00, corpo longo · 68 Pó, 8,61, apoio, legenda, Crédito de Prova · 55 Fumaça, 5,08, auxiliar de 14 px ou mais; abaixo disso não é texto. **Profundidade por tom, nunca por sombra:** Sala, Bastidor, Coxia.

**Regra de ouro do contraste:** par fora da lista de [`references/cor-e-contraste.md`](references/cor-e-contraste.md) não é usado até ser calculado (`python3 tools/contraste.py`, no repositório). Texto sobre foto só com Véu (70% padrão, 62% sob texto abaixo de 24 px), amostrando o pior pixel. Os erros mais comuns: texto Tela no Campo Start (ali o texto é Sala), terracota pura em texto pequeno no escuro (só Terracota Luz), Fumaça abaixo de 14 px.

**Estados**, sempre com ícone Lucide e palavra: Sucesso em Musgo Luz, Atenção em Areia, Erro em Ferrugem Luz, Informação em Névoa (valores no escuro e no claro na referência). **Erro nunca é urgência.**

### Tema por produto (`data-estacao`)

O tema troca com **um único atributo** no contêiner: `data-estacao="chamado|start|master|pro|voiders"`. "Estação" é palavra de código e **nunca aparece em copy pública**. O logotipo continua preto ou branco em todos: **a cor mora no selo, no campo, no grafismo e na seta do botão, nunca no logotipo.**

| Item | `chamado` | `start` | `master` | `pro` | `voiders` |
|---|---|---|---|---|---|
| Campo de produto | nenhum: Sala, Tela e grão | Campo Start, texto Sala, logotipo branco | Campo Master, texto Tela, logotipo branco | Sala com faixa Ardósia ou Chumbo | nenhum |
| Destaque de texto no escuro | Areia | Areia | Terracota Luz (pequeno) ou Terracota Viva (24 px ou mais) | Névoa | Areia |
| Grafismo | Tela a 32% | Ouro Velho (Caramelo sobre Coxia) | Terracota | Névoa | Tela a 32% |
| Palavra Sensível de assinatura | *o primeiro passo* | *o primeiro traço* | *a sua identidade* | *o seu plano* | *família* |

Seta do botão, duotom, órbita e círculo ativo: tabela completa na referência de cor. **A cor se conquista:** topo de funil e aula experimental são monocromáticos; a aula assina com `void-start` e o selo Start aparece só como "próxima etapa" [P 14].

**Modo Leitura** (classe `.modo-leitura`): a Tela vira página só onde a leitura é longa e racional (corpo de artigo, corpo de e-mail, oferta e fatos da LP, PDF, contrato, certificado, leitura nos membros). **Nunca** em hero, capa, post de topo, story, Reels, VSL fora da oferta, thumbnail ou Campo de Produto. Até [P 2]: artigo e e-mail em Sala com corpo Cal.

**Sai da paleta:** verde de botão, vermelho de urgência, rosa, magenta, ciano, laranja e lilás, gradiente bege para cobre, verde do WhatsApp como interface e **qualquer gradiente de cor** (só existem gradientes de luz: Janela de Luz, Véu e Esfera).

---

## Tipografia (o essencial)

Registros, escalas (documento, peça de 1080 e vídeo), regra de largura e as oito regras da voz em off: [`references/tipografia.md`](references/tipografia.md).

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

- **Alga é paga.** Nunca entra no repositório, no autocontido, no Canva nem em pasta de cliente. **Até [P 3], todo material público sai em Newsreader Italic 300.**
- **Registros do Archivo** (classes do `tokens.css`): `.titulo-filme` 800/112 (hero, capa, gancho) · `.titulo-secao` 700/100 · `.fala` 600/100 (subtítulo, FAQ, legenda de vídeo) · `.credito` 500/125, +0,18em · `.numeral-prova` 700/75 · `.botao` 700/106, +0,06em. Nenhuma peça usa mais de dois registros de largura além do texto.
- **Título que não cabe:** antes de reduzir, estreite (`wdth` 112, 100, 92, 85); depois reduza até o piso de 34 px; abaixo disso, **reescreva** (L6).
- **Voz em off:** uma linha por bloco, só a palavra que sente (até 7 palavras), 1,2 vez o Archivo da linha, piso de 20 px em tela; **nunca** em botão, número, preço, data, instrução, legenda funcional, texto legal, formulário, tabela ou nome de pessoa. No e-mail cai para Georgia itálico, nunca vira imagem.
- **Texto:** caixa alta só em título, botão, crédito e rótulo; itálico só na voz em off; sem contorno, sombra ou degradê em texto; corpo de 18 px no computador e 17 no celular. **Zero travessão** em qualquer texto, inclusive legenda, assunto de e-mail, texto alternativo, `title` e comentário visível.

---

## A marca (o essencial)

**O logotipo é desenho, não texto: nunca redigite THE VOID.** Sempre os arquivos de `assets/brand/` (exportação da Plataforma de Branding, aureadesign, 2025). Medidas, proteção, arquitetura de marca e co-assinatura: [`references/marca-e-selos.md`](references/marca-e-selos.md).

| Peça | Arquivos em `assets/brand/svg/` (`-preto` e `-branco`) |
|---|---|
| Horizontal THE VOID® TATTOO | `void-horizontal-*.svg` |
| Vertical THE / VOID® / TATTOO ACADEMY | `void-vertical-*.svg` |
| De produto | `void-start-*`, `void-master-*`, `void-pro-*` |
| Selo completo e simples | `selo-completo-start\|master\|pro.svg`, `selo-simples-start\|master\|pro.svg` |
| Raster, favicon, redes | `png/web/`, `favicon/`, `social/avatar-1080.png`, `social/og-1200x630.png` [P 12] |

- **Preto e branco são as versões oficiais.** Branco sobre Sala, Nanquim, Bastidor, Coxia, Campo Start, Campo Master, Café ou foto com véu de 55% ou mais; preto sobre Tela, Branco, Cinza 100, Areia ou Névoa; **nunca** sobre Terracota, Ouro Velho, Caramelo ou foto sem véu.
- **Mínimos** (proposta a validar [P 11]): horizontal e de produto 24 px de altura em tela (66 u na peça de 1080); vertical 80 px; selo completo 200 px; selo simples 96 px. **Abaixo de 96 px não existe selo:** use o Rótulo de Produto em texto ou o favicon. Proteção de 1 X em volta do desenho.
- **Proibido:** redigitar, recolorir, contornar, sombrear, distorcer, girar, digitar descritor ("THE VOID® TALKS" à mão), logotipo antigo serifado, logotipo nítido duas vezes na peça.
- **Selo Pro simples sobre Sala** vai num disco Coxia (a base Nanquim some, 1,18:1). `VForms.render(el,'selo',{produto,tamanho})` resolve sozinho.

---

## Recursos assinatura (o essencial)

**No máximo três recursos de destaque por tela; o Grão conta como um.** Formas pelo [`vforms.js`](vforms.js) (`data-vforms="nome"`, `VForms.render(el,'nome',opções)` ou `VForms.svg('nome',opções)`); **nunca `var()` em atributo SVG**. Onde usar, onde nunca e a construção de cada um: [`references/recursos-assinatura.md`](references/recursos-assinatura.md).

Os 20: Grão do Vazio · Esfera do Vazio (a única ilustração) · Eco do VOID · Janela de Luz · Véu de Leitura · Faixa Cinemascope · Corte do Logo · Cartela · Palavra Sensível · Órbitas da Trilha · Mapa da Trilha · Marcador de Estação e Marcador de Capítulo · Selo como Carimbo e Palavra de Produto · Ficha Técnica · Créditos Finais e Letreiro Corrido · Crédito de Prova · Revelação · Duotom de Produto · Anel de Preenchimento (só membros) · Assinatura de Produto do Pro (a única pílula).

---

## Regra de prova e claims vetados (TRAVADA)

Todo número, depoimento, avaliação ou dado de mercado leva o **Crédito de Prova**. Doze regras de prova, frases-modelo e avisos: [`references/conformidade.md`](references/conformidade.md) (prontas no [`lockup.html`](lockup.html), grupo 08). Não substitui orientação jurídica.

```html
<figure class="prova" data-origem="medido">
 <data class="prova-n" value="0">[N]</data>
 <figcaption class="prova-o-que">alunos concluíram a formação Start</figcaption>
 <p class="prova-regua"><span class="origem"></span>contagem da secretaria · turmas até [mês/ano] · registro interno</p>
</figure>
```

Marca de origem (fio de 16 por 2 px): **cheio = medido** (registro da escola) · **tracejado = terceiro** (Google, imprensa; link e data da captura) · **pontilhado = mercado** (estudo externo com link) · **em validação**: "dado em validação", só no arquivo de trabalho, **bloqueia exportação e publicação**. Sem prova, o número sai; nunca vira zero, nunca vai com colchete, **nunca anima contando**.

Em resumo: número só com prova arquivada, recorte, data e fonte · nenhuma promessa financeira com número ou prazo · urgência só real (Barra de Turma ligada ao calendário) · preço igual ao checkout [P 15] · depoimento real e autorizado · nenhum menor em procedimento · nunca presumir condição pessoal de quem lê · **concorrente nunca citado** · material interno da agência nunca em público.

<div data-exemplo="proibido" markdown="1">

**Quadro de exemplos proibidos (nunca em peça pública; só aqui, para reconhecer):**

- Superlativo sem prova pública (maior, melhor, número 1, "#1", líder, único). Número de alunos sem método de contagem publicado. Tempo de mercado ou ano de fundação ("[N] anos", "desde [ano]") até a confirmação [P 5]. Dado de mercado sem fonte publicada.
- Reconhecimento oficial de ensino sem validação de advogado: MEC, diploma, curso técnico, habilitação, credenciamento, certificação por instituição parceira.
- Promessa de valor cobrado ou faturamento com número e prazo: "o curso se paga em [N] meses", "cobrei R$ [valor] em [N] meses", "dobrar o valor", "cobrar [N] vezes mais", nome de produto ou desafio com valor em dinheiro.
- Rótulos de botão: "SAIBA MAIS", "CLIQUE AQUI", "COMPRE AGORA", "LEARN MORE", "Quero sentir a máquina na mão" (até o roteiro da aula ser confirmado [P 16]), "Quero meu diagnóstico técnico" no Master (diagnóstico é do Pro).
- Frase de curso livre, **pendente de advogado [P 20]**, só entra marcada como pendente: "A The VOID oferece formação livre em tatuagem. Ao concluir, você recebe o certificado de conclusão da escola. Curso livre não depende de autorização do MEC e não equivale a curso técnico ou superior."

</div>

---

## Voz e imagem (o essencial)

**Voz:** um artista que virou professor; inspira sem intimidar, ensina sem condescendência. **Corajosa**, não agressiva · **Inspiradora**, não idealizada · **Técnica**, não fria · **Próxima**, não invasiva. "Formação", não "curso"; "você" no singular; nada de incrível, fácil, empoderar, revolucionário, nível, XP, ranking; nada de inglês em copy pública. Tom por canal, frases de assinatura, tagline e a régua M1 a M8: [`references/voz-e-m1-m8.md`](references/voz-e-m1-m8.md).

**Imagem:** toda peça tem **foto real e autorizada** do acervo (`assets/foto/acervo/catalogo.json`; no ZIP, pelas URLs públicas do Pages); nada de banco de imagem ou imagem gerada apresentada como real. Uma luz, preto denso, as mãos como personagem, P&B "Ritual" como padrão, no máximo 1 imagem colorida em 4, biossegurança visível. Critérios, temas, recortes por canal, alertas, crédito, LUTs e vídeo: [`references/fotografia-e-acervo.md`](references/fotografia-e-acervo.md).

---

## Checklist de aprovação de peça

Persona e crença declaradas · **um** CTA · vocabulário no território · **zero travessão** · todo número com Crédito de Prova · nenhum claim vetado · aviso de resultado quando há prova · autorização de imagem cobrindo o canal · biossegurança visível · nenhum menor · preço e condições iguais ao checkout · vagas reais · arrependimento informado em venda online · contraste conferido na tabela (texto sobre foto, amostragem do pior pixel) · logotipo oficial com área de proteção · selo acima do mínimo · tagline só em contexto de peso · última linha que fica.

Validação estrutural não prova qualidade visual: **renderize e olhe** em 1440 e 390 px (320 em página) antes de entregar. No repositório: `python3 tools/verificar.py <arquivo.html>` e `python3 tools/contraste.py --check` ([`references/dados-e-acessibilidade.md`](references/dados-e-acessibilidade.md)).

---

## Armadilhas (vão te morder)

1. **Redigitar THE VOID** porque "fica igual". O logotipo é sempre arquivo ou o data URI do `lockup.html`.
2. **Pintar o logotipo** com a cor do produto. A cor mora no selo, no campo, no grafismo e na seta; o logotipo é preto ou branco.
3. **Selo abaixo de 96 px** (não existe: Rótulo de Produto) e **selo Pro simples sobre Sala sem o disco Coxia** (a base some, 1,18:1).
4. **Texto Tela no Campo Start** (ali o texto é Sala), **terracota pura em texto pequeno no escuro** (só Terracota Luz) ou **véu calculado sobre off-white** (o pior pixel é branco puro).
5. **Botão em pílula, com sombra ou com pulso**, ou dois botões cheios na dobra.
6. **Voz em off em botão, preço, data ou nome**, ou em duas linhas no mesmo bloco (só a tagline tem essa exceção).
7. **Título com sete palavras.** Estreite o `wdth`, reduza até 34 px e, se não couber, reescreva.
8. **Número plausível sem prova** (vai `{{A_CONFIRMAR}}` ou "dado em validação"; nunca zero, nunca colchete publicado) e **Barra de Turma vencida, com contador** ou "últimas vagas" sem número.
9. **Peça sem foto**, ou foto de banco ou gerada para ficar bonito. Use o acervo; sem foto que sirva, "foto real da escola, com autorização".
10. **Clichê:** claquete, "CENA", caveira, rosa, chama, neon; ou dois dispositivos de cinema na mesma peça.
11. **Gamificação nos membros** (nível, XP, ranking, medalha). O Anel enche só com marco validado.
12. **Modo Leitura no hero, story ou capa**, ou seguindo o tema do aparelho.
13. **`var()` em `fill` de SVG**, `mask:url(#...)` em HTML, ícone de CDN, emoji na arte, Alga em qualquer arquivo.
14. **"Estação" na copy**, inglês na copy pública, concorrente citado, ritos inventados [P 6], ano de fundação [P 5], material interno da agência (diagnóstico, análises internas, dado pessoal).
15. **Fonte com caminho de pasta.** Cite "Plataforma de Branding, aureadesign, 2025", "Brand DNA da The VOID, set/2026", "Personas, set/2026", "site oficial, consultado em 06/10/2026".

---

## Pendências com a The VOID (não resolva por conta própria)

São 22, de [P 1] a [P 22]. Entregue só a versão permitida e diga qual pendência travou o quê (manual 36.5). A lista com o que fazer enquanto cada uma não fecha: [`references/pendencias.md`](references/pendencias.md).

---

## Mapa de arquivos

Lista no `README.md` e no `index.html` do repositório. Para enviar: `dist/` (HTML em arquivo único e PDF), só no repositório.

---

Marca e selos são da The VOID Tattoo Academy, desenho da aureadesign.co (Plataforma de Branding, 2025). Sistema organizado com a GrowAI. Sala Escura v1 · publicado em 06/10/2026; propostas em aprovação pela The VOID ([P 1] a [P 22]). Não substitui orientação jurídica.
