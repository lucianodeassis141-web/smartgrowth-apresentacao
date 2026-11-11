/* Smart Growth · palco 3D do símbolo
   O símbolo SG desce do alto e acende quando a página abre.
   Ao rolar, o texto do topo some aos poucos e o símbolo vai para o meio da tela, gira, cresce e brilha em laranja.
   Leve no celular: resolução limitada, desenha só quando algo muda e ignora a barra do navegador subindo e descendo.
   Sem WebGL, fica a imagem estática no lugar. */
(function () {
  var alvo = document.querySelector('[data-g-alvo]');
  var palco = document.querySelector('[data-palco]');
  var canvas = document.querySelector('.palco3d-canvas');
  var brilho = document.querySelector('.palco3d-brilho');
  var texto = document.querySelector('[data-palco-texto]');
  if (!alvo || !canvas || !window.THREE) return;

  var reduz = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var movel = window.matchMedia('(max-width: 960px), (pointer: coarse)').matches;
  var dpr = Math.min(window.devicePixelRatio || 1, movel ? 1.5 : 2);
  var T = window.THREE;
  var renderer;
  try {
    renderer = new T.WebGLRenderer({ canvas: canvas, antialias: dpr < 1.5, alpha: true, powerPreference: movel ? 'default' : 'high-performance' });
  } catch (e) { return; }
  renderer.setPixelRatio(dpr);
  renderer.outputEncoding = T.sRGBEncoding;
  renderer.toneMapping = T.ACESFilmicToneMapping;

  /* Celular (como a RZD): o 3D fica numa camada que primeiro rola junto com a página e depois gruda
     no meio da tela. Quem move o símbolo é o próprio navegador, não o código, então não trava. */
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

  /* ---- símbolo: o mesmo caminho do SVG oficial (viewBox 1557 x 954) ---- */
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
  var geo = new T.ExtrudeGeometry(formas, {
    depth: 0.16, bevelEnabled: true, bevelThickness: 0.014, bevelSize: 0.009,
    bevelSegments: movel ? 2 : 3, curveSegments: movel ? 8 : 20
  });
  geo.center();

  var corFrente0 = new T.Color('#F3F1EC'), corFrente1 = new T.Color('#F56A00');
  var corLado0 = new T.Color('#FA7715'), corLado1 = new T.Color('#B8400A');
  var frente = new T.MeshStandardMaterial({ color: corFrente0.clone(), roughness: 0.38, metalness: 0.08, emissive: new T.Color('#E85A00'), emissiveIntensity: 0 });
  var lado = new T.MeshStandardMaterial({ color: corLado0.clone(), roughness: 0.45, metalness: 0.12, emissive: new T.Color('#C2410C'), emissiveIntensity: 0.15 });
  var grupo = new T.Group();
  grupo.add(new T.Mesh(geo, [frente, lado]));
  cena.add(grupo);

  cena.add(new T.AmbientLight(0xffffff, 0.35));
  var chave = new T.DirectionalLight(0xfff4e8, 1.6); chave.position.set(-4, 5, 6); cena.add(chave);
  var recorte = new T.DirectionalLight(0xff8a3d, 1.1); recorte.position.set(5, -2, -3); cena.add(recorte);
  var quente = new T.PointLight(0xff7a1a, 0, 9); quente.position.set(0, 0, 2.5); cena.add(quente);

  // brilho desenhado dentro do 3D (como a RZD), em vez de um círculo gigante separado na página
  var tela = document.createElement('canvas'); tela.width = tela.height = 256;
  var cx2 = tela.getContext('2d'), grad = cx2.createRadialGradient(128, 128, 0, 128, 128, 128);
  grad.addColorStop(0, 'rgba(255,130,40,0.75)'); grad.addColorStop(0.3, 'rgba(250,110,15,0.26)');
  grad.addColorStop(0.62, 'rgba(250,119,21,0.05)'); grad.addColorStop(1, 'rgba(250,119,21,0)');
  cx2.fillStyle = grad; cx2.fillRect(0, 0, 256, 256);
  var texHalo = new T.CanvasTexture(tela); texHalo.encoding = T.sRGBEncoding;
  var halo = new T.Sprite(new T.SpriteMaterial({ map: texHalo, toneMapped: false, transparent: true, depthWrite: false, opacity: 0 }));
  halo.renderOrder = -1; halo.position.z = -0.8;
  cena.add(halo);
  if (brilho) brilho.style.display = 'none';

  /* ---- medidas ----
     No celular a barra do navegador muda a altura da tela o tempo todo. Só redimensiona
     quando a largura muda ou a altura muda muito (girar o aparelho). */
  var vw = 0, vh = 0, mundoH = 0;
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
  function pxParaMundo(x, y) {
    var k = mundoH / vh;
    return { x: (x - vw / 2) * k, y: -(y - vh / 2) * k, k: k };
  }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function suave(t) { t = Math.min(1, Math.max(0, t)); return t * t * (3 - 2 * t); }
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
      if (p <= passos[j][0]) {
        var a = passos[j - 1], b = passos[j];
        return lerp(a[1], b[1], (p - a[0]) / (b[0] - a[0]));
      }
    }
    return 1;
  }

  // medidas do palco, refeitas só quando a página muda de tamanho
  var chegada = 1, palcoFim = 1, alvoX = 0, alvoY = 0, alvoW = 0, meioQ = 0;
  function medirPalco() {
    var y = window.scrollY;
    var rp = palco.getBoundingClientRect(), palcoTopo = rp.top + y, palcoBase = rp.bottom + y;
    // chegada: o símbolo no meio da tela; depois ele gira 360 e brilha até o fim do palco
    chegada = Math.max(1, palcoTopo - vh * 0.15);
    palcoFim = Math.max(chegada + 1, palcoBase - vh);
    var r = alvo.getBoundingClientRect();
    alvoX = r.left + r.width / 2; alvoY = r.top + y + r.height / 2; alvoW = r.width;
    if (camada) {
      var cab = topoEl ? topoEl.offsetHeight : 0;
      meioQ = cab + (vh - cab) / 2;                    // onde o símbolo fica quando a camada gruda
      var mainTopo = main.getBoundingClientRect().top + y;
      var inicio = alvoY - meioQ;                      // a camada começa de modo que o símbolo caia na caixa
      camada.style.top = (inicio - mainTopo) + 'px';
      camada.style.height = Math.max(vh, palcoBase - inicio) + 'px';
    }
    sujo = true;
  }


  var sujo = true, ultimoY = -1, ultimoTexto = -1, escondido = false, yS = -1, tAnt = 0, pronto = false;
  window.addEventListener('scroll', function () { sujo = true; }, { passive: true });
  window.addEventListener('resize', function () { medir(false); medirPalco(); });
  window.addEventListener('load', function () { medirPalco(); });

  function quadro(agora) {
    requestAnimationFrame(quadro);
    var ms = agora - t0;
    var abrindo = ms < FIM_ABERTURA;
    var y = window.scrollY;
    var flutuar = !movel && !reduz;
    // suavização (como a RZD): o símbolo alcança a rolagem aos poucos, sem repetir os solavancos do dedo
    var dt = Math.min(64, Math.max(0, agora - tAnt)); tAnt = agora;
    if (yS < 0 || Math.abs(y - yS) > vh * 2.5 || reduz) yS = y;
    else { yS += (y - yS) * (1 - Math.exp(-dt / 90)); if (Math.abs(y - yS) < 0.5) yS = y; }
    var alcancando = yS !== y;
    if (!abrindo && !flutuar && !sujo && !alcancando && y === ultimoY) return; // nada mudou: não desenha
    sujo = false; ultimoY = y;

    var t = suave(yS / chegada);
    var g = Math.min(1, Math.max(0, (yS - chegada) / (palcoFim - chegada)));
    var giro = g < 0.5 ? 4 * g * g * g : 1 - Math.pow(-2 * g + 2, 3) / 2; // entra e sai devagar
    var forte = Math.sin(Math.PI * g); // brilho mais forte no meio do giro
    var passou = camada ? 0 : Math.max(0, y - palcoFim);

    if ((camada ? y - palcoFim : passou) > vh * 1.4) {
      if (!escondido) { canvas.style.visibility = 'hidden'; if (brilho) brilho.style.opacity = 0; escondido = true; }
      return;
    } else if (escondido) { canvas.style.visibility = 'visible'; escondido = false; }

    var desce = reduz ? 1 : sai(ms / DUR_DESCE);
    var luz = reduz ? 1 : piscar(ms - INICIO_LUZ);

    // texto do topo some enquanto o símbolo assume a tela
    if (texto) {
      var op = Math.max(0, 1 - t * 2.8);
      if (Math.abs(op - ultimoTexto) > 0.01) { texto.style.opacity = op.toFixed(2); ultimoTexto = op; }
    }

    // partida: a caixa ao lado (ou embaixo) do título; chegada: meio da tela
    // no celular a posição na tela é fixa (o meio da camada); quem move é a própria página
    var topoAlvo = camada ? meioQ : alvoY - y;
    var ini = pxParaMundo(alvoX, topoAlvo);
    var larg0 = alvoW * ini.k;
    var larg1 = Math.min(vw * 0.82, vh * 0.42 * (W / H)) * ini.k;
    var centro = pxParaMundo(vw / 2, camada ? meioQ : vh / 2 - passou);

    var x = lerp(ini.x, centro.x, t);
    var yy = lerp(ini.y, centro.y, t) + (1 - desce) * (mundoH * 0.55);
    var flutua = flutuar ? Math.sin(ms / 1400) * 0.04 * desce : 0;

    grupo.position.set(x, yy + flutua, 0);
    grupo.scale.setScalar(lerp(larg0, larg1, t) * (1 + 0.08 * forte));
    grupo.rotation.set(
      lerp(0.22, 0.32, t) + (1 - desce) * -0.6,
      lerp(-0.42, 0.38, t) + giro * Math.PI * 2 + (flutuar ? Math.sin(ms / 2600) * 0.05 * (1 - t) : 0),
      lerp(-0.05, -0.12, t)
    );

    var calor = t;
    frente.color.copy(corFrente0).lerp(corFrente1, calor);
    lado.color.copy(corLado0).lerp(corLado1, calor);
    frente.emissiveIntensity = luz * (0.04 + calor * 0.32 + forte * 0.55);
    lado.emissiveIntensity = 0.15 + luz * (0.2 + calor * 0.3 + forte * 0.5);
    quente.intensity = luz * (0.5 + calor * 1.2 + forte * 2.5);
    renderer.toneMappingExposure = 0.95 + luz * 0.08 - calor * 0.08 + forte * 0.12;

    var tamH = lerp(alvoW * 1.9, Math.max(vw, vh) * 0.95, t) * (1 + 0.3 * forte) * ini.k * 1.08;
    halo.position.x = x; halo.position.y = yy + flutua;
    halo.scale.set(tamH, tamH, 1);
    halo.material.opacity = Math.min(1, luz * (0.55 + calor * 0.45) * (1 + 0.6 * forte));

    renderer.render(cena, camera);
    if (!pronto) { pronto = true; document.documentElement.classList.add('tem-3d'); }
  }

  medir(true);
  medirPalco();
  requestAnimationFrame(quadro);
})();
