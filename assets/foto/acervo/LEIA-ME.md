# Acervo fotográfico The VOID

Fotos reais da The VOID Tattoo Academy (escola, aulas, professores, alunos, trabalhos e eventos), tratadas no sistema Sala Escura. **Uso autorizado pela The VOID, 10/2026.** A lista completa, com descrição, texto alternativo, origem e onde usar cada foto, está em `catalogo.json`. A visão geral está em `_folha-de-contato.webp`.

## O que tem aqui

- **78 fotos reais**: pele tatuada finalizada (18), retratos de alunos e professores (14), concentração (10), mãos e máquina (6), aula (5), professor ensinando (5), espaço da escola (4), eventos (4), comunidade (3), traço (3), materiais de treino (3), marca no ambiente (3).
- **27 mockups** do rebranding em `../../aplicacoes/mockups/`.
- **4 ilustrações de persona** em `../personas/`. Foram geradas por IA. Use sempre com o rótulo "Ilustração: persona fictícia, não é aluno da The VOID" e nunca como foto da escola.

## Nome dos arquivos

`void_<tema>_<nn>_<variante>.webp`

| Variante | O que é |
|---|---|
| `original` | Cor original com tratamento leve, lado maior até 2400 px |
| `pb` | P&B pela LUT Ritual (`../void-ritual.cube`) |
| `vazio` | P&B dramático pela LUT Vazio, para capa e topo de funil |
| `terra` | Cor contida pela LUT Terra, para depoimento e comunidade |
| `4x5`, `9x16`, `16x9`, `1x1` | Recortes com o foco no assunto, a partir da versão principal do regime |
| `thumb` | Miniatura de 640 px |

Quando a foto original é menor que o formato, o recorte fica no tamanho nativo, e o `catalogo.json` informa isso. Quando nem isso é possível, o recorte não existe e aparece como `null`.

## Regimes

- **pb-ritual**: padrão da marca (processo, aula, professor, marca).
- **pb-vazio**: capa, hero e topo de funil.
- **cor-terra**: depoimento e comunidade.
- **cor-arte**: tatuagem colorida finalizada, com a cor real da arte.

A regra da especificação continua valendo: no máximo 1 imagem colorida a cada 4 em uma peça ou sequência. O grão não vai nos arquivos. Aplique no layout (Grão do Vazio) ou no editor, conforme `../receitas.md`.

## Cuidados

- Os alertas de cada foto estão no campo `alerta` do catálogo. Fotos com placa de premiação: só para comunidade e área de membros. Mockups com banco de imagem ou erro de grafia: só como referência.
- Antes de usar uma foto em anúncio pago, confira se a autorização de imagem cobre essa finalidade.
- Não coloque antes e depois lado a lado em anúncio pago.
- Os arquivos estão sem metadados de câmera e sem GPS.
