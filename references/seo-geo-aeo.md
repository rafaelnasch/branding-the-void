# SEO, GEO e AEO

Entidade, descrição de uma linha, NAP canônico, arquitetura do site, dados estruturados e llms.txt. Manual: 36.2 e 36.3.

Parte da skill [`branding-the-void`](../SKILL.md). Os valores batem com [`tokens.json`](../tokens.json) (conferido por `tools/conferir_skill.py`).

## SEO, GEO e AEO: entidade, NAP, JSON-LD e llms.txt

Manual 36.2 e 36.3; modelos em `assets/seo/` (ver `LEIA-ME.md`).

**Entidade.** Nome legal e de dados estruturados **The VOID Tattoo Academy**; marca The VOID; coloquial a Void. `alternateName`: The VOID Tattoo, The Void Tattoo Academy, Void Tattoo Academy, The VOID Escola de Tatuagem. **Descrição de uma linha (literal em todo lugar):** "A The VOID Tattoo Academy é uma escola de tatuagem na Vila Madalena, em São Paulo, que forma tatuadores do primeiro traço à carreira profissional." Primeira menção sempre com "escola de tatuagem na Vila Madalena, em São Paulo" (há homônimos "Void"). Nenhum superlativo, contagem de alunos ou reconhecimento oficial de ensino nas descrições.

**Bloco NAP canônico (copiar, nunca redigitar):**

```
The VOID Tattoo Academy
Rua Jericó, 217 · Vila Madalena · São Paulo, SP · 05435-040
+55 11 92481-8712
```

"Rua", nunca "R."; um telefone principal, a confirmar com a The VOID [P 8]; igual em rodapé, contato, JSON-LD, Perfil da Empresa no Google, redes, membros e e-mails. Razão social e CNPJ: `{{A_CONFIRMAR}}` [P 8].

**Arquitetura do site:** `/` a escola · `/sobre/` · `/fatos/` (Ficha de Fatos com método de contagem e data) · `/trilha/` e `/trilha/start/`, `/trilha/master/`, `/trilha/pro/` (`Course`) · `/aula-experimental/` (`Event` recorrente) · `/talks/` · `/ritos/<rito>/` · `/professores/<nome>/` (`Person`) · `/voiders/` · `/guia/<pilar>/<pergunta>/` · `/perguntas-frequentes/` · `/contato/` · `/seja-modelo/` · `/llms.txt`. URLs atuais com 301 (`/the-void-start-curso-de-tatuagem/` para `/trilha/start/`); captura com `noindex`; nada de página por bairro; domínio canônico [P 18]. Cada artigo do guia tem um produto, que define Marcador, CTA e link interno.

**Dados estruturados** (`assets/seo/json-ld/`): `organizacao.json` (`EducationalOrganization` + `LocalBusiness`, em todas as páginas) · `curso-start.json`, `curso-master.json`, `curso-pro.json` (`Course` com `hasCourseInstance`) · `evento-aula.json`, `evento-talks.json` (`Event` só com data futura confirmada) · `faq.json` · `pessoa-professor.json` · `video.json` (com transcrição) · `artigo.json` · `breadcrumb.json`. **Campo com `{{A_CONFIRMAR}}` não vai ao ar: sai do JSON.** `assets/seo/llms.txt` (modelo na arquitetura `/trilha/`), `robots.txt` (robôs de busca de IA liberados; treino [P 19]) e `fatos.md` (status de cada fato).
