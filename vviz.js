/* =====================================================================
   VVIZ · motor de gráficos da The VOID · sistema Sala Escura v1
   SVG puro, zero dependências, ES2015, determinístico (sem Math.random e sem
   Date): a mesma entrada e a mesma largura geram sempre o mesmo desenho.
   Fonte normativa: especificação do sistema Sala Escura v1 (documento de trabalho,
   fora deste repositório), §14 (Dados e gráficos) e §6.16 (Crédito de Prova).

   A REGRA QUE O MOTOR GUARDA (L2: toda prova tem crédito)
     Nenhum gráfico é desenhado sem a régua de prova completa:
       titulo   título que AFIRMA a conclusão ("Sexta concentra as inscrições")
       mede     o que o número mede
       periodo  recorte de tempo ("ago/2026 a set/2026")
       base     recorte de base ("turmas Start de 2026")
       fonte    de onde o número veio ("registro da secretaria")
       origem   marca de origem, uma de quatro:
                medido        registro da escola, arquivado     (fio cheio)
                terceiro      declarado por terceiro            (fio tracejado; pede link e captura)
                mercado       estudo externo                    (fio pontilhado; pede link)
                em-validacao  número ainda não validado         (moldura tracejada; BLOQUEIA exportação)
     Faltou uma parte: o motor não desenha e mostra o aviso com o que falta.
     Com origem em-validacao: desenha só para o arquivo de trabalho, com moldura
     tracejada e o selo "DADO EM VALIDAÇÃO"; VViz.svg() lança erro (não exporta).

   COMO USAR
     1. Declarativo: <div data-vviz='{"tipo":"barras","titulo":"...","rotulos":[...],
                      "valores":[...],"mede":"...","periodo":"...","base":"...",
                      "fonte":"...","origem":"medido"}'></div>
     2. Chamada:     VViz.render(el, 'barras', dados)
     3. Exportação:  VViz.svg('barras', dados) devolve o SVG (texto, HEX por extenso,
                     xmlns, width e height, fundo do campo). VViz.svg(el) exporta um
                     gráfico já desenhado. Os dois lançam erro em dado não validado.
     4. Conferência: VViz.valida('barras', dados) devolve { faltas:[], avisos:[] }.

   TIPOS
     barras              { rotulos, valores | series, destaque, meta }
     barras-horizontais  { rotulos, valores | series, destaque }        (ranking)
     linha               { rotulos, valores | series, destaque, meta }
     coluna-empilhada    { rotulos, series (até 3), totais }
     numeral             { valor, vrotulo }                              Numeral de Prova
     comparativo-traco   { antes:{data, foto, alt, legenda}, depois:{...},
                           canal:'organico'|'pagina-interna', autorizacao:true }
     series: [{ nome, valores, papel:'principal'|'destaque'|'comparacao' }], no máximo 3.

   COR (spec §14 e §3.5)
     Série principal: Tela no escuro, Sala no Modo Leitura. Destaque: o grafismo do
     produto (Areia no chamado, Start e VOIDERS; Terracota no Master; Névoa no Pro).
     Comparação e meta: tracejado em Fumaça. O produto vem do data-estacao mais próximo
     (ou da opção estacao); o campo (Sala ou Leitura) vem de .modo-leitura (ou da opção
     campo:'sala'|'leitura'). Nenhuma cor sai fora de tokens.json; nada de var() em
     atributo SVG. Barras retas, sem sombra, sem 3D, sem pizza, eixo de barra em zero.

   OUTRAS OPÇÕES
     sobretitulo  rótulo em Crédito acima do título
     exemplo      true: marca "DADO DE EXEMPLO" no topo e na régua (material de teste)
     aviso        linha extra na régua (ex.: Aviso de Conformidade da spec §11.2)
     unidade      sufixo dos valores ('%' cola no número; outras com espaço)
     prefixo      prefixo dos valores ('R$ ')
     casas        casas decimais (padrão: automático)
     vrotulos     valores já escritos em pt-BR
     altura       altura da área do gráfico
     largura      largura do viewBox (padrão: a do contêiner, entre 260 e 1200)
     escala       multiplica letra e traço (peças de 1080: escala 1,86 leva 14 px a 26 u)
   ===================================================================== */
(function (raiz) {
  'use strict';

  var VERSAO = '1.0';
  var temDoc = typeof document !== 'undefined';

  /* ---------- tokens (iguais a tokens.json; nenhum HEX fora daqui) ---------- */
  var HEX = {
    nanquim: '#000000', sala: '#181818', bastidor: '#212121', coxia: '#2B2B2B', fio: '#363636',
    chumbo: '#474747', penumbra: '#5F5F5C', fumaca: '#898989', po: '#B4B5B0', cal: '#DCDDD8',
    cinza100: '#ECEDE7', tela: '#F8F9F4', nevoa: '#C9D0D8', ardosia: '#3F4E4F',
    terracota: '#B25A32', terracotaLuz: '#DE8C66', terracotaFunda: '#8C4529',
    areia: '#DBC5A3', ouroVelho: '#93693B', ouroFundo: '#734120',
    ambarFundo: '#7A5418', ferrugemLuz: '#EF8A80', ferrugem: '#A8322C'
  };

  /* campo escuro (Sala) e campo claro (Modo Leitura) */
  var CAMPOS = {
    sala: {
      nome: 'sala', fundo: HEX.sala, titulo: HEX.tela, texto: HEX.cal, apoio: HEX.po, aux: HEX.fumaca,
      grade: HEX.fio, base: HEX.fumaca, principal: HEX.tela, comparacao: HEX.fumaca, terceira: HEX.fumaca,
      placa: HEX.bastidor, placaFio: HEX.fio, atencao: HEX.areia
    },
    leitura: {
      nome: 'leitura', fundo: HEX.tela, titulo: HEX.sala, texto: HEX.sala, apoio: HEX.ardosia, aux: HEX.penumbra,
      grade: HEX.cinza100, base: HEX.fumaca, principal: HEX.sala, comparacao: HEX.fumaca, terceira: HEX.fumaca,
      placa: HEX.cinza100, placaFio: HEX.fumaca, atencao: HEX.ambarFundo
    }
  };

  /* destaque por produto: marca (grafismo) e texto, em cada campo */
  var ESTACOES = {
    chamado: { sala: { marca: HEX.areia, texto: HEX.areia, fio: HEX.tela, fioOp: 0.32 }, leitura: { marca: HEX.terracotaFunda, texto: HEX.terracotaFunda, fio: HEX.sala, fioOp: 0.32 } },
    start: { sala: { marca: HEX.areia, texto: HEX.areia, fio: HEX.ouroVelho, fioOp: 1 }, leitura: { marca: HEX.ouroVelho, texto: HEX.ouroFundo, fio: HEX.ouroVelho, fioOp: 1 } },
    master: { sala: { marca: HEX.terracota, texto: HEX.terracotaLuz, fio: HEX.terracota, fioOp: 1 }, leitura: { marca: HEX.terracota, texto: HEX.terracotaFunda, fio: HEX.terracota, fioOp: 1 } },
    pro: { sala: { marca: HEX.nevoa, texto: HEX.nevoa, fio: HEX.nevoa, fioOp: 1 }, leitura: { marca: HEX.ardosia, texto: HEX.ardosia, fio: HEX.ardosia, fioOp: 1 } },
    voiders: { sala: { marca: HEX.areia, texto: HEX.areia, fio: HEX.tela, fioOp: 0.32 }, leitura: { marca: HEX.terracotaFunda, texto: HEX.terracotaFunda, fio: HEX.sala, fioOp: 0.32 } }
  };

  /* marca de origem (spec §6.16): fio de 16 por 2 px antes da régua */
  var ORIGENS = {
    'medido': { rotulo: 'MEDIDO', dash: '', descricao: 'registro da escola, arquivado' },
    'terceiro': { rotulo: 'DECLARADO POR TERCEIRO', dash: '4 2', descricao: 'declarado por terceiro, com link e data da captura' },
    'mercado': { rotulo: 'MERCADO', dash: '2 2', descricao: 'estudo externo, com link' },
    'em-validacao': { rotulo: 'EM VALIDAÇÃO · NÃO PUBLICAR', dash: '4 2', descricao: 'dado em validação; bloqueia exportação e publicação' }
  };

  var TIPOS = {
    'barras': 'barras', 'barras-horizontais': 'barras-horizontais', 'barras-h': 'barras-horizontais', 'ranking': 'barras-horizontais',
    'linha': 'linha', 'coluna-empilhada': 'coluna-empilhada', 'empilhada': 'coluna-empilhada',
    'numeral': 'numeral', 'numeral-de-prova': 'numeral', 'numero': 'numeral',
    'comparativo-traco': 'comparativo-traco', 'comparativo': 'comparativo-traco'
  };
  var LISTA_TIPOS = ['barras', 'barras-horizontais', 'linha', 'coluna-empilhada', 'numeral', 'comparativo-traco'];
  var NOME_TIPO = {
    'barras': 'gráfico de barras', 'barras-horizontais': 'gráfico de barras horizontais', 'linha': 'gráfico de linha',
    'coluna-empilhada': 'gráfico de colunas empilhadas', 'numeral': 'Numeral de Prova', 'comparativo-traco': 'comparativo de traço, antes e depois'
  };

  /* ícones Lucide (copiados do pacote oficial, viewBox 24), traço 1,5 */
  var ICONES = {
    'triangle-alert': '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    'circle-dashed': '<path d="M10.1 2.182a10 10 0 0 1 3.8 0"/><path d="M13.9 21.818a10 10 0 0 1-3.8 0"/><path d="M17.609 3.721a10 10 0 0 1 2.69 2.7"/><path d="M2.182 13.9a10 10 0 0 1 0-3.8"/><path d="M20.279 17.609a10 10 0 0 1-2.7 2.69"/><path d="M21.818 10.1a10 10 0 0 1 0 3.8"/><path d="M3.721 6.391a10 10 0 0 1 2.7-2.69"/><path d="M6.391 20.279a10 10 0 0 1-2.69-2.7"/>',
    'images': '<path d="m22 11-1.296-1.296a2.4 2.4 0 0 0-3.408 0L11 16"/><path d="M4 8a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2"/><circle cx="13" cy="7" r="1"/><rect x="8" y="2" width="14" height="14" rx="2"/>',
    'lock': '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>'
  };
  function icone(nome, x, y, tam, cor) {
    var d = ICONES[nome]; if (!d) return '';
    var k = tam / 24;
    return '<g transform="translate(' + r2(x) + ' ' + r2(y) + ') scale(' + r3(k) + ')" fill="none" stroke="' + cor + '" stroke-width="' + r2(1.5 / k) + '" stroke-linecap="square" stroke-linejoin="miter" aria-hidden="true">' + d + '</g>';
  }
  function iconeHTML(nome, cor, tam) {
    return '<svg width="' + tam + '" height="' + tam + '" viewBox="0 0 24 24" fill="none" stroke="' + cor + '" stroke-width="1.5" stroke-linecap="square" stroke-linejoin="miter" aria-hidden="true" style="flex:none;margin-top:1px">' + ICONES[nome] + '</svg>';
  }

  /* ---------- utilidades ---------- */
  function r2(n) { return Math.round(n * 100) / 100; }
  function r3(n) { return Math.round(n * 1000) / 1000; }
  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  function vazio(v) { return v == null || String(v).trim() === ''; }
  function num(v) { return typeof v === 'number' && isFinite(v); }
  function hash(s) { var h = 5381; for (var i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) >>> 0; return h.toString(36); }
  function caixaAlta(s) { return String(s).toLocaleUpperCase('pt-BR'); }

  var FL = "Archivo,'Arial Narrow',Arial,sans-serif";
  var FT = "'Nunito Sans',Arial,sans-serif";
  /* registros da spec §4.2 usados no gráfico */
  var REG = {
    titulo: { f: FL, p: 700, w: 100, ls: -0.012 },                 /* Título de Seção */
    credito: { f: FL, p: 500, w: 125, ls: 0.18 },                  /* Crédito */
    numeral: { f: FL, p: 700, w: 75, ls: -0.01, num: true },       /* Numeral de Prova */
    valor: { f: FL, p: 600, w: 87, ls: 0, num: true },             /* rótulo de valor */
    eixo: { f: FL, p: 500, w: 100, ls: 0, num: true },             /* marcas do eixo */
    cat: { f: FL, p: 500, w: 100, ls: 0.01 },                      /* categoria */
    catForte: { f: FL, p: 700, w: 100, ls: 0.01 },
    fala: { f: FL, p: 600, w: 100, ls: -0.005 },                   /* Fala */
    texto: { f: FT, p: 400, w: 100, ls: 0 }                        /* Nunito Sans */
  };
  function estilo(reg, tam) {
    return 'font-family:' + reg.f + ';font-weight:' + reg.p + ';font-stretch:' + reg.w + '%;font-size:' + r2(tam) + 'px' +
      (reg.ls ? ';letter-spacing:' + r2(reg.ls * tam) + 'px' : '') + (reg.num ? ';font-variant-numeric:lining-nums tabular-nums' : '');
  }
  function T(x, y, txt, reg, tam, cor, anc, extra) {
    return '<text x="' + r2(x) + '" y="' + r2(y) + '"' + (anc && anc !== 'start' ? ' text-anchor="' + anc + '"' : '') +
      ' fill="' + cor + '" style="' + estilo(reg, tam) + '"' + (extra || '') + '>' + esc(txt) + '</text>';
  }
  function L(x1, y1, x2, y2, cor, w, extra) {
    return '<line x1="' + r2(x1) + '" y1="' + r2(y1) + '" x2="' + r2(x2) + '" y2="' + r2(y2) + '" stroke="' + cor + '" stroke-width="' + r2(w || 1) + '"' + (extra || '') + '/>';
  }
  function R(x, y, w, h, cor, extra) {
    return '<rect x="' + r2(x) + '" y="' + r2(y) + '" width="' + r2(Math.max(0, w)) + '" height="' + r2(Math.max(0, h)) + '" fill="' + cor + '"' + (extra || '') + '/>';
  }

  /* ---------- medição de texto (SVG oculto; sem documento, estima) ---------- */
  var cache = {};
  var medidor = null;
  function mede(txt, reg, tam) {
    txt = String(txt);
    var k = reg.f.length + '|' + reg.p + '|' + reg.w + '|' + reg.ls + '|' + tam + '|' + txt;
    if (cache[k] != null) return cache[k];
    var w = 0;
    try {
      if (temDoc && document.body) {
        if (!medidor || !medidor.isConnected) {
          var NS = 'http://www.w3.org/2000/svg';
          medidor = document.createElementNS(NS, 'svg');
          medidor.setAttribute('aria-hidden', 'true');
          medidor.setAttribute('width', '1'); medidor.setAttribute('height', '1');
          medidor.style.cssText = 'position:absolute;left:0;top:0;width:1px;height:1px;overflow:hidden;visibility:hidden;pointer-events:none';
          medidor.appendChild(document.createElementNS(NS, 'text'));
          document.body.appendChild(medidor);
        }
        var t = medidor.firstChild;
        t.setAttribute('style', estilo(reg, tam));
        t.textContent = txt;
        w = t.getComputedTextLength();
      }
    } catch (e) { w = 0; }
    if (!w) w = txt.length * tam * (reg.f === FT ? 0.52 : 0.56) * (reg.w / 100) + reg.ls * tam * txt.length;
    cache[k] = w;
    return w;
  }
  function quebra(txt, reg, tam, maxW, maxL) {
    var pal = String(txt == null ? '' : txt).split(/\s+/).filter(Boolean);
    if (!pal.length) return [];
    var linhas = [], atual = pal[0];
    for (var i = 1; i < pal.length; i++) {
      var tenta = atual + ' ' + pal[i];
      if (mede(tenta, reg, tam) <= maxW) atual = tenta; else { linhas.push(atual); atual = pal[i]; }
    }
    linhas.push(atual);
    if (maxL && linhas.length > maxL) {
      var resto = linhas.slice(maxL - 1).join(' ');
      while (resto.length > 1 && mede(resto + '...', reg, tam) > maxW) resto = resto.slice(0, -1).replace(/\s+$/, '');
      linhas = linhas.slice(0, maxL - 1).concat([resto + '...']);
    }
    return linhas;
  }

  /* ---------- números em pt-BR ---------- */
  function fmt(n, o) {
    o = o || {};
    if (!num(n)) return '';
    var casas = o.casas;
    if (casas == null) casas = Math.abs(n - Math.round(n)) < 1e-9 ? 0 : (Math.abs(n) < 10 ? 2 : 1);
    var s;
    try { s = new Intl.NumberFormat('pt-BR', { minimumFractionDigits: casas, maximumFractionDigits: casas }).format(n); }
    catch (e) { s = n.toFixed(casas).replace('.', ','); }
    var u = o.unidade || '';
    var suf = !u ? '' : (u === '%' || u === 'x' || u === 'h' ? u : ' ' + u);
    return (o.prefixo || '') + s + suf;
  }
  function rotuloValor(o, s, i) {
    if (s.vrotulos && s.vrotulos[i] != null) return String(s.vrotulos[i]);
    return fmt(s.valores[i], o);
  }
  /* escala "redonda" para o eixo: passos de 1, 2, 2,5 e 5 */
  function escalaRedonda(max, marcas) {
    if (max <= 0) return { max: 1, passo: 1 };
    var bruto = max / (marcas || 4);
    var p = Math.pow(10, Math.floor(Math.log(bruto) / Math.LN10));
    var opcoes = [1, 2, 2.5, 5, 10];
    for (var i = 0; i < opcoes.length; i++) { if (opcoes[i] * p >= bruto) { p = opcoes[i] * p; break; } }
    return { max: Math.ceil(max / p - 1e-9) * p, passo: p };
  }

  /* ---------- conferência (a régua manda) ---------- */
  var PROIBIDOS = [
    /maior\s+(escola|do\s+brasil|da\s+am[eé]rica)/i, /#\s?1\b/, /\bn[ºo°]\s?1\b/i, /\ba\s+melhor\b/i, /\bo\s+melhor\b/i,
    /\b[uú]nica\s+escola\b/i, /\bMEC\b/, /l[ií]der\s+no\s+segmento/i, /\btato{2}\b/i
  ];
  function textos(o) {
    var t = [o.titulo, o.mede, o.periodo, o.base, o.fonte, o.sobretitulo, o.aviso, o.vrotulo];
    (o.rotulos || []).forEach(function (r) { t.push(r); });
    (o.series || []).forEach(function (s) { t.push(s.nome); });
    ['antes', 'depois'].forEach(function (k) { if (o[k]) { t.push(o[k].legenda, o[k].alt, o[k].data); } });
    return t.filter(function (x) { return !vazio(x); }).map(String);
  }
  function seriesDe(o) {
    var s = Array.isArray(o.series) && o.series.length ? o.series : (o.valores ? [{ nome: o.nomeSerie || '', valores: o.valores, vrotulos: o.vrotulos }] : []);
    var padrao = s.length === 1 ? ['principal'] : s.length === 2 ? ['principal', 'comparacao'] : ['principal', 'destaque', 'comparacao'];
    return s.map(function (x, i) { return { nome: x.nome || '', valores: x.valores || [], vrotulos: x.vrotulos, papel: x.papel || padrao[i] || 'comparacao' }; });
  }
  function valida(tipo, o) {
    var faltas = [], avisos = [];
    o = o || {};
    var t = TIPOS[tipo];
    if (!t) { faltas.push('tipo desconhecido: "' + tipo + '" (use ' + LISTA_TIPOS.join(', ') + ')'); return { faltas: faltas, avisos: avisos, tipo: null }; }
    if (vazio(o.origem)) faltas.push('falta a origem do dado (medido, terceiro, mercado ou em-validacao)');
    else if (!ORIGENS[o.origem]) faltas.push('origem "' + o.origem + '" não existe (use medido, terceiro, mercado ou em-validacao)');
    if (vazio(o.fonte)) faltas.push('falta a fonte do dado');
    if (t !== 'numeral' && vazio(o.titulo)) faltas.push('falta o título-afirmação');
    if (vazio(o.mede)) faltas.push('falta dizer o que o número mede');
    if (vazio(o.periodo)) faltas.push('falta o período');
    if (vazio(o.base)) faltas.push('falta a base (recorte)');
    if (o.origem === 'terceiro' && vazio(o.link)) faltas.push('origem terceiro pede o link da declaração');
    if (o.origem === 'terceiro' && vazio(o.captura)) faltas.push('origem terceiro pede a data da captura');
    if (o.origem === 'mercado' && vazio(o.link)) faltas.push('origem mercado pede o link do estudo');

    if (t === 'barras' || t === 'barras-horizontais' || t === 'linha' || t === 'coluna-empilhada') {
      var s = seriesDe(o), rot = o.rotulos || [];
      if (!rot.length) faltas.push('faltam os rótulos das categorias');
      if (!s.length) faltas.push('faltam os valores');
      if (s.length > 3) faltas.push('no máximo 3 séries (recebidas ' + s.length + ')');
      s.forEach(function (x, i) {
        if (x.valores.length !== rot.length) faltas.push('a série ' + (i + 1) + ' tem ' + x.valores.length + ' valores para ' + rot.length + ' rótulos');
        if (x.valores.some(function (v) { return !num(v); })) faltas.push('a série ' + (i + 1) + ' tem valor que não é número');
        if ((t === 'barras-horizontais' || t === 'coluna-empilhada') && x.valores.some(function (v) { return v < 0; })) faltas.push('valores negativos não cabem em ' + NOME_TIPO[t]);
        if (s.length > 1 && vazio(x.nome)) faltas.push('a série ' + (i + 1) + ' precisa de nome');
      });
      if (t === 'linha' && rot.length < 2) faltas.push('linha precisa de ao menos 2 pontos');
    }
    if (t === 'numeral' && !num(o.valor) && vazio(o.vrotulo)) faltas.push('falta o valor do numeral');
    if (t === 'comparativo-traco') {
      if (o.canal !== 'organico' && o.canal !== 'pagina-interna') faltas.push('antes e depois de traço só em página interna ou orgânico (canal: "organico" ou "pagina-interna"); nunca em anúncio pago');
      if (o.autorizacao !== true) faltas.push('falta a autorização de imagem do aluno (autorizacao: true)');
      if (!o.antes || vazio(o.antes.data)) faltas.push('falta a data do antes');
      if (!o.depois || vazio(o.depois.data)) faltas.push('falta a data do depois');
    }
    var tx = textos(o);
    if (tx.some(function (x) { return /[\u2014\u2013]/.test(x); })) faltas.push('há travessão no texto (troque por ponto, vírgula ou dois pontos)');
    if (!o.exemploProibido) {
      tx.forEach(function (x) { PROIBIDOS.forEach(function (re) { if (re.test(x)) faltas.push('claim ou grafia vetada (spec §11.1): "' + x + '"'); }); });
    }
    if (!vazio(o.titulo) && String(o.titulo).trim().split(/\s+/).length > 6) avisos.push('título com mais de 6 palavras (L6)');
    if (t === 'barras' && o.destaque != null && seriesDe(o).length > 1) avisos.push('destaque por barra vale só para uma série');
    return { faltas: faltas, avisos: avisos, tipo: t };
  }

  /* ---------- campo e produto ---------- */
  function lerCampo(el, o) {
    if (o.campo === 'leitura' || o.campo === 'sala') return o.campo;
    try { if (el && el.closest && el.closest('.modo-leitura')) return 'leitura'; } catch (e) { /* ok */ }
    return 'sala';
  }
  function lerEstacao(el, o) {
    if (o.estacao && ESTACOES[o.estacao]) return o.estacao;
    try { var a = el && el.closest && el.closest('[data-estacao]'); if (a && ESTACOES[a.getAttribute('data-estacao')]) return a.getAttribute('data-estacao'); } catch (e) { /* ok */ }
    return 'chamado';
  }
  function paleta(campo, estacao) {
    var c = {}, base = CAMPOS[campo], est = ESTACOES[estacao][campo];
    for (var k in base) c[k] = base[k];
    c.destaque = est.marca; c.destaqueTexto = est.texto; c.fioProduto = est.fio; c.fioProdutoOp = est.fioOp;
    return c;
  }
  function corSerie(c, papel) { return papel === 'destaque' ? c.destaque : papel === 'comparacao' ? c.comparacao : c.principal; }

  /* ---------- cabeça: sobretítulo, título-afirmação, o que mede ---------- */
  function cabeca(W, o, c, k) {
    var s = '', y = 0;
    var cs = 12 * k;
    var sobre = vazio(o.sobretitulo) ? '' : caixaAlta(o.sobretitulo);
    if (sobre) {
      /* até duas linhas: o sobretítulo diz o tipo de gráfico e não pode perder palavra.
         O fio fica alinhado à primeira linha; a segunda começa no mesmo recuo. */
      var sl = quebra(sobre, REG.credito, cs, W - 32 * k, 2);
      y += cs;
      s += L(0, y - cs * 0.36, 24 * k, y - cs * 0.36, c.apoio, 1);
      sl.forEach(function (ln, i) { s += T(32 * k, y + i * cs * 1.35, ln, REG.credito, cs, c.apoio); });
      y += (sl.length - 1) * cs * 1.35 + 16 * k;
    }
    if (!vazio(o.titulo)) {
      var ts = (W >= 640 ? 30 : W >= 420 ? 24 : 21) * k;
      var linhas = quebra(caixaAlta(o.titulo), REG.titulo, ts, W, 3);
      linhas.forEach(function (ln, i) { s += T(0, y + ts * 0.8 + i * ts * 1.0, ln, REG.titulo, ts, c.titulo, 'start', i === 0 ? ' data-papel="titulo"' : ''); });
      y += ts * 0.8 + (linhas.length - 1) * ts + ts * 0.32;
    }
    if (!vazio(o.mede)) {
      var ms = 15 * k;
      var ml = quebra(o.mede, REG.texto, ms, Math.min(W, 640 * k), 3);
      y += 8 * k;
      ml.forEach(function (ln, i) { s += T(0, y + ms * 0.95 + i * ms * 1.45, ln, REG.texto, ms, c.apoio, 'start', i === 0 ? ' data-papel="mede"' : ''); });
      y += ms * 0.95 + (ml.length - 1) * ms * 1.45 + ms * 0.4;
    }
    return { svg: s, h: y };
  }

  /* ---------- pé: a Régua de Prova (spec §6.16) ---------- */
  function textoRegua(o) {
    var p = [];
    if (!vazio(o.periodo)) p.push(o.periodo);
    if (!vazio(o.base)) p.push(o.base);
    if (!vazio(o.fonte)) p.push('fonte: ' + o.fonte);
    if (o.origem === 'terceiro' && !vazio(o.captura)) p.push('capturado em ' + o.captura);
    if (!vazio(o.link)) p.push(String(o.link).replace(/^https?:\/\//, '').replace(/\/$/, ''));
    if (TIPOS[o.tipo] === 'comparativo-traco' || o.__comparativo) p.push('imagens usadas com autorização do aluno');
    return p.join(' · ');
  }
  function regua(W, o, c, k, y0, comFio) {
    var s = '', y = y0;
    var org = ORIGENS[o.origem];
    var validar = o.origem === 'em-validacao';
    var cs = 12 * k, ts = 13 * k;
    if (comFio !== false) { s += L(0, y + 0.5, W, y + 0.5, c.grade, 1, ' data-papel="fio-regua"'); y += 18 * k; }
    else y += cs;
    var corMarca = validar ? c.aux : c.apoio;
    s += '<g data-papel="regua" data-origem="' + esc(o.origem) + '">';
    s += L(0, y - cs * 0.36, 16 * k, y - cs * 0.36, corMarca, 2 * k, (org.dash ? ' stroke-dasharray="' + org.dash.split(' ').map(function (n) { return r2(n * k); }).join(' ') + '"' : '') + ' data-papel="marca-origem"');
    var rl = quebra(org.rotulo, REG.credito, cs, W - 24 * k, 2);
    rl.forEach(function (ln, i) { s += T(24 * k, y + i * cs * 1.6, ln, REG.credito, cs, validar ? c.atencao : c.apoio, 'start', i === 0 ? ' data-papel="rotulo-origem"' : ''); });
    y += (rl.length - 1) * cs * 1.6;
    if (o.exemplo) {
      /* dado de exemplo: na mesma linha da origem quando cabe; senão, na linha de baixo */
      var tg = 'DADO DE EXEMPLO', xo = 24 * k + mede(rl[rl.length - 1], REG.credito, cs) + 14 * k;
      if (xo + 24 * k + mede(tg, REG.credito, cs) <= W) {
        s += T(xo, y, '·', REG.credito, cs, c.apoio) + T(xo + 14 * k, y, tg, REG.credito, cs, c.atencao, 'start', ' data-papel="exemplo"');
      } else { y += cs * 1.6; s += T(24 * k, y, tg, REG.credito, cs, c.atencao, 'start', ' data-papel="exemplo"'); }
    }
    var linhas = quebra(textoRegua(o), REG.texto, ts, W, 4);
    if (!vazio(o.aviso)) linhas = linhas.concat(quebra(o.aviso, REG.texto, ts, W, 2));
    y += 8 * k;
    linhas.forEach(function (ln, i) { y += ts * 1.4; s += T(0, y, ln, REG.texto, ts, c.apoio, 'start', i === 0 ? ' data-papel="texto-regua"' : ''); });
    s += '</g>';
    return { svg: s, h: y - y0 + ts * 0.4 };
  }

  /* selo de trabalho para dado em validação */
  function seloValidacao(x, y, c, k, anc) {
    var cs = 12 * k, txt = 'DADO EM VALIDAÇÃO';
    var w = mede(txt, REG.credito, cs) + 24 * k;
    var x0 = anc === 'end' ? x - w : x;
    return '<g data-papel="selo-validacao">' + icone('circle-dashed', x0, y - cs * 1.05, 16 * k, c.atencao) + T(x0 + 24 * k, y, txt, REG.credito, cs, c.atencao) + '</g>';
  }

  /* legenda compacta (só quando o rótulo direto não cabe) */
  function legenda(W, series, c, k, y) {
    var s = '', x = 0, ts = 13 * k, linha = 0;
    series.forEach(function (sr) {
      var w = 22 * k + mede(sr.nome, REG.cat, ts) + 20 * k;
      if (x > 0 && x + w > W) { x = 0; linha++; }
      var yy = y + linha * 22 * k;
      s += amostra(x, yy - ts * 0.75, 14 * k, 8 * k, sr.papel, c, k);
      s += T(x + 22 * k, yy, sr.nome, REG.cat, ts, c.texto);
      x += w;
    });
    return { svg: '<g data-papel="legenda">' + s + '</g>', h: (linha + 1) * 22 * k };
  }
  function amostra(x, y, w, h, papel, c, k) {
    if (papel === 'comparacao') return R(x + 0.75, y + 0.75, w - 1.5, h - 1.5, 'none', ' stroke="' + c.comparacao + '" stroke-width="' + r2(1.5 * k) + '" stroke-dasharray="' + r2(3 * k) + ' ' + r2(2 * k) + '"');
    return R(x, y, w, h, corSerie(c, papel));
  }
  function barra(x, y, w, h, papel, c, k, validar, extra) {
    if (validar) return R(x + 0.5, y + 0.5, w - 1, h - 1, 'none', ' stroke="' + c.aux + '" stroke-width="1" stroke-dasharray="4 3"' + (extra || ''));
    if (papel === 'comparacao') return R(x + 0.75 * k, y + 0.75 * k, w - 1.5 * k, h - 1.5 * k, 'none', ' stroke="' + c.comparacao + '" stroke-width="' + r2(1.5 * k) + '" stroke-dasharray="' + r2(4 * k) + ' ' + r2(3 * k) + '"' + (extra || ''));
    return R(x, y, w, h, corSerie(c, papel), extra);
  }
  function eixoY(lo, hi, o, k) {
    var e = escalaRedonda(Math.max(Math.abs(hi), Math.abs(lo)), 4);
    var marcas = [];
    for (var v = 0; marcas.length < 12; v += e.passo) { marcas.push(r3(v)); if (v >= hi - 1e-9) break; }
    for (var w = -e.passo; w >= lo - 1e-9 && marcas.length < 16; w -= e.passo) marcas.unshift(r3(w));
    var topo = Math.max(hi, marcas[marcas.length - 1]), fundo = Math.min(lo, marcas[0]);
    return { marcas: marcas, hi: topo, lo: fundo };
  }

  /* ---------- tipo: barras ---------- */
  function corpoBarras(W, o, c, k, validar) {
    var series = seriesDe(o), rot = o.rotulos, n = rot.length, ns = series.length;
    var s = '', y = 0;
    var todos = [];
    series.forEach(function (sr) { todos = todos.concat(sr.valores); });
    if (num(o.meta)) todos.push(o.meta);
    var lo = Math.min(0, Math.min.apply(null, todos)), hi = Math.max(0, Math.max.apply(null, todos));
    if (hi === lo) hi = lo + 1;
    var multi = ns > 1;
    if (multi) { var lg = legenda(W, series, c, k, 13 * k); s += lg.svg; y += lg.h + 12 * k; }
    var ey = eixoY(lo, hi, o, k);
    if (multi) { lo = ey.lo; hi = ey.hi; }
    var es = 12 * k;
    var xL = multi ? Math.max.apply(null, ey.marcas.map(function (m) { return mede(fmt(m, o), REG.eixo, es); })) + 10 * k : 0;
    var plotW = W - xL;
    var topoRot = multi ? 8 * k : 28 * k;
    var plotH = (+o.altura || (W < 480 ? 200 : 250)) * k;
    var y0 = y + topoRot;
    function Y(v) { return y0 + (hi - v) / (hi - lo) * plotH; }
    var band = plotW / n;
    var gw = Math.min(band * (multi ? 0.74 : 0.56), (multi ? 30 * ns : 64) * k);
    var bw = multi ? (gw - (ns - 1) * 3 * k) / ns : gw;
    var vs = (W < 480 ? 15 : 17) * k;
    var dest = !multi && num(o.destaque) ? o.destaque : -1;
    if (multi) {
      ey.marcas.forEach(function (m) {
        if (m === 0) return;
        s += L(xL, Y(m) + 0.5, W, Y(m) + 0.5, c.grade, 1);
        s += T(xL - 8 * k, Y(m) + es * 0.35, fmt(m, o), REG.eixo, es, c.apoio, 'end');
      });
      s += T(xL - 8 * k, Y(0) + es * 0.35, '0', REG.eixo, es, c.apoio, 'end');
    }
    var cabeRot = true;
    if (!multi) series[0].valores.forEach(function (v, i) { if (mede(rotuloValor(o, series[0], i), REG.valor, vs) > band - 4 * k) cabeRot = false; });
    if (!cabeRot) vs = 12 * k;
    for (var i = 0; i < n; i++) {
      var cx = xL + band * i + band / 2;
      series.forEach(function (sr, j) {
        var v = sr.valores[i];
        var x = cx - gw / 2 + j * (bw + 3 * k);
        var ya = Y(Math.max(v, 0)), yb = Y(Math.min(v, 0));
        var papel = (!multi && i === dest) ? 'destaque' : sr.papel;
        s += barra(x, ya, bw, yb - ya, papel, c, k, validar, ' data-papel="barra" data-valor="' + v + '" data-serie="' + j + '"');
        if (!multi && !validar) {
          var cor = i === dest ? c.destaqueTexto : c.titulo;
          var ty = v >= 0 ? ya - 8 * k : yb + vs + 4 * k;
          s += T(cx, ty, rotuloValor(o, sr, i), REG.valor, vs, cor, 'middle', ' data-papel="valor"');
        }
      });
    }
    /* linha de base: o zero do eixo */
    s += L(xL, Y(0) + 0.5, W, Y(0) + 0.5, c.base, 1, ' data-papel="zero" data-y="' + r2(Y(0)) + '"');
    if (num(o.meta)) s += meta(xL, W, Y(o.meta), o, c, k);
    /* categorias */
    var cs = 13 * k, maxL = 0;
    var yc = Y(Math.min(lo, 0)) + 8 * k;
    for (var q = 0; q < n; q++) {
      var forte = q === dest;
      var linhas = quebra(rot[q], forte ? REG.catForte : REG.cat, cs, band - 6 * k, 2);
      maxL = Math.max(maxL, linhas.length);
      for (var li = 0; li < linhas.length; li++) s += T(xL + band * q + band / 2, yc + cs + li * cs * 1.2, linhas[li], forte ? REG.catForte : REG.cat, cs, forte ? c.destaqueTexto : c.apoio, 'middle');
    }
    return { svg: s, h: yc + cs + (maxL - 1) * cs * 1.2 + 4 * k, plot: { y0: y0, plotH: plotH, lo: lo, hi: hi } };
  }
  function meta(x1, x2, y, o, c, k) {
    var cs = 12 * k, txt = 'META · ' + (o.vmeta || fmt(o.meta, o));
    return '<g data-papel="meta">' + L(x1, y + 0.5, x2, y + 0.5, c.comparacao, 1.5 * k, ' stroke-dasharray="' + r2(5 * k) + ' ' + r2(4 * k) + '"') +
      T(x1 + 4 * k, y - 7 * k, txt, REG.credito, cs, c.apoio, 'start', ' stroke="' + c.fundo + '" stroke-width="' + r2(4 * k) + '" paint-order="stroke"') + '</g>';
  }

  /* ---------- tipo: barras horizontais (ranking) ---------- */
  function corpoBarrasH(W, o, c, k, validar) {
    var series = seriesDe(o), rot = o.rotulos, n = rot.length, ns = series.length;
    var s = '', y = 0, multi = ns > 1;
    if (multi) { var lg = legenda(W, series, c, k, 13 * k); s += lg.svg; y += lg.h + 12 * k; }
    var hi = 0;
    series.forEach(function (sr) { hi = Math.max(hi, Math.max.apply(null, sr.valores)); });
    if (!hi) hi = 1;
    var ls = 14 * k, vs = 15 * k;
    var empilha = W < 440 * k;
    var t = (multi ? 8 : 14) * k, gap = 3 * k;
    var bloco = ns * t + (ns - 1) * gap;
    var valW = 0;
    series.forEach(function (sr) { sr.valores.forEach(function (v, i) { valW = Math.max(valW, mede(rotuloValor(o, sr, i), REG.valor, vs)); }); });
    var labW = empilha ? 0 : Math.min(W * 0.38, Math.max.apply(null, rot.map(function (r) { return mede(r, REG.cat, ls); })) + 4 * k);
    var x0 = empilha ? 0 : labW + 16 * k;
    var maxW = W - x0 - valW - 10 * k;
    var dest = !multi && num(o.destaque) ? o.destaque : -1;
    var yTopo = y;
    for (var i = 0; i < n; i++) {
      var forte = i === dest;
      var reg = forte ? REG.catForte : REG.cat;
      var linhas = quebra(rot[i], reg, ls, empilha ? W : labW, 2);
      var lh = ls * 1.2;
      var alturaLinha;
      if (empilha) {
        linhas.forEach(function (ln, li) { s += T(0, y + ls + li * lh, ln, reg, ls, forte ? c.destaqueTexto : c.texto); });
        y += ls + (linhas.length - 1) * lh + 8 * k;
        alturaLinha = bloco;
      } else {
        alturaLinha = Math.max(bloco, linhas.length * lh);
        var ty = y + alturaLinha / 2 - (linhas.length * lh) / 2 + ls * 0.85;
        linhas.forEach(function (ln, li) { s += T(0, ty + li * lh, ln, reg, ls, forte ? c.destaqueTexto : c.texto); });
      }
      var by = y + (alturaLinha - bloco) / 2;
      series.forEach(function (sr, j) {
        var v = sr.valores[i];
        var w = v / hi * maxW;
        var yy = by + j * (t + gap);
        var papel = forte ? 'destaque' : sr.papel;
        s += barra(x0, yy, Math.max(w, validar ? 2 : 0), t, papel, c, k, validar, ' data-papel="barra" data-valor="' + v + '" data-serie="' + j + '"');
        if (!validar) s += T(x0 + w + 8 * k, yy + t / 2 + vs * 0.36, rotuloValor(o, sr, i), REG.valor, vs, forte ? c.destaqueTexto : c.titulo, 'start', ' data-papel="valor"');
      });
      y += alturaLinha + (empilha ? 18 : 14) * k;
    }
    y -= (empilha ? 18 : 14) * k;
    /* o zero do eixo, à esquerda das barras */
    s += L(x0 - 0.5, yTopo - 4 * k, x0 - 0.5, y + 4 * k, c.base, 1, ' data-papel="zero" data-x="' + r2(x0) + '"');
    return { svg: s, h: y + 6 * k, plot: { x0: x0, maxW: maxW, hi: hi } };
  }

  /* ---------- tipo: linha ---------- */
  function corpoLinha(W, o, c, k, validar) {
    var series = seriesDe(o), rot = o.rotulos, n = rot.length;
    var s = '', y = 0;
    var todos = [];
    series.forEach(function (sr) { todos = todos.concat(sr.valores); });
    if (num(o.meta)) todos.push(o.meta);
    var ey = eixoY(Math.min(0, Math.min.apply(null, todos)), Math.max(0, Math.max.apply(null, todos)) || 1, o, k);
    var lo = ey.lo, hi = ey.hi;
    var es = 12 * k, vs = 15 * k, ns13 = 12 * k;
    var xL = Math.max.apply(null, ey.marcas.map(function (m) { return mede(fmt(m, o), REG.eixo, es); })) + 10 * k;
    /* rótulo direto no fim de cada série */
    var fimW = 0;
    series.forEach(function (sr, j) {
      fimW = Math.max(fimW, mede(rotuloValor(o, sr, n - 1), REG.valor, vs));
      if (sr.nome) fimW = Math.max(fimW, Math.min(mede(sr.nome, REG.cat, ns13), 120 * k));
    });
    var direto = W >= 440 * k;
    var xR = W - (direto ? fimW + 14 * k : 8 * k);
    if (!direto && series.length > 1) { var lg = legenda(W, series, c, k, 13 * k); s += lg.svg; y += lg.h + 8 * k; }
    var y0 = y + 14 * k;
    var plotH = (+o.altura || (W < 480 ? 190 : 240)) * k;
    function Y(v) { return y0 + (hi - v) / (hi - lo) * plotH; }
    function X(i) { return xL + 6 * k + (xR - xL - 6 * k) * (n === 1 ? 0.5 : i / (n - 1)); }
    ey.marcas.forEach(function (m) {
      if (m !== 0) s += L(xL, Y(m) + 0.5, W, Y(m) + 0.5, c.grade, 1);
      s += T(xL - 8 * k, Y(m) + es * 0.35, fmt(m, o), REG.eixo, es, c.apoio, 'end');
    });
    s += L(xL, Y(0) + 0.5, W, Y(0) + 0.5, c.base, 1, ' data-papel="zero" data-y="' + r2(Y(0)) + '"');
    if (num(o.meta)) s += meta(xL, W, Y(o.meta), o, c, k);
    var dest = num(o.destaque) ? o.destaque : -1;
    /* séries: comparação embaixo, principal por cima */
    var ordem = series.map(function (sr, j) { return j; }).sort(function (a, b) {
      var pa = series[a].papel === 'comparacao' ? 0 : series[a].papel === 'destaque' ? 1 : 2;
      var pb = series[b].papel === 'comparacao' ? 0 : series[b].papel === 'destaque' ? 1 : 2;
      return pa - pb;
    });
    var fins = [];
    ordem.forEach(function (j) {
      var sr = series[j];
      var cor = validar ? c.aux : corSerie(c, sr.papel);
      var d = sr.valores.map(function (v, i) { return (i ? 'L' : 'M') + r2(X(i)) + ' ' + r2(Y(v)); }).join('');
      var dash = validar || sr.papel === 'comparacao' ? ' stroke-dasharray="' + r2(5 * k) + ' ' + r2(4 * k) + '"' : '';
      s += '<path d="' + d + '" fill="none" stroke="' + cor + '" stroke-width="' + r2((sr.papel === 'comparacao' ? 1.5 : 2) * k) + '" stroke-linejoin="round" stroke-linecap="butt"' + dash + ' data-papel="linha" data-serie="' + j + '"/>';
      var vf = sr.valores[n - 1];
      s += '<circle cx="' + r2(X(n - 1)) + '" cy="' + r2(Y(vf)) + '" r="' + r2(3.5 * k) + '" fill="' + (sr.papel === 'comparacao' ? c.fundo : cor) + '"' + (sr.papel === 'comparacao' ? ' stroke="' + cor + '" stroke-width="' + r2(1.5 * k) + '"' : '') + '/>';
      fins.push({ j: j, y: Y(vf), sr: sr, cor: sr.papel === 'destaque' ? c.destaqueTexto : sr.papel === 'comparacao' ? c.apoio : c.titulo });
    });
    /* destaque de um ponto (série principal) */
    if (dest >= 0 && dest < n && !validar) {
      var pr = series[0], yd = Y(pr.valores[dest]);
      s += L(X(dest), yd + 6 * k, X(dest), Y(0), c.grade, 1, ' data-papel="guia-destaque"');
      s += '<circle cx="' + r2(X(dest)) + '" cy="' + r2(yd) + '" r="' + r2(5 * k) + '" fill="' + c.destaque + '" stroke="' + c.fundo + '" stroke-width="' + r2(2 * k) + '" data-papel="ponto-destaque"/>';
      if (dest !== n - 1) s += T(X(dest), yd - 12 * k, rotuloValor(o, pr, dest), REG.valor, vs, c.destaqueTexto, 'middle', ' stroke="' + c.fundo + '" stroke-width="' + r2(4 * k) + '" paint-order="stroke"');
    }
    /* rótulos diretos sem colisão */
    if (direto && !validar) {
      fins.sort(function (a, b) { return a.y - b.y; });
      var alt = series.length > 1 ? 30 * k : 18 * k;
      for (var f = 1; f < fins.length; f++) if (fins[f].y - fins[f - 1].y < alt) fins[f].y = fins[f - 1].y + alt;
      fins.forEach(function (fi) {
        var x = X(n - 1) + 10 * k;
        s += T(x, fi.y + vs * 0.36, rotuloValor(o, fi.sr, n - 1), REG.valor, vs, fi.cor, 'start', ' data-papel="valor"');
        if (series.length > 1 && fi.sr.nome) s += T(x, fi.y + vs * 0.36 + ns13 * 1.25, quebra(fi.sr.nome, REG.cat, ns13, W - x, 1)[0], REG.cat, ns13, c.apoio);
      });
    }
    /* categorias do eixo x, espaçadas para caber */
    var cs = 13 * k;
    var largura = Math.max.apply(null, rot.map(function (r) { return mede(r, REG.cat, cs); })) + 12 * k;
    var passo = Math.max(1, Math.ceil(largura / ((xR - xL) / Math.max(1, n - 1) || 1)));
    var yc = Y(Math.min(lo, 0)) + 8 * k + cs;
    for (var i = 0; i < n; i++) {
      if (i % passo !== 0 && i !== n - 1) continue;
      if (i !== n - 1 && i + passo > n - 1 && (n - 1 - i) < passo) continue;
      var anc = n > 1 && i === 0 ? 'start' : i === n - 1 && n > 1 ? 'end' : 'middle';
      var xx = anc === 'start' ? X(i) - 4 * k : anc === 'end' ? X(i) + 4 * k : X(i);
      s += T(xx, yc, rot[i], i === dest ? REG.catForte : REG.cat, cs, i === dest ? c.destaqueTexto : c.apoio, anc);
    }
    return { svg: s, h: yc + 4 * k, plot: { y0: y0, plotH: plotH, lo: lo, hi: hi } };
  }

  /* ---------- tipo: coluna empilhada (até 3) ---------- */
  function corpoEmpilhada(W, o, c, k, validar) {
    var series = seriesDe(o), rot = o.rotulos, n = rot.length, ns = series.length;
    /* papéis fixos de empilhamento: principal, destaque, terceira (Fumaça cheia) */
    var papeis = ['principal', 'destaque', 'terceira'];
    var cores = { principal: c.principal, destaque: c.destaque, terceira: c.terceira };
    var s = '', y = 0;
    var totais = rot.map(function (r, i) { var t = 0; series.forEach(function (sr) { t += sr.valores[i]; }); return t; });
    var hi = Math.max.apply(null, totais) || 1;
    var ns13 = 13 * k, vs = 15 * k;
    var nomeW = Math.max.apply(null, series.map(function (sr) { return mede(sr.nome, REG.cat, ns13); }));
    var direto = W >= 480 * k && nomeW < W * 0.28;
    if (!direto) {
      var lg = legendaEmpilhada(W, series, cores, papeis, c, k, 13 * k);
      s += lg.svg; y += lg.h + 12 * k;
    }
    var xR = direto ? W - nomeW - 18 * k : W;
    var plotW = xR;
    var y0 = y + (o.totais === false ? 8 : 26) * k;
    var plotH = (+o.altura || (W < 480 ? 210 : 250)) * k;
    function Y(v) { return y0 + (hi - v) / hi * plotH; }
    var band = plotW / n;
    var bw = Math.min(band * 0.56, 56 * k);
    var gap = 2 * k;
    var ultimo = [];
    for (var i = 0; i < n; i++) {
      var cx = band * i + band / 2, acc = 0;
      series.forEach(function (sr, j) {
        var v = sr.valores[i];
        var ya = Y(acc + v), yb = Y(acc);
        var h = yb - ya - (j > 0 && v > 0 ? gap : 0);
        var extra = ' data-papel="segmento" data-valor="' + v + '" data-serie="' + j + '"';
        if (validar) s += R(cx - bw / 2 + 0.5, ya + 0.5, bw - 1, Math.max(0, h - 1), 'none', ' stroke="' + c.aux + '" stroke-width="1" stroke-dasharray="4 3"' + extra);
        else s += R(cx - bw / 2, ya, bw, Math.max(0, h), cores[papeis[j]], extra);
        if (i === n - 1) ultimo.push({ y: (ya + yb) / 2, h: yb - ya, sr: sr, j: j });
        acc += v;
      });
      if (o.totais !== false && !validar) s += T(cx, Y(totais[i]) - 8 * k, (o.vtotais && o.vtotais[i]) || fmt(totais[i], o), REG.valor, vs, c.titulo, 'middle', ' data-papel="total"');
    }
    s += L(0, Y(0) + 0.5, W, Y(0) + 0.5, c.base, 1, ' data-papel="zero" data-y="' + r2(Y(0)) + '"');
    if (direto) {
      var xn = band * (n - 1) + band / 2 + bw / 2 + 12 * k;
      for (var f = 1; f < ultimo.length; f++) if (ultimo[f - 1].y - ultimo[f].y < 18 * k) ultimo[f].y = ultimo[f - 1].y - 18 * k;
      ultimo.forEach(function (u) {
        s += L(xn - 8 * k, u.y, xn - 3 * k, u.y, c.apoio, 1);
        s += T(xn, u.y + ns13 * 0.35, u.sr.nome, REG.cat, ns13, c.texto, 'start', ' data-papel="rotulo-serie"');
      });
    }
    var cs = 13 * k, yc = Y(0) + 8 * k, maxL = 1;
    for (var q = 0; q < n; q++) {
      var linhas = quebra(rot[q], REG.cat, cs, band - 6 * k, 2);
      maxL = Math.max(maxL, linhas.length);
      linhas.forEach(function (ln, li) { s += T(band * q + band / 2, yc + cs + li * cs * 1.2, ln, REG.cat, cs, c.apoio, 'middle'); });
    }
    return { svg: s, h: yc + cs + (maxL - 1) * cs * 1.2 + 4 * k, plot: { y0: y0, plotH: plotH, hi: hi } };
  }
  function legendaEmpilhada(W, series, cores, papeis, c, k, y) {
    var s = '', x = 0, ts = 13 * k, linha = 0;
    series.forEach(function (sr, j) {
      var w = 22 * k + mede(sr.nome, REG.cat, ts) + 20 * k;
      if (x > 0 && x + w > W) { x = 0; linha++; }
      var yy = y + linha * 22 * k;
      s += R(x, yy - ts * 0.75, 14 * k, 8 * k, cores[papeis[j]]);
      s += T(x + 22 * k, yy, sr.nome, REG.cat, ts, c.texto);
      x += w;
    });
    return { svg: '<g data-papel="legenda">' + s + '</g>', h: (linha + 1) * 22 * k };
  }

  /* ---------- tipo: Numeral de Prova (spec §6.16) ---------- */
  function numeral(W, o, c, k, validar) {
    var s = '', y = 0, x = 18 * k;
    var iw = W - x;
    var cab = cabeca(iw, { sobretitulo: o.sobretitulo, exemplo: o.exemplo, titulo: o.titulo }, c, k);
    s += '<g transform="translate(' + r2(x) + ' 0)">' + cab.svg + '</g>';
    y += cab.h + (cab.h ? 14 * k : 0);
    var nsz = (W < 480 ? 56 : 80) * k;
    if (validar) {
      var vt = 'dado em validação';
      var vsz = (W < 480 ? 26 : 32) * k;
      s += T(x, y + vsz * 0.9, vt, REG.fala, vsz, c.aux, 'start', ' data-papel="numero"');
      y += vsz * 0.9 + 14 * k;
    } else {
      var txt = !vazio(o.vrotulo) ? String(o.vrotulo) : fmt(o.valor, o);
      while (mede(txt, REG.numeral, nsz) > iw && nsz > 32 * k) nsz -= 2 * k;
      s += T(x - nsz * 0.04, y + nsz * 0.86, txt, REG.numeral, nsz, c.titulo, 'start', ' data-papel="numero"');
      y += nsz * 0.86 + 14 * k;
    }
    var ms = 18 * k;
    var ml = quebra(o.mede, REG.fala, ms, Math.min(iw, 520 * k), 3);
    ml.forEach(function (ln, i) { s += T(x, y + ms * 0.95 + i * ms * 1.3, ln, REG.fala, ms, c.texto, 'start', i === 0 ? ' data-papel="mede"' : ''); });
    y += ms * 0.95 + (ml.length - 1) * ms * 1.3 + 16 * k;
    var rg = regua(iw, o, c, k, y, false);
    s += '<g transform="translate(' + r2(x) + ' 0)">' + rg.svg + '</g>';
    y += rg.h + 10 * k;
    /* o fio de produto à esquerda (2 px, grafismo do produto); tracejado em validação */
    var fio = L(1 * k, 0, 1 * k, y, validar ? c.aux : c.fioProduto, 2 * k, (validar ? ' stroke-dasharray="' + r2(4 * k) + ' ' + r2(3 * k) + '"' : '') + (c.fioProdutoOp < 1 && !validar ? ' stroke-opacity="' + c.fioProdutoOp + '"' : '') + ' data-papel="fio-produto"');
    return { svg: fio + s, h: y };
  }

  /* ---------- tipo: comparativo de traço, antes e depois (só orgânico) ---------- */
  function corpoComparativo(W, o, c, k, validar) {
    var s = '', gap = 24 * k;
    var fw = (W - gap) / 2;
    var fh = Math.min(fw * 1.25, 360 * k);
    var cs = 12 * k, y = cs;
    var rotulos = ['antes', 'depois'].map(function (lado) { return [(lado === 'antes' ? 'ANTES' : 'DEPOIS'), caixaAlta((o[lado] || {}).data || '')]; });
    var duas = rotulos.some(function (r) { return mede(r[0] + ' · ' + r[1], REG.credito, cs) > fw; });
    if (duas) y += cs * 1.5;
    ['antes', 'depois'].forEach(function (lado, i) {
      var d = o[lado] || {};
      var x = i * (fw + gap);
      var cor = i ? c.titulo : c.apoio, ex = ' data-papel="rotulo-' + lado + '"';
      if (duas) s += T(x, y - cs * 1.5, rotulos[i][0], REG.credito, cs, cor, 'start', ex) + T(x, y, rotulos[i][1], REG.credito, cs, cor);
      else s += T(x, y, rotulos[i][0] + ' · ' + rotulos[i][1], REG.credito, cs, cor, 'start', ex);
      var fy = y + 12 * k;
      if (!vazio(d.foto)) {
        s += '<svg x="' + r2(x) + '" y="' + r2(fy) + '" width="' + r2(fw) + '" height="' + r2(fh) + '" viewBox="0 0 ' + r2(fw) + ' ' + r2(fh) + '" preserveAspectRatio="none" data-papel="foto-' + lado + '">' +
          '<image href="' + esc(d.foto) + '" x="0" y="0" width="' + r2(fw) + '" height="' + r2(fh) + '" preserveAspectRatio="xMidYMid slice"' + (d.alt ? ' aria-label="' + esc(d.alt) + '"' : '') + '/></svg>';
      } else {
        s += R(x, fy, fw, fh, c.placa, ' data-papel="espaco-foto"');
        s += R(x + 0.5, fy + 0.5, fw - 1, fh - 1, 'none', ' stroke="' + c.placaFio + '" stroke-width="1" stroke-dasharray="' + r2(4 * k) + ' ' + r2(4 * k) + '"');
        var isz = 32 * k;
        s += icone('images', x + fw / 2 - isz / 2, fy + fh / 2 - isz - 10 * k, isz, c.aux);
        var pl = quebra('foto real da escola, com autorização', REG.texto, 13 * k, fw - 24 * k, 3);
        pl.forEach(function (ln, li) { s += T(x + fw / 2, fy + fh / 2 + 12 * k + li * 13 * k * 1.35, ln, REG.texto, 13 * k, c.apoio, 'middle'); });
      }
      if (!vazio(d.legenda)) {
        var ll = quebra(d.legenda, REG.texto, 13 * k, fw, 2);
        ll.forEach(function (ln, li) { s += T(x, fy + fh + 20 * k + li * 13 * k * 1.35, ln, REG.texto, 13 * k, c.apoio); });
      }
    });
    /* o fio entre os dois quadros */
    s += L(fw + gap / 2, y + 12 * k, fw + gap / 2, y + 12 * k + fh, c.grade, 1);
    var temLeg = !vazio((o.antes || {}).legenda) || !vazio((o.depois || {}).legenda);
    return { svg: s, h: y + 12 * k + fh + (temLeg ? 20 * k + 13 * k * 1.35 + 4 * k : 4 * k) };
  }

  /* ---------- tabela acessível (visualmente oculta) ---------- */
  var OCULTA = 'position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;border:0';
  function tabela(t, o) {
    var validar = o.origem === 'em-validacao';
    var cap = (vazio(o.titulo) ? o.mede : o.titulo) + '. ' + textoRegua(o) + '. Origem: ' + ORIGENS[o.origem].descricao + '.' + (o.exemplo ? ' Dado de exemplo.' : '');
    var h = '<div class="vviz-tabela-oculta" style="' + OCULTA + '"><table class="vviz-tabela"><caption>' + esc(cap) + '</caption>';
    function val(txt) { return validar ? 'em validação' : txt; }
    if (t === 'numeral') {
      h += '<thead><tr><th scope="col">O que mede</th><th scope="col">Valor</th></tr></thead><tbody><tr><th scope="row">' + esc(o.mede) + '</th><td>' + esc(val(!vazio(o.vrotulo) ? o.vrotulo : fmt(o.valor, o))) + '</td></tr></tbody>';
    } else if (t === 'comparativo-traco') {
      h += '<thead><tr><th scope="col">Momento</th><th scope="col">Data</th><th scope="col">Descrição</th></tr></thead><tbody>';
      ['antes', 'depois'].forEach(function (k) { var d = o[k] || {}; h += '<tr><th scope="row">' + (k === 'antes' ? 'Antes' : 'Depois') + '</th><td>' + esc(d.data) + '</td><td>' + esc(d.alt || d.legenda || 'foto real da escola, com autorização') + '</td></tr>'; });
      h += '</tbody>';
    } else {
      var series = seriesDe(o);
      h += '<thead><tr><th scope="col">' + esc(o.rotuloCategoria || 'Categoria') + '</th>';
      series.forEach(function (sr) { h += '<th scope="col">' + esc(sr.nome || o.mede) + '</th>'; });
      if (t === 'coluna-empilhada') h += '<th scope="col">Total</th>';
      h += '</tr></thead><tbody>';
      o.rotulos.forEach(function (r, i) {
        h += '<tr><th scope="row">' + esc(r) + '</th>';
        var tot = 0;
        series.forEach(function (sr) { tot += sr.valores[i]; h += '<td>' + esc(val(rotuloValor(o, sr, i))) + '</td>'; });
        if (t === 'coluna-empilhada') h += '<td>' + esc(val(fmt(tot, o))) + '</td>';
        h += '</tr>';
      });
      h += '</tbody>';
    }
    return h + '</table></div>';
  }

  /* ---------- aviso (o motor recusa desenhar) ---------- */
  function aviso(faltas, campo) {
    var claro = campo === 'leitura';
    var fundo = claro ? HEX.cinza100 : HEX.bastidor, fio = claro ? HEX.ambarFundo : HEX.areia, txt = claro ? HEX.sala : HEX.cal, rot = claro ? HEX.ambarFundo : HEX.areia;
    var h = '<div class="vviz-aviso" role="note" style="display:flex;gap:12px;align-items:flex-start;background:' + fundo + ';border-left:2px solid ' + fio + ';padding:16px 16px 16px 14px;color:' + txt + ';font:400 15px/1.5 ' + FT + '">' +
      iconeHTML('triangle-alert', rot, 20) + '<div style="min-width:0"><p style="margin:0 0 6px;font:500 12px/1.3 ' + FL + ';font-stretch:125%;letter-spacing:.18em;text-transform:uppercase;color:' + rot + '">Gráfico não desenhado</p><ul style="margin:0;padding-left:18px">';
    faltas.forEach(function (f) { h += '<li style="overflow-wrap:anywhere">' + esc(f) + '</li>'; });
    return h + '</ul></div></div>';
  }

  /* ---------- montagem ---------- */
  var seq = 0;
  var registro = [];
  function largura(el, o) {
    var w = +o.largura;
    if (!w && el) { w = el.clientWidth; if (!w && el.getBoundingClientRect) w = el.getBoundingClientRect().width; }
    return Math.max(260, Math.min(1200, Math.round(w || 960)));
  }
  function desenha(tipo, o, W, campo, estacao, idBase) {
    var v = valida(tipo, o);
    if (v.faltas.length) return { ok: false, faltas: v.faltas, avisos: v.avisos };
    var t = v.tipo;
    var c = paleta(campo, estacao);
    var k = +o.escala || 1;
    var validar = o.origem === 'em-validacao';
    var pad = validar ? 20 * k : 0;
    var iw = W - pad * 2;
    var miolo = '', y = 0;
    if (validar) { miolo += seloValidacao(0, 12 * k, c, k, 'start'); y = 0; }
    var topo = validar ? 32 * k : 0;
    if (t === 'numeral') {
      var nm = numeral(iw, o, c, k, validar);
      miolo += '<g transform="translate(0 ' + r2(topo) + ')">' + nm.svg + '</g>'; y = topo + nm.h;
    } else {
      var cab = cabeca(iw, o, c, k);
      miolo += '<g transform="translate(0 ' + r2(topo) + ')">' + cab.svg + '</g>'; y = topo + cab.h + 22 * k;
      var corpo = t === 'barras' ? corpoBarras(iw, o, c, k, validar)
        : t === 'barras-horizontais' ? corpoBarrasH(iw, o, c, k, validar)
          : t === 'linha' ? corpoLinha(iw, o, c, k, validar)
            : t === 'coluna-empilhada' ? corpoEmpilhada(iw, o, c, k, validar)
              : corpoComparativo(iw, o, c, k, validar);
      miolo += '<g transform="translate(0 ' + r2(y) + ')" data-papel="corpo">' + corpo.svg + '</g>';
      y += corpo.h + 18 * k;
      var oo = o; if (t === 'comparativo-traco') { oo = {}; for (var q in o) oo[q] = o[q]; oo.__comparativo = true; }
      var rg = regua(iw, oo, c, k, y, true);
      miolo += rg.svg; y += rg.h;
    }
    var H = Math.ceil(y + pad * 2);
    var tit = esc(!vazio(o.titulo) ? o.titulo : validar ? 'Dado em validação: ' + o.mede : (!vazio(o.vrotulo) ? o.vrotulo : fmt(o.valor, o)) + ' ' + o.mede);
    var dsc = esc(NOME_TIPO[t] + '. ' + (o.mede || '') + '. ' + textoRegua(o) + '. Origem: ' + ORIGENS[o.origem].descricao + '.' + (validar ? ' Dado em validação, não publicar.' : '') + (o.exemplo ? ' Dado de exemplo.' : '') + ' Os dados estão na tabela a seguir.');
    var svg = '<svg xmlns="http://www.w3.org/2000/svg" class="vviz-svg" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-labelledby="' + idBase + '-t ' + idBase + '-d" data-tipo="' + t + '" data-campo="' + campo + '" data-estacao="' + estacao + '" data-origem="' + esc(o.origem) + '" style="display:block;width:100%;height:auto;overflow:visible">' +
      '<title id="' + idBase + '-t">' + tit + '</title><desc id="' + idBase + '-d">' + dsc + '</desc>' +
      (validar ? '<rect x="0.5" y="0.5" width="' + (W - 1) + '" height="' + (H - 1) + '" fill="none" stroke="' + c.aux + '" stroke-width="1" stroke-dasharray="6 4" data-papel="moldura-validacao"/>' : '') +
      '<g transform="translate(' + r2(pad) + ' ' + r2(pad) + ')">' + miolo + '</g></svg>';
    return { ok: true, svg: svg, tabela: tabela(t, o), W: W, H: H, tipo: t, avisos: v.avisos, campo: campo, estacao: estacao, c: c };
  }

  function render(el, tipo, dados) {
    if (typeof el === 'string') el = document.querySelector(el);
    if (!el) return null;
    var o = dados || {};
    if (!tipo) tipo = o.tipo;
    var campo = lerCampo(el, o), estacao = lerEstacao(el, o);
    var W = largura(el, o);
    var id = el.__vviz && el.__vviz.id ? el.__vviz.id : 'vviz' + (++seq) + '-' + hash(JSON.stringify(o) + tipo);
    var r = desenha(tipo, o, W, campo, estacao, id);
    el.__vviz = { tipo: tipo, dados: o, id: id, resultado: r };
    if (registro.indexOf(el) < 0) { registro.push(el); observa(el); }
    el.classList.add('vviz');
    if (!r.ok) {
      el.setAttribute('data-vviz-estado', 'recusado');
      el.innerHTML = aviso(r.faltas, campo);
      return r;
    }
    el.setAttribute('data-vviz-estado', o.origem === 'em-validacao' ? 'em-validacao' : 'ok');
    if (getComputedStyle(el).position === 'static') el.style.position = 'relative';
    el.innerHTML = r.svg + r.tabela;
    if (r.avisos.length && typeof console !== 'undefined') console.warn('VViz:', r.avisos.join('; '));
    return r;
  }

  function erroExport(motivo) { var e = new Error('VViz: exportação bloqueada. ' + motivo); e.name = 'VVizExportacaoBloqueada'; return e; }
  function paraArquivo(r) {
    var s = r.svg.replace(' style="display:block;width:100%;height:auto;overflow:visible"', ' width="' + r.W + '" height="' + r.H + '"');
    return s.replace(/(<\/desc>)/, '$1<rect x="0" y="0" width="' + r.W + '" height="' + r.H + '" fill="' + r.c.fundo + '" data-papel="fundo"/>');
  }
  function svg(a, dados) {
    if (typeof a === 'string' && TIPOS[a]) {
      var o = dados || {};
      var v = valida(a, o);
      if (v.faltas.length) throw erroExport('Régua de prova incompleta: ' + v.faltas.join('; ') + '.');
      if (o.origem === 'em-validacao') throw erroExport('Dado em validação não sai do arquivo de trabalho (spec §6.16).');
      var campo = o.campo === 'leitura' ? 'leitura' : 'sala';
      var estacao = ESTACOES[o.estacao] ? o.estacao : 'chamado';
      var r = desenha(a, o, Math.max(260, Math.min(2400, +o.largura || 960)), campo, estacao, 'vvx-' + hash(JSON.stringify(o) + a));
      return paraArquivo(r);
    }
    var el = typeof a === 'string' ? document.querySelector(a) : a;
    if (!el || !el.__vviz) throw erroExport('Elemento sem gráfico do VViz.');
    var res = el.__vviz.resultado;
    if (!res || !res.ok) throw erroExport('O gráfico foi recusado: ' + ((res && res.faltas) || []).join('; ') + '.');
    if (el.__vviz.dados.origem === 'em-validacao') throw erroExport('Dado em validação não sai do arquivo de trabalho (spec §6.16).');
    return paraArquivo(res);
  }

  function montar(raizEl) {
    var base = raizEl || (temDoc ? document : null);
    if (!base) return;
    var nos = base.querySelectorAll('[data-vviz]');
    for (var i = 0; i < nos.length; i++) {
      var el = nos[i], o;
      try { o = JSON.parse(el.getAttribute('data-vviz')); }
      catch (e) { el.classList.add('vviz'); el.setAttribute('data-vviz-estado', 'recusado'); el.innerHTML = aviso(['o JSON de data-vviz não é válido: ' + e.message], lerCampo(el, {})); continue; }
      render(el, o.tipo, o);
    }
  }
  function redesenhar() {
    cache = {};
    registro = registro.filter(function (el) { return el.isConnected; });
    registro.forEach(function (el) { if (el.__vviz) render(el, el.__vviz.tipo, el.__vviz.dados); });
  }
  var ro = null, espera = 0, larguras = typeof WeakMap !== 'undefined' ? new WeakMap() : null;
  function observa(el) {
    if (!larguras || typeof ResizeObserver === 'undefined') return;
    if (!ro) ro = new ResizeObserver(function (ents) {
      var mudou = false;
      ents.forEach(function (en) { var w = Math.round(en.contentRect.width); if (larguras.get(en.target) !== w) { larguras.set(en.target, w); mudou = true; } });
      if (mudou) { clearTimeout(espera); espera = setTimeout(redesenhar, 120); }
    });
    larguras.set(el, Math.round(el.clientWidth || 0));
    ro.observe(el);
  }

  var api = {
    versao: VERSAO, tipos: LISTA_TIPOS.slice(), origens: ORIGENS, campos: CAMPOS, estacoes: ESTACOES, hex: HEX,
    render: render, svg: svg, valida: valida, montar: montar, redesenhar: redesenhar, fmt: fmt,
    barras: function (el, o) { return render(el, 'barras', o); },
    barrasHorizontais: function (el, o) { return render(el, 'barras-horizontais', o); },
    linha: function (el, o) { return render(el, 'linha', o); },
    colunaEmpilhada: function (el, o) { return render(el, 'coluna-empilhada', o); },
    numeral: function (el, o) { return render(el, 'numeral', o); },
    comparativoTraco: function (el, o) { return render(el, 'comparativo-traco', o); }
  };

  if (temDoc && typeof window !== 'undefined') {
    try {
      if (document.fonts) {
        document.fonts.ready.then(redesenhar);
        document.fonts.addEventListener('loadingdone', redesenhar);
      }
    } catch (e) { /* sem API de fontes */ }
    window.addEventListener('beforeprint', redesenhar);
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { montar(); });
    else montar();
  }
  raiz.VViz = api;
  raiz.vviz = api;
})(typeof window !== 'undefined' ? window : this);
