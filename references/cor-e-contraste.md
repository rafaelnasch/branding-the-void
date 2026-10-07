# Cor e contraste

Paleta completa (28 cores de interface), estados, hierarquia de luz, orçamento de área, os pares de contraste calculados, a regra por produto (`data-estacao`), o Modo Leitura e o que sai da paleta. Manual: seções 13 a 16.

Parte da skill [`branding-the-void`](../SKILL.md). Os valores batem com [`tokens.json`](../tokens.json) (conferido por `tools/conferir_skill.py`).

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
