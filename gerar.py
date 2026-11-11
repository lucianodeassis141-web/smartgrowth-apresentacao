# -*- coding: utf-8 -*-
"""Gera o site de apresentação da Smart Growth (estrutura no estilo RZD, identidade SG).
Rodar:  python gerar.py      (gera index.html, profissionais/, negocios/ e previa/<marca>/)
Os prints das prévias ficam em assets/telas/<marca>-pc.webp e <marca>-cel.webp (tirados à parte)."""
import os, html

AQUI = os.path.dirname(os.path.abspath(__file__))
import hashlib
def v(arq):
    return hashlib.md5(open(os.path.join(AQUI, "assets", arq), "rb").read()).hexdigest()[:8]

# Número do WhatsApp da SG, só dígitos com 55 e DDD (ex.: "5537999999999").
WHATSAPP = ""
INSTAGRAM = "https://instagram.com/smartgrowthai"
def contato_url(msg="Olá! Vi o site da Smart Growth e quero conversar."):
    from urllib.parse import quote
    # Sem número, o wa.me abre o WhatsApp com a mensagem pronta para escolher o contato.
    return f"https://wa.me/{WHATSAPP}?text={quote(msg)}"
CONTATO_ROTULO = "Chamar no WhatsApp"

e = html.escape

# ---------------- ícones ----------------
IC = {
 "monitor": '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/>',
 "celular": '<rect x="6" y="2" width="12" height="20" rx="2"/><path d="M11 18h2"/>',
 "robo": '<rect x="4" y="8" width="16" height="12" rx="2"/><path d="M12 4v4M9 13h.01M15 13h.01M9 17h6"/>',
 "pincel": '<path d="M12 20h9"/><path d="M16.4 3.6a2.1 2.1 0 1 1 3 3L7 19l-4 1 1-4Z"/>',
 "alvo": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
 "estrela": '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1Z"/>',
 "seta": '<path d="M5 12h14M12 5l7 7-7 7"/>',
 "voltar": '<path d="M19 12H5M12 19l-7-7 7-7"/>',
 "fora": '<path d="M7 17 17 7M7 7h10v10"/>',
 "lapis": '<path d="M13 21h8"/><path d="M21.2 6.8a1 1 0 0 0-4-4L3.8 16.2a2 2 0 0 0-.5.8l-1.3 4.4a.5.5 0 0 0 .6.6l4.4-1.3a2 2 0 0 0 .8-.5z"/>',
 "relogio": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 "conversa": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
 "x": '<path d="M18 6 6 18M6 6l12 12"/>',
 "ok": '<path d="M20 6 9 17l-5-5"/>',
 "grafico": '<path d="M3 3v18h18"/><path d="m7 15 4-4 4 4 5-6"/>',
 "engrenagem": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>',
 "mapa": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
 "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
}
def ic(nome, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{IC[nome]}</svg>'
IG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.4A4 4 0 1 1 12.6 8 4 4 0 0 1 16 11.4z"/><path d="M17.5 6.5h.01"/></svg>'
ZAP = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.7-.8-2-.9-.3-.1-.5-.1-.7.1-.2.3-.8.9-.9 1.1-.2.2-.3.2-.6.1-.3-.1-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.4-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.1 4.9 4.3 2.4.9 2.9.8 3.4.7.6-.1 1.7-.7 2-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.3zM12 21.8c-1.7 0-3.4-.5-4.9-1.3l-.4-.2-3.6.9 1-3.5-.2-.4A9.8 9.8 0 1 1 12 21.8zm0-21.6A11.8 11.8 0 0 0 1.9 18l-1.7 6 6.2-1.6A11.8 11.8 0 1 0 12 .2z"/></svg>'

# ---------------- marcas conceito ----------------
MARCAS = {
 "nike": dict(nome="Nike", seg="Esporte, calçados e vestuário", tipo="loja",
   bg="#0F0F0F", fg="#FFFFFF", ac="#D7FF3A", ac_fg="#0F0F0F", fonte="Anton",
   titulo="Feito para quem não para.", sub="Escolha o modelo, o tamanho e a cor. O pedido chega pronto no WhatsApp da loja mais perto de você.",
   itens=[("Tênis de corrida","Amortecimento para treino longo"),("Tênis casual","Do treino para a rua"),("Camiseta Dry","Tecido que seca rápido"),("Short de treino","Leve, com bolso para o celular"),("Mochila","Compartimento para o tênis"),("Meia esportiva","Kit com 3 pares")],
   cta="Montar meu pedido"),
 "adidas": dict(nome="adidas", seg="Lançamentos e coleções", tipo="lancamento",
   bg="#FFFFFF", fg="#000000", ac="#000000", ac_fg="#FFFFFF", fonte="Anton",
   titulo="O próximo lançamento sai sábado.", sub="Entre na lista e receba o aviso no WhatsApp antes de abrir para todo mundo.",
   itens=[("Coleção Originals","12 peças"),("Linha Running","8 peças"),("Futebol","Chuteiras e camisas"),("Infantil","Do 20 ao 36")],
   cta="Entrar na lista"),
 "v4": dict(nome="V4 Company", seg="Assessoria de marketing", tipo="agencia",
   bg="#0B0B0B", fg="#FFFFFF", ac="#E50914", ac_fg="#FFFFFF", fonte="Anton",
   titulo="Diagnóstico do seu marketing em 3 minutos.", sub="Responda seis perguntas. O robô monta o diagnóstico e um especialista chama você no WhatsApp com o plano.",
   itens=[("Tráfego pago","Google e Meta"),("CRM e vendas","Funil do lead ao fechamento"),("Conteúdo","Calendário e criativos"),("Dados","Painel com os números do mês")],
   cta="Fazer o diagnóstico"),
 "smartfit": dict(nome="Smart Fit", seg="Academia", tipo="academia",
   bg="#111111", fg="#FFFFFF", ac="#FFB800", ac_fg="#111111", fonte="Anton",
   titulo="Encosta o celular. O treino abre.", sub="Cada aparelho tem uma tag. O aluno aproxima o celular e vê o vídeo do instrutor da unidade mostrando o exercício certo.",
   itens=[("Leg press","Vídeo de 40 s · Instrutor da unidade"),("Supino","Vídeo de 35 s · Carga e postura"),("Puxada","Vídeo de 30 s · Pegada aberta"),("Esteira","Vídeo de 25 s · Intervalado"),("Cadeira extensora","Vídeo de 30 s"),("Remada baixa","Vídeo de 35 s")],
   cta="Ver os planos"),
 "natura": dict(nome="Natura", seg="Beleza e cuidados", tipo="catalogo",
   bg="#FFF6EE", fg="#3B2416", ac="#E8762D", ac_fg="#FFFFFF", fonte="Figtree",
   titulo="O catálogo da sua consultora, no celular.", sub="Escolha os produtos, monte a sacola e mande o pedido direto para a consultora pelo WhatsApp.",
   itens=[("Hidratante corporal","Pele macia o dia todo"),("Perfume feminino","Floral amadeirado"),("Perfume masculino","Fresco e cítrico"),("Sabonete em barra","Kit com 5"),("Óleo trifásico","Corpo e cabelo"),("Kit presente","Pronto para dar")],
   cta="Montar a sacola"),
 "boticario": dict(nome="O Boticário", seg="Perfumaria e maquiagem", tipo="agenda",
   bg="#F2F7F4", fg="#0E3B2E", ac="#0B7A55", ac_fg="#FFFFFF", fonte="Figtree",
   titulo="Maquiagem para o seu evento, com hora marcada.", sub="Escolha o serviço, o dia e o horário. A ficha de pele vai antes, e a maquiadora já sabe o que usar.",
   itens=[("Maquiagem social","50 min"),("Maquiagem de noiva","Com teste antes"),("Pele e preparação","30 min"),("Aula de automaquiagem","1 h")],
   cta="Agendar horário"),
 "havaianas": dict(nome="Havaianas", seg="Sandálias e brindes", tipo="personaliza",
   bg="#FFF8D6", fg="#1A1A1A", ac="#E2231A", ac_fg="#FFFFFF", fonte="Anton",
   titulo="A sandália com a marca da sua empresa.", sub="Escolha a cor, mande o logo e veja como fica antes de pedir. Para eventos, brindes e uniformes.",
   itens=[("Amarelo","Mais pedido"),("Azul","Eventos"),("Preto","Uniforme"),("Branco","Casamentos"),("Verde","Campanhas"),("Rosa","Ações de marca")],
   cta="Personalizar agora"),
 "cocacola": dict(nome="Coca-Cola", seg="Bebidas · campanha", tipo="campanha",
   bg="#F40009", fg="#FFFFFF", ac="#FFFFFF", ac_fg="#F40009", fonte="Anton",
   titulo="Abriu, ganhou.", sub="Digite o código da tampinha, gire a roleta e retire o prêmio no ponto de venda mais perto.",
   itens=[("Código da tampinha","8 letras e números"),("Roleta de prêmios","Na hora"),("Mapa dos pontos","Perto de você"),("Regulamento","Em linguagem simples")],
   cta="Cadastrar código"),
}
ORDEM = ["nike","adidas","v4","smartfit","natura","boticario","havaianas","cocacola"]

# casos (texto do caso conceito)
CASOS = {
 "nike": dict(cena="Uma loja de esporte com centenas de modelos, vendendo pela vitrine e pelo Instagram, sem um lugar onde o cliente veja tudo e peça sem esperar resposta.",
   feito=["Catálogo com busca por modelo, tamanho e cor","Sacola que manda o pedido pronto no WhatsApp da loja mais perto","Painel para atualizar estoque, preço e destaques pelo celular","Campanha no Google e na Meta com página própria para cada linha"],
   entregas=["Site e catálogo","Painel de gestão","Tráfego pago"]),
 "smartfit": dict(cena="Uma academia em que o aluno novo não sabe usar os aparelhos e o instrutor repete a mesma explicação o dia inteiro.",
   feito=["Tag NFC e QR Code em cada aparelho, abrindo o vídeo do instrutor da unidade","Página própria com o vídeo, sem anúncio de outra academia no meio","Contagem de toques por aparelho, para saber o que mais gera dúvida","Placa de avaliação no Google na recepção"],
   entregas=["Tags NFC","Aplicativo web","Perfil no Google"]),
 "boticario": dict(cena="Uma loja que faz maquiagem com hora marcada, com a agenda num caderno e as dúvidas da cliente chegando todas pelo WhatsApp.",
   feito=["Agendamento online com serviço, dia e horário","Ficha de pele que a cliente responde antes de chegar","Lembrete automático na véspera pelo WhatsApp","Robô que responde as dúvidas comuns e passa para a atendente"],
   entregas=["Site com agenda","Robô no WhatsApp","Automações"]),
 "natura": dict(cena="Uma consultora com o catálogo em PDF e os pedidos anotados um a um na conversa do WhatsApp.",
   feito=["Catálogo no celular com fotos, busca e sacola","Pedido pronto chegando no WhatsApp da consultora","Painel com pedidos, clientes e valores a receber","Posts do mês prontos na mesma identidade"],
   entregas=["Catálogo","Painel de gestão","Criativos"]),
 "havaianas": dict(cena="Uma fábrica que vende muito para empresas, mas faz cada orçamento de brinde personalizado à mão, por e-mail.",
   feito=["Personalizador: a empresa escolhe a cor, sobe o logo e vê como fica","Pedido mínimo e prazo calculados na tela","Orçamento que chega pronto no comercial","Página para cada tipo de cliente: evento, brinde e uniforme"],
   entregas=["Site sob medida","Automação de orçamento","SEO e GEO"]),
}

SERVICOS = [
 ("monitor","O essencial","Site profissional","Um site que apresenta a sua empresa, responde as dúvidas do cliente e leva direto para o seu WhatsApp.",["Textos por nossa conta","Feito para o celular","Pronto para o Google"]),
 ("celular","Com o seu nome","Sistema sob medida","Um sistema seu, para os clientes ou para a gestão: agenda, pedidos, estoque, acompanhamento. Do jeito que a sua rotina pede.",["Com a função que você precisar","Acesso para cada pessoa","Hospedagem e suporte"]),
 ("robo","Atende sozinho","Robô no WhatsApp e automações","Um robô que responde, qualifica e agenda, e automações que tiram do seu time o trabalho que se repete.",["Atendimento 24 horas","Passa para a pessoa certa","Ligado ao seu sistema"]),
 ("pincel","Sua marca","Identidade visual e criativos","Logo, cores e fontes pensados para o seu negócio, com o Instagram, os criativos e os roteiros na mesma linha.",["Logo e paleta","Manual da marca","Criativos e roteiros"]),
 ("alvo","Mais clientes","Tráfego pago, Google e IAs","Anúncios no Google e na Meta, o seu perfil no Google em ordem e a sua empresa aparecendo também nas respostas das IAs.",["Google Ads e Meta Ads","Google Meu Negócio","SEO e GEO"]),
]
SOB_MEDIDA = ("engrenagem","Sob medida","Marketing 360","Estratégia, consultoria e a gestão completa do marketing. Junte o que faz sentido para a sua empresa ou peça o que não está aqui. Montamos o projeto e o orçamento juntos.",["Combine os serviços","Gestão completa do marketing","Escopo e prazo na conversa"])

PROF_SERV = [
 ("monitor","Site com a sua cara","Uma página para cada serviço, com o seu registro profissional à vista quando o conselho pede."),
 ("relogio","Agenda online","O cliente escolhe o horário, e a mensagem chega pronta no seu WhatsApp."),
 ("lapis","Ficha antes do horário","Anamnese ou ficha de pele respondida de casa. Você atende já sabendo o que precisa."),
 ("celular","Painel no celular","Agenda, pacotes, caixa e lembretes, num sistema só seu."),
 ("robo","Robô que responde","Dúvidas de preço, endereço e horário respondidas na hora, de dia e de noite."),
 ("mapa","Google Meu Negócio","Perfil completo para aparecer no mapa de quem procura perto de você."),
]
NEG_SERV = [
 ("monitor","Site ou catálogo com pedido","Produtos com busca e sacola que manda o pedido pronto pelo WhatsApp."),
 ("grafico","Painel de estoque e pedidos","Você atualiza preço, estoque e destaques pelo celular, e o site muda na hora."),
 ("alvo","Anúncios no Google e na Meta","Campanha com página própria para cada produto, para o clique virar contato."),
 ("robo","Robô e automações","Atendimento, orçamento e acompanhamento rodando sozinhos, ligados ao seu sistema."),
 ("mapa","Google e IAs","Perfil no Google com fotos e avaliações, e a empresa aparecendo nas respostas das IAs."),
 ("pincel","Identidade e conteúdo","Logo, cores, criativos e roteiros na mesma linha."),
]

SEM = ["O cliente procura o seu nome, não acha nada e compra de quem apareceu primeiro",
       "A indicação chega desconfiada: sem site e sem prova, fica difícil decidir por você",
       "As vendas dependem do boca a boca e mudam muito de um mês para o outro",
       "Um perfil improvisado faz o seu produto parecer mais barato do que ele vale",
       "O time repete as mesmas respostas no WhatsApp o dia inteiro",
       "Concorrente com menos estrutura fica com cliente que seria seu"]
COM = ["A sua empresa aparece no Google e nas IAs quando procuram o que você vende",
       "A indicação vê o seu trabalho e já chega decidida",
       "Cliente chegando também pelo digital, com número para acompanhar",
       "Uma imagem profissional sustenta o seu preço sem precisar de desconto",
       "O robô responde as dúvidas e o time só fecha",
       "A sua marca é lembrada em todo lugar que o cliente encontra você"]

# ---------------- peças ----------------
def cabeca(titulo, desc, raiz):
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0B0D14">
<link rel="icon" href="{raiz}assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{raiz}assets/Anton.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{raiz}assets/sg.css?v={v("sg.css")}">
</head>
<body>
<div class="aviso-conceito">Apresentação · os projetos de marcas famosas são conceitos, sem vínculo com as marcas</div>
'''

def topo(raiz, pagina):
    base = "" if pagina == "inicio" else raiz
    def ativo(p): return ' aria-current="page"' if pagina == p else ""
    inicio = '' if pagina == "inicio" else f'<a href="{raiz}">Início</a>'
    return f'''<header class="topo">
  <div class="conteudo">
    <a class="logo" href="{raiz}" aria-label="Smart Growth, início"><img src="{raiz}assets/sg-horizontal-sem-slogan-negativo.svg" alt="Smart Growth" width="200" height="24"></a>
    <nav aria-label="Principal">
      {inicio}<a href="{base}#servicos">Serviços</a><a href="{raiz}profissionais/"{ativo("profissionais")}>Profissionais</a><a href="{raiz}negocios/"{ativo("negocios")}>Negócios</a><a href="{base}#casos">Casos</a><a href="{base}#sobre">Sobre</a><a href="{base}#contato">Contato</a>
    </nav>
    <div class="acoes">
      <a class="ig" href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram da Smart Growth">{IG}</a>
      <a class="bt bt-marca" href="{contato_url()}" target="_blank" rel="noopener">{ic("conversa")}Fale conosco</a>
      <button class="menu-bt" aria-label="Abrir o menu" aria-expanded="false">{ic("menu")}</button>
    </div>
  </div>
</header>
'''

def olho(txt):
    return f'<p class="olho"><span class="barras" aria-hidden="true"><i></i><i></i><i></i></span>{e(txt)}</p>'

def titulo_m(txt, destaque):
    """Título com a última parte em laranja."""
    return f'{e(txt)} <span class="m">{e(destaque)}</span>'

def secao_servicos(raiz):
    cards = []
    for i, (icn, tag, nome, desc, chips) in enumerate(SERVICOS):
        cards.append(f'''<article class="cartao" data-revelar style="--atraso:{(i%2)*0.08}s">
  <div class="cab"><span class="ic">{ic(icn)}</span><span class="tag">{e(tag)}</span></div>
  <h3>{e(nome)}</h3><p>{e(desc)}</p>
  <ul class="chips">{"".join(f"<li>{e(c)}</li>" for c in chips)}</ul>
  <a class="bt bt-tinta" href="{contato_url("Olá! Quero saber mais sobre " + nome + ".")}" target="_blank" rel="noopener">{ic("conversa")}Quero saber mais</a>
</article>''')
    icn, tag, nome, desc, chips = SOB_MEDIDA
    cards.append(f'''<article class="cartao larga" data-revelar>
  <div class="cab"><span class="ic">{ic(icn)}</span><span class="tag">{e(tag)}</span></div>
  <h3>{e(nome)}</h3><p>{e(desc)}</p>
  <ul class="chips">{"".join(f"<li>{e(c)}</li>" for c in chips)}</ul>
  <a class="bt" href="{contato_url("Olá! Quero montar um projeto com a Smart Growth.")}" target="_blank" rel="noopener">Montar meu projeto{ic("seta")}</a>
</article>''')
    return f'''<section id="servicos" class="secao clara seta">
  <div class="conteudo">
    <div data-revelar>{olho("Serviços")}</div>
    <h2 class="titulo" data-revelar>{titulo_m("Escolha como quer ser", "visto.")}</h2>
    <p class="intro apoio" data-revelar>Contrate um serviço ou junte vários. Você recebe tudo pronto, feito pela gente.</p>
    <div class="cartoes">{"".join(cards)}</div>
  </div>
</section>
'''

def tela(raiz, slug, cel=True, link=True):
    m = MARCAS[slug]
    flut = f'<div class="cel-flut"><img src="{raiz}assets/telas/{slug}-cel.webp" alt="" loading="lazy" width="390" height="780"></div>' if cel else ""
    lk = f'<a class="link" href="{raiz}previa/{slug}/" target="_blank" rel="noopener">{ic("fora")}Abrir o conceito</a>' if link else ""
    return f'''<div class="caso-tela" data-revelar>
  <div class="tela"><div class="barra"><i></i><i></i><i></i></div><span class="selo-conceito">Conceito</span><img src="{raiz}assets/telas/{slug}-pc.webp" alt="Tela do conceito para {e(m["nome"])}" loading="lazy" width="1280" height="800"></div>
  {flut}
  {lk}
</div>'''

def secao_casos(raiz, slugs, titulo, intro):
    blocos = []
    for s in slugs:
        m, c = MARCAS[s], CASOS[s]
        blocos.append(f'''<article class="caso">
  {tela(raiz, s)}
  <div data-revelar>
    <p class="seg">{e(m["seg"])} · conceito</p>
    <h3 class="titulo">{e(m["nome"])}</h3>
    <h4>O cenário</h4><p>{e(c["cena"])}</p>
    <h4>O que propomos</h4>
    <ul class="feito">{"".join(f"<li>{e(x)}</li>" for x in c["feito"])}</ul>
    <ul class="entregas">{"".join(f"<li>{e(x)}</li>" for x in c["entregas"])}</ul>
  </div>
</article>''')
    return f'''<section id="casos" class="secao escura seta depois-clara">
  <div class="conteudo">
    <div data-revelar>{olho("Casos")}</div>
    <h2 class="titulo" data-revelar>{titulo}</h2>
    <p class="intro apoio" data-revelar>{e(intro)}</p>
    <div class="casos">{"".join(blocos)}</div>
    <p class="nota">Projetos conceito criados pela Smart Growth para esta apresentação. Não foram encomendados pelas marcas, que pertencem aos seus donos.</p>
  </div>
</section>
'''

def secao_modelos(raiz, slugs):
    cards = []
    for i, s in enumerate(slugs):
        m = MARCAS[s]
        cards.append(f'''<article class="modelo" data-revelar style="--atraso:{i*0.07}s">
  <div class="cel"><span class="selo-conceito">Conceito</span><img src="{raiz}assets/telas/{s}-cel.webp" alt="Tela no celular do conceito para {e(m["nome"])}" loading="lazy" width="390" height="780"></div>
  <h3>{e(m["nome"])}</h3><p>{e(m["seg"])}</p>
  <a class="ver" href="{raiz}previa/{s}/" target="_blank" rel="noopener">Ver site{ic("seta")}</a>
</article>''')
    return f'''<section id="modelos" class="secao escura">
  <div class="conteudo">
    <div data-revelar>{olho("Conceitos")}</div>
    <h2 class="titulo" data-revelar>{titulo_m("Cada marca com o", "seu jeito.")}</h2>
    <p class="intro apoio" data-revelar>Sites conceito que montamos para mostrar o cuidado: a marca, as cores e o jeito de vender de quem está por trás. O seu segue o mesmo padrão.</p>
    <div class="modelos">{"".join(cards)}</div>
    <div class="centro"><a class="bt bt-marca" href="{contato_url("Olá! Quero um site assim.")}" target="_blank" rel="noopener">Quero o meu assim{ic("seta")}</a></div>
  </div>
</section>
'''

def secao_clientes(raiz, ordem):
    def card(s):
        m = MARCAS[s]
        return f'''<a class="cliente" href="{raiz}previa/{s}/" target="_blank" rel="noopener" tabindex="-1">
  <div class="tela"><div class="barra"><i></i><i></i><i></i></div><span class="selo-conceito">Conceito</span><img src="{raiz}assets/telas/{s}-pc.webp" alt="" width="1280" height="800"></div>
  <h3>{e(m["nome"])}</h3><span>{e(m["seg"])}</span>
</a>'''
    lista = "".join(card(s) for s in ordem)
    return f'''<section id="portfolio" class="secao clara seta">
  <div class="conteudo">
    <div data-revelar>{olho("Portfólio")}</div>
    <h2 class="titulo" data-revelar>{titulo_m("Seu negócio,", "sua identidade.")}</h2>
    <p class="intro apoio" data-revelar>Oito marcas conhecidas, oito conceitos diferentes. Passe o mouse para parar e clique em um deles para abrir o site.</p>
    <div class="numeros" data-revelar>
      <div><span>marcas em conceito</span><b>8</b></div>
      <div><span>frentes de serviço</span><b>8</b></div>
      <div><span>passos até o ar</span><b>3</b></div>
    </div>
  </div>
  <div class="esteira" data-revelar><div class="trilho">{lista}{lista.replace('tabindex="-1"', 'tabindex="-1" aria-hidden="true"')}</div></div>
  <div class="conteudo centro"><a class="bt bt-tinta" href="{contato_url("Olá! Quero um site assim.")}" target="_blank" rel="noopener">Quero o meu assim{ic("seta")}</a></div>
</section>
'''

def secao_diferenca():
    sem = "".join(f"<li>{ic('x')}<span>{e(x)}</span></li>" for x in SEM)
    com = "".join(f"<li>{ic('ok')}<span>{e(x)}</span></li>" for x in COM)
    return f'''<section id="diferenca" class="secao escura">
  <div class="conteudo">
    <div data-revelar>{olho("A diferença")}</div>
    <h2 class="titulo" data-revelar>{titulo_m("Estar na internet não é o mesmo que ser", "escolhido.")}</h2>
    <p class="intro apoio" data-revelar>O cliente decide em poucos segundos se confia em você. Veja o que muda quando a sua presença trabalha a seu favor.</p>
    <div class="comparar">
      <div class="lado-c" data-revelar><p class="rot">Sem presença</p><h3>Invisível para quem procura</h3><ul>{sem}</ul></div>
      <div class="lado-c forte" data-revelar style="--atraso:.1s"><p class="rot">Presença forte</p><h3>A primeira escolha de quem procura</h3><ul>{com}</ul></div>
    </div>
  </div>
</section>
'''

def secao_como():
    passos = [("01","Conversa","Você conta o que faz e como vende hoje, pelo WhatsApp ou por vídeo."),
              ("02","Prévia","Mostramos como fica o seu projeto, com a sua marca, antes de você decidir."),
              ("03","No ar","Publicamos, conferimos no celular e seguimos com você depois da entrega.")]
    li = "".join(f'<li data-revelar style="--atraso:{i*0.1}s"><b>{n}</b><h3>{t}</h3><p>{d}</p></li>' for i, (n, t, d) in enumerate(passos))
    return f'''<section id="como-funciona" class="secao escura" style="border-top:1px solid var(--linha-escura)">
  <div class="conteudo">
    <div data-revelar>{olho("Como funciona")}</div>
    <h2 class="titulo" data-revelar>{titulo_m("Do primeiro contato ao site", "no ar.")}</h2>
    <ol class="passos">{li}</ol>
  </div>
</section>
'''

def secao_sobre(raiz):
    return f'''<section id="sobre" class="secao clara seta">
  <div class="conteudo sobre">
    <div class="marca-bloco" data-revelar><img src="{raiz}assets/favicon.svg" alt="" width="300" height="184"><span>Crescimento inteligente</span></div>
    <div data-revelar>
      {olho("Sobre")}
      <h2 class="titulo">{titulo_m("Quem", "somos?")}</h2>
      <p>A Smart Growth é uma agência de marketing 360. Cuidamos do empresário e da empresa: site, sistema, automação, robô no WhatsApp, identidade, criativos e tráfego pago, tudo ligado.</p>
      <p>O nome quer dizer crescimento inteligente. A gente usa inteligência artificial onde ela economiza tempo e dinheiro, e gente onde precisa de gente.</p>
      <p>Você fala direto com a gente, do primeiro contato à entrega.</p>
      <a class="bt bt-tinta" href="{INSTAGRAM}" target="_blank" rel="noopener">{IG}Conheça nosso Instagram</a>
    </div>
  </div>
</section>
'''

def rodape(raiz):
    return f'''<section id="contato" class="contato">
  <div class="conteudo">
    <h2 class="titulo" data-revelar>{titulo_m("Inteligência que impulsiona", "resultados.")}</h2>
    <p class="intro" data-revelar>Conte o que você faz. Marcamos uma conversa rápida e mostramos como ficaria o seu projeto.</p>
    <a class="bt bt-marca" data-revelar href="{contato_url()}" target="_blank" rel="noopener">{ic("conversa")}{CONTATO_ROTULO}</a>
    <footer class="rodape">
      <img src="{raiz}assets/sg-horizontal-sem-slogan-negativo.svg" alt="Smart Growth" width="170" height="20">
      <div class="itens"><span>© 2026 Smart Growth</span><span>·</span><a href="{INSTAGRAM}" target="_blank" rel="noopener">@smartgrowthai</a><span>·</span><span>Marcas citadas nos conceitos pertencem aos seus donos</span></div>
    </footer>
  </div>
</section>
<a class="flutua-zap" href="{contato_url()}" target="_blank" rel="noopener" aria-label="{CONTATO_ROTULO}">{ZAP}</a>
<script src="{raiz}assets/sg.js?v={v("sg.js")}" defer></script>
'''

# ---------------- páginas ----------------
def pagina_inicio():
    r = ""
    h = cabeca("Smart Growth · Sites, sistemas e marketing", "Sites, sistemas, automações e marketing para profissionais e negócios.", r)
    h += topo(r, "inicio")
    h += '''<canvas class="palco3d-canvas" aria-hidden="true"></canvas><div class="palco3d-brilho" aria-hidden="true"></div>
<main>
<section id="inicio" class="inicio">
  <div class="conteudo">
    <div>
      <div data-revelar>''' + olho("Sites, sistemas e marketing para profissionais e negócios") + '''</div>
      <h1 class="titulo" data-revelar style="--atraso:.08s">Não basta estar na internet. É&nbsp;preciso <span class="m">ser escolhido.</span></h1>
      <p class="apoio" data-revelar style="--atraso:.16s">Fazemos sites, sistemas, automações e marketing para passar confiança, destacar a sua marca e aumentar as suas vendas.</p>
      <div data-revelar style="--atraso:.24s">
        <div class="bts"><a class="bt bt-marca" href="profissionais/">Sou profissional''' + ic("seta") + '''</a><a class="bt bt-linha" href="negocios/">Tenho um negócio''' + ic("seta") + '''</a></div>
        <a class="zap" href="''' + contato_url() + '''" target="_blank" rel="noopener">''' + ic("conversa") + '''Ou chame direto no WhatsApp</a>
      </div>
      <ul class="selos" data-revelar style="--atraso:.32s"><li>''' + ic("lapis") + '''Tudo feito por nós</li><li>''' + ic("relogio") + '''Prazo combinado desde o início</li><li>''' + ic("conversa") + '''Atendimento direto</li></ul>
    </div>
    <div class="lado-g"><div class="g-alvo" data-g-alvo><img src="assets/favicon.svg" alt="" width="440" height="270"></div></div>
  </div>
</section>
<div class="palco" data-palco aria-hidden="true"><p class="frase">Crescimento inteligente</p></div>
'''
    h += secao_servicos(r)
    h += secao_modelos(r, ["adidas","v4","havaianas","cocacola"])
    h += secao_clientes(r, ORDEM)
    h += secao_casos(r, ["nike","smartfit","boticario"], titulo_m("Trabalho que dá para", "abrir."), "Três conceitos completos, do cenário à proposta. Clique na tela para abrir o site.")
    h += secao_diferenca()
    h += secao_como()
    h += secao_sobre(r)
    h += '</main>\n' + rodape(r)
    h += f'<script src="assets/vendor/three.min.js" defer></script>\n<script src="assets/palco3d.js?v={v("palco3d.js")}" defer></script>\n</body>\n</html>\n'
    return h

def pagina_publico(chave):
    r = "../"
    if chave == "profissionais":
        t, d = "Smart Growth · Para profissionais", "Site, agenda, robô e Instagram para quem atende com hora marcada."
        rot, h1, sub = "Para profissionais", titulo_m("O seu trabalho já é bom. Agora ele precisa ser", "encontrado."), "Site, agenda, robô no WhatsApp e Instagram para dentistas, profissionais da estética, da saúde, academias e advogados. O cliente conhece você antes de chamar e já chega decidido."
        serv, s_tit, s_int = PROF_SERV, titulo_m("Tudo o que quem atende com hora marcada", "precisa."), "Montamos só o que faz sentido para a sua rotina. Você fala direto com a gente do começo ao fim."
        casos = ["smartfit","boticario"]; c_tit = titulo_m("Quem atende com hora marcada,", "em conceito."); c_int = "Uma academia e um serviço com agenda, cada um com o que a rotina pedia."
        mods = ["smartfit","boticario","natura","v4"]
    else:
        t, d = "Smart Growth · Para negócios", "Site, catálogo, sistema e anúncios para lojas, comércios e indústrias."
        rot, h1, sub = "Para negócios", titulo_m("Quem procura o que você vende precisa achar você", "primeiro."), "Site, catálogo, sistema e anúncios para lojas, comércios, distribuidoras e indústrias. O cliente vê o que você faz, escolhe e chama com o pedido pronto."
        serv, s_tit, s_int = NEG_SERV, titulo_m("Da vitrine ao pedido,", "tudo ligado."), "Montamos só o que faz sentido para o seu negócio. Você fala direto com a gente do começo ao fim."
        casos = ["nike","natura","havaianas"]; c_tit = titulo_m("Negócios,", "em conceito."); c_int = "Uma loja, uma revenda e uma fábrica, cada uma com o que o negócio pedia."
        mods = ["adidas","cocacola","havaianas","nike"]
    h = cabeca(t, d, r) + topo(r, chave)
    cards = "".join(f'''<article class="cartao" data-revelar style="--atraso:{(i%3)*0.07}s"><div class="cab"><span class="ic">{ic(a)}</span></div><h3>{e(b)}</h3><p>{e(c)}</p></article>''' for i, (a, b, c) in enumerate(serv))
    h += f'''<main>
<section id="inicio" class="pub-topo escura">
  <img class="g-fundo" src="{r}assets/favicon.svg" alt="">
  <div class="conteudo">
    <a class="voltar" href="{r}">{ic("voltar")}Voltar para o início</a>
    <div data-revelar style="margin-top:20px">{olho(rot)}</div>
    <h1 class="titulo" data-revelar>{h1}</h1>
    <p class="apoio" data-revelar>{e(sub)}</p>
    <div class="bts" data-revelar><a class="bt bt-marca" href="{contato_url()}" target="_blank" rel="noopener">{"Quero o meu site" if chave=="profissionais" else "Quero conversar"}{ic("seta")}</a><a class="bt bt-linha" href="#casos">Ver os casos</a></div>
  </div>
</section>
<section id="servicos" class="secao clara seta">
  <div class="conteudo">
    <div data-revelar>{olho("O que entregamos")}</div>
    <h2 class="titulo" data-revelar>{s_tit}</h2>
    <p class="intro apoio" data-revelar>{e(s_int)}</p>
    <div class="lista-servicos">{cards}</div>
  </div>
</section>
'''
    h += secao_casos(r, casos, c_tit, c_int)
    h += secao_clientes(r, mods + [s for s in ORDEM if s not in mods])
    h += secao_modelos(r, mods).replace('class="secao escura"', 'class="secao escura seta depois-clara"', 1)
    h += secao_como()
    h += secao_sobre(r)
    h += '</main>\n' + rodape(r) + '</body>\n</html>\n'
    return h

# ---------------- prévias (sites conceito) ----------------
def previa(slug):
    m = MARCAS[slug]
    fonte_t = "'Anton', Impact, sans-serif" if m["fonte"] == "Anton" else "'Figtree', system-ui, sans-serif"
    peso_t = "400" if m["fonte"] == "Anton" else "800"
    caixa = "uppercase" if m["fonte"] == "Anton" else "none"
    tipo = m["tipo"]
    # grade de itens
    def tile(i, nome, desc):
        if tipo == "personaliza":
            cores = {"Amarelo":"#FFD400","Azul":"#1F5FD1","Preto":"#1A1A1A","Branco":"#F4F4F4","Verde":"#1E9E57","Rosa":"#F27BA6"}
            c = cores.get(nome, m["ac"])
            vis = f'<div class="vis" style="background:linear-gradient(160deg,#fff,#f1f1f1)"><div class="sandalia" style="--c:{c}"><i></i></div></div>'
        elif tipo == "academia":
            vis = f'<div class="vis video"><span class="play"></span><span class="tag">NFC</span></div>'
        elif tipo in ("agenda",):
            vis = ""
        else:
            hue = (i * 47) % 360
            vis = f'<div class="vis"><div class="prod" style="--h:{hue}"></div></div>'
        extra = ""
        if tipo == "agenda":
            extra = '<div class="horas"><span>09:00</span><span>10:30</span><span class="on">14:00</span><span>16:30</span></div>'
        bt = {"loja":"Adicionar","catalogo":"Pôr na sacola","personaliza":"Escolher","lancamento":"Avise-me","academia":"Ver vídeo","agencia":"Saber mais","agenda":"Agendar","campanha":"Ver"}[tipo]
        return f'<article class="item">{vis}<div class="txt"><h3>{e(nome)}</h3><p>{e(desc)}</p>{extra}<button>{bt}</button></div></article>'
    itens = "".join(tile(i, n, d) for i, (n, d) in enumerate(m["itens"]))

    # bloco especial por tipo
    especial = ""
    if tipo == "lancamento":
        especial = '<div class="contagem"><div><b>02</b><span>dias</span></div><div><b>14</b><span>horas</span></div><div><b>37</b><span>min</span></div><div><b>09</b><span>seg</span></div></div>'
    elif tipo == "agencia":
        especial = '<div class="diag"><p class="q">Pergunta 3 de 6</p><h3>Quanto a sua empresa fatura por mês?</h3><div class="ops"><span>Até R$ 50 mil</span><span class="on">R$ 50 mil a R$ 200 mil</span><span>R$ 200 mil a R$ 1 milhão</span><span>Acima de R$ 1 milhão</span></div><div class="barra-p"><i style="width:50%"></i></div></div>'
    elif tipo == "campanha":
        especial = '<div class="codigo"><label>Código da tampinha</label><div class="campo"><span>A</span><span>7</span><span>K</span><span>2</span><span>P</span><span>9</span><span class="v"></span><span class="v"></span></div><button>Girar a roleta</button></div>'
    elif tipo == "academia":
        especial = '<div class="nfc"><div class="onda"></div><div class="fone"><div class="tela-f"><span class="play"></span><p>Leg press<br><small>Instrutor da unidade</small></p></div></div></div>'
    elif tipo == "agenda":
        especial = '<div class="cal"><p class="q">Novembro</p><div class="dias">' + "".join(f'<span class="{"on" if d==21 else ("x" if d in (16,23) else "")}">{d}</span>' for d in range(10, 31)) + '</div></div>'
    elif tipo == "personaliza":
        especial = '<div class="perso"><div class="sandalia grande" style="--c:#FFD400"><i></i><span class="logo-cli">SUA MARCA</span></div><div class="ops"><span style="background:#FFD400"></span><span style="background:#1F5FD1"></span><span style="background:#1A1A1A"></span><span style="background:#1E9E57"></span><span style="background:#E2231A"></span></div></div>'
    else:  # loja / catalogo
        especial = '<div class="destaque"><div class="prod grande" style="--h:20"></div><div class="sacola"><b>Sacola</b><p>2 itens</p><button>Enviar pedido no WhatsApp</button></div></div>'

    titulos_sec = {"loja":"Mais vendidos","catalogo":"Do catálogo","personaliza":"Cores","lancamento":"Coleções","academia":"Aparelhos com vídeo","agencia":"O que fazemos","agenda":"Serviços","campanha":"Como funciona"}
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(m["nome"])} · conceito Smart Growth</title>
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="../../assets/favicon.svg" type="image/svg+xml">
<style>
@font-face {{ font-family: "Anton"; src: url("../../assets/Anton.woff2") format("woff2"); font-display: swap; }}
@font-face {{ font-family: "Figtree"; src: url("../../assets/Figtree.woff2") format("woff2"); font-weight: 300 900; font-display: swap; }}
:root {{ --bg: {m["bg"]}; --fg: {m["fg"]}; --ac: {m["ac"]}; --acfg: {m["ac_fg"]}; color-scheme: light dark; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: var(--bg); color: var(--fg); font: 400 16px/1.55 "Figtree", system-ui, sans-serif; overflow-x: hidden; }}
.t {{ font-family: {fonte_t}; font-weight: {peso_t}; text-transform: {caixa}; line-height: 1; letter-spacing: -.005em; }}
button {{ font: 700 .85rem "Figtree", sans-serif; border: 0; cursor: pointer; background: var(--ac); color: var(--acfg); padding: 12px 18px; border-radius: 999px; }}
.faixa {{ background: #0B0D14; color: #FF9A3D; font: 800 .68rem "Figtree", sans-serif; letter-spacing: .14em; text-transform: uppercase; text-align: center; padding: 7px 16px; }}
.faixa a {{ color: #F3F4F8; text-decoration: underline; }}
.w {{ width: min(1140px, 100% - 32px); margin-inline: auto; }}
header .w {{ display: flex; align-items: center; justify-content: space-between; height: 68px; }}
header .marca {{ font-size: 1.7rem; }}
header nav {{ display: flex; gap: 24px; font-weight: 600; font-size: .9rem; opacity: .8; }}
.hero {{ padding: 56px 0 72px; }}
.hero .w {{ display: grid; grid-template-columns: 1.1fr .9fr; gap: 48px; align-items: center; }}
.hero .seg {{ font-weight: 800; font-size: .72rem; letter-spacing: .2em; text-transform: uppercase; color: var(--ac); }}
.hero h1 {{ margin-top: 16px; font-size: clamp(2.6rem, 6vw, 5rem); }}
.hero p {{ margin-top: 18px; max-width: 30rem; opacity: .8; font-size: 1.08rem; }}
.hero button {{ margin-top: 28px; padding: 16px 28px; font-size: .95rem; }}
section.lista {{ padding: 24px 0 80px; }}
section.lista h2 {{ font-size: clamp(1.8rem, 3vw, 2.4rem); margin-bottom: 24px; }}
.grade {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }}
.item {{ border-radius: 14px; overflow: hidden; background: color-mix(in srgb, var(--fg) 6%, var(--bg)); box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--fg) 10%, transparent); display: flex; flex-direction: column; }}
.item .vis {{ aspect-ratio: 4/3; display: grid; place-items: center; background: color-mix(in srgb, var(--fg) 4%, var(--bg)); position: relative; }}
.item .txt {{ padding: 16px; display: flex; flex-direction: column; gap: 4px; flex: 1; }}
.item h3 {{ font-size: 1.05rem; }}
.item p {{ opacity: .65; font-size: .88rem; }}
.item button {{ margin-top: auto; align-self: flex-start; padding: 9px 16px; font-size: .78rem; }}
.item .txt p + button {{ margin-top: 12px; }}
.prod {{ width: 54%; aspect-ratio: 1; border-radius: 30% 70% 60% 40% / 50% 40% 60% 50%; background: linear-gradient(140deg, hsl(var(--h) 70% 62%), hsl(calc(var(--h) + 40) 60% 40%)); box-shadow: 0 30px 40px -24px rgba(0,0,0,.55); transform: rotate(-12deg); }}
.prod.grande {{ width: 70%; }}
.video {{ background: linear-gradient(160deg, #2a2a2a, #121212) !important; }}
.play {{ width: 54px; height: 54px; border-radius: 50%; background: var(--ac); position: relative; }}
.play::after {{ content: ""; position: absolute; left: 21px; top: 16px; border-left: 16px solid var(--acfg); border-top: 11px solid transparent; border-bottom: 11px solid transparent; }}
.video .tag {{ position: absolute; top: 12px; left: 12px; font: 800 .65rem "Figtree"; letter-spacing: .12em; background: var(--ac); color: var(--acfg); padding: 4px 8px; border-radius: 4px; }}
.sandalia {{ width: 38%; aspect-ratio: 1/2.1; border-radius: 48% 48% 44% 44% / 30% 30% 22% 22%; background: var(--c); box-shadow: inset 0 0 0 4px rgba(0,0,0,.08), 0 24px 30px -18px rgba(0,0,0,.5); position: relative; transform: rotate(-14deg); }}
.sandalia i {{ position: absolute; left: 50%; top: 18%; width: 70%; height: 30%; transform: translateX(-50%); border: 5px solid rgba(255,255,255,.95); border-bottom: 0; border-radius: 50% 50% 0 0; }}
.sandalia .logo-cli {{ position: absolute; bottom: 20%; left: 0; right: 0; text-align: center; font: 900 .7rem "Figtree"; letter-spacing: .1em; color: rgba(0,0,0,.6); }}
.sandalia.grande {{ width: 34%; }}
.horas {{ display: flex; gap: 6px; flex-wrap: wrap; margin-top: 10px; }}
.horas span {{ font-size: .75rem; font-weight: 700; padding: 4px 8px; border-radius: 6px; box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--fg) 20%, transparent); }}
.horas .on {{ background: var(--ac); color: var(--acfg); box-shadow: none; }}
/* blocos especiais */
.painel {{ border-radius: 20px; padding: 28px; background: color-mix(in srgb, var(--fg) 7%, var(--bg)); box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--fg) 12%, transparent), 0 40px 80px -50px rgba(0,0,0,.6); min-height: 340px; display: grid; place-items: center; }}
.destaque {{ width: 100%; display: grid; grid-template-columns: 1fr .8fr; gap: 16px; align-items: center; }}
.destaque .prod {{ justify-self: center; }}
.sacola {{ background: var(--bg); border-radius: 14px; padding: 18px; display: flex; flex-direction: column; gap: 6px; box-shadow: 0 10px 30px -15px rgba(0,0,0,.4); }}
.sacola button {{ margin-top: 10px; font-size: .74rem; }}
.contagem {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; width: 100%; }}
.contagem div {{ text-align: center; padding: 22px 6px; border-radius: 12px; background: var(--ac); color: var(--acfg); }}
.contagem b {{ display: block; font: 400 3rem/1 "Anton", sans-serif; }}
.contagem span {{ font-size: .75rem; text-transform: uppercase; letter-spacing: .14em; opacity: .8; }}
.diag {{ width: 100%; }}
.q {{ font-size: .75rem; font-weight: 800; letter-spacing: .16em; text-transform: uppercase; color: var(--ac); }}
.diag h3 {{ margin: 10px 0 18px; font-size: 1.4rem; }}
.ops {{ display: flex; flex-direction: column; gap: 8px; }}
.diag .ops span {{ padding: 12px 14px; border-radius: 10px; box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--fg) 18%, transparent); font-weight: 600; }}
.diag .ops .on {{ box-shadow: inset 0 0 0 2px var(--ac); background: color-mix(in srgb, var(--ac) 14%, transparent); }}
.barra-p {{ margin-top: 18px; height: 6px; border-radius: 3px; background: color-mix(in srgb, var(--fg) 12%, transparent); }}
.barra-p i {{ display: block; height: 100%; border-radius: 3px; background: var(--ac); }}
.codigo {{ width: 100%; text-align: center; }}
.codigo label {{ font-weight: 800; letter-spacing: .14em; text-transform: uppercase; font-size: .75rem; }}
.campo {{ margin: 14px 0 22px; display: flex; gap: 8px; justify-content: center; }}
.campo span {{ width: 44px; height: 58px; border-radius: 10px; background: #fff; color: #222; display: grid; place-items: center; font: 400 1.8rem "Anton", sans-serif; }}
.campo .v {{ background: rgba(255,255,255,.35); }}
.codigo button {{ padding: 16px 30px; font-size: .95rem; }}
.nfc {{ position: relative; width: 100%; height: 300px; display: grid; place-items: center; }}
.onda {{ position: absolute; width: 240px; height: 240px; border-radius: 50%; box-shadow: 0 0 0 2px var(--ac), 0 0 0 26px color-mix(in srgb, var(--ac) 18%, transparent), 0 0 0 58px color-mix(in srgb, var(--ac) 8%, transparent); }}
.fone {{ position: relative; width: 150px; height: 290px; border-radius: 26px; background: #000; padding: 8px; box-shadow: 0 30px 50px -20px rgba(0,0,0,.8); }}
.tela-f {{ height: 100%; border-radius: 19px; background: linear-gradient(170deg, #333, #111); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 14px; color: #fff; text-align: center; font-weight: 700; }}
.tela-f small {{ font-weight: 400; opacity: .6; }}
.cal {{ width: 100%; }}
.dias {{ margin-top: 12px; display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px; }}
.dias span {{ aspect-ratio: 1; display: grid; place-items: center; border-radius: 10px; font-weight: 700; background: var(--bg); }}
.dias .on {{ background: var(--ac); color: var(--acfg); }}
.dias .x {{ opacity: .3; }}
.perso {{ width: 100%; display: flex; flex-direction: column; align-items: center; gap: 22px; }}
.perso .ops {{ flex-direction: row; }}
.perso .ops span {{ width: 34px; height: 34px; border-radius: 50%; box-shadow: 0 0 0 3px var(--bg), 0 0 0 4px color-mix(in srgb, var(--fg) 25%, transparent); }}
.selos {{ padding: 48px 0; background: color-mix(in srgb, var(--fg) 5%, var(--bg)); }}
.selos .w {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }}
.selos b {{ display: block; font-size: 1.05rem; }}
.selos p {{ opacity: .65; font-size: .9rem; }}
footer {{ padding: 36px 0 48px; font-size: .8rem; opacity: .7; }}
footer .w {{ display: flex; justify-content: space-between; gap: 16px; flex-wrap: wrap; }}
.zap {{ position: fixed; right: 18px; bottom: 18px; width: 56px; height: 56px; border-radius: 50%; background: #25D366; display: grid; place-items: center; box-shadow: 0 10px 24px -8px rgba(0,0,0,.5); }}
.zap svg {{ width: 28px; height: 28px; color: #fff; }}
@media (max-width: 820px) {{
  header nav {{ display: none; }}
  .hero .w {{ grid-template-columns: 1fr; }}
  .hero {{ padding-top: 32px; }}
  .grade {{ grid-template-columns: 1fr 1fr; gap: 10px; }}
  .item .txt {{ padding: 12px; }}
  .selos .w {{ grid-template-columns: 1fr; }}
  .contagem b {{ font-size: 2.2rem; }}
}}
</style>
</head>
<body>
<div class="faixa">Conceito Smart Growth · projeto não oficial, sem vínculo com a marca · <a href="../../">voltar</a></div>
<header><div class="w"><span class="marca t">{e(m["nome"])}</span><nav><span>Início</span><span>{e(titulos_sec[tipo])}</span><span>Sobre</span><span>Contato</span></nav><button>{e(m["cta"])}</button></div></header>
<section class="hero"><div class="w">
  <div><p class="seg">{e(m["seg"])}</p><h1 class="t">{e(m["titulo"])}</h1><p>{e(m["sub"])}</p><button>{e(m["cta"])}</button></div>
  <div class="painel">{especial}</div>
</div></section>
<section class="lista"><div class="w"><h2 class="t">{e(titulos_sec[tipo])}</h2><div class="grade">{itens}</div></div></section>
<section class="selos"><div class="w">
  <div><b>Pedido pelo WhatsApp</b><p>Sem taxa por venda e sem cadastro.</p></div>
  <div><b>Feito para o celular</b><p>Abre rápido em qualquer aparelho.</p></div>
  <div><b>Painel de gestão</b><p>A equipe atualiza tudo pelo celular.</p></div>
</div></section>
<footer><div class="w"><span>{e(m["nome"])} é marca de seus donos. Site conceito feito pela Smart Growth para apresentação.</span><span>Smart Growth · Inteligência que impulsiona resultados.</span></div></footer>
<span class="zap" aria-hidden="true">{ZAP}</span>
</body>
</html>
'''

def gravar(rel, txt):
    p = os.path.join(AQUI, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)

if __name__ == "__main__":
    gravar("index.html", pagina_inicio())
    gravar("profissionais/index.html", pagina_publico("profissionais"))
    gravar("negocios/index.html", pagina_publico("negocios"))
    for s in ORDEM:
        gravar(f"previa/{s}/index.html", previa(s))
    print("ok:", 3 + len(ORDEM), "páginas")
