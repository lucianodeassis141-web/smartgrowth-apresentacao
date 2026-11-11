(function () {
  var html = document.documentElement;
  html.classList.add('anima');

  // revelar ao entrar na tela
  var itens = document.querySelectorAll('[data-revelar]');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('visivel'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    itens.forEach(function (el) { io.observe(el); });
  } else { itens.forEach(function (el) { el.classList.add('visivel'); }); }

  // menu do celular
  var topo = document.querySelector('.topo'), bt = document.querySelector('.menu-bt');
  if (bt) {
    bt.addEventListener('click', function () {
      var aberto = topo.classList.toggle('aberto');
      bt.setAttribute('aria-expanded', aberto ? 'true' : 'false');
    });
    topo.querySelectorAll('nav a').forEach(function (a) { a.addEventListener('click', function () { topo.classList.remove('aberto'); }); });
  }

  // item do menu da seção visível
  var links = {};
  document.querySelectorAll('.topo nav a[href*="#"]').forEach(function (a) { links[a.getAttribute('href').split('#')[1]] = a; });
  if ('IntersectionObserver' in window) {
    var io2 = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var a = links[e.target.id]; if (!a) return;
        if (e.isIntersecting) { Object.values(links).forEach(function (l) { l.removeAttribute('aria-current'); }); a.setAttribute('aria-current', 'true'); }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(links).forEach(function (id) { var s = document.getElementById(id); if (s) io2.observe(s); });
  }
})();
