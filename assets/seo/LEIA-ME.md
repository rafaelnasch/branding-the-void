# assets/seo · kit de entidade da The VOID

Modelos de SEO, GEO e AEO do sistema Sala Escura (spec 12.7 e 13). Tudo aqui segue a arquitetura `/trilha/` (spec 13.3).

| Arquivo | Vai em |
|---|---|
| `json-ld/organizacao.json` | todas as páginas (EducationalOrganization + LocalBusiness + WebSite) |
| `json-ld/curso-start.json`, `curso-master.json`, `curso-pro.json` | `/trilha/start/`, `/trilha/master/`, `/trilha/pro/` |
| `json-ld/evento-aula.json` | `/aula-experimental/` (um evento por data real) |
| `json-ld/evento-talks.json` | `/talks/` (só depois de confirmar se é aberto ao público [P 6]) |
| `json-ld/pessoa-professor.json` | `/professores/<nome>/` (só com autorização [P 13]) |
| `json-ld/video.json` | página em que o vídeo é o conteúdo principal, com transcrição na página |
| `json-ld/artigo.json`, `breadcrumb.json`, `faq.json` | o artigo de exemplo (`artigo-template.html` usa os três num só `@graph`) |
| `llms.txt`, `robots.txt` | raiz do domínio |
| `fatos.md` | modelo da página `/fatos/` e ficha F01 a F21 |
| `og-artigo.html` e `og-preciso-saber-desenhar-1200x630.png` | imagem de compartilhamento do artigo (1200 por 630) |

**Regras.** `{{A_CONFIRMAR}}` marca campo não validado: o bloco não vai ao ar com ele. O domínio `https://thevoidtattoo.com.br` é provisório [P 18]. O NAP é o da spec 13.2, sem variação. Tudo o que está no JSON-LD precisa estar visível na página. Nada de `Review` ou `AggregateRating` sobre a própria escola. Turma encerrada sai do JSON-LD no mesmo dia em que sai da página.

**Decidir antes de subir o `robots.txt`.** O bloco dos robôs de treino de IA traz as duas opções (liberar ou bloquear) e a marca `{{A_CONFIRMAR}}` [P 19]. A escolha é da The VOID; subir o arquivo sem escolher equivale a liberar o treino.

**Conferir antes de publicar.** `python3 -m json.tool arquivo.json` (sintaxe) e o validador do schema.org (validator.schema.org) com a página publicada.
