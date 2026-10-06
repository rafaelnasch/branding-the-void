# The VOID · Ficha de Fatos

*Modelo da página `/fatos/` e fonte única dos dados que entram em JSON-LD, `llms.txt`, Ficha de Fatos do artigo, LP, bio e Perfil da Empresa no Google. Sistema Sala Escura, spec 13. Versão de 06/10/2026.*

**Regra.** Vai ao ar o fato com status **validado**, **decidido** ou **publicado pela escola**. O terceiro caso cobre só o que a própria The VOID já publica no site oficial: a peça repete a mesma redação, guarda a data da consulta e sai do ar no mesmo dia em que o site mudar. Os demais status ficam fora: o campo público mostra `{{A_CONFIRMAR}}` (ou some) e a pendência fica marcada como **[P n]**, com o número da lista de pendências da spec (seção 17). A validação formal com a escola segue pendente mesmo para o que já está publicado.

**Legenda de status**

| Status | O que quer dizer | Pode ir ao ar? |
|---|---|---|
| validado | Confirmado pela escola, com dono e data de revisão | Sim |
| decidido | Regra de marca fixada na spec (grafia, forma canônica) | Sim |
| publicado pela escola | Está no site oficial da The VOID com esta redação, na data da consulta; a escola ainda não validou formalmente | Sim, com a mesma redação e a data da consulta |
| encontrado, a confirmar | Aparece em material da escola, mas com versões diferentes entre fontes ou sem confirmação suficiente para publicar | Não, até validar |
| a confirmar | Não publicado em nenhuma fonte | Não |
| proibido até prova | Afirmação que só volta com prova pública e método de contagem (spec 11.1) | Não |
| decisão do cliente | Escolha de negócio, não de dado | Não, até decidir |

## Descrição oficial (usar literalmente)

> A The VOID Tattoo Academy é uma escola de tatuagem na Vila Madalena, em São Paulo, que forma tatuadores do primeiro traço à carreira profissional.

Status: decidido (spec 13.1). As versões de 50 e 150 palavras dependem do ano de fundação [P 5] e dos números de oferta [P 15].

## Bloco NAP canônico (copiar, nunca redigitar)

```
The VOID Tattoo Academy
Rua Jericó, 217 · Vila Madalena · São Paulo, SP · 05435-040
+55 11 92481-8712
```

Status: nome e endereço decididos (spec 13.2); telefone publicado pela escola (F06). "Rua", nunca "R.". A escolha do telefone principal entre os canais da escola segue em [P 8]: se mudar, muda aqui e em todos os pontos de uma vez.

## A ficha F01 a F21

| # | Fato | Valor no modelo | Fonte | Status | Pendência |
|---|---|---|---|---|---|
| F01 | Nome legal da entidade | The VOID Tattoo Academy | site oficial, consultado em 06/10/2026 | decidido (spec 5.5 e 13.1) | grafia confirmada pela spec |
| F02 | Razão social e CNPJ | `{{A_CONFIRMAR}}` | nenhuma fonte pública | a confirmar | [P 8] |
| F03 | Ano de fundação | `{{A_CONFIRMAR}}` | a confirmar com a escola | a confirmar | [P 5]; até lá, sem "EST", "desde" ou contagem de anos |
| F04 | Fundadores e sócios | `{{A_CONFIRMAR}}` | nomes e cargos publicados no site oficial | encontrado, a confirmar | [P 13]; uso de nome só com autorização |
| F05 | Endereço | Rua Jericó, 217 · Vila Madalena · São Paulo, SP · 05435-040 | site oficial (rodapé e dados estruturados) | decidido (spec 13.2) | confirmar complemento e se há outras unidades |
| F06 | Telefone e WhatsApp | +55 11 92481-8712 | site oficial e Perfil da Empresa no Google, consultados em 06/10/2026 | publicado pela escola | [P 8]; telefone principal entre os canais e WhatsApp oficial por produto |
| F07 | E-mail | thevoid@thevoidtattoo.com.br | site oficial (página inicial), consultado em 06/10/2026 | publicado pela escola | [P 8]; e-mail de atendimento por produto, se houver |
| F08 | Horário de atendimento | `{{A_CONFIRMAR}}` | não publicado | a confirmar | [P 8] |
| F09 | Alunos formados | `{{A_CONFIRMAR}}` | sem método de contagem publicado | proibido até prova | [P 15]; precisa de método, recorte e data |
| F10 | Superlativo de tamanho ("maior", "melhor", "número 1") | não usar | regra de conformidade (spec 11.1) | proibido até prova | spec 11.1; só volta com base de comparação e fonte independente |
| F11 | Menção a MEC ou instituição parceira | não usar | regra de conformidade (spec 11.1) | proibido até prova | [P 20]; exige parecer de advogado |
| F12 | Start: formato | presencial; 15 aulas presenciais, 45 horas no total, em 2 meses; 4 tatuagens em pele humana; não é preciso saber desenhar; festa de formatura | site oficial, página do Start, consultado em 06/10/2026 | publicado pela escola | [P 15]; calendário de turma; tamanho de turma |
| F13 | Start: conteúdo | 4 etapas: Fundamentos, Pele artificial, Pele humana e Mercado (portfólio, Instagram, precificação e primeiras vendas); 8 técnicas fundamentais (boldline, fineline, sculptline, sombra, rastelado, pontilhismo, preenchimento, transição de cor); aula de biossegurança | site oficial, página do Start, consultado em 06/10/2026 | publicado pela escola | [P 15]; a quarta etapa se chama "Mercado" em todas as peças |
| F14 | Master: formato | presencial; turmas de no máximo 8 alunos; formatos Padrão (56 horas), Plus (80 horas) e Black (96 horas, com o Pro incluído); sem preço publicado | site oficial, página do Master, consultado em 06/10/2026 | encontrado, a confirmar | [P 15]; calendário, tamanho de turma e formatos vigentes; nas peças, os valores saem como `{{A_CONFIRMAR: valor}}` até a escola confirmar |
| F15 | Pro: formato | online e ao vivo; calendário `{{A_CONFIRMAR}}` | site oficial, página do Pro, consultado em 06/10/2026 | publicado pela escola (formato) | [P 15]; lista de espera ou turma aberta |
| F16 | Rede de voluntários para tatuagem supervisionada | `{{A_CONFIRMAR}}` | sem método de contagem publicado | a confirmar | [P 15] |
| F17 | Professores | `{{A_CONFIRMAR}}` | nomes e anos de prática publicados no site oficial | encontrado, a confirmar | [P 13]; quadro atual, currículos e autorização |
| F18 | Idade mínima | 18 anos na aula experimental; formações `{{A_CONFIRMAR}}` | site oficial, página da aula | encontrado, a confirmar | [P 20]; aceitação de menores |
| F19 | Certificado | `{{A_CONFIRMAR}}` | site oficial e Plataforma de Branding, aureadesign, 2025 | a confirmar | [P 20]; frase de curso livre com advogado |
| F20 | Preços e parcelamento | Pro: R$ 2.997,00 à vista ou 12x de R$ 284,29 (total de R$ 3.411,48 no parcelado). Start e Master: `{{A_CONFIRMAR}}` | site oficial, página do Pro, consultado em 06/10/2026 | Pro: publicado pela escola. Start e Master: decisão do cliente | [P 15]; valor total, parcelas e condições sempre iguais ao checkout |
| F21 | Redes oficiais | Instagram e TikTok @thevoidtattooacademy; canal no YouTube | dados estruturados do site oficial | encontrado, a confirmar | perfis de professores, LinkedIn e Perfil da Empresa no Google a acrescentar |

## Como contamos nossos números

Seção da página `/fatos/` que só nasce quando o primeiro número for validado. Para cada número: o que mede, recorte (turma, período, base), data e fonte, e a marca de origem do Crédito de Prova (spec 6.16): **medido** (registro da escola, arquivado), **terceiro** (Google, imprensa, com link e data da captura) ou **mercado** (estudo externo com link). Número em validação não sai do arquivo de trabalho.

## O que nunca entra nesta ficha

Dado interno do cliente (receita, verba, contratos), telefone pessoal, concorrente nomeado, faixas de renda das personas e qualquer afirmação da lista 11.1 da spec sem prova pública.

## Revisão

Dono: `{{A_CONFIRMAR}}`. Revisão a cada 6 meses ou no mesmo dia em que um fato mudar. Toda mudança atualiza, juntas, esta ficha, `json-ld/`, `llms.txt`, a LP e o Perfil da Empresa no Google.
