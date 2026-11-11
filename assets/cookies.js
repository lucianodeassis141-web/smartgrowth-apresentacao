/* Aviso de cookies (LGPD): o Google Analytics só carrega depois do "Aceitar".
   Recusar apaga os cookies _ga. A escolha fica neste navegador e muda pelo link "Cookies" do rodapé. */
(function () {
  'use strict';
  var GA = 'G-K83D5QED08', CHAVE = 'sg-cookies';
  function le() { try { return localStorage.getItem(CHAVE); } catch (e) { return null; } }
  function grava(v) { try { localStorage.setItem(CHAVE, v); } catch (e) {} }

  function ligaGA() {
    if (window.__sgGA) return; window.__sgGA = true;
    window['ga-disable-' + GA] = false;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA);
    var s = document.createElement('script'); s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA;
    document.head.appendChild(s);
  }
  function apagaGA() {
    window['ga-disable-' + GA] = true;
    var partes = location.hostname.split('.'), dominios = [''];
    for (var i = 0; i < partes.length - 1; i++) dominios.push('.' + partes.slice(i).join('.'));
    document.cookie.split(';').forEach(function (c) {
      var nome = c.split('=')[0].trim();
      if (!/^_ga/.test(nome)) return;
      dominios.forEach(function (d) {
        document.cookie = nome + '=; Max-Age=0; path=/' + (d ? '; domain=' + d : '');
      });
    });
  }

  var css = '.ck{position:fixed;left:16px;right:16px;bottom:16px;z-index:60;max-width:560px;margin-left:auto;padding:20px 22px;border-radius:16px;background:#121A33;color:#F4F5F8;box-shadow:0 18px 50px -12px rgba(0,0,0,.55);font:400 15px/1.5 Figtree,system-ui,sans-serif}' +
    '.ck p{margin:0}.ck a{color:#FF9A3D}.ck-acoes{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}' +
    '.ck button{min-height:46px;padding:0 20px;border:0;border-radius:10px;font:700 15px Figtree,system-ui,sans-serif;cursor:pointer}' +
    '.ck .ck-sim{background:#FA7715;color:#11141F}.ck .ck-sim:hover{background:#E85F08}' +
    '.ck .ck-nao{background:transparent;color:#F4F5F8;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.3)}.ck .ck-nao:hover{background:rgba(255,255,255,.08)}' +
    '.ck :focus-visible{outline:3px solid #FF9A3D;outline-offset:3px}';
  var caixa = null, volta = null;

  function fecha() {
    if (!caixa) return;
    caixa.remove(); caixa = null;
    if (volta && volta.focus) volta.focus();
  }
  function abre(foco) {
    if (caixa) return;
    if (!document.getElementById('ck-css')) {
      var st = document.createElement('style'); st.id = 'ck-css'; st.textContent = css; document.head.appendChild(st);
    }
    caixa = document.createElement('section');
    caixa.className = 'ck'; caixa.setAttribute('aria-label', 'Aviso de cookies');
    caixa.innerHTML = '<p>Usamos cookies do Google Analytics para contar as visitas e saber como as pessoas chegam ao site. Eles só são ligados se você aceitar. <a href="/privacidade/">Política de privacidade</a></p>' +
      '<div class="ck-acoes"><button type="button" class="ck-sim">Aceitar</button><button type="button" class="ck-nao">Recusar</button></div>';
    document.body.appendChild(caixa);
    caixa.querySelector('.ck-sim').addEventListener('click', function () { grava('sim'); ligaGA(); fecha(); });
    caixa.querySelector('.ck-nao').addEventListener('click', function () { grava('nao'); apagaGA(); fecha(); });
    if (foco) { volta = document.activeElement; caixa.querySelector('.ck-sim').focus(); }
  }

  window.sgCookies = { abrir: function () { abre(true); } };
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('[data-cookies]');
    if (a) { e.preventDefault(); abre(true); }
  });

  var v = le();
  if (v === 'sim') ligaGA();
  else if (v === 'nao') apagaGA();
  else if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { abre(false); });
  else abre(false);
})();
