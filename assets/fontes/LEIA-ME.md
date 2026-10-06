# Fontes da The VOID

As três vozes do sistema Sala Escura carregam pelo link do Google Fonts abaixo. A única cópia de arquivo de fonte no repositório é `google/`: o cache das três famílias livres (Archivo, Newsreader e Nunito Sans, todas SIL Open Font License 1.1) que o `autocontido.py` usa para embutir as fontes nas versões de `dist/` e para trabalhar sem internet. O texto da licença e os avisos de copyright das três famílias estão em `google/OFL.txt`, como a licença exige. Nenhum arquivo comercial entra no repositório.

| Voz | Família | Licença | No repositório |
|---|---|---|---|
| Letreiro (títulos, botões, créditos, números) | **Archivo** variável, peso 100 a 900, largura 62 a 125, só romano | SIL Open Font License (livre) | Link do Google Fonts; cache em `google/` |
| Voz em off (a palavra que sente) | **Alga Italic** onde houver licença | **Paga** (Nova Type Foundry; disponível no Adobe Fonts com assinatura) | **Não entra.** O `.gitignore` bloqueia qualquer arquivo com "Alga" no nome |
| Voz em off, substituta livre | **Newsreader Italic 300**, eixo `opsz` 72 | SIL Open Font License (livre) | Link do Google Fonts; cache em `google/` |
| Texto (leitura longa) | **Nunito Sans** 400 e 600 (padrão provisório, pendência [P 1]) | SIL Open Font License (livre) | Link do Google Fonts; cache em `google/` |

## O link (único, igual em todo material)

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Newsreader:ital,opsz,wght@1,6..72,300&family=Nunito+Sans:wght@400;600&display=swap" rel="stylesheet">
```

```css
--font-letreiro: "Archivo", "Arial Narrow", Arial, sans-serif;
--font-off: "Alga", "Newsreader", Georgia, serif;   /* Alga só onde a licença estiver instalada */
--font-texto: "Nunito Sans", Arial, sans-serif;
```

A pilha já põe a Alga primeiro: quem tem a licença instalada na máquina vê a Alga; todo o resto vê a Newsreader. **Até a licença da Alga para web, aplicativo e vídeo ser confirmada (pendência [P 3]), todo material público sai em Newsreader Italic 300.**

## Onde cada caso cai

- **Site publicado:** servir os `woff2` localmente com subconjunto latino e `font-display: swap`; pré-carregar só o Archivo. Os `woff2` de `google/` servem (são os arquivos do próprio Google Fonts); leve o `google/OFL.txt` junto. O `.gitignore` só aceita `woff2` dentro de `google/`.
- **Canva e Google Slides:** Archivo, Newsreader (estilo Italic Light) e Nunito Sans pelo seletor de fontes da ferramenta.
- **E-mail:** a voz em off cai para Georgia itálico; nunca vira imagem.
- **Nenhuma outra serifada entra** (Playfair e similares saíram do sistema).

## Por que a Alga não está aqui

O repositório pode ser compartilhado, e a licença da Alga não permite redistribuir o arquivo. Quem trabalha com a Alga instala pela própria conta do Adobe Fonts.
