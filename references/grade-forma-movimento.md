# Grade, espaço, forma, movimento e ícones

Grade por formato, zonas da dobra, escala de espaço, raios, movimento (durações e curvas) e ícones. Manual: seções 26 e 27.

Parte da skill [`branding-the-void`](../SKILL.md). Os valores batem com [`tokens.json`](../tokens.json) (conferido por `tools/conferir_skill.py`).

## Grade, espaço, forma, movimento e ícones

**Grade:** site e LP no computador, 12 colunas, conteúdo até 1200 px, margem 64 px, medianiz 24 px, leitura em 680 px · tablet 8 colunas, 32 e 20 px · **celular 4 colunas, margem 16 px**, nada sai da tela entre 320 e 430 px, proibido `overflow-x:hidden` global · feed 1080 por 1350 e story ou Reels 1080 por 1920, 6 colunas, margem 72 u, medianiz 24 u · VSL e YouTube 1920 por 1080, 12 colunas, 120 px laterais e 96 px vertical, frase no terço esquerdo · e-mail 600 px, uma coluna, 24 px · deck 1440 por 900, 12 colunas, margem 96 px.

**Zonas da dobra:** **Vazio** (título que nomeia a crença), **Encontro** (o que é, onde é) e **Ação** (botão), em 640 px no celular. Ponto de interesse num cruzamento dos terços; texto no espaço negativo oposto ao olhar ou à mão.

**Espaço:** módulo 8, escala `4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128 · 192` (`--e-1` a `--e-11`). Entre seções de LP 128 e 96; hero e cartela 192 e 128; título para corpo 24; parágrafos 16; corpo para botão 32; botão para microcopy 12.

**Forma:** raio **0** em foto, vídeo, cartão, seção, campo, **botão**, tabela, modal, Barra de Turma, Rótulo de Produto; **50%** em avatar, selo, Esfera, ponto de marco e botão flutuante do WhatsApp; **999 px** só na Assinatura do Pro. Nenhuma sombra: elevação por tom. Foco 2 px Areia (no claro, Sala), afastado 3 px. Botão reto é decisão; o teste A/B 10 pode reabrir [P 9].

**Movimento:** "sempre em movimento, nunca com pressa" (Brand DNA); opacidade, foco e enquadramento, nada quica. `--t-corte` 0 ms (aba, estado) · `--t-micro` 120 ms (botão, link) · `--t-ui` 240 ms (acordeão, menu) · `--t-entrada` 480 ms (bloco com 16 px de deslocamento) · `--t-foco` 700 ms (desfoque de 8 px para 0) · `--t-revelar` 900 ms · `--t-anel` 1200 ms · `--t-abertura` 1200 ms · `--t-saida` 200 ms. Curvas: Cena `cubic-bezier(.2,0,0,1)` (micro, ui, entrada, revelar, abertura), Foco `cubic-bezier(.65,0,.35,1)` (foco, anel), Saída `cubic-bezier(.4,0,1,1)`. **Não anima:** logotipo (só opacidade), selos, grão no site, números, preço, Barra de Turma, botão (sem pulso), escala acima de 1,02, paralaxe acima de 8%, confete, brilho. Movimento reduzido, impressão e PDF: opacidade de 120 ms ou estado final.

**Ícones:** **Lucide** em contorno, **traço 1,5**, `stroke-linecap:square; stroke-linejoin:miter`, SVG inline (nunca CDN de ícone); 16, 20, **24**, 32 px (56 a 72 u na peça); cor do texto, cor de produto só a partir de 24 px; sempre com palavra. Mapa: turma `calendar-days` · local `map-pin` · traço `pen-line` · prática `hand` · biossegurança `shield-check` · professor `user-round` · comunidade `users-round` · marco `flag` · validado `circle-check` · pendente `circle-dashed` · seguir `arrow-right` (os demais no manual). **Clichês vedados:** caveira, rosa vermelha, adaga, chama, tinta respingando, sangue, neon, vidro fosco, gradiente colorido, troféu, medalha, "level up". **Emoji** nunca na arte, no site, na LP ou nos membros.
