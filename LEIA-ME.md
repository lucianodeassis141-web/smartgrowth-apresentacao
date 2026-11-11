# Site de apresentação da Smart Growth

Pedido do Luciano em 11/11/2026: o site da RZD group (rzdgroup.com.br) adaptado para a SG, só para apresentar.
Mesma estrutura, mas com a identidade da SG (laranja, símbolo SG) e textos nossos, sem copiar os da RZD.

**No ar (11/11/2026, pedido do Luciano):** https://lucianodeassis141-web.github.io/smartgrowth-apresentacao/ (GitHub Pages, repositório público `lucianodeassis141-web/smartgrowth-apresentacao`, ramo main). O site oficial continua em `site-novo/` (smartgrowthai.com.br). Todas as páginas levam `noindex`.
Para atualizar: `python gerar.py`, depois `git add -A && git commit -m ... && git push` nesta pasta.

## O que tem
- `index.html`: topo com o **símbolo SG em 3D** (three.js). Ele desce do alto e acende como lâmpada quando a página abre. Ao rolar, vai para o meio da tela, gira, cresce e brilha em laranja (efeito do "R" da RZD). Sem WebGL, aparece o símbolo parado.
  No celular (11/11, na pegada da RZD): o G fica embaixo do texto e aparece na primeira tela, o texto some ao rolar, e o 3D é leve (resolução limitada, só desenha quando algo muda e ignora a barra do navegador).
  Depois vêm, nesta ordem: Serviços, Conceitos, Portfólio (esteira), Casos, A diferença, Como funciona, Sobre e Contato.
- `profissionais/` e `negocios/`: páginas por público, como as da RZD.
- `previa/<marca>/`: 8 sites conceito de marcas famosas: Nike, adidas, V4 Company, Smart Fit, Natura, O Boticário, Havaianas e Coca-Cola.
  **Todos marcados como "Conceito · projeto não oficial"** (faixa no topo, selo em cada print e nota nos casos). Escolha do Luciano em 11/11: as marcas aparecem como conceito, não como cliente.
  As marcas aparecem só como nome escrito, sem o logo oficial.
- `assets/telas/`: prints das prévias (computador e celular), usados nos cartões.

## Como mexer
- Textos, marcas e serviços ficam em `gerar.py`. Depois de mudar, rode `python gerar.py`.
- Se mudar uma prévia, tire os prints de novo (1280x800 e 390x780, sem a faixa) e salve em `assets/telas/` como `.webp`.
- Para abrir: `python -m http.server 8765` nesta pasta e acesse http://127.0.0.1:8765/. Também abre com dois cliques no index.html.

## Em aberto
- WhatsApp: os botões dizem "Chamar no WhatsApp" (pedido do Luciano, 11/11). Sem o número da SG, o link abre o WhatsApp com a mensagem pronta para escolher o contato. Quando houver número, pôr em `WHATSAPP` no `gerar.py`.
- Quem aparece no "Quem somos" (a RZD mostra os sócios): [PENDENTE DE VALIDAÇÃO]. Por enquanto, só o texto e o símbolo.
- Números do portfólio: 8 marcas conceito, 8 frentes e 3 passos. São reais e não dizem que alguém é cliente.
