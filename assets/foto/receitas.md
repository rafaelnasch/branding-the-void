# Receitas de foto e vídeo da The VOID

Tratamento oficial do sistema Sala Escura para Lightroom (ou Camera Raw) e DaVinci Resolve. Os valores partem de um arquivo RAW (arquivo bruto da câmera) exposto corretamente. As LUTs desta pasta foram geradas por `tools/gerar_luts.py` com os números da especificação 8.3; regere com `python3 tools/gerar_luts.py --testar`.

Antes de tratar qualquer imagem: ela precisa ser **real e autorizada** (escola, aluno, professor ou evento da The VOID, com autorização de imagem por escrito e por finalidade). Banco de imagem e imagem gerada por IA não entram.

## Qual receita usar

| Receita | Arquivo | Onde usar | Nunca usar |
|---|---|---|---|
| **Ritual** (P&B padrão) | `void-ritual.cube` | Padrão de toda foto da marca: processo, aula, ritos, retrato | |
| **Vazio** (P&B dramático) | `void-vazio.cube` | Capa, topo de funil, hero | Depoimento |
| **Terra** (cor contida) | `void-terra.cube` | Depoimento, comunidade, bastidor | Capa de produto |
| **Duotom Start** | `void-duotom-start.cube` | Peça de produto Start: capa, VSL, separador de módulo, story | Depoimento, rosto de aluno, Primeira Pele |
| **Duotom Master** | `void-duotom-master.cube` | Peça de produto Master | Depoimento, rosto de aluno, Primeira Pele |
| **Duotom Pro** | `void-duotom-pro.cube` | Peça de produto Pro | Depoimento, rosto de aluno, Primeira Pele |

Regra de cor: **no máximo 1 imagem colorida em cada 4** de uma peça ou sequência. Colorida aqui é Terra ou duotom.

## Lightroom e Camera Raw

### VOID P&B 01 "Ritual" (padrão)

| Bloco | Ajuste |
|---|---|
| Perfil | Adobe Monochrome |
| Básico | Exposição de 0 a -0,3 · Contraste +25 · Realces -40 · Sombras +10 · Brancos +15 · Pretos -35 |
| Mistura P&B | Vermelho +10 · Laranja +15 (a pele clareia e a tatuagem ganha contraste) · Amarelo 0 · Verde -20 · Azul -25 · Roxo 0 |
| Curva de tons (pontos RGB, de 0 a 255) | 0>8 · 40>30 · 128>128 · 200>212 · 255>245 |
| Presença | Textura +15 · Claridade +12 · Neblina 0 (+5 só em ambiente) |
| Nitidez | Quantidade 50 · Raio 0,8 · Detalhe 30 · Máscara 60 |
| Ruído | Redução de luminância 10 (o grão vem depois) |
| Grão | Quantidade 28 · Tamanho 20 · Aspereza 55 |
| Vinheta pós-corte | -12 · ponto médio 40 · arredondamento 0 · difusão 80 |

### VOID P&B 02 "Vazio" (capa e topo de funil)

Parta do Ritual e troque: Contraste +40 · Pretos -55 · Grão 40 / 25 / 60 · Vinheta -25 · curva 0>0, 60>35, 128>120, 255>250.

### VOID COR 01 "Terra" (depoimento e comunidade)

| Bloco | Ajuste |
|---|---|
| Perfil | Adobe Color · temperatura 150 K acima da neutra |
| Básico | Contraste +15 · Realces -35 · Sombras +5 · Pretos -30 · Vibração -15 · Saturação -20 |
| HSL | Laranja: matiz -5, saturação -10, luminância +5 (pele) · Vermelho: saturação -15 · Verde: saturação -60, luminância -20 · Azul: saturação -70 · Roxo e magenta: saturação -80 |
| Gradação de cor | Sombras: matiz 25°, saturação 12 · Meios-tons: matiz 35°, saturação 6 · Altas luzes: matiz 45°, saturação 8 · Mistura 60 · Balanço -10 |
| Grão | 20 / 20 / 50 |

### Usar as LUTs no Lightroom

O Lightroom não abre `.cube` direto como preset. Dois caminhos:

1. **Perfil criativo:** no Photoshop, abra o Filtro Camera Raw, segure Alt (Option no Mac) e clique no botão de nova predefinição, que passa a criar um perfil; marque "Tabela de pesquisa de cores" e escolha o `.cube`. O perfil aparece no Lightroom depois de reiniciar.
2. **Photoshop:** camada de ajuste "Pesquisa de cores", carregue o `.cube` em "Arquivo 3DLUT".

Em qualquer caminho, **aplique o grão depois da LUT**, com os valores da receita.

## DaVinci Resolve

Captação: perfil log ou plano (S-Log3, C-Log, V-Log ou equivalente), 4K a 24 ou 25 quadros por segundo para depoimento e VSL; 60 ou 120 quadros por segundo para câmera lenta de mãos. Obturador no dobro do quadro. Filtro de densidade neutra para abrir o diafragma em luz do dia.

Copie os `.cube` para a pasta de LUTs do Resolve (Project Settings, Color Management, "Open LUT Folder") e clique em "Update Lists".

| Nó | O que faz |
|---|---|
| 1 | Transformação de espaço de cor do log para Rec.709 (gama 2,4) |
| 2 | Balanço de branco e exposição |
| 3 | LUT Ritual ou Terra (ou o duotom do produto), com 60 a 80% de intensidade (Key Output Gain) |
| 4 | Qualificador de pele: saturação -10, matiz levemente para o laranja |
| 5 | Vinheta suave |
| 6 | Grão de filme 35 mm a cerca de 30% de intensidade (no vídeo o grão troca a cada 2 quadros a 24 por segundo) |

Depoimento em vídeo usa Terra. Cena de processo dentro do mesmo vídeo pode ir para P&B como memória e voltar à cor no rosto.

## O que está dentro de cada LUT

Entrada **Rec.709 com gama 2,4**. Saída na mesma codificação. Grade de 33 pontos por eixo (35.937 linhas de dados). **O grão nunca vai dentro da LUT**: aplicado depois, para não congelar o padrão de ruído no vídeo.

| LUT | Conta |
|---|---|
| Ritual | Luminância = 0,36 R + 0,50 G + 0,14 B (o vermelho pesa mais para clarear a pele e escurecer fundo verde ou azul). Curva: 0,00>0,03 · 0,15>0,10 · 0,50>0,50 · 0,80>0,85 · 1,00>0,96 |
| Vazio | Mesma luminância. Curva: 0>0 · 0,235>0,137 · 0,50>0,47 · 1,00>0,98 |
| Terra | Saturação -20%; sombras +0,012 R e -0,010 B; altas luzes +0,008 R, +0,004 G e -0,012 B |
| Duotom Start | Preto da foto vira Café `#412919`, branco vira Areia `#DBC5A3` |
| Duotom Master | Preto vira `#21130C`, branco vira Terracota Viva `#C46039` |
| Duotom Pro | Preto vira Sala `#181818`, branco vira Névoa `#C9D0D8` |

As curvas passam exatamente pelos pontos acima (interpolação cúbica monótona, sem inverter tons). Nos duotons, a luminância linear da foto define a mistura entre a sombra e a alta luz, feita em RGB linear.

Na web, o mesmo duotom existe como filtro SVG (especificação 6.18). O filtro trabalha em sRGB e dá meios-tons um pouco mais claros que a LUT; para peça final de produto, prefira a foto já tratada com a LUT.

## Depois do tratamento

- **Nome do arquivo:** `the-void-[produto ou tema]-[o que aparece]-[contexto]-[aaaa-mm].webp`.
- **Texto alternativo:** frase de até 125 caracteres, sem "imagem de".
- **Metadados:** criador, detentor ("The VOID Tattoo Academy") e legenda; GPS removido de foto de pessoas.
- **Biossegurança visível** em todo procedimento: luva nitrílica, filme plástico, material de uso único, descarte.
