---
name: branding-the-void
description: "A identidade da The VOID Tattoo Academy (escola de tatuagem na Vila Madalena, em São Paulo) no sistema Sala Escura v1: Sala #181818 como campo, uma única luz por cena, Tela #F8F9F4 no título e no botão, terracota e terras como luz quente que se conquista, logotipo sempre em arquivo oficial preto ou branco, Archivo em caixa alta como letreiro, Newsreader Italic 300 como voz em off (Alga onde houver licença), Nunito Sans no texto, oito leis com teste, 20 recursos assinatura, tema por produto com data-estacao (chamado, start, master, pro, voiders), Crédito de Prova em todo número, voz corajosa, inspiradora, técnica e próxima, comunicação M1 a M8 por crença, conformidade de escola livre, acervo de fotos reais da escola (assets/foto/acervo) e motores vforms.js e vviz.js. Use em todo material da The VOID: post, carrossel, story, Reels, anúncio, landing page, VSL, e-mail, WhatsApp, área de membros, artigo do guia, deck, proposta, certificado, evento e impresso. Triggers: the void, the void tattoo academy, padrão void, sala escura, voiders, start, master, pro, aula experimental, the void talks."
---

# /branding-the-void · A identidade da The VOID Tattoo Academy

Um estilo de casa travado, chamado **Sala Escura** (nome de trabalho; nunca aparece em peça pública). O vazio da The VOID é a sala escura do cinema e do laboratório de revelação: o preto não é ausência, é o lugar onde a imagem ainda vai aparecer. O manifesto diz: "esse vazio não é uma fraqueza, é um chamado" (Plataforma de Branding, aureadesign, 2025, slide 10). Cada peça é uma cena em que **uma única luz** entra no escuro e revela uma mão que fica firme. A trilha Start, Master e Pro preenche esse vazio, desenhada pela agência como três círculos tangentes (slide 30).

Quatro regras de bolso: **o preto é a sala** (Sala `#181818` em pelo menos 60% de toda peça de marca), **uma luz por cena** (o botão é o ponto mais claro da tela), **a cor se conquista** (topo de funil é monocromático; a cor do produto aparece quando a pessoa entra numa formação) e **toda prova tem crédito** (nenhum número sem o que mede, recorte, data, fonte e marca de origem).

Frase-guia interna (não é copy): *No escuro, uma luz. Na luz, uma mão. Na mão, um traço.* A metáfora gera regras, não decoração.

**Abra PRIMEIRO:** [`brand-book.html`](brand-book.html), o manual vivo em 36 seções e 9 partes. Pedidos prontos por público: [`guia-de-uso.html`](guia-de-uso.html). Trechos para copiar: [`lockup.html`](lockup.html). Motores: [`vforms.js`](vforms.js) (formas) e [`vviz.js`](vviz.js) (gráficos com régua). Valores: [`tokens.css`](tokens.css) e [`tokens.json`](tokens.json). Peça parecida com esses arquivos está certa. Cada seção do manual abre por âncora: `brand-book.html#sNN-N` (ex.: `#s13-2`).

**Fontes desta skill.** Tudo sai da especificação Sala Escura v1 (06/10/2026), que consolida a Plataforma de Branding (aureadesign, 2025), o Brand DNA da The VOID (set/2026), as Personas (set/2026) e o site oficial (consultado em 06/10/2026). O que depende da escola aparece como **[P n]** (lista no fim) ou `{{A_CONFIRMAR}}`. Colchetes como `[ANO]` e `[N]` nunca vão ao ar.

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

## Onde a skill roda (e o que muda em cada lugar)

**Claude Code** (`~/.claude/skills/branding-the-void`) e **Codex CLI** (`~/.codex/skills/branding-the-void`) (`git clone https://github.com/rafaelnasch/branding-the-void.git`): ambiente completo. Manual: https://rafaelnasch.github.io/branding-the-void/. **claude.ai** (navegador e celular; ZIP do Releases em Configurações, Capacidades, Skills): **o artefato é um arquivo só e não enxerga `assets/`, `tokens.css` nem os `.js`.**

**REGRA DO NAVEGADOR (claude.ai):** todo HTML gerado ali é **autocontido**.

1. **Logotipo:** copie, por código, o valor `uri` do bloco `<script type="application/json" id="lk-datauri">` do [`lockup.html`](lockup.html) (entre `lockup-datauri:inicio` e `lockup-datauri:fim`; grupo 03). São os dez logotipos oficiais (horizontal, vertical, Start, Master e Pro, em preto e branco) e o favicon. **Nunca digite, resuma ou reconstrua um data URI; nunca desenhe o logotipo em `<path>` nem em texto.**
2. **Selos:** sem data URI pronto. Converta `assets/brand/svg/selo-*.svg` por código, sem alterar um byte. Sem o arquivo, use o Rótulo de Produto em texto (`THE VOID START` em Crédito com fio de 1 px) e avise.
3. **Tokens e motores:** cole `tokens.css` num `<style>` e `vforms.js` e `vviz.js` num `<script>`.
4. **Fontes:** pelo link do Google Fonts. **A Alga nunca entra.**
5. **PDF:** entregue o HTML e mande imprimir pelo Chrome com "Gráficos de segundo plano" ligado.

**Para ENVIAR um HTML** (e-mail, WhatsApp, Drive): `python3 autocontido.py <arquivo.html>` grava em `dist/` com tudo embutido; os 12 HTML da marca já estão em `dist/`. Em e-mail, data URI não funciona: vale o PNG hospedado (`lockup.html`, grupo 09).

---

## Cores (TRAVADAS)

O sistema é escuro por natureza: **não existe modo claro ou escuro automático**. `body` sempre com fundo explícito (`var(--sala)`); a página clara é uma **exceção nomeada** (Modo Leitura), escolhida pela peça ou pelo aluno, nunca pelo tema do aparelho. Um nome por valor; "Breu" não é token.

**Neutros: a sala e a luz**

| Token e nome | HEX | Papel |
|---|---|---|
| `--nanquim` Nanquim | `#000000` | Preto dos SVG oficiais e base do selo Pro; barras de vídeo. **Nunca campo de página** |
| `--sala` Sala | `#181818` | **O campo da marca** (site, LP, post, story, VSL, membros, cabeçalho e rodapé de e-mail); texto no Modo Leitura |
| `--bastidor` Bastidor | `#212121` | Cartão e painel sobre Sala; faixa alternada; Barra de Turma |
| `--coxia` Coxia | `#2B2B2B` | Cartão ativo, campo de formulário escuro, disco do selo Pro |
| `--fio` Fio | `#363636` | Só linha divisória no escuro |
| `--chumbo` Chumbo | `#474747` | Faixa inferior do selo Pro; texto forte no claro |
| `--penumbra` Penumbra | `#5F5F5C` | Legenda no Modo Leitura |
| `--fumaca` Fumaça | `#898989` | Texto auxiliar de 14 px ou mais e borda de campo no escuro; linha no claro |
| `--po` Pó | `#B4B5B0` | Apoio no escuro: Crédito de Prova, legenda, microcopy do botão |
| `--cal` Cal | `#DCDDD8` | **Corpo longo no escuro**; botão pressionado |
| `--cinza-100` Cinza 100 | `#ECEDE7` | Zebra e cabeçalho de tabela no Modo Leitura |
| `--tela` Tela | `#F8F9F4` | **A luz:** título e botão no escuro; campo do Modo Leitura |
| `--branco` Branco | `#FFFFFF` | Só o logotipo branco oficial e as linhas dos selos |
| `--nevoa` Névoa | `#C9D0D8` | Acento frio do Pro e estado informativo no escuro |
| `--ardosia` Ardósia | `#3F4E4F` | Miolo do selo Pro; apoio e informação no claro. Nunca texto sobre Sala |

**Quentes: terracota e terras** (marrons do slide 27 amostrados por pixel até o arquivo de tokens do cliente [P 4])

| Token e nome | HEX | Papel |
|---|---|---|
| `--terracota` Terracota | `#B25A32` | Acento quente; base do selo Master; grafismo e título grande do Master |
| `--terracota-viva` Terracota Viva | `#C46039` | Faixa inferior do selo Master; alta luz do duotom Master; palavra grande do Master |
| `--terracota-funda` Terracota Funda | `#8C4529` | Faixa superior do selo Master; link e filete no Modo Leitura |
| `--terracota-luz` Terracota Luz | `#DE8C66` | **A única terracota de texto pequeno no escuro** |
| `--terracota-noite` Terracota Noite | `#4A2416` | Cartela opcional do Master |
| `--areia` Areia | `#DBC5A3` | Luz quente de texto no escuro (Start e institucional); palavra de destaque; **anel de foco** |
| `--campo-start` Campo Start | `#B5966B` | **Campo do Start** (texto Sala; logotipo branco, como no slide 31) |
| `--caramelo` Caramelo | `#AE8A64` | Grafismo do Start sobre Sala; destaque grande |
| `--ouro-velho` Ouro Velho | `#93693B` | Base do selo Start; grafismo e barra de progresso do Start |
| `--ouro-fundo` Ouro Fundo | `#734120` | Faixa superior do selo Start; texto do Start no Modo Leitura |
| `--campo-master` Campo Master | `#76432B` | **Campo do Master** (texto Tela; logotipo branco) |
| `--couro` Couro | `#6C4327` | Superfície quente secundária (cartão Start em documento) |
| `--cafe` Café | `#412919` | Sombra do duotom Start; cartela escura do Start |

Apoio de imagem (não é cor de interface): sombra do duotom Master `#21130C`.

**Estados, sempre com ícone Lucide e palavra:** Sucesso, Musgo Luz `#9DB79B` no escuro e Musgo `#3E6A4B` no claro, `circle-check`, "Validado" · Atenção, Areia `#DBC5A3` e Âmbar Fundo `#7A5418`, `triangle-alert`, "Atenção", "Falta um passo" · Erro, Ferrugem Luz `#EF8A80` e Ferrugem `#A8322C`, `circle-x`, "Não deu certo" mais o que fazer · Informação, Névoa `#C9D0D8` e Ardósia `#3F4E4F`, `info`, "Para saber". No Pro, informação nunca sem ícone e palavra. **Erro nunca é urgência.**

**Hierarquia de luz no escuro** (sólidas, servem em e-mail, PDF e vídeo): nível 100 Tela, 16,78 sobre Sala, título, botão, número de prova · 86 Cal, 13,00, corpo longo · 68 Pó, 8,61, apoio, legenda, Crédito de Prova · 55 Fumaça, 5,08, auxiliar de 14 px ou mais; abaixo disso não é texto. **Profundidade por tom, nunca por sombra:** Sala, Bastidor, Coxia.

### Orçamento de área

No conjunto de um mês (feed, site, LP, e-mails): Sala, Nanquim, Bastidor e Coxia **55%** · fotografia P&B tratada (conta como escuro) **22%** · Tela (texto claro e Modo Leitura) **12%** · Névoa, Fumaça, Pó, Ardósia, Chumbo e Fio **5%** · cor de produto (campos, selos, duotons) **5%** · Terracota e Areia como acento **1%**.

Numa peça isolada:

| Tipo de peça | Teto de cor |
|---|---|
| Institucional, aula experimental, Talks, Convenção | Terracota ou Areia até **5%** |
| Peça de Start ou Master | Cor do produto até **12%** |
| Peça do Pro | Névoa até **8%** (o Pro é monocromático) |
| **Exceção nomeada: Campo de Produto** (modelo R8) | Peça inteira no campo do produto; no máximo **uma tela a cada cinco** num carrossel e **uma peça a cada seis** no feed |

### Pares de contraste (calculados por script, WCAG 2, 06/10/2026)

Os HEX de cada nome estão nas tabelas acima. **Véu** é Sala com a opacidade indicada sobre o **pior pixel, branco puro `#FFFFFF`**: véu 75% `#525252`, véu 70% `#5D5D5D`, véu 62% `#707070`, véu 55% `#808080`, véu 48% `#909090`. **Regra de ouro: par fora desta lista não é usado** até ser calculado (`python3 tools/contraste.py`) e acrescentado ao manual (14.2 a 14.4). Logotipo e selos são isentos do critério de texto (por isso o logotipo branco sobre o Campo Start fica; o texto corrido ali é Sala).

**Liberados para qualquer texto** (4,5:1 ou mais; AAA a partir de 7; estados sempre com ícone e palavra): Tela / Nanquim 19,85 · Branco / Sala 17,76 (logotipo e linhas do selo) · Tela / Sala 16,78 (título, botão) · Sala / Tela 16,78 (corpo no Modo Leitura; botão no claro) · Tela / Bastidor 15,22 · Sala / Cinza 100 15,08 · Tela / Coxia 13,38 · Cal / Sala 13,00 (corpo longo no escuro) · Tela / Café 12,76 · Tela / Terracota Noite 12,76 · Cal / Bastidor 11,79 · Névoa / Sala 11,41 · Sala / Névoa 11,41 · Areia / Sala 10,59 · Sala / Areia 10,59 · Areia / Bastidor 9,61 · Chumbo / Tela 8,78 · Pó / Sala 8,61 (apoio, legenda, Crédito de Prova) · Ardósia / Tela 8,22 · Musgo Luz / Sala 8,19 · Tela / Couro 8,04 · Tela / Ouro Fundo 7,92 · Pó / Bastidor 7,80 · Tela / Campo Master 7,61 · Tela / véu 75% 7,39 (caixa de legenda de vídeo) · Ferrugem Luz / Sala 7,29 · Pó / Coxia 6,86 · Terracota Luz / Sala 6,81 · Terracota Funda / Tela 6,62 · Sala / Campo Start 6,38 · Âmbar Fundo / Tela 6,38 · Ferrugem / Tela 6,29 · Tela / véu 70% 6,22 (**véu padrão**) · Terracota Luz / Bastidor 6,17 · Penumbra / Tela 6,05 · Musgo / Tela 5,89 · Caramelo / Sala 5,60 · Fumaça / Sala 5,08 (só 14 px ou mais, decisão de marca) · Tela / véu 62% 4,68 (**mínimo sob qualquer texto abaixo de 24 px**) · Areia / véu 75% 4,66 (palavra de destaque na legenda).

**Liberados com condição:** Tela / Ouro Velho 4,59 (só 19 px em 700 ou 24 px ou mais) · Ouro Velho / Tela 4,59 (título ou rótulo em 600 ou mais, nunca corpo) · Tela / Terracota 4,51 (só 19 px em 700 ou 24 px ou mais) · Terracota / Tela 4,51 (título e numeral, nunca corpo) · Terracota Viva / Sala 4,29 (só texto grande e ícone) · Areia / véu 70% 3,93 (só palavra de destaque em título de 24 px ou mais) · Tela / véu 55% 3,73 (só título de 24 px ou mais) · Terracota / Sala 3,72 (só título de 24 px ou mais, numeral e grafismo) · Ouro Velho / Sala 3,66 (só grafismo e texto de 24 px ou mais) · Tela / véu 48% 3,02 (só título de 32 px ou mais, sobre região da foto já escura e com amostragem conferida).

**Proibidos como texto:** Fumaça / Tela 3,31 (só linha no claro) · Caramelo / Tela 3,00 (só campo) · Penumbra / Sala 2,77 (decoração) · Tela / Campo Start 2,63 (no Campo Start o texto é Sala) · Ardósia / Sala 2,04 (só campo e miolo do selo) · Chumbo / Sala 1,91 (só fio decorativo) · Fio / Sala 1,47 (só linha) · Coxia / Sala 1,25 (superfície, disco do selo Pro) · Nanquim / Sala 1,18 (a base do selo Pro some: disco Coxia) · Tela sobre véu 48% nunca em texto abaixo de 24 px.

### Regra por produto (`data-estacao`)

O tema troca com **um único atributo** no contêiner: `data-estacao="chamado|start|master|pro|voiders"`. "Estação" é palavra de código e **nunca aparece em copy pública**. O logotipo continua preto ou branco em todos: **a cor mora no selo, no campo, no grafismo e na seta do botão, nunca no logotipo.** No `tokens.css`, o atributo define `--estacao-destaque`, `--estacao-grafismo`, `--estacao-seta`, `--estacao-campo` e `--estacao-campo-texto`.

| Item | `chamado` | `start` | `master` | `pro` | `voiders` |
|---|---|---|---|---|---|
| Campo de produto | nenhum: Sala, Tela e grão | Campo Start `#B5966B`, texto Sala, logotipo branco | Campo Master `#76432B`, texto Tela, logotipo branco; cartela opcional Terracota Noite | Sala com faixa Ardósia ou Chumbo | nenhum |
| Destaque de texto no escuro | Areia | Areia | Terracota Luz (pequeno) ou Terracota Viva (24 px ou mais) | Névoa | Areia |
| Grafismo (Fio de Produto, órbita ativa, barra) | Tela a 32% | Ouro Velho (Caramelo sobre Coxia) | Terracota | Névoa | Tela a 32% |
| Seta do botão (sobre Tela) | Sala | Ouro Velho (4,59) | Terracota (4,51) | Ardósia (8,22) | Sala |
| Duotom | não há | Café `#412919` para Areia `#DBC5A3` | `#21130C` para Terracota Viva `#C46039` | Sala `#181818` para Névoa `#C9D0D8` | não há |
| Órbita | nenhuma (só a Esfera) | duas elipses horizontais empilhadas | duas elipses verticais lado a lado | duas elipses entrelaçadas a ±32° da vertical | três círculos concêntricos |
| Círculo ativo no Mapa da Trilha | nenhum (todos em contorno) | o menor | o médio | o maior | os concluídos pela pessoa |
| Palavra Sensível de assinatura | *o primeiro passo* | *o primeiro traço* | *a sua identidade* | *o seu plano* | *família* |

**A cor se conquista:** topo de funil e aula experimental são monocromáticos. A aula experimental **continua assinando com o logotipo `void-start`, como está no ar** (é a porta do Start); o selo Start aparece como "próxima etapa", sem campo de cor. Tirar a aula do logotipo Start é a pendência [P 14], não regra.

### Modo Leitura (exceção editorial ao "nunca fundo principal")

O Brand DNA diz que o off-white "nunca" é fundo principal. A exceção nomeada: a Tela vira a página onde a leitura é longa e racional [P 2]. **Vale** em corpo de artigo (abaixo de cabeçalho Sala), corpo de e-mail (entre cabeçalho e rodapé Sala), oferta e fatos da LP (**até 25% da altura e no máximo 2 seções seguidas**), PDF, contrato, certificado, impresso de aula e leitura nos membros por escolha do aluno. **Nunca** em hero, capa, post de topo, story, Reels, VSL (fora a tela de oferta), thumbnail, Campo de Produto, Assinatura de Produto, fundo de foto ou vídeo, ou mais de uma tela em cinco num carrossel.

**Paleta:** campo Tela · texto Sala (16,78) · apoio Ardósia (8,22) · legenda Penumbra (6,05) · link e filete Terracota Funda (6,62) · zebra Cinza 100 · linhas Fumaça · grão 4% · logotipo preto. Classe `.modo-leitura`; nunca segue o tema do aparelho. **Até [P 2]:** artigo e e-mail em Sala com corpo Cal.

### O que sai da paleta

Verde de botão e vermelho saturado de faixa de urgência; âmbar de capas de vídeo anteriores ao sistema (substituído por Areia); rosa, magenta e ciano da marca antiga; laranja, verde, lilás e gradiente do deck da agência; gradiente bege para cobre dos botões; verde do WhatsApp como cor de interface; logotipo em ocre ou cinza como assinatura; **qualquer gradiente de cor** (só existem gradientes de luz: Janela de Luz, Véu e Esfera); estados em rosa ou azul.

---

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

---

## A marca (TRAVADA)

**O logotipo é desenho, não texto: nunca redigite THE VOID.** Sempre os arquivos de `assets/brand/` (exportação da Plataforma de Branding, aureadesign, 2025; cópia intacta em `assets/referencia-original/`).

| Peça | Arquivos em `svg/` (`-preto` e `-branco`) | viewBox |
|---|---|---|
| Horizontal THE VOID® TATTOO | `void-horizontal-*.svg` | 3804 por 579 |
| Vertical THE / VOID® / TATTOO ACADEMY | `void-vertical-*.svg` | 1937 por 1057 |
| De produto | `void-start-*` (3620 por 579), `void-master-*` (3894 por 579), `void-pro-*` (3745 por 578) | |
| Selo completo e simples | `selo-completo-start\|master\|pro.svg`, `selo-simples-start\|master\|pro.svg` | 869 e 770 |
| Raster, favicon, redes | `png/alta/`, `png/web/`, `webp/`; `favicon/` (o O em Tela sobre Sala), `social/avatar-1080.png`, `social/og-1200x630.png` [P 12] | |

**Preto `#000000` e branco `#FFFFFF` são as versões oficiais.** As versões `svg/cor/*-grafite.svg` (`#181818`) e `*-offwhite.svg` (`#F8F9F4`) só trocam o preenchimento e ficam de uso **interno e técnico** (favicon, avatar, placa de e-mail) até a validação [P 11]. Medidas completas em `assets/brand/marca.json`.

### Área de proteção e mínimos (proposta GrowAI a validar [P 11])

| Item | Regra |
|---|---|
| Área de proteção do logotipo | **1 X** livre em todos os lados, medido do desenho. X = altura das maiúsculas do THE = 0,352 H (no horizontal, 194 unidades, cerca de um terço da altura) |
| Área de proteção do selo | 12,5% do diâmetro em volta do círculo |
| Horizontal e de produto | mínimo **24 px** de altura em tela (cerca de 158 px de largura); 6 mm no impresso; na peça de 1080 (vista a 390 px no celular), **66 u** de altura, cerca de 430 u de largura |
| Vertical | mínimo **80 px** de altura (cerca de 147 px de largura); 16 mm |
| Selo completo | mínimo **200 px** de diâmetro; 40 mm. Abaixo, selo simples |
| Selo simples | mínimo **96 px**; 20 mm. **Abaixo de 96 px não existe selo**: use o Rótulo de Produto em texto ou o favicon |
| Abaixo dos mínimos do logotipo | favicon (o O do VOID) |

### Fundos permitidos

| Logotipo | Pode ir sobre |
|---|---|
| **Branco oficial** | Sala, Nanquim, Bastidor, Coxia, Campo Start (como no slide 31), Campo Master, Terracota Noite, Café, foto com véu de 55% ou mais |
| **Preto oficial** | Tela, Branco, Cinza 100, Areia, Névoa |
| Nunca | Terracota, Ouro Velho, Caramelo (os dois oficiais ficam ambíguos), foto sem véu, textura que atravesse o desenho |

### Usos proibidos

Redigitar THE VOID; recolorir (ocre, cinza, terracota, gradiente); contorno (o "Letreiro em Contorno" está vetado), sombra, brilho, distorção, rotação; descritor digitado ("THE VOID® TALKS" à mão); selo no lugar do "O" sem arquivo aprovado [P 10]; logotipo antigo serifado (nem em pôster ao fundo); grafia errada de TATTOO; ® cortado; logotipo nítido duas vezes na peça (o Eco não conta).

### Arquitetura de marca

| Nível | Nome canônico | Assinatura e regra |
|---|---|---|
| Marca-mãe | **The VOID** (texto); **The VOID Tattoo Academy** (dados estruturados, Google, imprensa, rodapé, primeira menção); **a Void** (coloquial, só em texto corrido) | Horizontal TATTOO ou vertical TATTOO ACADEMY. Primeira menção: "The VOID Tattoo Academy, escola de tatuagem na Vila Madalena, em São Paulo" |
| Formações | **The VOID Start**, **The VOID Master**, **The VOID Pro**; no texto, "formação Start", "formação Master", "programa Pro" | Logotipo de produto + selo; "The VOID" na frente na primeira menção |
| Método | **Método ARTE** (Artista, Tatuador, Empreendedor) | Só texto, sigla explicada na primeira menção; nunca logotipo ou selo |
| Porta de entrada | **Aula experimental** ("aula aberta" como alternativa) | `void-start` + selo Start como próxima etapa, campo `chamado`; "gratuita" é informação, nunca argumento principal |
| Eventos | **The VOID Talks** (grafia única), **Convenção The VOID** | Co-assinatura; página de evento sem oferta de formação |
| Rituais | **Ritual do Traço**, **Primeira Pele**, **Workshop do Estilo**, **Formatura com Pele** | Nome em Título de Seção, frase do slide na voz em off, selo da formação; nunca logotipo próprio |
| Comunidade | **VOIDERS** (plural), **VOIDER** (pessoa), sempre em caixa alta | Co-assinatura, sem logotipo próprio |
| Materiais e descritores | Business Playbook, Kit Boas-Vindas, Kit Start; CAST, STUDIO | Não usar antes de [P 7] |

**Co-assinatura:** o descritor fundido ao logotipo só existe nos arquivos oficiais (TATTOO, TATTOO ACADEMY, START, MASTER, PRO). Outro nome entra assim: logotipo horizontal oficial, **fio vertical de 1 px** na cor do texto com a altura do VOID e afastamento de 1 X de cada lado, nome em Archivo 700 largura 112, caixa alta, altura das maiúsculas igual à do THE: `[THE VOID® TATTOO] | TALKS`. Pronta no `lockup.html`, grupo 06.

### Selos

- Completo a partir de 200 px; simples de 96 a 199 px. Posição: canto superior direito da peça, ou à direita do logotipo de produto a 1 X.
- Nunca: girar, recolorir, deformar, sombrear, animar, usar como "selo de garantia" ou "selo de qualidade", sobre rosto, em peça institucional sem produto.
- **Selo Pro sobre Sala:** o completo dispensa ajuda (o anel branco externo fica inteiro visível). O simples (base Nanquim, 1,18:1 contra a Sala) é assentado num **disco Coxia `#2B2B2B`** com folga de 4% do diâmetro, sem alterar o vetor. O contorno do disco tem que ser percebido a 50% de zoom.
- `VForms.render(el,'selo',{produto,tamanho})` aplica tudo isso sozinho.

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

## Grade, espaço, forma, movimento e ícones

**Grade:** site e LP no computador, 12 colunas, conteúdo até 1200 px, margem 64 px, medianiz 24 px, leitura em 680 px · tablet 8 colunas, 32 e 20 px · **celular 4 colunas, margem 16 px**, nada sai da tela entre 320 e 430 px, proibido `overflow-x:hidden` global · feed 1080 por 1350 e story ou Reels 1080 por 1920, 6 colunas, margem 72 u, medianiz 24 u · VSL e YouTube 1920 por 1080, 12 colunas, 120 px laterais e 96 px vertical, frase no terço esquerdo · e-mail 600 px, uma coluna, 24 px · deck 1440 por 900, 12 colunas, margem 96 px.

**Zonas da dobra:** **Vazio** (título que nomeia a crença), **Encontro** (o que é, onde é) e **Ação** (botão), em 640 px no celular. Ponto de interesse num cruzamento dos terços; texto no espaço negativo oposto ao olhar ou à mão.

**Espaço:** módulo 8, escala `4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128 · 192` (`--e-1` a `--e-11`). Entre seções de LP 128 e 96; hero e cartela 192 e 128; título para corpo 24; parágrafos 16; corpo para botão 32; botão para microcopy 12.

**Forma:** raio **0** em foto, vídeo, cartão, seção, campo, **botão**, tabela, modal, Barra de Turma, Rótulo de Produto; **50%** em avatar, selo, Esfera, ponto de marco e botão flutuante do WhatsApp; **999 px** só na Assinatura do Pro. Nenhuma sombra: elevação por tom. Foco 2 px Areia (no claro, Sala), afastado 3 px. Botão reto é decisão; o teste A/B 10 pode reabrir [P 9].

**Movimento:** "sempre em movimento, nunca com pressa" (Brand DNA); opacidade, foco e enquadramento, nada quica. `--t-corte` 0 ms (aba, estado) · `--t-micro` 120 ms (botão, link) · `--t-ui` 240 ms (acordeão, menu) · `--t-entrada` 480 ms (bloco com 16 px de deslocamento) · `--t-foco` 700 ms (desfoque de 8 px para 0) · `--t-revelar` 900 ms · `--t-anel` 1200 ms · `--t-abertura` 1200 ms · `--t-saida` 200 ms. Curvas: Cena `cubic-bezier(.2,0,0,1)` (micro, ui, entrada, revelar, abertura), Foco `cubic-bezier(.65,0,.35,1)` (foco, anel), Saída `cubic-bezier(.4,0,1,1)`. **Não anima:** logotipo (só opacidade), selos, grão no site, números, preço, Barra de Turma, botão (sem pulso), escala acima de 1,02, paralaxe acima de 8%, confete, brilho. Movimento reduzido, impressão e PDF: opacidade de 120 ms ou estado final.

**Ícones:** **Lucide** em contorno, **traço 1,5**, `stroke-linecap:square; stroke-linejoin:miter`, SVG inline (nunca CDN de ícone); 16, 20, **24**, 32 px (56 a 72 u na peça); cor do texto, cor de produto só a partir de 24 px; sempre com palavra. Mapa: turma `calendar-days` · local `map-pin` · traço `pen-line` · prática `hand` · biossegurança `shield-check` · professor `user-round` · comunidade `users-round` · marco `flag` · validado `circle-check` · pendente `circle-dashed` · seguir `arrow-right` (os demais no manual). **Clichês vedados:** caveira, rosa vermelha, adaga, chama, tinta respingando, sangue, neon, vidro fosco, gradiente colorido, troféu, medalha, "level up". **Emoji** nunca na arte, no site, na LP ou nos membros.

## Fotografia, vídeo e LUTs

Manual: seções 29 e 30. Imagem que não passa, não entra.

1. **Real e autorizada**, por escrito e **por finalidade** (orgânico, site, anúncio, depoimento com nome, membros). **Nada de banco de imagem nem imagem gerada apresentada como real.** Comece pelo **acervo** (abaixo); só se nenhuma foto servir, espaço rotulado **"foto real da escola, com autorização"** com a direção da foto.
2. **Uma luz**, lateral ou de cima, queda rápida para o preto (8:1 a 16:1 em retrato, 4:1 a 8:1 em processo); **preto denso em 30% a 50% do quadro**; pele entre 45% e 65% de luminância.
3. **As mãos são o personagem** (um plano de mão em ação por série); **40% de espaço negativo** oposto ao olhar; olhar do hero aponta para título e botão; corte nunca em articulação.
4. **P&B "Ritual"** padrão, **"Vazio"** em capa e topo de funil; cor só em três regimes (duotom do produto, preset **"Terra"** em depoimento e comunidade, P&B sobre Campo de Produto); **no máximo 1 imagem colorida em 4**.
5. **Biossegurança visível**: luva nitrílica, filme plástico, material de uso único, descarte.
6. **Proibido:** sangue em destaque, pele lesionada em close, nudez, menor de 18 anos em procedimento, dinheiro, carro, "vida de luxo", sorriso posado, antes e depois lado a lado em anúncio, tela com dado de aluno, logotipo de equipamento sem acordo, pôster com logotipo antigo, trabalho de terceiro como de aluno.
7. **Legível por máquina:** `the-void-[produto ou tema]-[o que aparece]-[contexto]-[aaaa-mm].webp`; `alt` em frase de até 125 caracteres sem "imagem de"; IPTC com criador, detentor ("The VOID Tattoo Academy") e legenda; sem GPS em foto de pessoas.

### Acervo fotográfico (`assets/foto/acervo/`)

Escola de arte que vende tatuagem: **toda peça tem foto real**. Uso autorizado pela The VOID em 10/2026 (Lucas Tengan, sócio). **Catálogo:** `catalogo.json` (por foto: `tema`, `regime`, `versao_principal`, `alt`, `onde_usar`, `alerta`, `foco`, `arquivos`); visão geral em `_folha-de-contato.webp`.

- **78 fotos reais** em 13 temas: `pele` (18), `retrato` (14), `concentracao` (10), `maos` + `maquina` (6), `aula`, `professor` (5 cada), `escola`, `evento` (4 cada), `comunidade`, `traco`, `materiais`, `marca` (3 cada). **27 mockups** do rebranding em `assets/aplicacoes/mockups/` (referência de aplicação, nunca foto da escola). **4 personas geradas por IA** em `assets/foto/personas/`: só com o rótulo "Ilustração: persona fictícia, não é aluno da The VOID", nunca em peça pública.
- **Arquivo:** `void_<tema>_<nn>_<variante>.webp`: `pb` (Ritual), `vazio`, `terra`, `original`, recortes `4x5`, `9x16`, `16x9`, `1x1` e `thumb` (640 px).
- **Regimes:** `pb-ritual` padrão (processo, aula, professor, marca) · `pb-vazio` capa, hero, topo de funil · `cor-terra` depoimento, comunidade, evento · `cor-arte` tatuagem colorida com a cor real. Use a `versao_principal`; no máximo 1 colorida em 4. Grão no layout, nunca no arquivo.
- **Escolher por tema:** método e prática = `maos`, `traco`, `materiais` · prova de resultado = `pele` · autoridade = `professor`, `retrato` P&B · pertencimento = `comunidade`, `evento`, `retrato` Terra · lugar = `escola`, `marca`. **Por canal:** hero de LP e capa = `vazio` 16x9 (celular 4x5) · feed e carrossel = 4x5 · story, Reels e capa de VSL vertical = 9x16 · VSL e YouTube = 16x9 · e-mail = 1200 px em `assets/aplicacoes/email-foto/` · avatar e grade = 1x1 · prévia e PDF = `thumb`.
- **Na página:** `srcset` com `thumb`, `width`/`height`, `loading="lazy"` fora da dobra, `alt` do catálogo; texto sobre foto só com véu e longe do rosto.
- **Alertas** (campo `alerta`): decalque vermelho = só P&B; placa de premiação = só comunidade e membros; boné de terceiro e trabalho em andamento = fora de anúncio pago.
- **Crédito:** "Foto: acervo The VOID" na legenda ou no pé (com contexto: "Foto: acervo The VOID · aula prática"); mockup = "Aplicação do rebranding, Plataforma de Branding, aureadesign, 2025"; persona = rótulo de ilustração. Nome de professor só depois de [P 13].

**Ritos, sempre o mesmo enquadramento** (consentimento antes do clique): Ritual do Traço de cima do mural, mão entrando, 35 mm · Primeira Pele em plano médio de três quartos com professor e biossegurança, 35 a 50 mm · Formatura com Pele em retrato ambiental com trabalho e certificado, 50 a 85 mm · Workshop do Estilo em detalhe do estêncil e plano de crítica, 90 a 105 mm macro e 35 mm. Sessão de um dia: manual 29.5 [P 22].

**LUTs** em `assets/foto/` (`void-ritual`, `void-vazio`, `void-terra`, `void-duotom-start`, `-master`, `-pro`, `.cube` de 33 pontos, entrada Rec.709 gama 2,4; presets `.xmp` de Ritual, Vazio e Terra). Curvas, pesos de luminância e grão por preset: `assets/foto/receitas.md`; regerar com `python3 tools/gerar_luts.py --testar`. **O grão nunca vai na LUT.**

**Vídeo:** cinema (24 quadros, 2,39 por 1) só em VSL, filme de marca e YouTube longo; Reels e TikTok em 9:16 cheio, abrindo no gancho, sem vinheta. Planos de 2 a 4 s nos primeiros 30 s, 4 a 8 s no miolo, **respiro** a cada 90 a 120 s. **Assinatura sonora:** zumbido da máquina gravado na escola, 0,8 s, e silêncio, no fecho. Som -14 LUFS, pico -1 dBTP, trilha 18 a 22 dB abaixo da voz. **Legenda sempre** (queimada no vertical, `.srt` revisado; exemplo em `assets/vsl/exemplo.srt`) e transcrição na página. **Lower third:** fio de 2 px no grafismo que cresce em 8 quadros, nome Archivo 600 largura 112 caixa alta 40 px, função na voz em off 34 px, 3 a 4 s, a 120 px da lateral e 140 px da base, **sem selo**.

## Voz

**A marca como pessoa:** um artista que virou professor; inspira sem intimidar, ensina sem condescendência, acolhe sem perder a firmeza (Brand DNA da The VOID, set/2026). Comportamento: ousada, profunda, intencional.

**Quatro atributos, sempre em dupla** (no feminino, concordando com "a marca"): **Corajosa**, não agressiva · **Inspiradora**, não idealizada · **Técnica**, não fria · **Próxima**, não invasiva.

**Cinco pilares** (toda peça ancora em ao menos um): Transformação · Autoridade com afeto · Comunidade · Realidade do mercado · Arte como liberdade.

**Narrativa da falsa convicção:** iniciante, "Eu não sou capaz de viver da minha arte"; avançado, "Preciso ser melhor tecnicamente antes de cobrar o que mereço". Três atos: **o vazio, o encontro, a metamorfose**. As regras R01 a R08 do Brand DNA valem como estão (manual 31.10).

### Território de palavras

- **Usar:** voz própria, estilo autoral, traço limpo, metodologia, precisão, processo criativo, fundamento, rigor, do zero ao primeiro cliente, agenda cheia (sem promessa), evolução real, resultado concreto, dar o salto, faça mesmo com medo; proprietárias: vazio, traço, metamorfose, VOIDERS, Primeira Pele, ritual, chamado, preencher o vazio.
- **Terminologia:** The VOID / a Void; aluno; **formação** (não "curso", exceto onde a natureza legal pede "curso livre"); metodologia; mercado de tatuagem; "você" no singular; "Nós, a Void".
- **Fora:** incrível, maravilhoso, simples assim, fácil, em poucos cliques, sonho realizado, empoderar, revolucionário, disruptivo, "jornada" sem contexto, "transformação de vida" sem dado; curso rápido, certificado fácil, tatuagem comercial, conteúdo gratuito (como argumento), influencer de tattoo, aula online gravada, preço baixo ou acessível; nível, XP, desbloquear, ranking, sequência; jargão técnico sem explicação ("magnum", "liner"); inglês em copy pública ("Learn More" e afins; os textos fixos dos slides, Ficha Técnica, Créditos Finais e Letreiro Corrido, ficam como estão, com BRAZIL); "Self Hero/Self Made" só como conceito interno.
- **Ortografia travada:** TATTOO; "a uma carreira" sem crase; zero travessão.

### Tom por canal

- **Instagram (Reels, feed):** direto, provocador, visual; inspira antes de vender; gancho na falsa convicção nos 2 s iniciais; legenda até 3 parágrafos curtos.
- **TikTok:** autêntico, bastidor e realidade do mercado; sem vinheta.
- **Blog, guia, SEO:** educativo e confiável; resposta direta primeiro; voz em off só na abertura e no fecho.
- **Landing page:** emocional na hero, racional nas provas; uma persona e uma crença por página.
- **VSL:** mentor que já passou por isso; roteiro de 9 blocos.
- **E-mail:** próximo, mentoria; "Oi, {nome}.", uma ideia, pessoa real assina.
- **WhatsApp:** conversa humana; uma ideia por mensagem; quem abre a conversa se apresenta pelo nome.
- **Anúncio pago:** objetivo e provocador; sem promessa de renda, sem antes e depois lado a lado, sem atributo pessoal presumido.
- **Área de membros:** mentor que acompanha; progresso contra si mesmo, nunca comparação.
- **Deck e proposta:** técnica com calor; uma ideia por slide.

### Frases de assinatura (todas das fontes)

Institucional: "PREENCHA O VAZIO" (Créditos Finais) · Start: "Sempre faça arte" (apoio, nunca segunda tagline) · Master: "Descubra sua identidade artística" · Pro: "Seja um estrategista da sua carreira profissional" ou "A arte é sua. O plano é nosso." (uma por campanha) · Aula experimental: "Tatuar não é desenhar. É uma técnica nova." · The VOID Talks: "Da sala pra cena. A Void conecta você com quem vive disso." · Convenção: "Convocação a todos os *Artistas do Brasil*" · VOIDERS: "Aqui não existem estranhos, apenas família que ainda não se conheceu." · Primeira Pele: "Você nunca esquece sua primeira pele. Aqui, ela é celebrada." · Ritual do Traço: "Todo mundo começa com um traço. Aqui, ele tem nome, coragem e história." · Formatura: "Você não sai apenas com um certificado. Sai com um novo capítulo na pele." **Hero da LP:** Start usa o da persona; Master e Pro, a frase do produto (a crença do Bruno vai na LP04); aula e Talks, a frase deles. Detalhe no `lp-template.html`.

**Tagline:** "A arte que preenche. A carreira que liberta." **só** em home, LP de produto em lançamento de turma, boas-vindas da matrícula (M5), Formatura com Pele, campanha institucional e capa do brand book; uma vez por peça; **nunca** em LP de aula, Reels de topo, anúncio de conversão, WhatsApp ou fecho de toda LP. Composição permitida (duas linhas de voz em off): "*A arte* QUE PREENCHE / *A carreira* QUE LIBERTA". Apoio sem crase: "Do primeiro traço a uma carreira de sucesso".

---

## Comunicação M1 a M8 (resumo)

Leitura do bowtie da casa (M1 lead, M2 `mql`, M3 `sql`/`opportunity`, M4 `proposal`, M5 `won`, M6 `activated`, M7 `value_realized`/`retained`, M8 `expanded`/`advocacy`). Cada etapa tem **uma** crença, uma função, um recurso, um componente, **um** CTA e uma métrica. Matriz completa, 44 modelos de mensagem filtráveis por etapa, persona e canal (`?etapa=m4&persona=camila&canal=whatsapp`) e Cartões de Conversa: [`comunicacao-m1-m8.html`](comunicacao-m1-m8.html). Cada modelo traz status: **Decidido** (está na especificação), **Proposta** (escrito pela GrowAI, aguarda aprovação da The VOID; nada a ver com a etapa M4) ou **Pendente** (depende de dado do cliente). Lógica: manual 32.

| Etapa | Crença dominante | Voz que sobe | Recurso e componente | CTA único | Métrica |
|---|---|---|---|---|---|
| M1 Lead | "Isso não é para mim." | Corajosa | Esfera + Palavra Sensível; Gancho do Vazio, Plano de Abertura | Responder "o que te trouxe até aqui?" (mensagens); "GARANTIR MINHA VAGA NA AULA" na LP da aula | retenção de 3 s, conversão da página |
| M2 Qualificação | "Escola de tatuagem é tudo igual." | Próxima | Crédito de Prova; Antes Era, Roteiro | "Agendar minha conversa" (ou visita) | qualificados sobre cadastrados |
| M3 Oportunidade | "Lá dentro vou ser só mais um." | Técnica | Mapa da Trilha; Cartão de Turma, visita | "Receber minha proposta de turma" | comparecimento |
| M4 Proposta | "É caro." "Vou pensar." | Técnica + Próxima | Barra de Turma + Modo Leitura; Ficha da Formação, proposta de uma página | "Garantir minha vaga na turma de [mês]" | tempo em decisão |
| M5 Ganho | "Será que escolhi certo?" | Próxima | Selo como Carimbo; boas-vindas, Cartão do Primeiro Dia | "Confirmar presença no primeiro dia" | matrícula sobre propostas |
| M6 Ativação | "Minhas mãos não vão obedecer." | Próxima + Corajosa | Esfera no estado vazio, Ritual do Traço; Hoje, Meu Traço | "Registrar meu primeiro traço" | ativação no prazo |
| M7 Valor | "Todo mundo evolui mais rápido que eu." | Técnica | Anel, Mapa; Minha Trilha, Prática com Feedback, Marco | "Enviar meu trabalho para feedback" | conclusão da turma |
| M8 Expansão | "Já aprendi o que precisava." | Inspiradora | Próximo círculo aceso; Talks, Formatura, indicação | um por mensagem: "Conhecer o Master" **ou** "Indicar alguém" (evento: "Confirmar presença") | ascensão em 12 meses, indicação consentida |

**Qual CTA vale:** a coluna CTA vale para mensagem, e-mail e conversa; na LP vale o rótulo do produto (Landing page, Rótulos), um só na página inteira, mesmo quando ela cobre várias etapas (Master, M2 a M4). Post, story e Reels de M1 não desenham botão: a última linha, em Crédito, diz o caminho (`AULA EXPERIMENTAL · LINK NO PERFIL`; no story, "Responda AULA").

**Ritos na régua:** Ritual do Traço e Primeira Pele em M6; Workshop do Estilo e Formatura com Pele em M7; Talks e ex-alunos mentores em M8. Ritos propostos (Pergunta do Vazio, Primeiro Toque, Convite ao Traço, Passagem de Trilha, padrinho de turma, Mural do Vazio) **não entram** antes de [P 6].

---

## Conformidade e regra de prova (TRAVADA)

Manual: seção 33. Mapa de regras do dia a dia; não substitui orientação jurídica.

### As doze regras de prova

1. Número só com prova arquivada, recorte dito (turma, período, base), data e fonte; marca de origem visível.
2. **Claims vetados até prova pública na Ficha de Fatos** (lista no quadro abaixo, marcado como exemplo proibido).
3. **Vetado sem validação de advogado** (não é dado pendente, é claim vetado): qualquer menção a reconhecimento oficial de ensino (lista no quadro abaixo) [P 20].
4. **Nenhuma promessa financeira com número ou prazo** em público (nome de produto, desafio ou evento nunca traz valor em dinheiro [P 7]).
5. **Urgência só real:** Barra de Turma ligada ao calendário; nada de "últimas vagas" sem número, contador que reinicia, "só hoje" recorrente.
6. Preço com valor total, parcelas e condições batendo com o checkout [P 15].
7. Depoimento real, autorizado, sem edição que mude o sentido; caso excepcional dito como tal; #publi em parceria ou bolsa.
8. Antes e depois de traço só em página interna e orgânico, com data e autorização; nunca lado a lado em anúncio pago.
9. Menores: nenhum menor como modelo ou em procedimento; segmentação 18+ em mídia paga.
10. Nunca presumir condição pessoal de quem lê (dívida, renda, saúde); faixas de renda das personas são dado interno.
11. **Concorrente nunca citado, nem por insinuação.** Material interno da agência (diagnóstico de mercado, análises internas, dado pessoal) **nunca** em público.
12. Página de destino com a mesma promessa do anúncio e rodapé com razão social e CNPJ [P 8].

<div data-exemplo="proibido" markdown="1">

**Quadro de exemplos proibidos (nunca em peça pública; só aqui, para reconhecer):**

- Superlativo sem prova pública (maior, melhor, número 1, "#1", líder, único). Número de alunos sem método de contagem publicado. Tempo de mercado ou ano de fundação ("[N] anos", "desde [ano]") até a confirmação [P 5]. Dado de mercado sem fonte publicada.
- Reconhecimento oficial de ensino sem validação de advogado: MEC, diploma, curso técnico, habilitação, credenciamento, certificação por instituição parceira.
- Promessa de valor cobrado ou faturamento com número e prazo: "o curso se paga em [N] meses", "cobrei R$ [valor] em [N] meses", "dobrar o valor", "cobrar [N] vezes mais", nome de produto ou desafio com valor em dinheiro.
- Rótulos de botão: "SAIBA MAIS", "CLIQUE AQUI", "COMPRE AGORA", "LEARN MORE", "Quero sentir a máquina na mão" (até o roteiro da aula ser confirmado [P 16]), "Quero meu diagnóstico técnico" no Master (diagnóstico é do Pro).
- Frase de curso livre, **pendente de advogado [P 20]**, só entra marcada como pendente: "A The VOID oferece formação livre em tatuagem. Ao concluir, você recebe o certificado de conclusão da escola. Curso livre não depende de autorização do MEC e não equivale a curso técnico ou superior."

</div>

### Frases-modelo (usar como estão; prontas no `lockup.html`, grupo 08)

| Uso | Frase |
|---|---|
| Resultado, longa | "Os resultados mostrados são de alunos reais e não são garantia. O seu resultado depende da sua dedicação, da prática fora da aula e do seu mercado local." |
| Resultado, curta (**Aviso de Conformidade** da LP) | "Resultados individuais variam conforme prática e dedicação." |
| Vagas | "Turma de [mês/ano]: [N] vagas no total. Restam [N] em [data]." |
| Prazo | "Condição válida até [dia/mês], às [hora]. Depois disso, o valor volta para R$ [valor]." |
| Arrependimento | "Matrícula feita pela internet, telefone ou WhatsApp pode ser cancelada em até 7 dias a partir da contratação, com devolução integral do valor pago, conforme o artigo 49 do Código de Defesa do Consumidor." |
| Depoimento | "Depoimento real de [nome], aluno da formação [Start/Master/Pro], turma [mês/ano], usado com autorização." |
| Modelos | "Procuramos modelos maiores de 18 anos. Documento com foto obrigatório no dia. A sessão é feita por aluno sob supervisão de instrutor, com protocolo de biossegurança." (supervisão só se for verdade) |
| Biossegurança | "Na formação você aprende o protocolo de biossegurança. Para atender clientes no seu próprio espaço, você precisa da licença da vigilância sanitária da sua cidade." |
| Parceria | "#publi · Parceria paga com a The VOID." |
| Concurso cultural | "Concurso exclusivamente cultural, sem sorteio, sem compra e sem custo de participação. Vencedores escolhidos por júri com os critérios do regulamento." |
| Formulário | "Usamos seus dados para falar com você sobre a formação. Você pode sair quando quiser. Leia a Política de Privacidade." |
| Microcopy do botão (só enquanto o compromisso existir) | "Resposta de uma pessoa do time em até 2h, sem ligação invasiva." |

O que está entre colchetes é preenchido com dado real antes de publicar; sem o dado, a frase não vai ao ar.

---

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

---

## Componentes canônicos por canal

Os nomes são a interface do sistema: **nunca renomeie**. Cada canal tem um arquivo modelo que já cumpre as leis; parta dele.

### Utilitários do `tokens.css`

`.titulo-filme` (com `data-largura="92"` ou `"85"`) · `.titulo-secao` · `.fala` · `.credito` · `.numeral-prova` · `.off` (voz em off) · `.botao` (Letreiro Aceso) · `.grao` · `.janela-luz` · `.veu-esquerda` · `.veu-base` · `.campo-produto` · `.fio-produto` · `.modo-leitura` · `[data-estacao]`. Variáveis: cores, `--font-*`, `--e-1` a `--e-11`, `--t-*`, `--estacao-*`.

### Motores

| Motor | Chamada | O que guarda |
|---|---|---|
| `vforms.js` | `data-vforms`, `VForms.render`, `VForms.svg`, `VForms.montar(raiz)`, `VForms.redesenhar()` | `grao`, `esfera`, `eco`, `janela`, `veu`, `cinemascope`, `corte-logo`, `orbita`, `mapa-trilha`, `marcador-estacao`, `marcador-capitulo`, `anel`, `selo`, `logotipo`, `area-protecao`, `rodape`; lê `data-estacao` e `.modo-leitura`; recusa logotipo em texto e selo abaixo de 96 px. Opções: `logotipo {versao: horizontal\|vertical\|start\|master\|pro, cor: branco\|preto, altura}`, `selo {produto, tamanho, tipo: completo\|simples}`. Carregado por `src` do repositório, acha `assets/` sozinho; **colado num `<script>` ou fora do repositório, passe `base: "<caminho do repositório>/"`** (ou `VForms.config.base`), ou use os data URI do `lockup.html`: sem isso, logotipo e selo saem quebrados sem aviso |
| `vviz.js` | `data-vviz`, `VViz.render`, `VViz.svg`, `VViz.valida` | `barras`, `barras-horizontais`, `linha`, `coluna-empilhada`, `numeral`, `comparativo-traco`; sem `titulo`, `mede`, `periodo`, `base`, `fonte` e `origem` não desenha; `em-validacao` **não exporta** |

### Landing page · [`lp-template.html`](lp-template.html)

Fundo Sala; sem menu nem link de saída; **um CTA repetido de 3 a 5 vezes com o mesmo rótulo**; `data-estacao` no `<body>`; título, apoio e botão na primeira dobra do celular; maior elemento visível em menos de 2,5 s em 4G; imagens WebP ou AVIF com largura e altura. Densidade: aula 5 a 7 seções; Start 12 a 14; Master 10 a 12; Pro 9 a 11; Talks 5.

Cinco variantes no objeto `LP_VARIANTES` (`start`, `master`, `pro`, `aula`, `talks`), por `?variante=`; `?painel=1` audita leis, dobra e pendências; `?hoje=AAAA-MM-DD` simula a data; `?modo=publicacao` tira o incompleto. Copy só no objeto (`*palavra*` vira voz em off); JSON-LD e `dataLayer` (`ver_cta`, `clicar_cta`, `abrir_whatsapp`, `enviar_formulario`, `video_25/50/75/100`) saem dele.

**Os 21 componentes (tipo L8):** LP01 **Barra de Turma** (interface; 40 px, Bastidor, `calendar-days`, "TURMA DE [MÊS] · COMEÇA EM [DATA] · INSCRIÇÕES ATÉ [DATA]"; **só com `data_inicio` válida e futura, some sozinha quando vence**; nunca em M1 de topo, em vermelho ou com contador) · LP02 **Cabeçalho Mínimo** (sem menu) · LP03 **Plano de Abertura** (cena; foto P&B com véu 70%, 62% sob a linha de apoio, Título de Filme com Palavra Sensível, "Vila Madalena, São Paulo", Botão, Selo como Carimbo, Ficha Técnica sem ano) · LP04 **Cartela do Vazio** · LP05 **Virada** (a crença em Pó riscada, a verdade em Título de Filme) · LP06 **Rolo de Depoimentos** (cena; 3 ou 4 vídeos 9:16, Crédito de Prova, **Aviso de Conformidade** abaixo) · LP07 **Régua de Prova** (3 a 4 numerais validados; some sem nenhum) · LP08 **Método ARTE e Mapa da Trilha** · LP09 **Roteiro** (acordeão de módulos) · LP10 **Fotograma dos Rituais** · LP11 **Elenco** [P 13] · LP12 **Para Quem É** · LP13 **Locação** (NAP) · LP14 **Ficha da Formação** (documento em **Modo Leitura**: selo, o que inclui, carga, turma, valor total e parcelas [P 15], arrependimento, frase de curso livre pendente [P 20]) · LP15 **Perguntas** (= `FAQPage`) · LP16 **Créditos Finais** · LP17 **Barra Fixa** (só celular, 64 px; some na Ficha) · LP18 **Formulário Curto** (3 a 4 campos, consentimento desmarcado) · LP19 **Pós-Créditos** · LP20 **Sala de Projeção** (**transcrição no HTML**) · LP21 **Faixa de Manifesto**. Detalhe de cada um no `lp-template.html`. Ordem do Start: LP01 · 02 · 03 · 04 · 05 · 06 · 08 · 09 · 10 · 11 · 07 · 12 · 13 · 14 · 15 · 16 · 17; o Pro troca LP05 por **Autoavaliação** (cinco perguntas de sim ou não).

**Botão "Letreiro Aceso" (`.botao`, único estilo de CTA):** Tela com texto Sala, raio 0, Archivo Botão 16 px, altura 56 (52 no celular, largura total), seta em `--estacao-seta`; hover Branco, pressionado Cal, foco Areia; no Modo Leitura, Sala com texto Tela. Secundária: link ou botão vazado com borda Fumaça, **nunca dois botões cheios na dobra**. Carregando: o rótulo muda ("Abrindo o WhatsApp..."), sem spinner.

**Rótulos** (primeira pessoa, verbo, até 5 palavras): Start "QUERO CONVERSAR SOBRE MINHA TURMA" · Master "QUERO FALAR SOBRE O MASTER" · Pro "AGENDAR MEU DIAGNÓSTICO" · Aula "GARANTIR MINHA VAGA NA AULA" · Talks "CONFIRMAR PRESENÇA" (live "QUERO ASSISTIR") · M4 "GARANTIR MINHA VAGA NA TURMA" · Membros "REGISTRAR MEU PRIMEIRO TRAÇO", "ENVIAR MEU TRABALHO".

**Testes A/B:** a fila de dez está no manual 34.7; um por vez, hipótese e métrica antes; o 10 (botão reto ou pílula) é o [P 9].

### VSL · [`vsl-kit.html`](vsl-kit.html)

**9 blocos:** gancho (0 a 15 s), o vazio, história real autorizada, virada de crença, método (pilares e Mapa da Trilha), prova, oferta, objeções, CTA único falado e escrito. Start 12 a 18 min; Master 8 a 12; Pro 6 a 10; aula 60 a 120 s; cortes de 15, 30 e 60 s em 9:16. **Capa:** painel Sala à esquerda, logotipo branco de produto, 3 a 6 palavras com uma em Areia (ou destaque do produto), rosto ou mãos à direita com véu, **sem valor em reais**. **Cinco cartelas:** Vazio, Virada, Prova (Numeral com Crédito na mesma tela), Oferta (Modo Leitura, a única tela clara, um item por tela), Ação (rótulo dito e escrito, seta para o botão). **Legenda:** Tela sobre caixa Sala a 75% (7,39), uma palavra em Areia (4,66). **Fecho** de 1,5 a 2 s: Eco do VOID, logotipo branco, Créditos Finais, assinatura sonora. O kit desenha tudo no tamanho final e traz planos do acervo.

### Redes sociais · [`kit-social.html`](kit-social.html) (13 modelos)

Logotipo uma vez: horizontal branco no rodapé com **66 u de altura ou mais** (cerca de 430 u de largura; 300 u dá 16 px no celular, abaixo do mínimo), vertical no avatar; na aula experimental, `void-start` [P 14], e o selo Start só onde passar de 96 px na tela (cerca de 270 u), quase nunca no post; até 3 recursos; Campo de Produto uma peça a cada seis; nunca duas Cartelas seguidas.

R1 **Cartaz** (4:5, 9:16; M1: foto P&B, véu 70%, Título de Filme com Palavra Sensível, Créditos Finais) · R2 **Cartela** (4:5; M1) · R3 **Cinemascope** (4:5; M1 a M7) · R4 **Fotograma Triplo** (carrossel; M1, M2: primeira linha, mão guiando mão, traço firme) · R5 **Antes Era** (M2, nome autorizado, aviso curto) · R6 **Letreiro** (institucional, Corte do Logo) · R7 **Roteiro** (carrossel de até 10 cartões; M1, M2) · R8 **Campo de Produto** (M2 a M4; Palavra de Produto a 8%) · R9 **Convocação** (pré-M1, M8; data e local reais, Letreiro Corrido) · R10 **Bastidor** (story; M1 a M7; Marcador de Estação, legenda queimada) · R11 **Prova com Régua** (M2) · R12 **Turma Aberta** (M3, M4; Barra de Turma ampliada, "Responda TURMA") · R13 **Marco do Aluno** (M6 a M8; foto do rito com consentimento do aluno e do cliente tatuado). Fotos: seção Acervo fotográfico do `kit-social.html`.

O editor bloqueia a exportação PNG com: título acima de 6 palavras, travessão, claim vetado, prova sem origem ou em validação, terceiro sem link ou captura, turma vencida, cota de Campo de Produto estourada, contraste no pior pixel sob o texto (4,5:1 abaixo de 96 u, 3:1 a partir de 96 u), data de evento passada, R13 sem consentimento.

### Área de membros · [`membros-ui.html`](membros-ui.html)

**Diário de bordo do estúdio, não curso online.** Sala com Modo Leitura por escolha do aluno (nunca pelo tema do aparelho); `data-estacao` da formação ativa; ex-aluno sem trilha navega como `voiders`. Componentes: **Hoje** (um próximo passo), **Minha Trilha** (avança só com validação), **Anel**, **Cartão de Aula** (estado com ícone e palavra), **Meu Traço**, **Prática com Feedback** (um ponto forte, um ajuste), **Marcos**, **Comunidade VOIDERS**, **Agenda**, **Biblioteca**, **Suporte** (prazo e nome de quem responde), **Certificado de Passagem** (A4 em Modo Leitura, código `START · OUT/26 · SEMANA` [P 17], frase de curso livre pendente [P 20]) e **Perfil**. Estado vazio: Esfera e duas linhas (os nove no manual 36.1).

**Proibido:** ranking, sequência que pune falta, pontos, moedas, medalha de login ou de vídeo, "nível", "XP", "desbloquear", contagem regressiva, trabalho exposto sem consentimento, nota ou frequência visível a outros. Print de divulgação só com conta de demonstração.

### E-mail · [`email-template.html`](email-template.html)

`<meta name="color-scheme" content="light">` e `supported-color-schemes` light; fundos em tabela com `bgcolor`; 600 px, uma coluna, 24 px de margem. Cabeçalho Sala até 64 px com Janela de Luz (`assets/aplicacoes/placa-email-600.png`), logotipo branco 2x com 200 px; em marco, o selo (`selo-email-start|master|pro.png`). Marcador de Estação em texto. Corpo em Modo Leitura (Tela, texto Sala 17 px, entrelinha 1,6; até [P 2], Sala com Cal): "Oi, {nome}.", a ideia numa frase, até três parágrafos, uma prova no máximo. Botão reto de 48 px na cor oposta ao corpo: corpo Sala (padrão até [P 2]), botão Tela com texto Sala; corpo em Modo Leitura, botão Sala com texto Tela; rótulo em 15 px, pilha `'Archivo','Helvetica Neue',Arial,sans-serif`, e o link em texto abaixo. Assina pessoa real com cargo. Rodapé Sala com Créditos Finais em Pó, NAP, motivo, descadastro, privacidade. Assunto até 45 caracteres, pré-cabeçalho até 80. Tagline só em M5 e Formatura. Quatro mensagens prontas, com foto do acervo em `assets/aplicacoes/email-foto/`; assinaturas em `assets/aplicacoes/assinatura-email.html`.

### WhatsApp · [`comunicacao-m1-m8.html`](comunicacao-m1-m8.html) e `lockup.html`, grupo 09

Uma ideia por mensagem, "você" direto, zero travessão, sem caixa alta, negrito só em data, hora e endereço, pergunta ou link sozinho na última linha; quem abre a conversa se apresenta ("aqui é {consultor}, da The VOID") e assina "{consultor}, The VOID" (ou `{assinatura}`; professor, `{professor}`); resposta em conversa já aberta não repete. `{nome}` é sempre quem recebe. Aqui `*texto*` é negrito, nunca voz em off. **Emoji: nenhum em M1 a M4; no máximo um no fim em mensagem de marco (M6 a M8).** Cartões de Conversa: Turma, Primeiro Dia, Marco (com autorização), Convite Talks, Mapa da Trilha. Pré-preenchida com a origem. Número em `{{WHATSAPP_OFICIAL}}` até [P 8]. Botão flutuante: círculo de 56 px, Sala com fio de 1 px e glifo em Tela, nunca o verde do aplicativo.

### Artigo SEO, GEO e AEO · [`artigo-template.html`](artigo-template.html)

Cabeçalho de cinema, corpo de livro. Cabeçalho Sala até 40% da tela com Faixa Cinemascope de foto real, trilha de navegação, Marcador de Estação, **H1 em pergunta em Archivo Fala, caixa mista, 44/30 px** (exceção à L6), autor e "Atualizado em dd/mm/aaaa". **Resposta Direta** de 40 a 60 palavras com sujeito explícito ("A The VOID Tattoo Academy..."), Nunito Sans 20 px, filete Terracota Funda de 3 px, sem CTA. Corpo em Modo Leitura, coluna de 680 px, H2 em pergunta (Fala 28/23). Ficha de Fatos, tabela com Crédito de Prova, foto do acervo com crédito, FAQ visível igual ao `FAQPage`, fecho em Cartela com **um** CTA. Dados: `Article` (`author`, `about`, `isPartOf` para `/trilha/<produto>/`), `BreadcrumbList`, `FAQPage`. `?painel=1` confere. **Fatos:** a Resposta Direta só usa fato `validado` ou `decidido` de `assets/seo/fatos.md`; "a confirmar" só no corpo, com a situação escrita; **Resposta Direta com `{{A_CONFIRMAR}}` nunca vai ao ar**. **CTA:** `chamado` e `start` levam "GARANTIR MINHA VAGA NA AULA"; `master` e `pro`, o rótulo do produto. **Autor:** sem professor autorizado [P 13], `author` é a organização (`@id` da escola) e a linha de autor diz "The VOID Tattoo Academy".

### Deck · [`deck-template.html`](deck-template.html)

1440 por 900, 12 colunas, margem 96 px. Oito tipos: **Capa** (Sala, Eco do VOID, logotipo branco, Ficha Técnica), **Cartela**, **Documento** (Modo Leitura, no máximo 1 a cada 3 slides), **Prova**, **Mapa da Trilha**, **Foto cheia** com véu, **Comparativo**, **Fecho** (Créditos Finais). Uma ideia por slide; L8 na sequência. Teclas: setas, **P** notas, **C** conferência, **G** visão geral, **F** tela cheia. O seletor de formação troca `data-estacao`, selo e círculo aceso. PDF bloqueado com número em validação, `{{A_CONFIRMAR}}` ou [P n]. Proposta de uma página (M4): tipo Documento com o selo da formação.

### Trechos prontos · [`lockup.html`](lockup.html)

Nove grupos com botão Copiar: fontes e tokens, logotipo em arquivo e em data URI (03), avatar e favicon, selos e assinaturas de produto, co-assinatura, Créditos Finais e Ficha Técnica, Crédito de Prova e frases-modelo (08), NAP, bio, e-mail e WhatsApp (09). Estilo em linha com HEX dos tokens: serve em construtor de página e em e-mail.

---

## SEO, GEO e AEO: entidade, NAP, JSON-LD e llms.txt

Manual 36.2 e 36.3; modelos em `assets/seo/` (ver `LEIA-ME.md`).

**Entidade.** Nome legal e de dados estruturados **The VOID Tattoo Academy**; marca The VOID; coloquial a Void. `alternateName`: The VOID Tattoo, The Void Tattoo Academy, Void Tattoo Academy, The VOID Escola de Tatuagem. **Descrição de uma linha (literal em todo lugar):** "A The VOID Tattoo Academy é uma escola de tatuagem na Vila Madalena, em São Paulo, que forma tatuadores do primeiro traço à carreira profissional." Primeira menção sempre com "escola de tatuagem na Vila Madalena, em São Paulo" (há homônimos "Void"). Nenhum superlativo, contagem de alunos ou reconhecimento oficial de ensino nas descrições.

**Bloco NAP canônico (copiar, nunca redigitar):**

```
The VOID Tattoo Academy
Rua Jericó, 217 · Vila Madalena · São Paulo, SP · 05435-040
+55 11 92481-8712
```

"Rua", nunca "R."; um telefone principal, a confirmar com a The VOID [P 8]; igual em rodapé, contato, JSON-LD, Perfil da Empresa no Google, redes, membros e e-mails. Razão social e CNPJ: `{{A_CONFIRMAR}}` [P 8].

**Arquitetura do site:** `/` a escola · `/sobre/` · `/fatos/` (Ficha de Fatos com método de contagem e data) · `/trilha/` e `/trilha/start/`, `/trilha/master/`, `/trilha/pro/` (`Course`) · `/aula-experimental/` (`Event` recorrente) · `/talks/` · `/ritos/<rito>/` · `/professores/<nome>/` (`Person`) · `/voiders/` · `/guia/<pilar>/<pergunta>/` · `/perguntas-frequentes/` · `/contato/` · `/seja-modelo/` · `/llms.txt`. URLs atuais com 301 (`/the-void-start-curso-de-tatuagem/` para `/trilha/start/`); captura com `noindex`; nada de página por bairro; domínio canônico [P 18]. Cada artigo do guia tem um produto, que define Marcador, CTA e link interno.

**Dados estruturados** (`assets/seo/json-ld/`): `organizacao.json` (`EducationalOrganization` + `LocalBusiness`, em todas as páginas) · `curso-start.json`, `curso-master.json`, `curso-pro.json` (`Course` com `hasCourseInstance`) · `evento-aula.json`, `evento-talks.json` (`Event` só com data futura confirmada) · `faq.json` · `pessoa-professor.json` · `video.json` (com transcrição) · `artigo.json` · `breadcrumb.json`. **Campo com `{{A_CONFIRMAR}}` não vai ao ar: sai do JSON.** `assets/seo/llms.txt` (modelo na arquitetura `/trilha/`), `robots.txt` (robôs de busca de IA liberados; treino [P 19]) e `fatos.md` (status de cada fato).

---

## Dados e gráficos (`vviz.js`)

Gráfico só quando o dado existir e tiver Crédito de Prova. Série principal: Tela no escuro e Sala no claro; destaque: o grafismo do produto (Areia, Terracota ou Névoa); comparação e meta: tracejado em Fumaça; **no máximo 3 séries**. Barras retas (raio 0), sem sombra, sem 3D, sem pizza com mais de 3 fatias, eixo de barra começando em zero. Rótulo direto no lugar de legenda sempre que couber. Todo gráfico leva **título-afirmação** ("Sexta concentra as inscrições"), o que mede, período, base, fonte e marca de origem; com origem `em-validacao`, o motor desenha a moldura tracejada e recusa exportar. Manual: seção 28.

---

## Acessibilidade, celular e PDF

L3 inteira; `lang="pt-BR"`; títulos sem pular nível; texto real em HTML (nunca número só em imagem); `alt` descritivo e `alt=""` em decoração; `<th scope>`; rótulo visível e erro em texto. Maior elemento visível abaixo de 2,5 s em 4G; `woff2` locais; grão em ladrilho WebP; imagem com largura e altura; vídeo sem som automático.

**Celular:** legível e sem corte entre **320 e 430 px**, margem 16 px, grades empilham, tabela de até 3 colunas vira blocos, matriz maior rola no próprio quadro com indicação. **Proibido `overflow-x:hidden` global.**

**PDF:** `python3 exportar_pdf.py` (A4 para o manual, 1440 por 900 para o deck) ou Chrome com "Gráficos de segundo plano" ligado (senão a Sala some).

**Conferência:** `python3 tools/verificar.py <arquivo.html>` (HTML, um h1, links, travessão, TATTOO, claims fora de exemplo proibido, HEX só de tokens, `var()` em SVG, rolagem em 320, 390 e 1440, movimento reduzido; `--rapido`, `--sem-lighthouse`) e `python3 tools/contraste.py --check`. Validação estrutural não prova qualidade visual: **renderize e olhe** em 1440 e 390 px (320 em página) antes de entregar.

---

## Checklist de aprovação de peça

Persona e crença declaradas · **um** CTA · vocabulário no território · **zero travessão** · todo número com Crédito de Prova · nenhum claim vetado · aviso de resultado quando há prova · autorização de imagem cobrindo o canal · biossegurança visível · nenhum menor · preço e condições iguais ao checkout · vagas reais · arrependimento informado em venda online · contraste conferido na tabela (texto sobre foto, amostragem do pior pixel) · logotipo oficial com área de proteção · selo acima do mínimo · tagline só em contexto de peso · última linha que fica.


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

Entregue só a versão permitida e diga qual pendência travou o quê (manual 36.5).

| # | Pendência | Enquanto isso |
|---|---|---|
| [P 1] | Corpo: Nunito Sans, Nunito clássica ou Archivo | Nunito Sans 400 e 600 |
| [P 2] | Modo Leitura como exceção (artigo, e-mail, oferta, impresso) | Artigo e e-mail em Sala com corpo Cal |
| [P 3] | Licença da Alga para web, aplicativo e vídeo | Newsreader Italic 300 |
| [P 4] | Tokens e design system do cliente; marrons e campos do slide 31 | Tokens daqui, marcados como amostrados |
| [P 5] | Ano de fundação a confirmar com a The VOID | Sem "EST", "desde" ou tempo em anos |
| [P 6] | Brand moment 5, ritos propostos, mural do Ritual do Traço, frequência dos Talks | Só os quatro ritos; Talks sem "todo mês" |
| [P 7] | Kit Start, Kit Boas-Vindas, Business Playbook, Imersão Tatuagem com Liberdade, CAST, STUDIO, nome do desafio de prática | Não citar |
| [P 8] | Razão social, CNPJ, telefone principal, WhatsApp oficial por produto | `{{A_CONFIRMAR}}`, `{{WHATSAPP_OFICIAL}}`, NAP canônico |
| [P 9] | Botão reto contra pílula (teste A/B 10) | Botão reto |
| [P 10] | Arquivo do selo dentro do "O" | Não compor |
| [P 11] | Proteção, mínimos, versões grafite e offwhite | Valores propostos; grafite e offwhite só uso técnico |
| [P 12] | Favicon, avatar e imagem de compartilhamento | Propostas de `assets/brand/` |
| [P 13] | Professores, currículos, anos de prática, autorização de nome e imagem | Elenco com espaço rotulado |
| [P 14] | Aula experimental com logotipo Start ou institucional | `void-start`, campo `chamado` |
| [P 15] | Alunos formados, avaliações, preços, parcelas, carga, vagas, calendário, garantia | Só dado público com fonte e data; resto pendente |
| [P 16] | Roteiro e duração da aula experimental | Nenhum rótulo que prometa experiência |
| [P 17] | Código de turma e selos de formação no perfil | `START · OUT/26 · SEMANA` como modelo |
| [P 18] | Domínio canônico e migração para `/trilha/` | Caminhos relativos |
| [P 19] | Robôs de treino de IA | Busca liberada |
| [P 20] | Advogado: curso livre, reconhecimento oficial, imagem, cessão da arte, cancelamento, menores, licença sanitária, concursos | Curso livre só como pendente |
| [P 21] | Faixa etária das personas | Faixa fora das peças |
| [P 22] | Autorização por finalidade (anúncio pago) e sessão de um dia | Acervo de 10/2026; anúncio pago só com autorização confirmada |

---

## Mapa de arquivos

Lista no `README.md` e no `index.html`. Para enviar: `dist/` (HTML em arquivo único e PDF).

---

Marca e selos são da The VOID Tattoo Academy, desenho da aureadesign.co (Plataforma de Branding, 2025). Sistema organizado com a GrowAI. Sala Escura v1 · publicado em 06/10/2026; propostas em aprovação pela The VOID ([P 1] a [P 22]). Não substitui orientação jurídica.
