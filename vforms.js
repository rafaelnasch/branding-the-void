/* =====================================================================
   VFORMS · motor de formas SVG da The VOID · sistema Sala Escura v1 · 06/10/2026
   Fonte normativa: spec do sistema Sala Escura (seções 3.5, 5.2, 5.6, 6 e 7.4).

   Quando uma peça da The VOID precisa de uma forma da casa (grão, Esfera, Eco do VOID,
   Janela de Luz, véu, Faixa Cinemascope, Corte do Logo, órbitas, Mapa da Trilha,
   marcadores, Anel de Preenchimento, selo, área de proteção, rodapé), ela sai daqui:
   nunca de banco de imagem, nunca de desenho feito na hora, nunca de clichê de cinema.

   Regras do motor
   · ES2015, zero dependências, SVG puro, determinístico (sem Math.random e sem Date):
     mesma entrada e mesmo tamanho, mesmo desenho, byte a byte.
   · Toda cor sai em HEX por extenso ou por classe. Nunca var() em atributo de SVG e
     nunca máscara CSS apontando para um mask SVG por id em elemento HTML.
   · O logotipo é sempre o arquivo oficial (assets/brand/svg). O motor recusa texto no
     lugar do logotipo e recusa selo abaixo de 96 px (devolve o Rótulo de Produto).
   · Com opção aria, o SVG ganha role="img" e <title>; sem ela, é decorativo
     (aria-hidden="true").
   · Movimento (assentamento do Anel, Letreiro Corrido) só em tela; desligado com
     prefers-reduced-motion e na impressão.

   Como usar
     <div data-vforms="esfera"></div>                                   (monta sozinho)
     <div data-vforms="mapa-trilha" data-vforms-opts='{"ativa":"master"}'></div>
     <div data-vforms='{"forma":"selo","produto":"pro","tamanho":120}'></div>
     <div data-vforms="janela"><h2>conteúdo</h2></div>   (com conteúdo, a forma vira
                                                          camada atrás do bloco)
     VForms.render(el, forma, opts) · VForms.svg(forma, opts) (texto pronto para salvar,
     levar ao Figma ou ao Canva) · VForms.montar(raiz) · VForms.redesenhar()

   Opções comuns: tema ('sala' | 'leitura', lido de .modo-leitura), estacao ('chamado' |
   'start' | 'master' | 'pro' | 'voiders', lido de [data-estacao]), aria, id, base
   (pasta do repositório, para achar assets/brand), largura e altura em px.
   ===================================================================== */
(function (raiz) {
  'use strict';

  /* ---------- tokens (iguais a tokens.json; não altere aqui sem alterar lá) ---------- */
  const T = {
    nanquim: '#000000', sala: '#181818', bastidor: '#212121', coxia: '#2B2B2B', fio: '#363636',
    chumbo: '#474747', penumbra: '#5F5F5C', fumaca: '#898989', po: '#B4B5B0', cal: '#DCDDD8',
    cinza100: '#ECEDE7', tela: '#F8F9F4', branco: '#FFFFFF', nevoa: '#C9D0D8', ardosia: '#3F4E4F',
    terracota: '#B25A32', terracotaViva: '#C46039', terracotaFunda: '#8C4529', terracotaLuz: '#DE8C66',
    terracotaNoite: '#4A2416', areia: '#DBC5A3', campoStart: '#B5966B', caramelo: '#AE8A64',
    ouroVelho: '#93693B', ouroFundo: '#734120', campoMaster: '#76432B', couro: '#6C4327', cafe: '#412919',
    musgoLuz: '#9DB79B', musgo: '#3E6A4B'
  };
  const ESTACOES = ['chamado', 'start', 'master', 'pro', 'voiders'];
  const PRODUTOS = ['start', 'master', 'pro'];

  /* grafismo por produto (spec 3.5): {c: cor, o: opacidade} */
  const GRAFISMO = {
    sala: {
      chamado: { c: T.tela, o: 0.32 }, start: { c: T.ouroVelho, o: 1 }, master: { c: T.terracota, o: 1 },
      pro: { c: T.nevoa, o: 1 }, voiders: { c: T.tela, o: 0.32 }
    },
    leitura: {
      chamado: { c: T.sala, o: 0.4 }, start: { c: T.ouroVelho, o: 1 }, master: { c: T.terracota, o: 1 },
      pro: { c: T.ardosia, o: 1 }, voiders: { c: T.sala, o: 0.4 }
    }
  };
  /* superfície de grafismo mais clara para o Start sobre Coxia (spec 3.5) */
  const GRAFISMO_COXIA_START = { c: T.caramelo, o: 1 };
  const NEUTRO = {
    sala: { linha: T.fumaca, nome: T.cal, apoio: T.po, forte: T.tela, campo: T.sala, orbita: { c: T.tela, o: 0.28 } },
    leitura: { linha: T.fumaca, nome: T.sala, apoio: T.ardosia, forte: T.sala, campo: T.tela, orbita: { c: T.sala, o: 0.28 } }
  };
  /* cor de preenchimento da formação concluída no Anel (base do selo de cada produto) */
  const COR_FORMACAO = { start: T.ouroVelho, master: T.terracota, pro: T.ardosia };

  const FONTE_LETREIRO = "Archivo, 'Arial Narrow', Arial, sans-serif";
  const FONTE_OFF = "Alga, Newsreader, Georgia, serif";

  /* ---------- medidas do vetor (marca.json) ---------- */
  const MARCA = {
    horizontal: { vb: [3804, 579], bbox: [5.4, 0.9, 3754, 573.5], X: 194.22, H: 551.81 },
    vertical: { vb: [1937, 1057], bbox: [124.1, 1.5, 1869.9, 1030.7], X: 184.14, H: 523.17 },
    start: { vb: [3620, 579], bbox: [5.4, 0.7, 3559.6, 573.3], X: 194.22, H: 551.81 },
    master: { vb: [3894, 579], bbox: [5.4, 0.5, 3849, 573.1], X: 194.22, H: 551.81 },
    pro: { vb: [3745, 578], bbox: [5.4, 0.3, 3251.7, 572.9], X: 194.22, H: 551.81 }
  };
  /* Corte do Logo: linhas de corte no vão entre letras inteiras do horizontal
     (medidas no vetor: THE termina em 567, V começa em 726; O termina em 1792, I vai
     de 1834 a 1945, D de 2005 a 2475, ® de 2483 a 2568, TATTOO começa em 2647).
     Entre V e O não existe vão (o O começa em 1244, antes do fim do V em 1263). */
  const CORTES = { antesV: 646, oI: 1813, iD: 1975, depoisReg: 2607 };
  const VOID_TOPO = 3, VOID_BASE = 573;
  const RECORTES = {
    'VO': [CORTES.antesV, CORTES.oI], 'VOI': [CORTES.antesV, CORTES.iD], 'VOID': [CORTES.antesV, CORTES.depoisReg],
    'I': [CORTES.oI, CORTES.iD], 'ID': [CORTES.oI, CORTES.depoisReg], 'D': [CORTES.iD, CORTES.depoisReg]
  };

  /* ---------- Mapa da Trilha (spec 6.11): raios 65/150/232, tangentes em x = 250 ---------- */
  const TRILHA = { tangente: 250, eixo: 280, raios: { start: 65, master: 150, pro: 232 } };

  /* ---------- órbitas (spec 6.10, medidas nos selos simples) ---------- */
  const ORBITA = {
    /* faixa = duas elipses iguais deslocadas no eixo menor (como no símbolo do selo) */
    start: { a: 1, b: 0.39, desloc: 0.24, separa: 0.75 },     /* conjunto 1,13 : 1 */
    master: { a: 1, b: 0.39, desloc: 0.24, separa: 0.75 },    /* o Start girado: 0,89 : 1 */
    pro: { a: 1, b: 0.63, desloc: 0.17, angulo: 32 },          /* ±32° da vertical, menor/maior 0,63 */
    voiders: { raios: [1, 0.72, 0.44] },
    interrupcao: 6                                               /* px no cruzamento do Pro */
  };

  const RODAPE = ['TATTOO ACADEMY', '® 2025', 'SÃO PAULO', 'BRAZIL', 'PREENCHA O VAZIO'];
  const RODAPE_CORRIDO = ['THE VOID TATTOO', '® 2025', 'SÃO PAULO', 'BRAZIL'];
  const MARCOS_START = [
    { nome: 'Ritual do Traço', angulo: 200 }, { nome: 'Primeira Pele', angulo: 250 }, { nome: 'Formatura com Pele', angulo: 300 }
  ];
  const ROTULO_PRODUTO = { start: 'THE VOID START', master: 'THE VOID MASTER', pro: 'THE VOID PRO' };
  const NOME_PRODUTO = { start: 'Start', master: 'Master', pro: 'Pro' };

  /* ---------- utilidades ---------- */
  const f = n => { const v = Math.round(n * 100) / 100; return (Object.is(v, -0) ? 0 : v).toString(); };
  const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const limita = (v, a, b) => Math.max(a, Math.min(b, v));
  function hash(s) { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return (h >>> 0).toString(36); }
  function aviso(msg) { api.ultimoAviso = msg; if (raiz.console && console.warn) console.warn('vforms: ' + msg); return msg; }
  function base(o) {
    let b = o.base != null ? o.base : api.config.base;
    if (b && !/\/$/.test(b)) b += '/';
    return b || '';
  }
  function tema(o) { return o.tema === 'leitura' || o.tema === 'claro' ? 'leitura' : 'sala'; }
  function estacao(o) { return ESTACOES.indexOf(o.estacao) >= 0 ? o.estacao : 'chamado'; }
  function grafismo(o) {
    const e = estacao(o);
    if (e === 'start' && o.superficie === 'coxia' && tema(o) === 'sala') return GRAFISMO_COXIA_START;
    return GRAFISMO[tema(o)][e];
  }
  function campoDe(o) { return /^#[0-9A-F]{6}$/i.test(o.campo || '') ? o.campo.toUpperCase() : (tema(o) === 'leitura' ? T.tela : T.sala); }
  function traco(cor, extra) { return 'stroke="' + cor.c + '"' + (cor.o < 1 ? ' stroke-opacity="' + f(cor.o) + '"' : '') + (extra || ''); }
  function preench(cor) { return 'fill="' + cor.c + '"' + (cor.o < 1 ? ' fill-opacity="' + f(cor.o) + '"' : ''); }

  /* abre o <svg> com acessibilidade; dims = [w, h]; px = [w, h] ou null */
  function abre(forma, o, vb, px, extra) {
    const id = o.id;
    const tam = px ? ' width="' + f(px[0]) + '" height="' + f(px[1]) + '"' : '';
    let acess;
    if (o.aria) acess = ' role="img" aria-labelledby="' + id + '-t"';
    else acess = ' aria-hidden="true" focusable="false"';
    const t = o.aria ? '<title id="' + id + '-t">' + esc(o.aria) + '</title>' : '';
    return '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="vf vf-' + forma + '" data-vforms-forma="' + forma + '" viewBox="' + vb.map(f).join(' ') + '"' + tam +
      ' preserveAspectRatio="' + (o.ajuste || 'xMidYMid meet') + '"' + acess + (extra || '') + '>' + t;
  }

  /* ============================== FORMAS ============================== */
  const FORMAS = {};

  /* ---- Grão do Vazio (6.1) ---- */
  FORMAS.grao = function (o) {
    const w = o.largura || 240, h = o.altura || 240, claro = tema(o) === 'leitura';
    const op = claro ? 0.04 : 0.06, mist = claro ? 'multiply' : 'screen';
    const id = o.id;
    let corpo;
    if (o.textura) {
      corpo = '<defs><pattern id="' + id + '-p" width="240" height="240" patternUnits="userSpaceOnUse"><image href="' + esc(o.textura) + '" width="240" height="240"/></pattern></defs>' +
        '<rect width="' + f(w) + '" height="' + f(h) + '" fill="url(#' + id + '-p)"/>';
    } else {
      corpo = '<defs><filter id="' + id + '-g" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">' +
        '<feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="' + (o.semente || 7) + '" stitchTiles="stitch"/>' +
        '<feColorMatrix type="saturate" values="0"/></filter></defs>' +
        '<rect width="' + f(w) + '" height="' + f(h) + '" filter="url(#' + id + '-g)"/>';
    }
    return abre('grao', o, [0, 0, w, h], o.fixo ? [w, h] : null, ' style="opacity:' + op + ';mix-blend-mode:' + mist + '"') + corpo + '</svg>';
  };

  /* ---- Esfera do Vazio (6.2): aerógrafo com grão real, sem máscara CSS ---- */
  FORMAS.esfera = function (o) {
    const claro = tema(o) === 'leitura';
    const cor = o.cor || (claro ? T.nanquim : T.penumbra);
    const op = o.opacidade != null ? o.opacidade : (claro ? 1 : 0.6);
    /* diâmetro do corpo (onde a tinta passa de 50%) em fração do quadro: 0,4 a 0,6 */
    const d = limita(o.diametro != null ? o.diametro : 0.56, 0.4, 0.6);
    const tam = o.tamanho || 600;               /* px na tela; regula o tamanho do grão */
    const r = d * 1000 / (2 * 0.66);            /* raio do halo inteiro */
    const freq = f(limita(tam / 1500, 0.12, 2.2));
    const id = o.id;
    if (o.png) {
      return abre('esfera', o, [0, 0, 1000, 1000], o.fixo ? [tam, tam] : null) +
        '<image href="' + esc(o.png) + '" x="' + f(500 - r) + '" y="' + f(500 - r) + '" width="' + f(2 * r) + '" height="' + f(2 * r) + '" opacity="' + f(op) + '"/></svg>';
    }
    const stops = [[0, 1], [0.38, 1], [0.5, 0.9], [0.62, 0.64], [0.74, 0.36], [0.86, 0.14], [1, 0]]
      .map(s => '<stop offset="' + s[0] + '" stop-color="' + T.nanquim + '" stop-opacity="' + s[1] + '"/>').join('');
    return abre('esfera', o, [0, 0, 1000, 1000], o.fixo ? [tam, tam] : null) +
      '<defs><radialGradient id="' + id + '-r" cx="500" cy="500" r="' + f(r) + '" gradientUnits="userSpaceOnUse">' + stops + '</radialGradient>' +
      '<filter id="' + id + '-s" x="0" y="0" width="1000" height="1000" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">' +
      '<feTurbulence type="fractalNoise" baseFrequency="' + freq + '" numOctaves="2" seed="' + (o.semente || 7) + '" result="t"/>' +
      '<feColorMatrix in="t" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1.2 0 0 0 0" result="n"/>' +
      '<feTurbulence type="fractalNoise" baseFrequency=".006" numOctaves="2" seed="3" result="lt"/>' +
      '<feColorMatrix in="lt" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0" result="l"/>' +
      '<feComposite in="SourceAlpha" in2="l" operator="arithmetic" k2="1" k3=".16" k4="-.08" result="a2"/>' +
      '<feComposite in="a2" in2="n" operator="arithmetic" k2="1.1" k3="1" k4="-.72" result="m"/>' +
      '<feComponentTransfer in="m" result="d"><feFuncA type="linear" slope="4" intercept="-1.05"/></feComponentTransfer>' +
      '<feComponentTransfer in="SourceAlpha" result="sv"><feFuncA type="gamma" amplitude=".9" exponent="1.7" offset="0"/></feComponentTransfer>' +
      '<feComposite in="sv" in2="d" operator="arithmetic" k1="-1" k2="1" k3="1" result="u"/>' +
      '<feFlood flood-color="' + cor + '" flood-opacity="' + f(op) + '"/><feComposite in2="u" operator="in"/></filter></defs>' +
      '<rect class="esfera-corpo" width="1000" height="1000" fill="url(#' + id + '-r)" filter="url(#' + id + '-s)"/></svg>';
  };

  /* ---- Eco do VOID (6.3): o arquivo oficial ampliado e desfocado ---- */
  FORMAS.eco = function (o) {
    const w = o.largura || 1200, h = o.altura || 600;
    if (w < 600) { aviso('Eco do VOID recusado: abaixo de 600 px de largura não existe Eco (spec 6.3).'); return ''; }
    if (o.texto) { aviso('Eco do VOID recusado: o logotipo é arquivo, nunca texto.'); return ''; }
    const src = o.src || (base(o) + 'assets/brand/svg/void-horizontal-' + (tema(o) === 'leitura' ? 'preto' : 'branco') + '.svg');
    const lw = 1.6 * w, lh = lw * 579 / 3804;
    const x = w / 2 + 0.288 * w - lw / 2, y = h / 2 - lh / 2;
    const blur = limita(w * 0.026, 18, 40);
    return abre('eco', o, [0, 0, w, h], o.fixo ? [w, h] : null, ' style="overflow:hidden"') +
      '<defs><filter id="' + o.id + '-b" filterUnits="userSpaceOnUse" x="0" y="0" width="' + f(w) + '" height="' + f(h) + '"><feGaussianBlur stdDeviation="' + f(blur) + '"/></filter></defs>' +
      '<g filter="url(#' + o.id + '-b)" opacity=".12"><image href="' + esc(src) + '" x="' + f(x) + '" y="' + f(y) + '" width="' + f(lw) + '" height="' + f(lh) + '"/></g></svg>';
  };

  /* ---- Janela de Luz (6.4) ---- */
  FORMAS.janela = function (o) {
    const w = o.largura || 1440, h = o.altura || 900;
    if (tema(o) === 'leitura') { aviso('Janela de Luz recusada: não existe no Modo Leitura (spec 6.4).'); return ''; }
    return abre('janela', o, [0, 0, w, h], o.fixo ? [w, h] : null, '') +
      '<defs><radialGradient id="' + o.id + '-j" cx="' + f(0.12 * w) + '" cy="0" r="' + f(1.1 * w) + '" gradientUnits="userSpaceOnUse" gradientTransform="translate(0 0) scale(1 ' + f((0.75 * h) / (1.1 * w)) + ')">' +
      '<stop offset="0" stop-color="' + T.tela + '" stop-opacity=".09"/><stop offset=".62" stop-color="' + T.tela + '" stop-opacity="0"/></radialGradient></defs>' +
      (o.campo === false ? '' : '<rect width="' + f(w) + '" height="' + f(h) + '" fill="' + T.sala + '"/>') +
      '<rect width="' + f(w) + '" height="' + f(h) + '" fill="url(#' + o.id + '-j)"/></svg>';
  };

  /* ---- Véu de Leitura (6.5) ---- */
  const VEUS = [0.48, 0.55, 0.62, 0.70, 0.75];
  FORMAS.veu = function (o) {
    const w = o.largura || 1080, h = o.altura || 1350, dir = o.direcao || 'esquerda';
    let grad, alvo;
    if (dir === 'uniforme') {
      let op = o.opacidade != null ? o.opacidade : 0.70;
      if (VEUS.indexOf(op) < 0) { aviso('Véu de ' + op + ' não está na tabela 3.4; usado o padrão de 0,70.'); op = 0.70; }
      return abre('veu', o, [0, 0, w, h], o.fixo ? [w, h] : null, ' preserveAspectRatio="none"') +
        '<rect width="' + f(w) + '" height="' + f(h) + '" fill="' + T.sala + '" fill-opacity="' + f(op) + '"/></svg>';
    }
    if (dir === 'base') { grad = 'x1="0" y1="1" x2="0" y2="0"'; alvo = [[0, 0.78], [0.38, 0.70], [0.70, 0]]; }
    else { grad = 'x1="0" y1="0" x2="1" y2="0"'; alvo = [[0, 0.78], [0.42, 0.70], [0.72, 0]]; }
    return abre('veu', o, [0, 0, w, h], o.fixo ? [w, h] : null, '') +
      '<defs><linearGradient id="' + o.id + '-v" ' + grad + '>' +
      alvo.map(s => '<stop offset="' + s[0] + '" stop-color="' + T.sala + '" stop-opacity="' + f(s[1]) + '"/>').join('') +
      '</linearGradient></defs><rect width="' + f(w) + '" height="' + f(h) + '" fill="url(#' + o.id + '-v)"/></svg>';
  };

  /* ---- Faixa Cinemascope (6.6): 1080 por 1350, faixa 1080 por 452 com topo em y = 449 ---- */
  function placeholderFoto(x, y, w, h, u, claro) {
    const tx = x + w / 2, ty = y + h / 2;
    return '<rect x="' + f(x) + '" y="' + f(y) + '" width="' + f(w) + '" height="' + f(h) + '" fill="' + (claro ? T.cinza100 : T.bastidor) + '"/>' +
      '<rect x="' + f(x + 12 * u) + '" y="' + f(y + 12 * u) + '" width="' + f(w - 24 * u) + '" height="' + f(h - 24 * u) + '" fill="none" stroke="' + T.fumaca + '" stroke-width="1" stroke-dasharray="6 6" vector-effect="non-scaling-stroke"/>' +
      '<text x="' + f(tx) + '" y="' + f(ty + 9 * u) + '" text-anchor="middle" fill="' + (claro ? T.ardosia : T.po) + '" font-family="' + FONTE_LETREIRO + '" font-size="' + f(26 * u) + '" font-weight="500" letter-spacing="' + f(26 * u * 0.18) + '" style="font-variation-settings:\'wdth\' 125">FOTO REAL DA ESCOLA, COM AUTORIZAÇÃO</text>';
  }
  FORMAS.cinemascope = function (o) {
    const W = 1080, H = o.formato === 'faixa' ? 452 : 1350;
    const fy = o.formato === 'faixa' ? 0 : 449, fh = 452;
    let s = abre('cinemascope', o, [0, 0, W, H], o.fixo ? [W, H] : null) + '<rect width="' + W + '" height="' + H + '" fill="' + T.nanquim + '"/>';
    if (o.foto) {
      s += '<image href="' + esc(o.foto) + '" x="0" y="' + fy + '" width="' + W + '" height="' + fh + '" preserveAspectRatio="xMidYMid slice"' + (o.alt ? '' : '') + '/>';
    } else s += placeholderFoto(0, fy, W, fh, 1, false);
    if (o.formato !== 'faixa') {
      if (o.titulo) {
        const linhas = String(o.titulo).toUpperCase().split('\n').slice(0, 3);
        const fs = 84, lh = fs * 0.92, y0 = fy - 72 - (linhas.length - 1) * lh;
        s += '<text fill="' + T.tela + '" font-family="' + FONTE_LETREIRO + '" font-size="' + fs + '" font-weight="800" letter-spacing="' + f(-0.02 * fs) + '" style="font-variation-settings:\'wdth\' 112">' +
          linhas.map((l, i) => '<tspan x="72" y="' + f(y0 + i * lh) + '">' + esc(l) + '</tspan>').join('') + '</text>';
      }
      if (o.credito) {
        s += '<text x="72" y="' + (fy + fh + 72 + 20) + '" fill="' + T.po + '" font-family="' + FONTE_LETREIRO + '" font-size="26" font-weight="500" letter-spacing="' + f(26 * 0.18) + '" style="font-variation-settings:\'wdth\' 125">' + esc(String(o.credito).toUpperCase()) + '</text>';
      }
    }
    return s + '</svg>';
  };

  /* ---- Corte do Logo (6.7): o arquivo oficial gigante, cortado só entre letras inteiras ---- */
  function corteGeometria(W, H, mostra) {
    const c = RECORTES[mostra];
    const s = W / (c[1] - c[0]);
    const alturaVoid = (VOID_BASE - VOID_TOPO) * s;
    return { escala: s, x: -c[0] * s, fracao: alturaVoid / H, corte: c };
  }
  FORMAS['corte-logo'] = function (o) {
    if (o.texto) { aviso('Corte do Logo recusado: o logotipo é arquivo, nunca texto redigitado.'); return ''; }
    const W = o.largura || 1080, H = o.altura || 1350;
    let mostra = o.mostra || 'auto';
    if (mostra !== 'auto' && !RECORTES[mostra]) { aviso('Corte "' + mostra + '" não existe: o corte cai sempre entre letras inteiras (VO, VOI, VOID, I, ID ou D).'); mostra = 'auto'; }
    if (mostra === 'auto') {
      /* escolhe o corte cuja altura do VOID fica entre 70% e 110% da peça, mais perto de 85% */
      let melhor = null;
      ['VO', 'VOI', 'VOID', 'ID'].forEach(k => {
        const g = corteGeometria(W, H, k);
        const dentro = g.fracao >= 0.7 && g.fracao <= 1.1;
        const nota = (dentro ? 0 : 10) + Math.abs(g.fracao - 0.85);
        if (!melhor || nota < melhor.nota) melhor = { k: k, nota: nota };
      });
      mostra = melhor.k;
    }
    const g = corteGeometria(W, H, mostra);
    if (g.fracao < 0.7 || g.fracao > 1.1) aviso('Corte do Logo: com "' + mostra + '" o VOID ocupa ' + Math.round(g.fracao * 100) + '% da altura da peça (a spec pede de 70% a 110%). Nesta proporção, nenhum corte entre letras inteiras alcança a faixa.');
    const claro = tema(o) === 'leitura' || o.campo === 'claro';
    const src = o.src || (base(o) + 'assets/brand/svg/void-horizontal-' + (claro ? 'preto' : 'branco') + '.svg');
    const lw = 3804 * g.escala, lh = 579 * g.escala;
    const ancora = o.ancora || 'centro';
    const yVoidTopo = ancora === 'topo' ? 0 : ancora === 'base' ? H - (VOID_BASE - VOID_TOPO) * g.escala : (H - (VOID_BASE - VOID_TOPO) * g.escala) / 2;
    const y = yVoidTopo - VOID_TOPO * g.escala;
    const op = o.textura ? 0.08 : 1;
    return abre('corte-logo', o, [0, 0, W, H], o.fixo ? [W, H] : null, ' style="overflow:hidden" data-corte="' + mostra + '" data-fracao="' + f(g.fracao) + '"') +
      '<defs><clipPath id="' + o.id + '-c"><rect width="' + W + '" height="' + H + '"/></clipPath></defs>' +
      '<g clip-path="url(#' + o.id + '-c)"><image href="' + esc(src) + '" x="' + f(g.x) + '" y="' + f(y) + '" width="' + f(lw) + '" height="' + f(lh) + '"' + (op < 1 ? ' opacity="' + op + '"' : '') + '/></g></svg>';
  };

  /* ---- Órbitas da Trilha (6.10) ---- */
  function amostraElipse(cx, cy, a, b, rotGraus, n) {
    const r = rotGraus * Math.PI / 180, cr = Math.cos(r), sr = Math.sin(r), pts = [];
    for (let i = 0; i < n; i++) {
      const t = 2 * Math.PI * i / n, x = a * Math.cos(t), y = b * Math.sin(t);
      pts.push([cx + x * cr - y * sr, cy + x * sr + y * cr]);
    }
    return pts;
  }
  function cruzaSeg(p1, p2, p3, p4) {
    const d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0]);
    if (Math.abs(d) < 1e-12) return null;
    const ua = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d;
    const ub = ((p3[0] - p1[0]) * (p2[1] - p1[1]) - (p3[1] - p1[1]) * (p2[0] - p1[0])) / d;
    if (ua < 0 || ua >= 1 || ub < 0 || ub >= 1) return null;
    return [p1[0] + ua * (p2[0] - p1[0]), p1[1] + ua * (p2[1] - p1[1])];
  }
  function cruzamentos(A, B) {
    const out = [];
    for (let i = 0; i < A.length; i++) {
      const a1 = A[i], a2 = A[(i + 1) % A.length];
      for (let j = 0; j < B.length; j++) {
        const p = cruzaSeg(a1, a2, B[j], B[(j + 1) % B.length]);
        if (p) out.push(p);
      }
    }
    return out;
  }
  /* caminho fechado, pulando os pontos perto das interrupções (fio que passa por baixo) */
  function caminho(pts, furos, folga) {
    let d = '', abre = true;
    const longe = p => furos.every(q => (p[0] - q[0]) * (p[0] - q[0]) + (p[1] - q[1]) * (p[1] - q[1]) > folga * folga);
    const ok = pts.map(longe);
    /* começa num ponto visível para o traço não emendar no meio de um furo */
    const ini = ok.indexOf(true); if (ini < 0) return '';
    if (ok.every(Boolean)) return pts.map((p, i) => (i ? 'L' : 'M') + f(p[0]) + ' ' + f(p[1])).join('') + 'Z';
    /* começa logo depois de um furo, para cada trecho visível ser um único subcaminho */
    let k0 = ini; while (ok[(k0 - 1 + pts.length) % pts.length]) k0 = (k0 + 1) % pts.length;
    for (let k = 0; k < pts.length; k++) {
      const i = (k0 + k) % pts.length;
      if (!ok[i]) { abre = true; continue; }
      d += (abre ? 'M' : 'L') + f(pts[i][0]) + ' ' + f(pts[i][1]);
      abre = false;
    }
    return d;
  }
  /* geometria normalizada das órbitas (centro em 0,0; altura total do conjunto = 2 * meiaAltura) */
  function geometriaOrbita(e) {
    const g = { elipses: [], meiaAltura: 1, meiaLargura: 1 };
    if (e === 'start' || e === 'master') {
      const q = ORBITA[e], gira = e === 'master';
      [-1, 1].forEach(lado => [-1, 1].forEach(fio => {
        const cy = lado * q.separa / 2 + fio * q.desloc / 2;
        g.elipses.push(gira ? { cx: cy, cy: 0, a: q.b, b: q.a, rot: 0, faixa: lado } : { cx: 0, cy: cy, a: q.a, b: q.b, rot: 0, faixa: lado });
      }));
      const mh = q.separa / 2 + q.desloc / 2 + q.b;
      if (gira) { g.meiaLargura = mh; g.meiaAltura = q.a; } else { g.meiaLargura = q.a; g.meiaAltura = mh; }
    } else if (e === 'pro') {
      const q = ORBITA.pro;
      [-1, 1].forEach(lado => [-1, 1].forEach(fio => {
        /* eixo maior a ±32° da vertical: em SVG, rot = 90 ± 32 a partir do eixo x */
        const rot = 90 + lado * q.angulo, rr = rot * Math.PI / 180;
        /* desloca no eixo menor */
        const nx = -Math.sin(rr), ny = Math.cos(rr), d = fio * q.desloc / 2;
        g.elipses.push({ cx: nx * d, cy: ny * d, a: q.a, b: q.b, rot: rot, faixa: lado });
      }));
      const s = Math.sin(q.angulo * Math.PI / 180), c = Math.cos(q.angulo * Math.PI / 180);
      g.meiaLargura = Math.sqrt(q.a * q.a * s * s + q.b * q.b * c * c) + q.desloc / 2;
      g.meiaAltura = Math.sqrt(q.a * q.a * c * c + q.b * q.b * s * s) + q.desloc / 2;
      g.angulo = q.angulo;
    } else if (e === 'voiders') {
      ORBITA.voiders.raios.forEach(r => g.elipses.push({ cx: 0, cy: 0, a: r, b: r, rot: 0, faixa: 0 }));
    }
    return g;
  }
  FORMAS.orbita = function (o) {
    const e = o.estacao && o.estacao !== 'chamado' ? o.estacao : null;
    if (!e || ESTACOES.indexOf(e) < 0) { aviso('Órbitas recusadas: o chamado (institucional) não tem órbita, só a Esfera (spec 3.5).'); return ''; }
    const w = o.largura || 1000, h = o.altura || 1000;
    const g = geometriaOrbita(e);
    const alt = (o.escala || 0.86) * Math.min(w, h);
    const k = alt / (2 * Math.max(g.meiaAltura, g.meiaLargura * (h >= w ? 1 : 1)));
    const cx = (o.cx != null ? o.cx : 0.5) * w, cy = (o.cy != null ? o.cy : 0.5) * h;
    const cor = o.cor === 'grafismo' ? grafismo(o) : NEUTRO[tema(o)].orbita;
    const tr = o.traco || 1.5;
    let s = abre('orbita', o, [0, 0, w, h], o.fixo ? [w, h] : null, ' data-estacao="' + e + '"') +
      '<g fill="none" ' + traco(cor, ' stroke-width="' + f(tr) + '" vector-effect="non-scaling-stroke" stroke-linecap="butt"') + '>';
    if (e === 'pro') {
      /* entrelaçado: nos 4 cruzamentos das faixas, uma passa por cima e a outra por baixo, alternando */
      const n = 480;
      const P = g.elipses.map(el => amostraElipse(cx + el.cx * k, cy + el.cy * k, el.a * k, el.b * k, el.rot, n));
      const centroA = amostraElipse(cx, cy, ORBITA.pro.a * k, ORBITA.pro.b * k, 90 - ORBITA.pro.angulo, n);
      const centroB = amostraElipse(cx, cy, ORBITA.pro.a * k, ORBITA.pro.b * k, 90 + ORBITA.pro.angulo, n);
      const regioes = cruzamentos(centroA, centroB)
        .map(p => ({ p: p, ang: Math.atan2(p[1] - cy, p[0] - cx) }))
        .sort((x, y) => x.ang - y.ang);
      const furos = P.map(() => []);
      const folga = (o.interrupcao || ORBITA.interrupcao) / 2 + tr;
      for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) {
        const A = g.elipses[i], B = g.elipses[j];
        if (A.faixa !== -1 || B.faixa !== 1) continue;
        cruzamentos(P[i], P[j]).forEach(p => {
          let melhor = 0, dm = Infinity;
          regioes.forEach((r, ri) => { const dd = Math.hypot(r.p[0] - p[0], r.p[1] - p[1]); if (dd < dm) { dm = dd; melhor = ri; } });
          /* regiões pares: a faixa da esquerda (-32°) passa por baixo; ímpares: a da direita */
          if (melhor % 2 === 0) furos[i].push(p); else furos[j].push(p);
        });
      }
      s += P.map((pts, i) => '<path d="' + caminho(pts, furos[i], folga) + '"/>').join('');
    } else {
      s += g.elipses.map(el => el.a === el.b ?
        '<circle cx="' + f(cx + el.cx * k) + '" cy="' + f(cy + el.cy * k) + '" r="' + f(el.a * k) + '"/>' :
        '<ellipse cx="' + f(cx + el.cx * k) + '" cy="' + f(cy + el.cy * k) + '" rx="' + f(el.a * k) + '" ry="' + f(el.b * k) + '"/>').join('');
    }
    return s + '</g></svg>';
  };

  /* ---- Mapa da Trilha (6.11) ---- */
  function geometriaMapa(vertical) {
    const R = TRILHA.raios, c = {};
    PRODUTOS.forEach(p => {
      c[p] = vertical ? { cx: 280, cy: 110 + R[p], r: R[p] } : { cx: TRILHA.tangente + R[p], cy: TRILHA.eixo, r: R[p] };
    });
    return vertical ?
      { vb: [0, 0, 560, 900], c: c, tangente: [280, 110], fimSeta: [280, 860] } :
      { vb: [0, 0, 1000, 560], c: c, tangente: [250, 280], fimSeta: [940, 280] };
  }
  FORMAS['mapa-trilha'] = function (o) {
    const vert = o.orientacao === 'vertical';
    const G = geometriaMapa(vert), th = tema(o), N = NEUTRO[th];
    const e = estacao(o);
    let ativa = o.ativa;
    if (!ativa && PRODUTOS.indexOf(e) >= 0) ativa = e;
    if (PRODUTOS.indexOf(ativa) < 0) ativa = null;
    const concl = (o.concluidas || []).filter(p => PRODUTOS.indexOf(p) >= 0);
    const gr = grafismo(Object.assign({}, o, { estacao: ativa || (concl.length ? 'voiders' : e) }));
    const grAtivo = ativa ? GRAFISMO[th][ativa] : gr;
    const aria = o.aria || ('Trilha da The VOID: Start, Master e Pro' + (ativa ? '. Você está no ' + NOME_PRODUTO[ativa] : '') +
      (concl.length ? '. Concluídas: ' + concl.map(p => NOME_PRODUTO[p]).join(', ') : '') + '.');
    const oo = Object.assign({}, o, { aria: o.decorativo ? null : aria });
    /* Piso de leitura: nenhum rótulo do mapa fica abaixo de 11 px reais. O desenho escala
       com o contêiner, então o corpo do texto em unidades do viewBox cresce na razão inversa
       (11 / escala). Se o nome não cabe mais no seu círculo, ele sai do SVG e vai para a
       legenda em HTML que o render() põe ao lado; o nome continua no aria-label. */
    const PISO = 11;
    const real = o.larguraReal > 0 ? o.larguraReal : 0;
    const esc1 = real ? real / G.vb[2] : 0;
    const piso = (base) => esc1 ? Math.max(base, PISO / esc1) : base;
    const fsNome = piso(22);
    /* corpo máximo que ainda cabe: START dentro do próprio círculo, acima do eixo (horizontal,
       medido: 3,09 em de largura) e na corda de 130 u (vertical) */
    const nomesCabem = fsNome <= (vert ? 40 : 33);
    const mostraNomes = nomesCabem && o.nomes !== false;
    const querAqui = !!(ativa && o.voceEstaAqui !== false && (o.voceEstaAqui || o['voce-esta-aqui']));
    const ROT_AQUI = 'VOCÊ ESTÁ AQUI';
    const fsAqui = piso(13);
    const lwAqui = ROT_AQUI.length * 0.954 * fsAqui;
    const aquiCabe = lwAqui <= (vert ? 540 : 984);
    /* na horizontal o rótulo fica embaixo dos círculos: o viewBox cresce o quanto o texto pedir */
    const baseAquiH = Math.max(550, 536 + 0.74 * fsAqui);
    const vb = G.vb.slice();
    if (!vert && querAqui && aquiCabe) vb[3] = Math.max(vb[3], Math.ceil(baseAquiH + 0.26 * fsAqui + 6));
    const fora = [];
    if (!mostraNomes && o.nomes !== false) fora.push('nomes');
    if (querAqui && !aquiCabe) fora.push('aqui');
    let s = abre('mapa-trilha', oo, vb, o.fixo ? [vb[2], vb[3]] : null, (ativa ? ' data-ativa="' + ativa + '"' : '') + ' data-orientacao="' + (vert ? 'vertical' : 'horizontal') + '"' +
      (fora.length ? ' data-fora="' + fora.join(' ') + '"' : '') + (esc1 ? ' data-piso="' + f(fsNome) + '"' : ''));
    s += '<g class="mt-linhas" fill="none" stroke="' + N.linha + '" stroke-width="1.5" vector-effect="non-scaling-stroke">';
    ['pro', 'master', 'start'].forEach(p => {
      const c = G.c[p], marcado = p === ativa || concl.indexOf(p) >= 0;
      const cor = p === ativa ? grAtivo : (marcado ? GRAFISMO[th][p] : null);
      s += '<circle class="c-' + p + '" cx="' + c.cx + '" cy="' + c.cy + '" r="' + c.r + '"' + (cor ? ' ' + traco(cor, ' stroke-width="2.5"') : '') + '/>';
    });
    const t = G.tangente, fim = G.fimSeta;
    if (vert) s += '<path d="M' + t[0] + ' ' + t[1] + 'V' + fim[1] + '"/><path d="M' + (fim[0] - 8) + ' ' + (fim[1] - 12) + 'L' + fim[0] + ' ' + fim[1] + 'L' + (fim[0] + 8) + ' ' + (fim[1] - 12) + '"/>';
    else s += '<path d="M' + t[0] + ' ' + t[1] + 'H' + fim[0] + '"/><path d="M' + (fim[0] - 12) + ' ' + (fim[1] - 8) + 'L' + fim[0] + ' ' + fim[1] + 'L' + (fim[0] - 12) + ' ' + (fim[1] + 8) + '"/>';
    s += '</g>';
    /* nomes na voz em off, caixa alta (exceção nomeada 4.6). Na horizontal, logo acima do
       eixo como no S30; na vertical, sobre o eixo, com uma placa do campo interrompendo a linha */
    const fundo = campoDe(o);
    const nomes = vert ?
      { start: [280, 175], master: [280, 325], pro: [280, 492] } :
      { start: [315, 270], master: [465, 270], pro: [632, 270] };
    const kN = fsNome / 22;
    if (mostraNomes) {
      if (vert) PRODUTOS.forEach(p => {
        const lw = (p.length * 13 + 16) * kN;
        s += '<rect x="' + f(nomes[p][0] - lw / 2) + '" y="' + f(nomes[p][1] - 16 * kN) + '" width="' + f(lw) + '" height="' + f(24 * kN) + '" fill="' + fundo + '"/>';
      });
      s += '<g class="mt-nomes" fill="' + N.nome + '" font-family="' + FONTE_OFF + '" font-style="italic" font-weight="300" font-size="' + f(fsNome) + '" text-anchor="middle" style="font-variation-settings:\'opsz\' 72">';
      PRODUTOS.forEach(p => { s += '<text x="' + nomes[p][0] + '" y="' + f(nomes[p][1] + (vert ? 4 * kN : 0)) + '"' + (p === ativa ? ' fill="' + (th === 'sala' ? T.tela : T.sala) + '"' : '') + '>' + p.toUpperCase() + '</text>'; });
      s += '</g>';
    }
    if (querAqui) {
      /* o ponto no círculo ativo e um fio até fora dos três círculos, onde fica o rótulo */
      const c = G.c[ativa];
      const pt = vert ? [c.cx + c.r * Math.cos(Math.PI / 6), c.cy + c.r * Math.sin(Math.PI / 6)] : [c.cx, c.cy + c.r];
      const fim = vert ? [pt[0], 600] : [pt[0], 528];
      const rot = ROT_AQUI, lw = lwAqui;
      /* vertical: à direita do eixo quando cabe; se o piso pedir mais, centrado no eixo
         com uma placa do campo interrompendo a linha (como os nomes) */
      const aoLado = vert && lw <= 548 - 296;
      const lb = vert ?
        (aoLado ? [Math.max(296, Math.min(pt[0], 548 - lw)), Math.max(622, 608 + 0.74 * fsAqui)] : [280, 610 + 0.74 * fsAqui]) :
        [Math.max(lw / 2 + 8, Math.min(vb[2] - lw / 2 - 8, pt[0])), baseAquiH];
      const ancora = vert && aoLado ? 'start' : 'middle';
      const placa = vert && !aoLado && aquiCabe ? '<rect x="' + f(280 - lw / 2 - 8) + '" y="' + f(lb[1] - 0.86 * fsAqui) + '" width="' + f(lw + 16) + '" height="' + f(1.2 * fsAqui) + '" fill="' + fundo + '"/>' : '';
      s += '<g class="mt-aqui">' +
        '<path d="M' + f(pt[0]) + ' ' + f(pt[1]) + 'V' + fim[1] + '" fill="none" ' + traco(grAtivo, ' stroke-width="1" stroke-dasharray="2 4" vector-effect="non-scaling-stroke"') + '/>' +
        '<circle cx="' + f(pt[0]) + '" cy="' + f(pt[1]) + '" r="7" ' + preench(grAtivo) + '/>' +
        '<circle cx="' + f(pt[0]) + '" cy="' + f(pt[1]) + '" r="12" fill="none" ' + traco(grAtivo, ' stroke-width="1" vector-effect="non-scaling-stroke"') + '/>' +
        (aquiCabe ? placa + '<text x="' + f(lb[0]) + '" y="' + f(lb[1]) + '" text-anchor="' + ancora + '" fill="' + (th === 'sala' ? T.po : T.ardosia) + '" font-family="' + FONTE_LETREIRO + '" font-size="' + f(fsAqui) + '" font-weight="500" letter-spacing="' + f(fsAqui * 0.177) + '" style="font-variation-settings:\'wdth\' 125">' + rot + '</text>' : '') + '</g>';
    }
    if (o.frases && o.frasesSvg) {
      /* versão para exportar como arquivo (no HTML, as frases vão em texto real fora do SVG) */
      const cr = 'fill="' + N.forte + '" font-family="' + FONTE_LETREIRO + '" font-size="16" font-weight="500" letter-spacing="2.9" style="font-variation-settings:\'wdth\' 125"';
      s += vert ?
        '<text ' + cr + ' x="40" y="60">ESSE É O VAZIO</text><text ' + cr + ' x="300" y="720">ESSE É O CAMINHO</text><text ' + cr + ' x="300" y="744">PARA PREENCHÊ-LO</text>' :
        '<text ' + cr + ' x="40" y="140">ESSE É O VAZIO</text><text ' + cr + ' x="740" y="236">ESSE É O CAMINHO</text><text ' + cr + ' x="740" y="260">PARA PREENCHÊ-LO</text>';
    }
    if (o.frases && !vert) {
      /* a seta curva do S30, do "ESSE É O VAZIO" até o ponto de tangência */
      s += '<g class="mt-seta-vazio" fill="none" stroke="' + N.forte + '" stroke-width="1.2" vector-effect="non-scaling-stroke"><path d="M118 160C128 222 178 252 240 262"/><path d="M230 255L240 262L229 268"/></g>';
    }
    return s + '</svg>';
  };

  /* ---- Marcador de Estação (6.12): mini Mapa da Trilha de 14 px ---- */
  FORMAS['marcador-estacao'] = function (o) {
    const th = tema(o), e = estacao(o), N = NEUTRO[th];
    const ativa = PRODUTOS.indexOf(o.ativa || e) >= 0 ? (o.ativa || e) : null;
    const tam = o.tamanho || 14;
    const g = geometriaMapa(false);
    const pad = 14;
    const vb = [TRILHA.tangente - pad, TRILHA.eixo - 232 - pad, 464 + 2 * pad, 464 + 2 * pad];
    let s = abre('marcador-estacao', o, vb, [tam, tam], ' style="display:inline-block;vertical-align:-2px;flex:none"');
    s += '<g fill="none" stroke="' + (th === 'sala' ? T.po : T.ardosia) + '" stroke-width="1" vector-effect="non-scaling-stroke">';
    ['pro', 'master', 'start'].forEach(p => {
      const c = g.c[p];
      const cheio = p === ativa ? GRAFISMO[th][p] : null;
      s += '<circle cx="' + c.cx + '" cy="' + c.cy + '" r="' + c.r + '"' + (cheio ? ' ' + preench(cheio) + ' ' + traco(cheio) : '') + '/>';
    });
    return s + '</g></svg>';
  };

  /* ---- Marcador de Capítulo (6.12) ---- */
  function textoCapitulo(o) {
    const dd = n => (n < 10 ? '0' : '') + Math.max(0, Math.floor(n || 0));
    const tit = o.titulo ? ' · ' + String(o.titulo).toUpperCase() : '';
    if (o.formato === 'carrossel') {
      const mostraTotal = o.total && (o.numero === 1 || o.numero === o.total || o.mostrarTotal);
      return dd(o.numero) + (mostraTotal ? ' / ' + dd(o.total) : '') + tit;
    }
    return 'CAPÍTULO ' + dd(o.numero) + tit;
  }
  FORMAS['marcador-capitulo'] = function (o) {
    const txt = textoCapitulo(o), u = o.u || 1, fs = (o.peca ? 26 : 12) * u;
    const w = 24 * u + 12 * u + txt.length * fs * 0.86, h = fs * 1.6;
    const cor = tema(o) === 'leitura' ? T.ardosia : T.po;
    return abre('marcador-capitulo', o, [0, 0, w, h], [w, h]) +
      '<rect x="0" y="' + f(h / 2 - 0.5 * u) + '" width="' + f(24 * u) + '" height="' + f(u) + '" fill="' + cor + '"/>' +
      '<text x="' + f(36 * u) + '" y="' + f(h / 2 + fs * 0.36) + '" fill="' + cor + '" font-family="' + FONTE_LETREIRO + '" font-size="' + f(fs) + '" font-weight="500" letter-spacing="' + f(fs * 0.18) + '" style="font-variation-settings:\'wdth\' 125">' + esc(txt) + '</text></svg>';
  };

  /* ---- Anel de Preenchimento (6.19): o Mapa da Trilha pessoal da área de membros ---- */
  function marcosDe(o, atual) {
    if (o.marcos && o.marcos.length) return o.marcos;
    return atual === 'start' ? MARCOS_START.map(m => ({ nome: m.nome, angulo: m.angulo, validado: false })) : [];
  }
  FORMAS.anel = function (o) {
    const th = tema(o), N = NEUTRO[th], G = geometriaMapa(false);
    const concl = (o.concluidas || []).filter(p => PRODUTOS.indexOf(p) >= 0);
    const atual = PRODUTOS.indexOf(o.atual) >= 0 ? o.atual : null;
    const marcos = atual ? marcosDe(o, atual) : [];
    const validados = marcos.filter(m => m.validado === true).length;
    const aria = o.aria || ('Anel de Preenchimento' + (concl.length ? ': formação ' + concl.map(p => NOME_PRODUTO[p]).join(' e ') + ' concluída' : '') +
      (atual ? '; formação ' + NOME_PRODUTO[atual] + ' em curso, ' + validados + ' de ' + marcos.length + ' marcos validados' : '') + '.');
    const oo = Object.assign({}, o, { aria: aria });
    const vb = [228, 26, 508, 508];
    let s = abre('anel', oo, vb, o.fixo ? [vb[2], vb[3]] : null, ' data-validados="' + validados + '"');
    s += '<defs><filter id="' + o.id + '-g" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">' +
      '<feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2" seed="7" result="t"/>' +
      '<feColorMatrix in="t" type="matrix" values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 .5 0 0 0 -.18"/>' +
      '<feComposite in2="SourceAlpha" operator="in"/></filter></defs>';
    /* formações concluídas: cheias, da maior para a menor, com grão */
    ['pro', 'master', 'start'].forEach(p => {
      if (concl.indexOf(p) < 0) return;
      const c = G.c[p];
      s += '<circle cx="' + c.cx + '" cy="' + c.cy + '" r="' + c.r + '" fill="' + COR_FORMACAO[p] + '"/>' +
        '<circle cx="' + c.cx + '" cy="' + c.cy + '" r="' + c.r + '" fill="' + COR_FORMACAO[p] + '" filter="url(#' + o.id + '-g)"/>';
    });
    s += '<g fill="none" stroke="' + N.linha + '" stroke-width="1.5" vector-effect="non-scaling-stroke">';
    ['pro', 'master', 'start'].forEach(p => {
      const c = G.c[p];
      const cor = p === atual ? GRAFISMO[th][p] : (concl.indexOf(p) >= 0 ? { c: th === 'sala' ? T.tela : T.sala, o: 0.5 } : null);
      s += '<circle cx="' + c.cx + '" cy="' + c.cy + '" r="' + c.r + '"' + (cor ? ' ' + traco(cor, ' stroke-width="' + (p === atual ? 2.5 : 1.5) + '"') : '') + '/>';
    });
    s += '</g>';
    if (atual) {
      const c = G.c[atual], cor = GRAFISMO[th][atual];
      marcos.forEach((m, i) => {
        /* graus na convenção do SVG: sentido horário a partir da direita; 180° é o ponto de
           tangência, então 200°, 250° e 300° sobem pela esquerda e passam por cima */
        const a = (m.angulo != null ? m.angulo : 200 + i * 50) * Math.PI / 180;
        const x = c.cx + c.r * Math.cos(a), y = c.cy + c.r * Math.sin(a);
        const ok = m.validado === true;
        s += '<circle class="vf-marco' + (ok && o.animar ? ' vf-assenta' : '') + '" data-validado="' + ok + '" cx="' + f(x) + '" cy="' + f(y) + '" r="12" ' +
          (ok ? preench(cor) + ' ' + traco(cor, ' stroke-width="1.5"') : 'fill="' + campoDe(o) + '" ' + traco(cor, ' stroke-width="1.5" stroke-dasharray="2 3"')) +
          ' vector-effect="non-scaling-stroke"><title>' + esc(m.nome) + ': ' + (ok ? 'validado' : 'pendente') + '</title></circle>';
      });
    }
    return s + '</svg>';
  };

  /* ---- Selo (5.6): arquivo oficial, mínimos e disco do Pro ---- */
  function rotuloProduto(o, p) {
    const claro = tema(o) === 'leitura';
    return '<span class="vf-rotulo" data-vforms-motivo="selo-abaixo-de-96" style="display:inline-block;padding:6px 10px;border:1px solid ' + T.fumaca +
      ';border-radius:0;color:' + (claro ? T.sala : T.tela) + ';font:500 12px/1.2 ' + FONTE_LETREIRO + ';font-variation-settings:\'wdth\' 125;letter-spacing:.18em;text-transform:uppercase;max-width:100%;box-sizing:border-box">' + ROTULO_PRODUTO[p] + '</span>';
  }
  FORMAS.selo = function (o) {
    const p = PRODUTOS.indexOf(o.produto) >= 0 ? o.produto : (PRODUTOS.indexOf(o.estacao) >= 0 ? o.estacao : null);
    if (!p) { aviso('Selo recusado: selo só existe para Start, Master e Pro, nunca em peça institucional (spec 5.6).'); return ''; }
    const d = o.tamanho || 200;
    if (d < 96) { aviso('Selo recusado: abaixo de 96 px não existe selo (spec 5.2). Saiu o Rótulo de Produto.'); return rotuloProduto(o, p); }
    let tipo = o.tipo || (d >= 200 ? 'completo' : 'simples');
    if (tipo === 'completo' && d < 200) { aviso('Selo completo abaixo de 200 px vira selo simples (spec 5.2).'); tipo = 'simples'; }
    const src = o.src || (base(o) + 'assets/brand/svg/selo-' + tipo + '-' + p + '.svg');
    const disco = p === 'pro' && tipo === 'simples' && tema(o) === 'sala' && o.disco !== false;
    const folga = disco ? 0.04 * d : 0;
    const L = d + 2 * folga;
    const aria = o.aria === undefined ? 'Selo The VOID ' + NOME_PRODUTO[p] : o.aria;
    let s = abre('selo', Object.assign({}, o, { aria: aria }), [0, 0, L, L], [L, L], ' data-produto="' + p + '" data-tipo="' + tipo + '"' + (disco ? ' data-disco="coxia"' : ''));
    if (disco) s += '<circle class="vf-disco" cx="' + f(L / 2) + '" cy="' + f(L / 2) + '" r="' + f(L / 2) + '" fill="' + T.coxia + '"/>';
    return s + '<image href="' + esc(src) + '" x="' + f(folga) + '" y="' + f(folga) + '" width="' + f(d) + '" height="' + f(d) + '"/></svg>';
  };

  /* ---- Logotipo: só por arquivo ---- */
  FORMAS.logotipo = function (o) {
    if (o.texto) { aviso('Logotipo recusado: THE VOID nunca é redigitado; use o arquivo oficial (spec 5.1).'); return ''; }
    const v = ['horizontal', 'vertical', 'start', 'master', 'pro'].indexOf(o.versao) >= 0 ? o.versao : 'horizontal';
    const cor = o.cor === 'preto' || (o.cor == null && tema(o) === 'leitura') ? 'preto' : 'branco';
    const m = MARCA[v], arq = v === 'horizontal' || v === 'vertical' ? 'void-' + v : 'void-' + v;
    const src = o.src || (base(o) + 'assets/brand/svg/' + arq + '-' + cor + '.svg');
    const altura = o.altura || (v === 'vertical' ? 80 : 24);
    const minimo = v === 'vertical' ? 80 : 24;
    if (altura < minimo) aviso('Logotipo abaixo do mínimo (' + minimo + ' px de altura): use o favicon (spec 5.2).');
    const largura = altura * m.vb[0] / m.vb[1];
    return abre('logotipo', Object.assign({}, o, { aria: o.aria === undefined ? 'The VOID Tattoo Academy' : o.aria }), [0, 0, m.vb[0], m.vb[1]], [largura, altura]) +
      '<image href="' + esc(src) + '" width="' + m.vb[0] + '" height="' + m.vb[1] + '"/></svg>';
  };

  /* ---- Área de proteção (5.2): diagrama medido do marca.json ---- */
  FORMAS['area-protecao'] = function (o) {
    const th = tema(o), N = NEUTRO[th];
    const v = o.versao === 'selo' ? 'selo' : (MARCA[o.versao] ? o.versao : 'horizontal');
    const acento = th === 'sala' ? T.areia : T.terracotaFunda;
    const cotaFonte = 'font-family="' + FONTE_LETREIRO + '" font-weight="500" style="font-variation-settings:\'wdth\' 125"';
    let s, vb;
    if (v === 'selo') {
      const p = PRODUTOS.indexOf(o.produto) >= 0 ? o.produto : 'start', D = 770, m = 0.125 * D, pad = 150;
      vb = [-m - pad, -m - pad, D + 2 * m + 2 * pad, D + 2 * m + 2 * pad];
      const src = o.src || (base(o) + 'assets/brand/svg/selo-simples-' + p + '.svg');
      s = abre('area-protecao', Object.assign({}, o, { aria: o.aria || 'Área de proteção do selo: 12,5% do diâmetro livre em volta do círculo.' }), vb, null, ' data-versao="selo"');
      s += '<circle cx="385" cy="385" r="' + f(385 + m) + '" fill="' + (th === 'sala' ? T.tela : T.sala) + '" fill-opacity=".05" stroke="' + acento + '" stroke-width="1.5" stroke-dasharray="8 6" vector-effect="non-scaling-stroke"/>';
      if (p === 'pro' && th === 'sala') s += '<circle cx="385" cy="385" r="' + f(385 + 0.04 * D) + '" fill="' + T.coxia + '"/>';
      s += '<image href="' + esc(src) + '" width="770" height="770"/>';
      s += '<g stroke="' + acento + '" stroke-width="1.5" vector-effect="non-scaling-stroke"><path d="M770 385H' + f(770 + m) + '"/><path d="M770 370V400M' + f(770 + m) + ' 370V400"/></g>';
      s += '<text x="' + f(770 + m / 2) + '" y="350" text-anchor="middle" fill="' + acento + '" font-size="40" ' + cotaFonte + '>12,5%</text>';
      return s + '</svg>';
    }
    const M = MARCA[v], X = M.X, b = M.bbox, pad = X * 0.9;
    vb = [b[0] - X - pad, b[1] - X - pad, (b[2] - b[0]) + 2 * X + 2 * pad, (b[3] - b[1]) + 2 * X + 2 * pad];
    const cor = th === 'sala' ? 'branco' : 'preto';
    const arq = v === 'horizontal' || v === 'vertical' ? 'void-' + v : 'void-' + v;
    const src = o.src || (base(o) + 'assets/brand/svg/' + arq + '-' + cor + '.svg');
    s = abre('area-protecao', Object.assign({}, o, { aria: o.aria || 'Área de proteção do logotipo: 1 X livre em todos os lados, X igual à altura das maiúsculas do THE.' }), vb, null, ' data-versao="' + v + '"');
    const zx = b[0] - X, zy = b[1] - X, zw = b[2] - b[0] + 2 * X, zh = b[3] - b[1] + 2 * X;
    s += '<rect x="' + f(zx) + '" y="' + f(zy) + '" width="' + f(zw) + '" height="' + f(zh) + '" fill="' + (th === 'sala' ? T.tela : T.sala) + '" fill-opacity=".05" stroke="' + acento + '" stroke-width="1.5" stroke-dasharray="8 6" vector-effect="non-scaling-stroke"/>';
    s += '<rect x="' + f(b[0]) + '" y="' + f(b[1]) + '" width="' + f(b[2] - b[0]) + '" height="' + f(b[3] - b[1]) + '" fill="none" stroke="' + N.linha + '" stroke-width="1" vector-effect="non-scaling-stroke"/>';
    /* quadrados X nos quatro cantos */
    [[zx, zy], [b[2], zy], [zx, b[3]], [b[2], b[3]]].forEach(q => {
      s += '<rect x="' + f(q[0]) + '" y="' + f(q[1]) + '" width="' + f(X) + '" height="' + f(X) + '" fill="' + acento + '" fill-opacity=".14" stroke="' + acento + '" stroke-width="1" vector-effect="non-scaling-stroke"/>' +
        '<text x="' + f(q[0] + X / 2) + '" y="' + f(q[1] + X / 2 + X * 0.16) + '" text-anchor="middle" fill="' + acento + '" font-size="' + f(X * 0.42) + '" ' + cotaFonte + '>X</text>';
    });
    s += '<image href="' + esc(src) + '" width="' + M.vb[0] + '" height="' + M.vb[1] + '"/>';
    /* guias do X: topo e base das maiúsculas do THE, levadas até a borda da área */
    if (v !== 'vertical') {
      s += '<g stroke="' + acento + '" stroke-width="1" stroke-dasharray="2 4" vector-effect="non-scaling-stroke">' +
        '<path d="M' + f(zx) + ' 187H' + f(b[0] + 560) + '"/><path d="M' + f(zx) + ' 381H' + f(b[0] + 560) + '"/></g>';
    }
    return s + '</svg>';
  };

  /* ---- Créditos Finais (6.15): texto literal, único ---- */
  FORMAS.rodape = function (o) {
    const corrido = o.variante === 'corrido';
    const partes = corrido ? RODAPE_CORRIDO : RODAPE;
    const claro = tema(o) === 'leitura';
    const corBase = claro ? T.ardosia : T.po, corFim = claro ? T.sala : T.tela;
    const fs = o.peca ? 26 : 12;
    const w = o.largura || (o.peca ? 1080 : 760), h = fs * 2.4;
    let s = abre('rodape', o, [0, 0, w, h], o.fixo ? [w, h] : null) +
      '<text x="' + (o.alinhar === 'esquerda' ? (o.peca ? 72 : 0) : f(w / 2)) + '" y="' + f(h / 2 + fs * 0.36) + '" text-anchor="' + (o.alinhar === 'esquerda' ? 'start' : 'middle') + '" fill="' + corBase + '" font-family="' + FONTE_LETREIRO + '" font-size="' + fs + '" font-weight="500" letter-spacing="' + f(fs * 0.18) + '" style="font-variation-settings:\'wdth\' 125">';
    partes.forEach((p, i) => {
      if (i) s += '<tspan dx="' + f(fs * 0.9) + '">·</tspan><tspan dx="' + f(fs * 0.9) + '"';
      else s += '<tspan';
      const ultimo = !corrido && i === partes.length - 1;
      s += (ultimo ? ' fill="' + corFim + '" font-weight="700"' : '') + '>' + esc(p) + '</tspan>';
    });
    return s + '</text></svg>';
  };
  function rodapeHTML(o) {
    const corrido = o.variante === 'corrido';
    const partes = corrido ? RODAPE_CORRIDO : RODAPE;
    /* cada termo vai com o separador que o antecede num grupo que não quebra por dentro
       ("® 2025" e "SÃO PAULO" nunca se partem). As quebras são desenhadas, nunca deixadas
       ao acaso; ajustaRodape() mede a largura disponível e escolhe:
         1 linha  quando tudo cabe;
         3 linhas TATTOO ACADEMY · ® 2025 / SÃO PAULO · BRAZIL / PREENCHA O VAZIO;
         4 linhas abaixo disso, também antes de ® 2025.
       A quebra da spec (depois de BRAZIL) vale sempre que a linha não cabe inteira; o
       separador que começaria uma linha some. */
    const linha = partes.map((p, i) => {
      const ultimo = !corrido && i === partes.length - 1;
      const sep = i ? '<span class="vf-sep" aria-hidden="true">·</span>' : '';
      const q = corrido || !i ? '' : ultimo ? 'fim' : p === 'SÃO PAULO' ? 'meio' : p === '® 2025' ? 'curta' : '';
      return (q ? '<span class="vf-quebra vf-q-' + q + '"></span>' : '') + '<span class="vf-grupo">' + sep + '<span class="vf-termo' + (ultimo ? ' vf-fim' : '') + '">' + esc(p) + '</span></span>';
    }).join('');
    if (!corrido) return '<p class="vf-rodape credito">' + linha + '</p>';
    /* Letreiro Corrido: o mesmo texto repetido, em loop a 40 px por segundo */
    const bloco = '<span class="vf-corrido-bloco">' + linha + '<span class="vf-sep" aria-hidden="true">·</span></span>';
    return '<div class="vf-corrido credito" role="marquee" aria-label="' + esc(RODAPE_CORRIDO.join(', ')) + '"><div class="vf-corrido-trilho" aria-hidden="true">' + bloco + bloco + bloco + bloco + '</div></div>';
  }

  /* testa os desenhos de linha na diagramação real (1, depois 3, depois 4 linhas) e fica
     com o primeiro em que nenhum grupo quebrou sozinho: a altura do parágrafo tem de ser
     exatamente o número de linhas previsto, e nenhuma linha pode passar da largura (os
     grupos não têm espaço entre si, então uma linha longa não quebra: estoura) */
  function ajustaRodape(el) {
    const p = el.querySelector('.vf-rodape');
    if (!p) return;
    p.removeAttribute('data-linhas');
    if (!p.clientWidth) return;
    const lh = parseFloat(getComputedStyle(p).lineHeight) || 19.2;
    const n = [1, 3, 4].find(k => { p.setAttribute('data-linhas', String(k)); return p.clientHeight <= k * lh + 1 && p.scrollWidth <= p.clientWidth + 1; });
    p.setAttribute('data-linhas', String(n || 4));
  }

  /* vector-effect não é herdado: cada forma de linha recebe o atributo, para o traço
     ficar com a espessura pedida em qualquer tamanho */
  const TRACO_FIXO = ['orbita', 'mapa-trilha', 'marcador-estacao', 'anel', 'area-protecao', 'cinemascope'];
  Object.keys(FORMAS).forEach(n => {
    if (TRACO_FIXO.indexOf(n) < 0) return;
    const fn = FORMAS[n];
    FORMAS[n] = o => fn(o).replace(/<(circle|ellipse|path|rect)\b(?![^>]*vector-effect)/g, '<$1 vector-effect="non-scaling-stroke"');
  });
  const NOMES = Object.keys(FORMAS);

  /* ============================== CSS do motor ============================== */
  const CSS = [
    '.vf-host{position:relative}',
    '.vf-camada{position:absolute;inset:0;z-index:0;pointer-events:none;overflow:hidden}',
    '.vf-camada>svg{display:block;width:100%;height:100%}',
    '.vf-host>:not(.vf-camada){position:relative;z-index:2}',
    'svg.vf{max-width:100%}',
    '.vf-bloco{display:block;width:100%;height:auto}',
    '.vf-mapa{position:relative;margin:0;container-type:inline-size}',
    '.vf-mapa .vf-frase{position:absolute;margin:0;color:var(--tela,#F8F9F4);font:500 12px/1.35 var(--font-letreiro,Archivo,Arial,sans-serif);font-variation-settings:"wdth" 125;letter-spacing:.18em;text-transform:uppercase}',
    '.modo-leitura .vf-mapa .vf-frase{color:var(--sala,#181818)}',
    '.vf-mapa[data-orientacao="horizontal"] .vf-vazio{left:2%;top:18%;max-width:22%}',
    '.vf-mapa[data-orientacao="horizontal"] .vf-caminho{left:74%;top:38%;max-width:26%}',
    '.vf-mapa[data-orientacao="vertical"] .vf-vazio{left:0;top:0}',
    '.vf-mapa[data-orientacao="vertical"] .vf-caminho{right:0;top:76%;width:47%}',
    '@container (max-width:640px){.vf-mapa[data-orientacao="horizontal"] .vf-frase{position:static;max-width:none;margin-top:8px}.vf-mapa .mt-seta-vazio{display:none}}',
    '.vf-mapa .vf-inteira{white-space:nowrap}',
    /* vertical estreito: a coluna à direita do eixo não comporta PREENCHÊ-LO; as frases descem para o fluxo */
    '@container (max-width:300px){.vf-mapa[data-orientacao="vertical"] .vf-frase{position:static;width:auto;max-width:none;margin-top:8px}}',
    '.vf-mapa-legenda{display:flex;flex-wrap:wrap;justify-content:center;gap:4px 1.6em;margin:8px 0 0;color:var(--po,#B4B5B0);font:500 12px/1.4 var(--font-letreiro,Archivo,Arial,sans-serif);font-variation-settings:"wdth" 125;letter-spacing:.18em;text-transform:uppercase}',
    '.vf-mapa-legenda .vf-termo{white-space:nowrap}',
    '.vf-mapa-legenda .vf-ativa{color:var(--tela,#F8F9F4);font-weight:700}',
    '.vf-mapa-legenda .vf-aqui{font-weight:500;text-transform:none;letter-spacing:.04em}',
    '.vf-mapa[data-tema="leitura"] .vf-mapa-legenda{color:var(--ardosia,#3F4E4F)}.vf-mapa[data-tema="leitura"] .vf-mapa-legenda .vf-ativa{color:var(--sala,#181818)}',
    '.vf-marcador{display:inline-flex;align-items:center;gap:8px}',
    '.vf-capitulo{display:inline-flex;align-items:center;gap:12px}',
    '.vf-capitulo .vf-fio{display:inline-block;width:24px;height:1px;background:currentColor}',
    '.vf-rodape{margin:0;color:var(--po,#B4B5B0);font:500 12px/1.6 var(--font-letreiro,Archivo,Arial,sans-serif);font-variation-settings:"wdth" 125;letter-spacing:.18em;text-transform:uppercase}',
    '.vf-rodape .vf-sep,.vf-corrido .vf-sep{margin:0 .9em}',
    '.vf-rodape .vf-fim{color:var(--tela,#F8F9F4);font-weight:700}',
    '.modo-leitura .vf-rodape{color:var(--ardosia,#3F4E4F)}.modo-leitura .vf-rodape .vf-fim{color:var(--sala,#181818)}',
    '.vf-rodape .vf-grupo,.vf-corrido .vf-grupo{white-space:nowrap}',
    '.vf-rodape .vf-quebra{display:none}',
    '.vf-rodape[data-linhas="3"] :is(.vf-q-meio,.vf-q-fim),.vf-rodape[data-linhas="4"] .vf-quebra{display:block;height:0}',
    '.vf-rodape[data-linhas="3"] :is(.vf-q-meio,.vf-q-fim)+.vf-grupo>.vf-sep,.vf-rodape[data-linhas="4"] .vf-quebra+.vf-grupo>.vf-sep{display:none}',
    /* sem medida (contêiner ainda invisível): no celular, o desenho de 3 linhas */
    '@media (max-width:430px){.vf-rodape:not([data-linhas]) :is(.vf-q-meio,.vf-q-fim){display:block;height:0}.vf-rodape:not([data-linhas]) :is(.vf-q-meio,.vf-q-fim)+.vf-grupo>.vf-sep{display:none}}',
    '.vf-corrido{overflow:hidden;white-space:nowrap;min-height:48px;display:flex;align-items:center;color:var(--po,#B4B5B0);font:500 12px/1 var(--font-letreiro,Archivo,Arial,sans-serif);font-variation-settings:"wdth" 125;letter-spacing:.18em}',
    '.vf-corrido-trilho{display:inline-flex;animation:vf-correr var(--vf-duracao,40s) linear infinite}',
    '.vf-corrido:hover .vf-corrido-trilho{animation-play-state:paused}',
    '@keyframes vf-correr{from{transform:translateX(0)}to{transform:translateX(-25%)}}',
    '.vf-anel-fig{margin:0}',
    '.vf-anel-legenda{list-style:none;margin:12px 0 0;padding:0;display:grid;gap:8px;font:400 15px/1.5 var(--font-texto,"Nunito Sans",Arial,sans-serif);color:var(--cal,#DCDDD8)}',
    '.modo-leitura .vf-anel-legenda{color:var(--sala,#181818)}',
    '.vf-anel-legenda li{display:flex;align-items:center;gap:8px}',
    '.vf-anel-legenda svg{width:20px;height:20px;flex:none;fill:none;stroke:currentColor;stroke-width:1.5;stroke-linecap:square;stroke-linejoin:miter}',
    '.vf-anel-legenda b{font-weight:600}',
    '.vf-assenta{animation:vf-assentar var(--t-anel,1200ms) var(--curva-foco,cubic-bezier(.65,0,.35,1)) both}',
    '@keyframes vf-assentar{from{opacity:0}to{opacity:1}}',
    '.vf-recusa{display:block;font:400 13px/1.4 var(--font-texto,"Nunito Sans",Arial,sans-serif);color:var(--po,#B4B5B0)}',
    '@media (prefers-reduced-motion:reduce){.vf-corrido-trilho{animation:none}.vf-assenta{animation:none}}',
    '@media print{.vf-corrido-trilho{animation:none}.vf-assenta{animation:none}}'
  ].join('\n');
  function injetaCSS() {
    if (!raiz.document || document.getElementById('vforms-css')) return;
    const st = document.createElement('style'); st.id = 'vforms-css'; st.textContent = CSS;
    (document.head || document.documentElement).appendChild(st);
  }

  /* ícones Lucide (copiados, traço 1,5, pontas retas) */
  const ICONE = {
    'circle-check': '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    'circle-dashed': '<path d="M10.1 2.182a10 10 0 0 1 3.8 0"/><path d="M13.9 21.818a10 10 0 0 1-3.8 0"/><path d="M17.609 3.721a10 10 0 0 1 2.69 2.7"/><path d="M2.182 13.9a10 10 0 0 1 0-3.8"/><path d="M20.279 17.609a10 10 0 0 1-2.7 2.69"/><path d="M21.818 10.1a10 10 0 0 1 0 3.8"/><path d="M3.721 6.391a10 10 0 0 1 2.7-2.69"/><path d="M6.391 20.279a10 10 0 0 1-2.69-2.7"/>'
  };
  const icone = n => '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' + ICONE[n] + '</svg>';

  /* ============================== API ============================== */
  let contador = 0;
  function hexDe(rgb) {
    const m = /rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/.exec(rgb || '');
    if (!m || (m[4] != null && +m[4] < 1)) return null;
    return '#' + [m[1], m[2], m[3]].map(v => ('0' + (+v).toString(16)).slice(-2)).join('').toUpperCase();
  }
  function fundoDe(el) {
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const c = getComputedStyle(n).backgroundColor;
      if (c && c !== 'transparent' && !/rgba\(0,\s*0,\s*0,\s*0\)/.test(c)) { const h = hexDe(c); return h; }
    }
    return null;
  }
  function opcoesDoContexto(el, o) {
    const r = Object.assign({}, o);
    if (!r.campo && raiz.getComputedStyle) { const h = fundoDe(el); if (h && Object.keys(T).some(k => T[k] === h)) r.campo = h; }
    if (!r.tema && el.closest) r.tema = el.closest('.modo-leitura') ? 'leitura' : 'sala';
    if (!r.estacao && el.closest) { const e = el.closest('[data-estacao]'); r.estacao = e ? e.getAttribute('data-estacao') : 'chamado'; }
    return r;
  }
  function filhosDeConteudo(el) { return Array.prototype.filter.call(el.children, n => !n.classList.contains('vf-camada') && !n.hasAttribute('data-vforms-gerado')); }
  const CAMADAS = ['grao', 'esfera', 'eco', 'janela', 'veu', 'orbita', 'corte-logo'];

  /* largura visível em px reais (getBoundingClientRect já inclui transform/escala) */
  function larguraVisivel(n) {
    if (!n || !n.getBoundingClientRect) return 0;
    const r = n.getBoundingClientRect();
    let w = r.width;
    if (n.clientWidth && n.tagName !== 'svg' && n.tagName !== 'SVG') {
      const cs = raiz.getComputedStyle ? getComputedStyle(n) : null;
      const pad = cs ? (parseFloat(cs.paddingLeft) || 0) + (parseFloat(cs.paddingRight) || 0) : 0;
      w = Math.max(0, w - pad * (r.width / (n.offsetWidth || r.width || 1)));
    }
    return w;
  }
  function mapaHTML(oo) {
    const sv = FORMAS['mapa-trilha'](oo);
    const frases = oo.frases ? '<p class="vf-frase vf-vazio">Esse é o vazio</p><p class="vf-frase vf-caminho">Esse é o caminho para <span class="vf-inteira">preenchê-lo</span></p>' : '';
    /* legenda em HTML: só aparece quando o piso de 11 px tirou nomes ou rótulo do desenho.
       aria-hidden porque o SVG já diz tudo no aria-label (evita leitura duplicada) */
    const m = /data-fora="([^"]+)"/.exec(sv), fora = m ? m[1].split(' ') : [];
    let leg = '';
    if (fora.length && !oo.decorativo) {
      const ativa = (/data-ativa="([a-z]+)"/.exec(sv) || [])[1];
      const aqui = !!(ativa && oo.voceEstaAqui !== false && (oo.voceEstaAqui || oo['voce-esta-aqui']));
      leg = '<figcaption class="vf-mapa-legenda" aria-hidden="true">' + PRODUTOS.map(p =>
        '<span class="vf-termo' + (p === ativa ? ' vf-ativa' : '') + '">' + NOME_PRODUTO[p].toUpperCase() +
        (p === ativa && aqui && fora.indexOf('aqui') >= 0 ? '<span class="vf-aqui">, você está aqui</span>' : '') + '</span>').join('') + '</figcaption>';
    }
    return '<figure class="vf-mapa" data-orientacao="' + oo.orientacao + '" data-tema="' + tema(oo) + '">' +
      sv.replace('class="vf vf-mapa-trilha"', 'class="vf vf-mapa-trilha vf-bloco"') + frases + leg + '</figure>';
  }
  /* o mapa redesenha quando a largura do contêiner muda (inclusive quando sai de display:none) */
  let observador = null;
  function observaLargura(el) {
    /* a largura com que este desenho foi feito (a do conteúdo, como o contentRect mede) */
    const cs = raiz.getComputedStyle ? getComputedStyle(el) : null;
    el.__vfLargura = Math.round(el.clientWidth - (cs ? (parseFloat(cs.paddingLeft) || 0) + (parseFloat(cs.paddingRight) || 0) : 0));
    if (!raiz.ResizeObserver || el.__vfObservado) return;
    if (!observador) observador = new ResizeObserver(entradas => entradas.forEach(en => {
      const alvo = en.target, w = Math.round(en.contentRect.width);
      if (!alvo.__vforms || w === alvo.__vfLargura) return;
      alvo.__vfLargura = w;
      raiz.requestAnimationFrame(() => render(alvo, alvo.__vforms.forma, alvo.__vforms.opts));
    }));
    el.__vfObservado = true;
    observador.observe(el);
  }

  function render(alvo, forma, opts) {
    const el = typeof alvo === 'string' ? document.querySelector(alvo) : alvo;
    if (!el) return null;
    if (NOMES.indexOf(forma) < 0) { aviso('forma desconhecida: ' + forma + '. Formas: ' + NOMES.join(', ')); return null; }
    injetaCSS();
    const o = opcoesDoContexto(el, opts || {});
    if (!o.id) o.id = el.id ? el.id + '-vf' : 'vf' + (++contador);
    el.__vforms = { forma: forma, opts: opts || {} };
    el.setAttribute('data-vforms-montado', forma);
    api.ultimoAviso = null;
    const larg = el.clientWidth || o.largura || 0;
    const alt = el.clientHeight || o.altura || 0;
    let html = '';
    const camada = CAMADAS.indexOf(forma) >= 0 && filhosDeConteudo(el).length > 0;

    if (forma === 'mapa-trilha') {
      const vertical = o.orientacao === 'vertical' || (o.orientacao !== 'horizontal' && raiz.matchMedia && matchMedia('(max-width:430px)').matches);
      const oo = Object.assign({}, o, { orientacao: vertical ? 'vertical' : 'horizontal', frases: o.frases !== false });
      /* largura real em px (já com zoom e transform das miniaturas), para o piso de 11 px */
      if (!(o.larguraReal > 0)) oo.larguraReal = larguraVisivel(el);
      html = mapaHTML(oo);
      el.innerHTML = html;
      /* segunda passada: mede o próprio SVG (padding e transform do contêiner) e acerta */
      const sv = el.querySelector('svg.vf-mapa-trilha');
      const medida = sv ? larguraVisivel(sv) : 0;
      if (medida && !(o.larguraReal > 0) && Math.abs(medida - (oo.larguraReal || 0)) > 1) { oo.larguraReal = medida; html = mapaHTML(oo); }
      observaLargura(el);
    } else if (forma === 'marcador-estacao') {
      const rot = o.rotulo != null ? o.rotulo : '';
      html = '<span class="vf-marcador">' + FORMAS['marcador-estacao'](o) + (rot ? '<span>' + esc(String(rot).toUpperCase()) + '</span>' : '') + '</span>';
    } else if (forma === 'marcador-capitulo') {
      html = '<span class="vf-capitulo credito"><span class="vf-fio" aria-hidden="true"></span><span>' + esc(textoCapitulo(o)) + '</span></span>';
    } else if (forma === 'rodape') {
      html = rodapeHTML(o);
    } else if (forma === 'anel') {
      const sv = FORMAS.anel(o);
      const atual = PRODUTOS.indexOf(o.atual) >= 0 ? o.atual : null;
      const marcos = atual ? marcosDe(o, atual) : [];
      const leg = marcos.length ? '<ul class="vf-anel-legenda">' + marcos.map(m => {
        const ok = m.validado === true;
        return '<li>' + icone(ok ? 'circle-check' : 'circle-dashed') + '<span><b>' + (ok ? 'Validado' : 'Pendente') + '</b> · ' + esc(m.nome) + '</span></li>';
      }).join('') + '</ul>' : '';
      html = '<figure class="vf-anel-fig">' + sv.replace('class="vf vf-anel"', 'class="vf vf-anel vf-bloco"') + leg + '</figure>';
    } else if (forma === 'selo' || forma === 'logotipo') {
      if (forma === 'selo' && !o.tamanho) o.tamanho = Math.min(larg || 200, 869);
      html = FORMAS[forma](o);
    } else {
      /* formas de campo: desenham no tamanho real do contêiner (1 unidade = 1 px) */
      const oo = Object.assign({}, o);
      if (['grao', 'eco', 'janela', 'veu', 'orbita', 'corte-logo'].indexOf(forma) >= 0) {
        if (larg) oo.largura = o.largura || larg;
        if (alt) oo.altura = o.altura || alt;
        if (forma === 'eco' && larg) oo.largura = larg;
        oo.ajuste = forma === 'veu' ? 'none' : (o.ajuste || 'xMidYMid slice');
      }
      if (forma === 'esfera' && !o.tamanho) oo.tamanho = Math.min(larg || 600, alt || larg || 600);
      html = FORMAS[forma](oo);
      if (html && !camada) html = html.replace('class="vf vf-' + forma + '"', 'class="vf vf-' + forma + ' vf-bloco"');
    }
    if (!html) {
      const msg = api.ultimoAviso || 'forma recusada';
      el.setAttribute('data-vforms-recusa', msg);
      if (!camada) el.innerHTML = '';
      else { const c = el.querySelector(':scope > .vf-camada'); if (c) c.remove(); }
      return null;
    }
    el.removeAttribute('data-vforms-recusa');
    if (camada) {
      el.classList.add('vf-host');
      let cam = el.querySelector(':scope > .vf-camada');
      if (!cam) { cam = document.createElement('div'); cam.className = 'vf-camada'; cam.setAttribute('aria-hidden', 'true'); el.insertBefore(cam, el.firstChild); }
      cam.innerHTML = html;
    } else {
      el.innerHTML = html;
    }
    if (forma === 'rodape' && o.variante !== 'corrido') { ajustaRodape(el); observaLargura(el); }
    if (forma === 'rodape' && o.variante === 'corrido') {
      const tr = el.querySelector('.vf-corrido-trilho');
      if (tr && tr.scrollWidth) tr.style.setProperty('--vf-duracao', (tr.scrollWidth / 4 / 40).toFixed(2) + 's');
    }
    if (api.ultimoAviso) el.setAttribute('data-vforms-aviso', api.ultimoAviso); else el.removeAttribute('data-vforms-aviso');
    return el;
  }

  function svg(forma, opts) {
    if (NOMES.indexOf(forma) < 0) throw new Error('vforms: forma desconhecida: ' + forma);
    const o = Object.assign({}, opts || {});
    if (!o.id) o.id = 'vf-' + forma + '-' + hash(forma + JSON.stringify(opts || {}));
    api.ultimoAviso = null;
    return FORMAS[forma](o);
  }

  function lerOpcoes(el) {
    const v = el.getAttribute('data-vforms');
    let nome = v, o = {};
    if (/^\s*\{/.test(v)) { try { o = JSON.parse(v); nome = o.forma; delete o.forma; } catch (e) { console.error('vforms: data-vforms não é JSON válido', el); return null; } }
    const extra = el.getAttribute('data-vforms-opts');
    if (extra) { try { o = Object.assign(o, JSON.parse(extra)); } catch (e) { console.error('vforms: data-vforms-opts não é JSON válido', el); } }
    return { nome: nome, o: o };
  }
  function montar(r) {
    (r || document).querySelectorAll('[data-vforms]').forEach(el => {
      const c = lerOpcoes(el); if (c) render(el, c.nome, c.o);
    });
  }
  function redesenhar(r) {
    (r || document).querySelectorAll('[data-vforms-montado]').forEach(el => {
      if (el.__vforms) render(el, el.__vforms.forma, el.__vforms.opts);
    });
  }

  /* geometria exposta para testes e para outras ferramentas */
  const geometria = {
    mapa: v => geometriaMapa(!!v),
    orbita: e => geometriaOrbita(e),
    corte: (w, h, m) => corteGeometria(w, h, m),
    cortes: CORTES, recortes: RECORTES, trilha: TRILHA, marca: MARCA, orbitas: ORBITA
  };

  const scriptAtual = raiz.document && document.currentScript ? document.currentScript.getAttribute('src') || '' : '';
  const api = {
    versao: '1.0',
    render: render, svg: svg, montar: montar, redesenhar: redesenhar,
    formas: NOMES.slice(), tokens: T, geometria: geometria, css: CSS,
    rodapeTexto: RODAPE.join(' · '),
    config: { base: scriptAtual.replace(/vforms\.js(\?.*)?$/, '') },
    ultimoAviso: null
  };
  NOMES.forEach(n => { api[n.replace(/-([a-z])/g, (m, c) => c.toUpperCase())] = (e, o) => render(e, n, o); });
  raiz.VForms = api; raiz.vforms = api;

  if (raiz.document) {
    const iniciar = () => {
      montar();
      /* o rodapé é diagramado medindo o texto: refaz quando a Archivo terminar de carregar */
      const reajusta = () => document.querySelectorAll('.vf-rodape').forEach(p => ajustaRodape(p.parentNode));
      if (document.fonts) {
        if (document.fonts.ready) document.fonts.ready.then(reajusta);
        if (document.fonts.addEventListener) document.fonts.addEventListener('loadingdone', reajusta);
      }
      let ultimaLargura = raiz.innerWidth, pedido = 0;
      raiz.addEventListener('resize', () => {
        if (raiz.innerWidth === ultimaLargura) return;
        ultimaLargura = raiz.innerWidth;
        if (pedido) raiz.cancelAnimationFrame(pedido);
        pedido = raiz.requestAnimationFrame(() => { pedido = 0; redesenhar(); });
      });
    };
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar); else iniciar();
  }
})(typeof window !== 'undefined' ? window : (typeof globalThis !== 'undefined' ? globalThis : this));
