# Fotografia, acervo, vídeo e LUTs

Os sete critérios de imagem, o acervo fotográfico real (catálogo, temas, regimes, recortes, alertas, crédito), ritos, LUTs e vídeo. Manual: seções 29 e 30.

Parte da skill [`branding-the-void`](../SKILL.md). Os valores batem com [`tokens.json`](../tokens.json) (conferido por `tools/conferir_skill.py`).

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
