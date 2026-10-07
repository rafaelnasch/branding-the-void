# branding-the-void

**A identidade visual da The VOID Tattoo Academy (escola de tatuagem na Vila Madalena, em São Paulo), empacotada como uma Skill (Claude e ChatGPT/Codex, no padrão aberto Agent Skills) e um kit de produção.** Sistema Sala Escura v1, outubro de 2026. Material publicado em 06/10/2026 no GitHub Pages pela GrowAI para a The VOID: versão 1, com propostas ainda em aprovação pela The VOID (pendências `[P 1]` a `[P 22]`).

Instale uma vez e peça o material em português. O Claude passa a produzir post, carrossel, story, Reels, anúncio, landing page, VSL, e-mail, WhatsApp, tela da área de membros, artigo do guia, deck, proposta, certificado, peça de evento e impresso **já no padrão da The VOID**: a Sala como campo, uma única luz por cena, o logotipo sempre em arquivo oficial, o letreiro em Archivo, a voz em off em itálico, a cor do produto só quando ela foi conquistada, todo número com crédito de prova e as regras de conformidade de escola livre. Sem você precisar explicar nada disso de novo.

> "No padrão da The VOID, faz um post 4:5 de topo de funil para a aula experimental, persona Gabriel."
> "Monta a LP do Master com o hero da persona Bruno e a Ficha da Formação em Modo Leitura."
> "Escreve a mensagem de WhatsApp de M4 para a Camila, que disse que vai pensar."

**Ver o brand book no navegador:** [rafaelnasch.github.io/branding-the-void](https://rafaelnasch.github.io/branding-the-void/) (abre em qualquer aparelho, sem instalar nada). Pedidos prontos para copiar: [guia de uso](https://rafaelnasch.github.io/branding-the-void/guia-de-uso.html). Manual completo: [brand book](https://rafaelnasch.github.io/branding-the-void/brand-book.html).

---

## O que vem na caixa

| Arquivo | O que é |
|---|---|
| `SKILL.md` | O essencial para o agente operar sem improvisar (295 linhas): a primeira pergunta (peça, etapa M1 a M8, persona, produto), o mapa de qual referência e qual kit abrir em cada passo, onde a skill roda, as oito leis, as cores principais e o tema por produto, a tipografia e o link de fontes, a marca (sempre em arquivo), a regra de prova e os claims vetados, o checklist e as armadilhas. A lista de arquivos é esta tabela. |
| `references/` | O detalhe, aberto só quando o passo pede (13 arquivos): `cor-e-contraste.md`, `tipografia.md`, `marca-e-selos.md`, `recursos-assinatura.md`, `grade-forma-movimento.md`, `fotografia-e-acervo.md`, `voz-e-m1-m8.md`, `conformidade.md`, `canais-e-medidas.md`, `kits-por-canal.md`, `seo-geo-aeo.md`, `dados-e-acessibilidade.md`, `pendencias.md`. Nada do sistema ficou de fora: todo valor é conferido contra o `tokens.json`. |
| `agents/openai.yaml` | Metadados de exibição para Codex e ChatGPT (nome "The VOID · Sala Escura", descrição curta, ícone e cor). O Claude ignora. |
| `index.html` | **Abra primeiro.** A entrada: manual, guia e modelos, uma linha cada. |
| `brand-book.html` | O manual vivo em 36 seções e 9 partes, com busca, seletor de produto (Institucional, Start, Master, Pro, VOIDERS), peças em tamanho real e impressão A4. |
| `guia-de-uso.html` | 36 pedidos prontos em 10 públicos (social media, tráfego, design, comercial e WhatsApp, atendimento, professores, vídeo, gráfica, desenvolvimento, agentes de IA), cada um com a seção do manual e o arquivo a abrir. |
| `lockup.html` | Trechos prontos para copiar em nove grupos: logotipo em arquivo e em data URI, avatar, favicon, selos, assinaturas de produto, co-assinatura, Créditos Finais, Crédito de Prova, frases-modelo, NAP, e-mail e WhatsApp. |
| `kit-social.html` | Editor dos 13 modelos de rede (R1 a R13) em tamanho real, com áreas seguras, amostragem do pior pixel sob o texto e exportação em PNG que só sai quando a peça passa nas regras. |
| `lp-template.html` | Landing page parametrizada em cinco variantes (Start, Master, Pro, aula experimental, Talks), com painel de auditoria (`?painel=1`), Barra de Turma que expira, JSON-LD e eventos de medição. |
| `vsl-kit.html` | Capa em três formatos, cinco cartelas, legenda queimada com `.srt`, lower third em sequência PNG, fecho, roteiro em 9 blocos e checklist. |
| `membros-ui.html` | UI kit da área de membros: Hoje, Minha Trilha, Anel de Preenchimento, Cartão de Aula, Meu Traço, Marcos, estados vazios, Sala e Modo Leitura, Certificado de Passagem em A4. |
| `comunicacao-m1-m8.html` | Matriz M1 a M8, 44 modelos de mensagem (WhatsApp, e-mail, DM, Reels, anúncio) filtráveis por etapa, persona e canal, e os Cartões de Conversa. |
| `email-template.html` | Quatro e-mails da régua em tabela, à prova de modo escuro, com Copiar e Baixar. |
| `artigo-template.html` | Artigo do guia com Resposta Direta, Ficha de Fatos, FAQ e dados estruturados. |
| `deck-template.html` | Apresentação 1440 por 900 com os oito tipos de slide, notas na tecla P e conferência na tecla C. |
| `tokens.css` · `tokens.json` | Os valores do sistema: cores, véus, tema por produto (`data-estacao`), fontes, registros, escalas, espaço, grade, raio, movimento, grão, marca, trilha. |
| `vforms.js` · `vviz.js` | Os motores: formas da casa (grão, Esfera, Eco, Mapa da Trilha, órbitas, selo, rodapé...) e gráficos com régua de prova, em SVG puro, sem dependências. |
| `autocontido.py` · `exportar_pdf.py` | Arquivo único para enviar (em `dist/`) e PDF. |
| `tools/` | Geradores e conferências (comandos abaixo). |
| `assets/` | Marca oficial, **acervo fotográfico** (`foto/acervo/`, 78 fotos reais da escola com catálogo), mockups do rebranding (`aplicacoes/mockups/`), texturas, LUTs, SEO, aplicações de e-mail, leia-me das fontes, exemplo de legenda e a pasta original da agência intacta. |
| `dist/` | **Para enviar a alguém.** Os 12 HTML em arquivo único (abrem sozinhos no e-mail, WhatsApp, Drive e celular) e os PDF do manual e da apresentação. |

## Instalar

O nome da pasta tem que ser exatamente `branding-the-void`, com o `SKILL.md` dentro. A mesma pasta serve ao Claude e ao ChatGPT/Codex: segue o padrão aberto [Agent Skills](https://agentskills.io/specification).

### Claude Code (terminal, VS Code, app de desktop)

```bash
git clone https://github.com/rafaelnasch/branding-the-void.git ~/.claude/skills/branding-the-void
```

Abra uma sessão nova e digite `/branding-the-void`, ou simplesmente peça "faz no padrão da The VOID". Para atualizar:

```bash
cd ~/.claude/skills/branding-the-void && git pull
```

### Codex (CLI, extensão de IDE e app de desktop)

```bash
git clone https://github.com/rafaelnasch/branding-the-void.git ~/.agents/skills/branding-the-void
```

O Codex lê `~/.agents/skills/`; versões anteriores leem `~/.codex/skills/` (mesmo comando, trocando a pasta). O `agents/openai.yaml` dá o nome e a descrição que aparecem na lista de skills.

### claude.ai (navegador e celular) e ChatGPT

1. Baixe o pacote pronto na página de **[Releases](https://github.com/rafaelnasch/branding-the-void/releases/latest)**: o arquivo `branding-the-void.zip`.
2. No claude.ai, vá em **Configurações, Capacidades, Skills** e envie o ZIP. No ChatGPT, envie o mesmo ZIP (ou a pasta extraída) onde o app oferecer Skills; o caminho do menu muda conforme a versão do app.

> Use o ZIP do Releases, **não** o "Code, Download ZIP" do GitHub: aquele vem com o nome da pasta trocado (`branding-the-void-main`), traz o repositório inteiro (mais de 100 MB com o acervo e o `dist/`) e a skill sobe com o nome errado.

O pacote leva `SKILL.md`, `references/`, `agents/openai.yaml`, tokens, motores, os nove kits HTML, a marca (SVG, PNG web, favicon, avatar), texturas web, LUTs e o kit de SEO. **As fotos do acervo não viajam no ZIP:** o `catalogo.json` e os kits do pacote apontam para as URLs públicas do Pages (`https://rafaelnasch.github.io/branding-the-void/assets/foto/acervo/...`); as miniaturas de 640 px vão junto. No navegador o material sai como arquivo único: o logotipo entra pelo data URI oficial do `lockup.html` (grupo 03), nunca digitado; os motores e o `tokens.css` entram dentro do próprio arquivo. Só o PDF muda: a skill entrega o HTML e você imprime pelo Chrome (instruções abaixo).

**Gerar o pacote** (para subir num Release novo): `python3 tools/empacotar_skill.py` grava `dist-skill/branding-the-void.zip` (fora do git) e falha se algum limite abaixo estourar.

### Limites atendidos (conferidos em 07/10/2026)

| Limite | Regra | Esta skill |
|---|---|---|
| `name` | minúsculas, números e hífen, até 64, igual ao nome da pasta | `branding-the-void` (17) |
| `description` | até 1.024 caracteres; caso de uso e gatilhos no começo | 891 caracteres; caso de uso e gatilhos nos primeiros 420 |
| Campos do frontmatter | só os da especificação | `name` e `description` |
| `SKILL.md` | menos de 500 linhas; detalhe em `references/`, um nível abaixo | 295 linhas (31 KB); 13 referências citadas no passo em que entram |
| Links relativos | todo link de `SKILL.md` e `references/` aponta para arquivo do pacote | 0 quebrados |
| ZIP | até 30 MB (meta 10 MB) | 5,88 MB |
| Descompactado | até 25 MB | 11,58 MB |
| Arquivos | até 400; nenhum acima de 10 MB | 207; o maior tem 0,93 MB (LUT `.cube`) |
| Estrutura | uma pasta `branding-the-void/` no topo, um só `SKILL.md` | sim |
| Validador oficial | `skills-ref validate` (agentskills/agentskills) | "Valid skill: branding-the-void" no pacote e no repositório |

Os limites de nome, descrição, campos e linhas são os da [especificação Agent Skills](https://agentskills.io/specification); os de tamanho do ZIP são as travas do `tools/empacotar_skill.py`.

## O primeiro teste

Abra uma conversa nova e peça:

> "No padrão da The VOID, faz um post 1080 por 1350 para a aula experimental, para quem acha que não tem talento."

Está funcionando se vier: campo quase preto (Sala `#181818`) com grão fino, título em caixa alta de até seis palavras com **uma** palavra em itálico, uma única luz no canto superior esquerdo, o botão como o ponto mais claro, o logotipo branco oficial uma vez no rodapé, nenhuma cor de produto (a aula é monocromática), nenhum número sem crédito e nenhum travessão. Se vier um post genérico, a skill não carregou: abra o Claude de novo e confira se a pasta se chama exatamente `branding-the-void` e tem o `SKILL.md` dentro.

## Usar

Diga, ou deixe o Claude perguntar numa frase só:

1. **que peça** (post, carrossel, story, Reels, anúncio, LP, VSL, e-mail, WhatsApp, tela de membros, artigo, deck, impresso);
2. **para qual etapa**, de M1 (lead) a M8 (expansão): ela decide a crença que a peça derruba e o **único** pedido;
3. **qual persona**: Gabriel (Start), Camila (Start, depois Master) ou Bruno (Master e Pro);
4. **qual produto**: institucional, Start, Master, Pro ou VOIDERS. No código isso é o atributo `data-estacao`; na copy, a palavra "estação" nunca aparece.

**Abrir no computador.** O manual, o guia e os modelos abrem com duplo clique. Os dois editores que exportam imagem (`kit-social.html` e `vsl-kit.html`) não exportam quando abertos direto do disco (`file://`): o navegador bloqueia a leitura do logotipo e do grão (testado em 06/10/2026). Para eles, rode `python3 -m http.server 8000` na raiz do repositório e abra `http://localhost:8000/`, ou use a versão do mesmo arquivo em `dist/`, que já traz tudo dentro. No endereço público funciona sem nada disso.

Preço, vaga, data, telefone, CNPJ, nome de professor e qualquer número sem prova saem como `{{A_CONFIRMAR}}` ou com a pendência `[P n]`: preencha com dado real antes de publicar. Para **PDF**: abra o HTML no Chrome, `Cmd+P`, **Salvar como PDF** e, em "Mais definições", ligue **Gráficos de segundo plano** (sem isso a Sala some); apresentação em Paisagem, margens Nenhuma. Ou rode `python3 exportar_pdf.py`.

## As oito leis

Quando duas brigam, vence a de número menor. No manual (seção 06) cada uma tem o teste de menos de um minuto e a peça certa ao lado da errada.

1. **Um vazio, uma ação.** Uma crença, um pedido; em fundo de funil, todo botão vai ao mesmo destino com o mesmo rótulo.
2. **Toda prova tem crédito.** O que mede, recorte, data, fonte e marca de origem em todo número.
3. **AA ou não sai.** Só pares de cor da tabela calculada; toque de 44 px; legenda em todo vídeo.
4. **O preto é a sala.** Campo escuro em pelo menos 60% de toda peça de marca.
5. **Uma luz por cena.** Um acento; o botão é o ponto mais claro da tela.
6. **Título é letreiro.** Archivo em caixa alta, até seis palavras; a voz em off em uma linha.
7. **Duas formas, nenhuma no meio.** Retângulo e círculo; a única pílula é a assinatura do Pro.
8. **Montagem com ritmo.** Cena, cartela e documento alternados; nunca três iguais seguidas.

## A marca e as fontes

O logotipo da The VOID **nunca** é redigitado, redesenhado, contornado ou recolorido: é sempre um arquivo de `assets/brand/` (exportação da Plataforma de Branding, aureadesign, 2025), em preto ou branco oficiais. A cor de cada formação mora no selo, no campo, no grafismo e na seta do botão. Abaixo de 24 px de altura o logotipo vira favicon; abaixo de 96 px o selo vira o Rótulo de Produto em texto. As medidas propostas aguardam validação com a escola e a agência.

Títulos em **Archivo** (variável, peso e largura), voz em off em **Newsreader Italic 300** (a **Alga**, comercial, entra só onde houver licença e nunca neste repositório) e texto em **Nunito Sans** (provisória). As três livres vêm de um único link do Google Fonts, que está no `SKILL.md` e no `lockup.html`.

## Acervo fotográfico

A The VOID é uma escola de arte que vende tatuagem: toda peça leva foto real da escola. O acervo está em `assets/foto/acervo/`, com **uso autorizado pela The VOID em 10/2026** (Lucas Tengan, sócio; confirmado pela GrowAI). Os arquivos estão sem metadados de câmera e sem GPS.

| O quê | Onde |
|---|---|
| 78 fotos reais em 13 temas: pele tatuada finalizada (18), retratos de alunos e professores (14), concentração (10), mãos e máquina (6), aula (5), professor ensinando (5), escola (4), eventos (4), comunidade (3), traço (3), materiais de treino (3), marca no ambiente (3) | `assets/foto/acervo/` |
| Catálogo: descrição, texto alternativo, tema, regime, versão principal, onde usar, alerta, ponto de foco e origem de cada foto | `assets/foto/acervo/catalogo.json` |
| Visão geral em uma imagem e guia curto | `_folha-de-contato.webp` e `LEIA-ME.md`, na mesma pasta |
| 27 mockups das aplicações do rebranding (referência, nunca foto da escola) | `assets/aplicacoes/mockups/` |
| 4 personas geradas por IA, só com o rótulo "Ilustração: persona fictícia, não é aluno da The VOID" | `assets/foto/personas/` |
| Fotos de e-mail em 1200 px e demonstração das LUTs | `assets/aplicacoes/email-foto/` e `assets/foto/demo/` |

**Nome e variantes.** `void_<tema>_<nn>_<variante>.webp`: `pb` (P&B Ritual), `vazio`, `terra`, `original`, recortes `4x5`, `9x16`, `16x9` e `1x1` com o foco no assunto, e `thumb` de 640 px.

**Regimes.** `pb-ritual` é o padrão (processo, aula, professor, marca); `pb-vazio` vai em capa, hero e topo de funil; `cor-terra` em depoimento, comunidade e evento; `cor-arte` só em tatuagem colorida, com a cor real do trabalho. Use a `versao_principal` do catálogo e no máximo uma imagem colorida a cada quatro. O grão é aplicado no layout, nunca no arquivo.

**Como escolher.** Por tema: método e prática pedem `maos`, `traco` e `materiais`; prova de resultado, `pele`; autoridade, `professor` e `retrato` em P&B; pertencimento, `comunidade`, `evento` e `retrato` em Terra; lugar, `escola` e `marca`. Por canal: hero de LP e capa em `vazio` 16x9 (4x5 no celular); feed e carrossel em 4x5; story, Reels e capa vertical em 9x16; VSL e YouTube em 16x9; e-mail com as fotos de 1200 px; avatar e grade em 1x1; prévias e PDF com a `thumb`. Na página, use `srcset` com a `thumb`, `width` e `height`, `loading="lazy"` fora da primeira dobra e o `alt` do catálogo.

**Cuidados.** Confira o campo `alerta` antes de usar: decalque vermelho sai só em P&B; placa de premiação só em comunidade e membros; boné com marca de terceiro e trabalho em andamento ficam fora de anúncio pago. Antes de impulsionar, confirme se a autorização de imagem cobre anúncio pago [P 22]. Nada de sangue em destaque, pele lesionada em close, pessoa que pareça menor de 18 anos, tela com dado de aluno ou cartão com telefone (o mockup do cartão de visita já vem com os dados borrados).

**Crédito.** Foto: "Foto: acervo The VOID", na legenda ou no pé, com contexto quando ajudar ("Foto: acervo The VOID · aula prática"). Mockup: "Aplicação do rebranding, Plataforma de Branding, aureadesign, 2025". Persona: o rótulo de ilustração. Nome de professor só depois da confirmação de grafia e autorização [P 13].

## Comandos

Todos rodam da raiz do repositório com `python3` (os que renderizam precisam de Playwright com Chromium; os de imagem, de Pillow). Os marcados com ✓ foram rodados em 06/10/2026 e passaram.

| Para | Comando |
|---|---|
| Regerar a marca em PNG, WebP, favicon, avatar e prévia de link | `python3 tools/build_assets.py` |
| Regerar o grão e a Esfera | `python3 tools/gerar_texturas.py` · conferir: `--verificar` ✓ (gera duas vezes e compara) |
| Regerar as seis LUTs `.cube` | `python3 tools/gerar_luts.py` · conferir: `--testar` ✓ |
| Regerar o data URI do `lockup.html` | `python3 tools/gerar_lockup_datauri.py` · conferir: `--verificar` ✓ (11 data URI byte a byte) |
| Regerar a placa e os selos do e-mail | `python3 tools/gerar_email_assets.py` · conferir: `--verificar` ✓ |
| Regerar a matriz M1 a M8 | `python3 tools/gerar_comunicacao_m1_m8.py` |
| Montar o manual a partir dos fragmentos | `python3 tools/montar_brand_book.py` ✓ (36 de 36 seções, 0 erros) |
| Conferir os pares de contraste | `python3 tools/contraste.py --check` ✓ (40 livres, 10 condicionados, 33 HEX iguais ao `tokens.json`) |
| Conferir a skill (`SKILL.md` + `references/`) | `python3 tools/conferir_skill.py` ✓ (346 verificações contra o `tokens.json` e os limites da especificação Agent Skills, em 07/10/2026) · contra a especificação Sala Escura: `--spec <caminho>` (59 pares de contraste) |
| Pacote da skill para claude.ai e ChatGPT | `python3 tools/empacotar_skill.py` → `dist-skill/branding-the-void.zip` ✓ (5,88 MB, 207 arquivos, limites atendidos) |
| Gate de aceite dos HTML | `python3 tools/verificar.py` ✓ (completo, com Lighthouse) · só o arquivo: `--rapido` ✓ · sem desempenho: `--sem-lighthouse` · com `dist/`: `--dist` ✓ |
| Arquivo único para enviar | `python3 autocontido.py` (todos) ou `python3 autocontido.py arquivo.html` → `dist/` ✓ (se passar de 16 MB, refaz com as fotos reduzidas; ver abaixo) |
| PDF | `python3 exportar_pdf.py` → `dist/brand-book.pdf` (A4) e `dist/apresentacao-the-void.pdf` (1440 por 900) ✓ (fotos em JPEG de até 1000 px e miniaturas onde houver) |

### Última verificação: 06/10/2026

| Conferência | Resultado |
|---|---|
| Montagem do manual (`tools/montar_brand_book.py`) | Aprovada: 36 de 36 seções, 348 ids, 209 links internos, 0 erros e 0 avisos |
| Gate de aceite (`tools/verificar.py`, itens 1 a 10) | Aprovado: 17 arquivos HTML, 0 falhas e 0 avisos; largura sem rolagem em 320, 390 e 1440 px; movimento reduzido conferido |
| Lighthouse de acessibilidade (item 10) | Manual 97; modelo de LP 100; modelo de artigo 100; área de membros 100 (mínimo exigido: 95) |
| Gate sobre `dist/` (`--dist --sem-lighthouse`) | Aprovado: 29 arquivos HTML, 0 falhas |
| Contraste (`tools/contraste.py --check`) | Aprovado: 40 pares livres com 4,5:1 ou mais, 10 condicionados com 3:1 ou mais, 33 HEX iguais ao `tokens.json` |
| Valores da skill (`tools/conferir_skill.py`) | 06/10: 197 verificações contra o `tokens.json`; 261 com `--spec` (59 de 59 pares de contraste). 07/10, depois da divisão em `SKILL.md` + `references/`: 346 verificações (valores e limites), 0 divergências; `--spec` não rodado de novo (especificação fora do repositório) |
| Arquivos únicos (`autocontido.py`) | 12 HTML em `dist/`, com imagens e fontes livres dentro, todos abaixo de 16 MB. O manual (15,5 MB) leva as fotos reduzidas a 1024 px no lado maior; os outros levam as fotos em resolução cheia. O kit social e o kit de VSL embutem as fotos de partida; o resto do acervo abre no site publicado |
| PDF (`exportar_pdf.py`) | Manual: 267 páginas A4, 27 MB, nenhuma em branco; apresentação: 10 páginas de 1440 por 900, 8 MB, nenhuma em branco (fotos em JPEG de até 1000 px) |
| Olhar humano (item 11) | Manual renderizado seção a seção em 1440 e 390 px, com amostra conferida a olho; cada modelo renderizado uma vez em 1440 px; nenhuma imagem quebrada |
| Peso do manual no site | Abertura: cerca de 2 MB em 29 pedidos; rolando até o fim: cerca de 12 MB em 1440 px e 11 MB em 390 px (fotos fora da primeira dobra com `loading="lazy"`) |

## Conformidade

Escola livre de tatuagem: nada de superlativo sem prova pública, nada de reconhecimento oficial de ensino sem advogado, nenhuma promessa de renda com número ou prazo, urgência só com turma e vagas reais, depoimento real e autorizado, nenhum menor em procedimento, biossegurança visível, preço igual ao do checkout e direito de arrependimento informado. Frases-modelo prontas no `lockup.html` (grupo 08) e em `references/conformidade.md`. Este material é um mapa de regras para o dia a dia e não substitui orientação jurídica.

## Pendências com a The VOID

São 22 (`[P 1]` a `[P 22]`): corpo de texto, aprovação do Modo Leitura, licença da Alga, tokens do cliente, ano de fundação, ritos, materiais, dados legais e WhatsApp, botão reto ou pílula, selo no "O", medidas do logotipo, favicon e avatar, professores, logotipo da aula experimental, números e dados de oferta, roteiro da aula, código de turma, domínio, robôs de IA, validações jurídicas, faixa etária das personas e acervo de fotografia. A lista com o que fazer enquanto cada uma não fecha está em `references/pendencias.md` e na seção 36.5 do manual. Até cada uma ser resolvida, a skill entrega só a versão permitida.

## Publicação

Material publicado em 06/10/2026 no GitHub Pages pela GrowAI para a The VOID, em [rafaelnasch.github.io/branding-the-void](https://rafaelnasch.github.io/branding-the-void/). É a versão 1, com propostas ainda em aprovação pela The VOID (pendências `[P 1]` a `[P 22]`): enquanto cada uma não fecha, o material entrega só a versão permitida.

**Nunca entram aqui:** dado de aluno, foto sem autorização, telefone pessoal, material interno da agência (diagnóstico e análises internas), arquivo da Alga, número não validado, dado de acesso ou caminho de pasta de quem mantém o repositório. Os padrões locais do gate de claims ficam em `tools/claims-locais.txt`, fora do git. Navegadores: Chrome, Edge ou Safari recentes.

### Verificação visual

- 06/10/2026: manual renderizado em 1440 e 390 px por seção; guia, entrada e modelos em 1440, 390 e 320 px; amostras do PDF A4 conferidas a olho.
- 06/10/2026 (fechamento): manual renderizado de novo em 1440 e 390 px por seção depois das últimas correções; entrada, guia, trechos, kit social, LP, VSL, área de membros, M1 a M8, e-mail, artigo e apresentação renderizados uma vez em 1440 px.
- 06/10/2026 (publicação): casos concretos do cliente trocados por regras genéricas; seções alteradas do manual (objeções, régua de prova, cores fora do sistema, claims vetados e pendências) renderizadas em 1440 e 390 px, sem rolagem lateral; imagem de compartilhamento regerada.
- 06/10/2026 (acervo fotográfico): manual com fotos reais renderizado por seção em 1440 e 390 px e cada modelo uma vez em 1440 px; leitura de texto nas 119 imagens do acervo, mockups, personas, e-mail e canal, sem telefone nem dado pessoal (o mockup do cartão de visita já vem borrado); a faixa de texto da arte original de uma foto de concentração foi cortada; capa do PDF com a foto atrás do título.

---

Marca, logotipo e selos são propriedade da **The VOID Tattoo Academy**; desenho da marca pela aureadesign.co (Plataforma de Branding, 2025). Os motores `vforms.js` e `vviz.js` foram escritos para este sistema. Sistema de identidade organizado com a GrowAI. Sala Escura v1 · outubro de 2026.
