/* Smart Growth · palco 3D do símbolo (na pegada do R da RZD)
   - Abre: o símbolo desce e acende.
   - Rolando: o texto do topo some, o símbolo vai para o meio e cresce.
   - No meio: gira 360, as duas peças se afastam e voltam, acende forte e termina num clarão
     que vira a seção clara de Serviços. Se a pessoa para perto do fim, a página completa até Serviços.
   - Frente clara e brilhante, laterais acesas em laranja.
   - Celular: camada que gruda (o navegador move, não o código), resolução 1,5x, só desenha quando algo muda.
   Sem WebGL, fica a imagem estática no lugar. */
(function () {
  var alvo = document.querySelector('[data-g-alvo]');
  var palco = document.querySelector('[data-palco]');
  var canvas = document.querySelector('.palco3d-canvas');
  var brilhoDom = document.querySelector('.palco3d-brilho');
  var texto = document.querySelector('[data-palco-texto]');
  var servicos = document.getElementById('servicos');
  var frase = document.querySelector('.palco .frase'), ultimaFrase = -1;
  if (!alvo || !canvas || !window.THREE) return;

  var reduz = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var movel = window.matchMedia('(max-width: 960px), (pointer: coarse)').matches;
  var dpr = Math.min(window.devicePixelRatio || 1, movel ? 1.5 : 2);
  var T = window.THREE;
  var renderer;
  try {
    renderer = new T.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true, powerPreference: 'high-performance', premultipliedAlpha: true });
  } catch (e) { return; }
  renderer.setPixelRatio(dpr);
  renderer.setClearColor(0x000000, 0);
  renderer.outputEncoding = T.sRGBEncoding;
  renderer.toneMapping = T.ACESFilmicToneMapping;
  if (brilhoDom) brilhoDom.style.display = 'none';

  /* camada que gruda (celular) */
  var main = document.querySelector('main'), topoEl = document.querySelector('.topo');
  var camada = null, fixa = null;
  if (movel && main) {
    main.style.position = 'relative';
    camada = document.createElement('div'); camada.className = 'palco3d-camada'; camada.setAttribute('aria-hidden', 'true');
    fixa = document.createElement('div'); fixa.className = 'palco3d-fixa';
    fixa.appendChild(canvas); camada.appendChild(fixa); main.insertBefore(camada, main.firstChild);
  }

  var cena = new T.Scene();
  var camera = new T.PerspectiveCamera(30, 1, 0.1, 100);
  camera.position.set(0, 0, 12);

  /* ---- símbolo: o mesmo caminho do SVG oficial (viewBox 1557 x 954), em duas peças ---- */
  var D = 'M1557.00,340.00 L962.00,340.00 C861.85,340.00 738.60,430.70 706.00,524.00 L1270.00,524.00 C1241.36,615.62 1138.69,699.11 1049.87,730.40 C1000.17,747.91 956.68,752.00 905.00,752.00 L276.00,752.00 C175.14,752.00 22.27,854.00 0.00,954.00 L927.00,954.00 C971.30,954.00 1026.50,940.36 1068.89,927.70 C1300.35,858.58 1417.63,690.30 1506.00,477.60 C1523.58,435.30 1548.74,384.10 1557.00,340.00 Z M1316.00,0.00 L755.00,0.00 C729.61,0.00 687.49,12.19 662.73,19.71 C472.57,77.43 362.59,211.91 284.09,387.27 C265.45,428.88 240.68,478.10 231.00,522.00 C268.03,525.24 289.36,520.87 323.77,506.78 C433.12,461.99 457.37,372.92 531.86,294.81 C571.89,252.83 618.81,220.72 672.20,198.19 C693.11,189.37 750.66,169.50 772.00,169.50 L1093.00,169.50 C1101.79,169.50 1124.80,163.11 1134.24,160.74 C1212.27,141.12 1291.03,77.74 1316.00,0.00 Z';
  var W = 1557, H = 954;
  function px(x) { return (x - W / 2) / W; }
  function py(y) { return -(y - H / 2) / W; }
  var formas = [], f = null;
  var tk = D.match(/[MLCZ]|-?\d+(\.\d+)?/g), i = 0, cmd;
  function n() { return parseFloat(tk[i++]); }
  while (i < tk.length) {
    if (/[MLCZ]/.test(tk[i])) cmd = tk[i++];
    if (cmd === 'M') { f = new T.Shape(); f.moveTo(px(n()), py(n())); formas.push(f); cmd = 'L'; }
    else if (cmd === 'L') { f.lineTo(px(n()), py(n())); }
    else if (cmd === 'C') { var a = n(), b = n(), c = n(), d = n(), e = n(), g = n(); f.bezierCurveTo(px(a), py(b), px(c), py(d), px(e), py(g)); }
    else if (cmd === 'Z') { f.closePath(); }
  }
  var opExt = { depth: 0.17, bevelEnabled: true, bevelThickness: 0.016, bevelSize: 0.011, bevelSegments: movel ? 2 : 4, curveSegments: movel ? 18 : 32 };
  var geoTudo = new T.ExtrudeGeometry(formas, opExt); geoTudo.computeBoundingBox();
  var meio = new T.Vector3(); geoTudo.boundingBox.getCenter(meio); geoTudo.dispose();

  // frente clara e brilhante; laterais escuras que acendem em laranja (como o R da RZD)
  // camada prata: um estúdio de luz invisível que o metal reflete (faixas de brilho, como no R da RZD)
  (function () {
    var estudio = new T.Scene();
    estudio.add(new T.Mesh(new T.BoxGeometry(20, 24, 12), new T.MeshBasicMaterial({ color: 0x050505, side: T.BackSide })));
    function painel(w, h, cor, pos) {
      var m = new T.Mesh(new T.PlaneGeometry(w, h), new T.MeshBasicMaterial({ color: cor, side: T.DoubleSide }));
      m.position.set(pos[0], pos[1], pos[2]); m.lookAt(0, 0, 0); estudio.add(m);
    }
    painel(3, 12, new T.Color(6, 5.8, 5.4), [-8, 1, 6]);
    painel(1.2, 10, new T.Color(3, 2.9, 2.8), [8, 0, 4]);
    painel(10, 2, new T.Color(1.6, 1.55, 1.5), [0, 9, 2]);
    painel(14, 6, new T.Color(1.4, 0.45, 0.15), [0, -2, -10]);
    var pm = new T.PMREMGenerator(renderer);
    cena.environment = pm.fromScene(estudio, 0.045).texture;
    pm.dispose();
    estudio.traverse(function (o) { if (o.isMesh) { o.geometry.dispose(); o.material.dispose(); } });
  })();
  var frente = new T.MeshStandardMaterial({ color: 0xF3EEE6, metalness: 0.45, roughness: 0.24, envMapIntensity: 1.7, emissive: 0xFFE2C4, emissiveIntensity: 0 });
  var lado = new T.MeshStandardMaterial({ color: 0x1D1B19, metalness: 0.7, roughness: 0.32, envMapIntensity: 1.2, emissive: 0xFA5A14, emissiveIntensity: 1 });
  lado.roughness = 0.4;
  var grupo = new T.Group();
  // sombreado suave: junta as normais de faces vizinhas quase paralelas (menos de 35 graus) e mantém as quinas
  function suavizar(geo) {
    var pos = geo.attributes.position, nor = geo.attributes.normal, nv = pos.count;
    var faces = new Float32Array(nv * 3), a = new T.Vector3(), b = new T.Vector3(), c = new T.Vector3();
    for (var v = 0; v < nv; v += 3) {
      a.fromBufferAttribute(pos, v); b.fromBufferAttribute(pos, v + 1); c.fromBufferAttribute(pos, v + 2);
      b.sub(a); c.sub(a); b.cross(c); if (b.lengthSq() > 0) b.normalize();
      for (var q = 0; q < 3; q++) { faces[(v + q) * 3] = b.x; faces[(v + q) * 3 + 1] = b.y; faces[(v + q) * 3 + 2] = b.z; }
    }
    var mapa = {}, chave = function (v) { return Math.round(pos.getX(v) * 1e4) + '_' + Math.round(pos.getY(v) * 1e4) + '_' + Math.round(pos.getZ(v) * 1e4); };
    for (var v2 = 0; v2 < nv; v2++) { var k = chave(v2); (mapa[k] || (mapa[k] = [])).push(v2); }
    var limite = Math.cos(35 * Math.PI / 180);
    for (var v3 = 0; v3 < nv; v3++) {
      var lista = mapa[chave(v3)], fx = faces[v3 * 3], fy = faces[v3 * 3 + 1], fz = faces[v3 * 3 + 2], sx = 0, sy = 0, sz = 0;
      // frente e fundo ficam planos (sem riscos); só as laterais e o chanfro se suavizam entre si
      if (Math.abs(fz) > 0.97) { nor.setXYZ(v3, fx, fy, fz); continue; }
      for (var j = 0; j < lista.length; j++) {
        var o = lista[j], ox = faces[o * 3], oy = faces[o * 3 + 1], oz = faces[o * 3 + 2];
        if (Math.abs(oz) <= 0.97 && fx * ox + fy * oy + fz * oz >= limite) { sx += ox; sy += oy; sz += oz; }
      }
      var l = Math.hypot(sx, sy, sz) || 1; nor.setXYZ(v3, sx / l, sy / l, sz / l);
    }
    nor.needsUpdate = true;
  }
  var pecas = formas.map(function (forma) {
    var geo = new T.ExtrudeGeometry([forma], opExt);
    geo.translate(-meio.x, -meio.y, -meio.z);
    suavizar(geo);
    var m = new T.Mesh(geo, [frente, lado]);
    grupo.add(m);
    return m;
  });
  // peça 0 = a de baixo (maior), peça 1 = a de cima
  cena.add(grupo);

  var chave = new T.DirectionalLight(0xffffff, 0.5); chave.position.set(-4, 5, 6); cena.add(chave);
  var quente = new T.PointLight(0xff7a1a, 0, 9); quente.position.set(0, 0, 2.5); cena.add(quente);

  // brilho e clarão desenhados dentro do 3D
  function gradiente(paradas) {
    var tl = document.createElement('canvas'); tl.width = tl.height = 256;
    var cx = tl.getContext('2d'), gr = cx.createRadialGradient(128, 128, 0, 128, 128, 128);
    paradas.forEach(function (p) { gr.addColorStop(p[0], p[1]); });
    cx.fillStyle = gr; cx.fillRect(0, 0, 256, 256);
    var tx = new T.CanvasTexture(tl); tx.encoding = T.sRGBEncoding; return tx;
  }
  function sprite(tx, ordem, cobre) {
    var s = new T.Sprite(new T.SpriteMaterial({ map: tx, transparent: true, depthWrite: false, depthTest: false, toneMapped: false, blending: cobre ? T.NormalBlending : T.AdditiveBlending, opacity: 0 }));
    s.renderOrder = ordem; cena.add(s); return s;
  }
  var halo = sprite(gradiente([[0, 'rgba(255,120,50,0.7)'], [0.3, 'rgba(255,90,31,0.22)'], [0.62, 'rgba(255,90,31,0.05)'], [1, 'rgba(255,90,31,0)']]), -1);
  halo.position.z = -0.8;
  var clarao = sprite(gradiente([[0, 'rgba(255,250,242,1)'], [0.45, 'rgba(250,244,236,1)'], [0.75, 'rgba(243,244,248,0.85)'], [1, 'rgba(243,244,248,0)']]), 10, true);
  clarao.position.z = 1;

  /* ---- medidas ---- */
  var vw = 0, vh = 0, mundoH = 0, sujo = true;
  function medir(forcar) {
    var nw = window.innerWidth, nh = window.innerHeight;
    if (!forcar && nw === vw && Math.abs(nh - vh) < 160) return;
    vw = nw; vh = nh;
    renderer.setSize(vw, vh, false);
    canvas.style.height = vh + 'px';
    if (fixa) fixa.style.height = vh + 'px';
    camera.aspect = vw / vh; camera.updateProjectionMatrix();
    mundoH = 2 * camera.position.z * Math.tan((camera.fov * Math.PI / 180) / 2);
    sujo = true;
  }
  function pxParaMundo(x, y) { var k = mundoH / vh; return { x: (x - vw / 2) * k, y: -(y - vh / 2) * k, k: k }; }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function suave(t) { t = Math.min(1, Math.max(0, t)); return t * t * (3 - 2 * t); }
  function faixa(t, a, b) { return suave((t - a) / (b - a)); }
  function sai(t) { t = Math.min(1, Math.max(0, t)); return 1 - Math.pow(1 - t, 3); }

  /* ---- abertura: desce e acende ---- */
  var t0 = performance.now();
  var DUR_DESCE = reduz ? 0 : 1900, INICIO_LUZ = reduz ? 0 : 1100, DUR_LUZ = reduz ? 0 : 1500;
  var FIM_ABERTURA = INICIO_LUZ + DUR_LUZ + 100;
  function piscar(ms) {
    if (ms <= 0) return 0;
    if (ms >= DUR_LUZ) return 1;
    var p = ms / DUR_LUZ;
    var passos = [[0, 0], [0.12, 0.9], [0.2, 0.25], [0.3, 1], [0.4, 0.35], [0.52, 1.1], [0.7, 0.8], [1, 1]];
    for (var j = 1; j < passos.length; j++) {
      if (p <= passos[j][0]) { var a = passos[j - 1], b = passos[j]; return lerp(a[1], b[1], (p - a[0]) / (b[0] - a[0])); }
    }
    return 1;
  }

  /* ---- medidas do palco ---- */
  var chegada = 1, palcoFim = 1, alvoX = 0, alvoY = 0, alvoW = 0, meioQ = 0, servTopo = 0;
  function medirPalco() {
    var y = window.scrollY;
    var rp = palco.getBoundingClientRect(), palcoTopo = rp.top + y, palcoBase = rp.bottom + y;
    chegada = Math.max(1, palcoTopo - vh * 0.15);
    palcoFim = Math.max(chegada + 1, palcoBase - vh);
    var r = alvo.getBoundingClientRect();
    alvoX = r.left + r.width / 2; alvoY = r.top + y + r.height / 2; alvoW = r.width;
    var cab = topoEl ? topoEl.offsetHeight : 0;
    if (servicos) servTopo = servicos.getBoundingClientRect().top + y - cab;
    if (camada) {
      meioQ = cab + (vh - cab) / 2;
      var mainTopo = main.getBoundingClientRect().top + y;
      var inicio = alvoY - meioQ;
      camada.style.top = (inicio - mainTopo) + 'px';
      camada.style.height = Math.max(vh, palcoBase - inicio) + 'px';
    }
    sujo = true;
  }

  /* ---- termina sozinho até Serviços quando a pessoa para perto do fim (como a RZD) ---- */
  var tocando = false, descendo = true, ultimoScroll = window.scrollY, espera = 0;
  function completar() {
    if (tocando || !servicos || reduz) return;
    var y = window.scrollY;
    var g = (y - chegada) / (palcoFim - chegada);
    if (g < 0.7 || y >= servTopo - 2) return;
    window.scrollTo({ top: descendo ? servTopo : chegada + (palcoFim - chegada) * 0.55, behavior: 'smooth' });
  }
  window.addEventListener('scroll', function () {
    sujo = true;
    var y = window.scrollY; if (y !== ultimoScroll) descendo = y > ultimoScroll; ultimoScroll = y;
    clearTimeout(espera); if (!('onscrollend' in window)) espera = setTimeout(completar, 160);
  }, { passive: true });
  if ('onscrollend' in window) window.addEventListener('scrollend', completar);
  window.addEventListener('touchstart', function () { tocando = true; clearTimeout(espera); }, { passive: true });
  window.addEventListener('touchend', function () { tocando = false; clearTimeout(espera); espera = setTimeout(completar, 160); }, { passive: true });
  window.addEventListener('resize', function () { medir(false); medirPalco(); });
  window.addEventListener('load', function () { medirPalco(); });

  var veu = document.createElement('div'); veu.className = 'palco-veu'; veu.setAttribute('aria-hidden', 'true');
  document.body.appendChild(veu);
  var estadoVeu = 'livre', ultimoVeu = -1;
  function pularParaServicos() {
    estadoVeu = 'saltando'; veu.classList.remove('some'); veu.style.opacity = '1'; ultimoVeu = 1;
    window.scrollTo({ top: servTopo, behavior: 'instant' });
    setTimeout(function () {
      veu.classList.add('some'); veu.style.opacity = '0'; ultimoVeu = 0; estadoVeu = 'sumindo';
    }, 90);
  }

  var ultimoY = -1, ultimoTexto = -1, escondido = false, yS = -1, tAnt = 0, pronto = false;

  function quadro(agora) {
    requestAnimationFrame(quadro);
    var ms = agora - t0;
    var abrindo = ms < FIM_ABERTURA;
    var y = window.scrollY;
    var flutuar = !movel && !reduz;
    // suavização: o símbolo alcança a rolagem aos poucos
    var dt = Math.min(64, Math.max(0, agora - tAnt)); tAnt = agora;
    if (yS < 0 || Math.abs(y - yS) > vh * 2.5 || reduz) yS = y;
    else { yS += (y - yS) * (1 - Math.exp(-dt / 90)); if (Math.abs(y - yS) < 0.5) yS = y; }
    var alcancando = yS !== y;
    if (!abrindo && !flutuar && !sujo && !alcancando && y === ultimoY) return;
    sujo = false; ultimoY = y;

    var t = suave(yS / chegada);
    var g = Math.min(1, Math.max(0, (yS - chegada) / (palcoFim - chegada)));
    var giro = faixa(g, 0.04, 0.62);                                 // volta inteira
    var explode = faixa(g, 0.18, 0.36) * (1 - faixa(g, 0.48, 0.64)); // peças se afastam e voltam
    var bordas = faixa(g, 0.62, 0.74) * (1 - faixa(g, 0.9, 0.97));  // bordas acendem
    var acende = faixa(g, 0.72, 0.86);                               // frente esquenta
    var flash = faixa(g, 0.8, 0.92);                                 // estouro de luz saindo do centro
    var passou = camada ? 0 : Math.max(0, y - palcoFim);

    // flash: a tela fica clara e a página pula para Serviços por trás da luz (como a RZD)
    var gReal = (y - chegada) / (palcoFim - chegada);
    if (estadoVeu === 'livre') {
      var vo = faixa(g, 0.86, 0.95);
      if (Math.abs(vo - ultimoVeu) > 0.01) { veu.style.opacity = vo.toFixed(3); ultimoVeu = vo; }
      if (servicos && !reduz && descendo && gReal >= 0.95 && y < servTopo - 2) pularParaServicos();
    } else if (estadoVeu === 'sumindo' && y < chegada + (palcoFim - chegada) * 0.8) {
      veu.classList.remove('some'); estadoVeu = 'livre';
    }

    if ((camada ? y - palcoFim : passou) > vh * 1.4) {
      if (!escondido) { canvas.style.visibility = 'hidden'; escondido = true; }
      return;
    } else if (escondido) { canvas.style.visibility = 'visible'; escondido = false; }

    var desce = reduz ? 1 : sai(ms / DUR_DESCE);
    var luz = reduz ? 1 : piscar(ms - INICIO_LUZ);

    // texto do topo some e sobe um pouco
    if (texto) {
      var e = faixa(t, 0.05, 0.4), op = 1 - e;
      if (Math.abs(op - ultimoTexto) > 0.01) {
        texto.style.opacity = op.toFixed(2);
        texto.style.transform = e > 0 ? 'translate3d(0,' + (-6 * e).toFixed(2) + 'vh,0)' : '';
        ultimoTexto = op;
      }
    }

    var topoAlvo = camada ? meioQ : alvoY - y;
    var ini = pxParaMundo(alvoX, topoAlvo);
    var larg0 = alvoW * ini.k;
    var larg1 = Math.min(vw * (movel ? 0.9 : 0.62), vh * 0.46 * (W / H)) * ini.k;
    var centro = pxParaMundo(vw / 2, camada ? meioQ : vh / 2 - passou);

    var x = lerp(ini.x, centro.x, t);
    var yy = lerp(ini.y, centro.y, t) + (1 - desce) * (mundoH * 0.55);
    var flutua = flutuar ? Math.sin(ms / 1400) * 0.04 * desce : 0;
    var escala = lerp(larg0, larg1, t) * (1 - 0.12 * explode);

    grupo.position.set(x, yy + flutua, 0);
    grupo.scale.setScalar(escala);
    grupo.rotation.set(
      lerp(0.22, 0.12, t) + (1 - desce) * -0.6,
      lerp(-0.42, 0.3, t) * (1 - giro) + giro * Math.PI * 2 + (flutuar ? Math.sin(ms / 2600) * 0.05 * (1 - t) : 0),
      0.07 * Math.sin(g * Math.PI * 3) * (1 - 0.6 * explode) + lerp(-0.05, 0, t)
    );
    if (cena.environment && cena.environmentRotation) cena.environmentRotation.set(0, -0.6 * giro * Math.PI * 2, 0);
    // as duas peças se afastam (de cima para cima e à direita, de baixo para baixo e à esquerda)
    var k2 = 0.42 * explode;
    pecas[1].position.set(0.08 * k2, 0.34 * k2, -0.2 * k2); pecas[1].rotation.set(-0.3 * k2, 0.2 * k2, 0.08 * k2);
    pecas[0].position.set(-0.1 * k2, -0.3 * k2, 0.22 * k2); pecas[0].rotation.set(0.15 * k2, -0.35 * k2, -0.06 * k2);

    // luz: laterais acesas desde a abertura; acende forte no fim do giro
    var forca = 1 + 0.3 * faixa(g, 0.1, 0.35) + 2.4 * acende;
    lado.emissiveIntensity = luz * (0.15 + 0.85 * Math.max(0, explode) + 0.4 * Math.max(0, forca - 1) + 2.2 * bordas);
    frente.emissiveIntensity = luz * 0.3 * acende;
    quente.intensity = luz * (0.2 + 0.4 * t + 2.2 * acende);
    renderer.toneMappingExposure = 1.05 + 0.12 * acende;

    var tamH = lerp(alvoW * 1.9, Math.min(vw, vh) * 1.5, t) * ini.k * (1 + 0.25 * acende + 0.3 * explode);
    halo.position.set(x, yy + flutua, -0.8);
    halo.scale.set(tamH, tamH, 1);
    halo.material.opacity = Math.min(1, luz * (0.45 + 0.1 * t + 0.25 * explode) + 0.45 * acende);

    if (frase) { var of = (1 - flash).toFixed(2); if (of !== ultimaFrase) { frase.style.opacity = of; ultimaFrase = of; } }
    clarao.visible = flash > 0.001;
    if (clarao.visible) {
      var diag = Math.hypot(vw, vh) * ini.k;
      clarao.position.set(x, yy, 1);
      var tc = (0.3 + flash * 3.2) * diag;
      clarao.scale.set(tc, tc, 1);
      clarao.material.opacity = Math.min(1, 1.5 * flash);
      if (!camada) clarao.position.y = centro.y;
    }

    renderer.render(cena, camera);
    if (!pronto) { pronto = true; document.documentElement.classList.add('tem-3d'); }
  }

  medir(true);
  medirPalco();
  renderer.compile(cena, camera);
  requestAnimationFrame(quadro);
})();
