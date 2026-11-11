/* Smart Growth · palco 3D do símbolo
   O símbolo SG desce do alto e acende quando a página abre.
   Ao rolar, ele sai do lado do título, vai para o meio da tela, gira, cresce e brilha em laranja.
   Sem WebGL, fica a imagem estática no lugar. */
(function () {
  var alvo = document.querySelector('[data-g-alvo]');
  var palco = document.querySelector('[data-palco]');
  var canvas = document.querySelector('.palco3d-canvas');
  var brilho = document.querySelector('.palco3d-brilho');
  if (!alvo || !canvas || !window.THREE) return;

  var reduz = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var T = window.THREE;
  var renderer;
  try {
    renderer = new T.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  } catch (e) { return; }
  document.documentElement.classList.add('tem-3d');
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.outputEncoding = T.sRGBEncoding;
  renderer.toneMapping = T.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;

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
    depth: 0.16, bevelEnabled: true, bevelThickness: 0.014, bevelSize: 0.009, bevelSegments: 4, curveSegments: 40
  });
  geo.center();

  var corFrente0 = new T.Color('#F3F1EC'), corFrente1 = new T.Color('#F56A00');
  var corLado0 = new T.Color('#FA7715'), corLado1 = new T.Color('#B8400A');
  var frente = new T.MeshStandardMaterial({ color: corFrente0.clone(), roughness: 0.38, metalness: 0.08, emissive: new T.Color('#E85A00'), emissiveIntensity: 0 });
  var lado = new T.MeshStandardMaterial({ color: corLado0.clone(), roughness: 0.45, metalness: 0.12, emissive: new T.Color('#C2410C'), emissiveIntensity: 0.15 });
  var g = new T.Mesh(geo, [frente, lado]);
  var grupo = new T.Group();
  grupo.add(g);
  cena.add(grupo);

  cena.add(new T.AmbientLight(0xffffff, 0.35));
  var chave = new T.DirectionalLight(0xfff4e8, 1.6); chave.position.set(-4, 5, 6); cena.add(chave);
  var recorte = new T.DirectionalLight(0xff8a3d, 1.1); recorte.position.set(5, -2, -3); cena.add(recorte);
  var quente = new T.PointLight(0xff7a1a, 0, 9); quente.position.set(0, 0, 2.5); cena.add(quente);

  /* ---- medidas ---- */
  var vw = 0, vh = 0, mundoH = 0;
  function medir() {
    vw = window.innerWidth; vh = window.innerHeight;
    renderer.setSize(vw, vh, false);
    camera.aspect = vw / vh; camera.updateProjectionMatrix();
    mundoH = 2 * camera.position.z * Math.tan((camera.fov * Math.PI / 180) / 2);
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
  function piscar(ms) {
    // tremida de lâmpada acendendo, termina acesa
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

  var rodando = true;
  function quadro(agora) {
    var ms = agora - t0;
    var desce = reduz ? 1 : sai(ms / DUR_DESCE);
    var luz = reduz ? 1 : piscar(ms - INICIO_LUZ);

    // progresso da rolagem: 0 no topo, 1 quando o palco está no meio da tela
    var y = window.scrollY;
    var palcoTopo = palco.offsetTop, palcoAlt = palco.offsetHeight;
    var fim = Math.max(1, palcoTopo + palcoAlt / 2 - vh / 2);
    var t = suave(y / fim);
    var passou = Math.max(0, y - fim);

    if (passou > vh * 1.4) {
      if (rodando) { canvas.style.visibility = 'hidden'; if (brilho) brilho.style.opacity = 0; rodando = false; }
      requestAnimationFrame(quadro); return;
    } else if (!rodando) { canvas.style.visibility = 'visible'; rodando = true; }

    // ponto de partida: a caixa ao lado do título
    var r = alvo.getBoundingClientRect();
    // r.top já desconta a rolagem: no topo o símbolo acompanha a caixa, descendo ele vai para o centro
    var ini = pxParaMundo(r.left + r.width / 2, r.top + r.height / 2);
    var larg0 = r.width * ini.k;
    var larg1 = Math.min(vw * 0.78, vh * 0.42 * (W / H)) * ini.k;
    var centro = pxParaMundo(vw / 2, vh / 2 - passou);
    var x = lerp(ini.x, centro.x, t);
    var yy = lerp(ini.y, centro.y, t);
    var esc = lerp(larg0, larg1, t);

    // abertura: começa acima e desce
    yy += (1 - desce) * (mundoH * 0.55);
    var flutua = reduz ? 0 : Math.sin(ms / 1400) * 0.04 * desce;

    grupo.position.set(x, yy + flutua, 0);
    grupo.scale.setScalar(esc);
    grupo.rotation.set(
      lerp(0.22, 0.32, t) + (1 - desce) * -0.6,
      lerp(-0.42, 0.38, t) + Math.sin(ms / 2600) * 0.05 * (1 - t),
      lerp(-0.05, -0.12, t)
    );

    // brilho: acende na abertura e esquenta ao rolar
    var calor = t;
    frente.color.copy(corFrente0).lerp(corFrente1, calor);
    lado.color.copy(corLado0).lerp(corLado1, calor);
    frente.emissiveIntensity = luz * (0.04 + calor * 0.32);
    lado.emissiveIntensity = 0.15 + luz * (0.2 + calor * 0.3);
    quente.intensity = luz * (0.5 + calor * 1.2);
    renderer.toneMappingExposure = 0.95 + luz * 0.08 - calor * 0.08;

    if (brilho) {
      var bx = lerp(r.left + r.width / 2, vw / 2, t);
      var by = lerp(r.top + r.height / 2, vh / 2, t) - passou + (1 - desce) * -vh * 0.4;
      var tam = lerp(r.width * 1.9, Math.max(vw, vh) * 0.95, t);
      brilho.style.transform = 'translate(' + (bx - tam / 2) + 'px,' + (by - tam / 2) + 'px)';
      brilho.style.width = brilho.style.height = tam + 'px';
      brilho.style.opacity = (luz * (0.55 + calor * 0.45)).toFixed(3);
    }

    renderer.render(cena, camera);
    requestAnimationFrame(quadro);
  }

  medir();
  window.addEventListener('resize', medir);
  requestAnimationFrame(quadro);
})();
