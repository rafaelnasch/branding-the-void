# Dados, acessibilidade, celular e PDF

Gráficos com `vviz.js`, acessibilidade, regra de celular, PDF e os comandos de conferência. Manual: seção 28 e lei L3.

Parte da skill [`branding-the-void`](../SKILL.md). Os valores batem com [`tokens.json`](../tokens.json) (conferido por `tools/conferir_skill.py`).

## Dados e gráficos (`vviz.js`)

Gráfico só quando o dado existir e tiver Crédito de Prova. Série principal: Tela no escuro e Sala no claro; destaque: o grafismo do produto (Areia, Terracota ou Névoa); comparação e meta: tracejado em Fumaça; **no máximo 3 séries**. Barras retas (raio 0), sem sombra, sem 3D, sem pizza com mais de 3 fatias, eixo de barra começando em zero. Rótulo direto no lugar de legenda sempre que couber. Todo gráfico leva **título-afirmação** ("Sexta concentra as inscrições"), o que mede, período, base, fonte e marca de origem; com origem `em-validacao`, o motor desenha a moldura tracejada e recusa exportar. Manual: seção 28.

---

## Acessibilidade, celular e PDF

L3 inteira; `lang="pt-BR"`; títulos sem pular nível; texto real em HTML (nunca número só em imagem); `alt` descritivo e `alt=""` em decoração; `<th scope>`; rótulo visível e erro em texto. Maior elemento visível abaixo de 2,5 s em 4G; `woff2` locais; grão em ladrilho WebP; imagem com largura e altura; vídeo sem som automático.

**Celular:** legível e sem corte entre **320 e 430 px**, margem 16 px, grades empilham, tabela de até 3 colunas vira blocos, matriz maior rola no próprio quadro com indicação. **Proibido `overflow-x:hidden` global.**

**PDF:** `python3 exportar_pdf.py` (A4 para o manual, 1440 por 900 para o deck) ou Chrome com "Gráficos de segundo plano" ligado (senão a Sala some).

**Conferência:** `python3 tools/verificar.py <arquivo.html>` (HTML, um h1, links, travessão, TATTOO, claims fora de exemplo proibido, HEX só de tokens, `var()` em SVG, rolagem em 320, 390 e 1440, movimento reduzido; `--rapido`, `--sem-lighthouse`) e `python3 tools/contraste.py --check`. Validação estrutural não prova qualidade visual: **renderize e olhe** em 1440 e 390 px (320 em página) antes de entregar.
