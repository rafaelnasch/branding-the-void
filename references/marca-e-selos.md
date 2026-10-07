# Marca e selos

Arquivos oficiais do logotipo, área de proteção e mínimos, fundos permitidos, usos proibidos, arquitetura de marca, co-assinatura e selos. Manual: seções 08 a 12.

Parte da skill [`branding-the-void`](../SKILL.md). Os valores batem com [`tokens.json`](../tokens.json) (conferido por `tools/conferir_skill.py`).

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
