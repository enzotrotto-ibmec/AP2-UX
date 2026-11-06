# -*- coding: utf-8 -*-
"""
MANIFESTO DE IMAGENS - Ristorantti Cucina Italiana (AP2 Design Grafico e UX)

Lista TODAS as imagens do site com:
  - nome de arquivo estrategico para SEO (palavras-chave, sem acento, separado por hifen)
  - dimensao EXATA da imagem equivalente no template Royal Hotel (exigencia do professor)
  - texto "alt" e "title" (usados tambem no HTML)
  - de qual foto-base (chave "src") ela e recortada

Para trocar uma foto: coloque o ORIGINAL em  fotos-originais/<chave>.jpg  (ex.: ossobuco.jpg)
e rode  python ferramentas/imagens.py  - todas as versoes recortadas/otimizadas sao refeitas.
"""

MARCA = "Ristorantti Cucina Italiana"

# --------------------------------------------------------------------------
# FOTOS-BASE: chave -> (nome curto, o que a foto deve mostrar)
# --------------------------------------------------------------------------
FONTES = {
    # ja temos (fotos escolhidas pelo grupo; versao provisoria em ferramentas/fontes-provisorias)
    "terraco":    ("Terraco italiano",   "Terraco/patio rustico com mesas e cadeiras azuis, vasos de flores e guarda-sois (min. 1920 px de largura)"),
    "pizza_forno": ("Pizza no forno",    "Pizza artesanal sobre bandeja, com manjericao e tomates ao redor (min. 1920 px de largura)"),
    "pizza":      ("Pizza margherita",   "Close de pizza margherita com folhas de manjericao"),
    "ossobuco":   ("Ossobuco al Ragu",   "Prato de ossobuco com molho de tomate, cenoura e salsinha"),
    "lasanha":    ("Lasagna Bolognese",  "Fatia de lasanha a bolonhesa gratinada em prato branco"),
    "camarao":    ("Massa com camarao",  "Tagliatelle/espaguete com camaroes e ervas frescas"),
    "salao":      ("Salao principal",    "Salao interno rustico do restaurante"),
    "bar":        ("Bar principal",      "Bar com prateleiras de garrafas e banquetas"),
    "cerveja":    ("Area da cerveja",    "Balcao com chopeiras de cerveja"),
    "externa":    ("Area externa",       "Rua/area externa italiana com mesas ao ar livre"),
    # ainda NAO temos - 8 pratos do cardapio (quadro "FOTO PENDENTE" ate chegarem)
    "bruschetta":     ("Bruschetta",       "Bruschetta al pomodoro: pao tostado com tomate, manjericao e azeite"),
    "caprese":        ("Insalata Caprese", "Salada caprese: tomate, mussarela de bufala e manjericao"),
    "carbonara":      ("Carbonara",        "Spaghetti alla carbonara com queijo pecorino e pimenta"),
    "nhoque":         ("Nhoque ao sugo",   "Nhoque de batata ao molho de tomate com parmesao"),
    "risoto":         ("Risoto alla Milanese", "Risoto cremoso de açafrão em prato fundo"),
    "quatro_queijos": ("Quatro queijos",   "Pizza quattro formaggi"),
    "tiramisu":       ("Tiramisu",         "Fatia de tiramisu com cacau"),
    "panna_cotta":    ("Panna cotta",      "Panna cotta com calda de frutas vermelhas"),
    # fotos de perfil fictícias (rostos gerados por IA) dos depoimentos - ja baixadas
    "cliente_ana":    ("Perfil Ana Beatriz",   "Rosto de mulher jovem, fundo neutro (1024 x 1024 px)"),
    "cliente_rafael": ("Perfil Rafael",        "Rosto de homem, fundo neutro (1024 x 1024 px)"),
    "cliente_camila": ("Perfil Camila",        "Rosto de mulher sorrindo (1024 x 1024 px)"),
    "cliente_lucas":  ("Perfil Lucas",         "Rosto de homem jovem sorrindo (1024 x 1024 px)"),
}

# --------------------------------------------------------------------------
# SLOTS: id -> especificacao
#   out   : caminho dentro de royal-master/image/
#   w,h   : dimensao EXATA do template
#   kind  : foto | css | avatar | logo | favicon | promo
#   src   : chave da foto-base (FONTES)
#   focus : ponto de interesse (x,y de 0 a 1) usado no recorte
#   zoom  : 1 = recorte maximo; >1 aproxima
# --------------------------------------------------------------------------
SLOTS = {}


def _add(id, out, w, h, kind="foto", src=None, focus=(.5, .5), zoom=1.0,
         alt="", title="", ini="", cor=""):
    assert id not in SLOTS, id
    SLOTS[id] = dict(id=id, out=out, w=w, h=h, kind=kind, src=src, focus=focus,
                     zoom=zoom, alt=alt, title=title, ini=ini, cor=cor)


def foto(id, out, w, h, src, alt, title, focus=(.5, .5), zoom=1.0):
    _add(id, out, w, h, "foto", src, focus, zoom, alt, title)


def fundo(id, out, w, h, src, focus=(.5, .5), zoom=1.0):
    """Imagem usada so no CSS (background) - nao tem alt/title."""
    _add(id, out, w, h, "css", src, focus, zoom)


def avatar(id, out, tam, ini, cor, alt, title):
    _add(id, out, tam, tam, "avatar", None, (.5, .5), 1.0, alt, title, ini, cor)


# ---------------- marca ----------------
_add("logo", "logo-ristorantti-cucina-italiana.png", 460, 100, "logo", None, (.5, .5), 1.0,
     "Logotipo do Ristorantti Cucina Italiana", "Ristorantti Cucina Italiana - Início")
_add("favicon", "favicon.png", 64, 64, "favicon", None, (.5, .5), 1.0, "", "")

# ---------------- fundos (CSS) ----------------
fundo("bg_banner",     "restaurante-cucina-italiana.webp",                      1920, 1210, "terraco")
fundo("bg_facilidades", "pizza-italiana-artesanal-ingredientes-frescos.webp",   1920, 1140, "pizza_forno")
fundo("bg_cabecalho",  "cabecalho-terraco-italiano-mesas-flores.webp",          1920, 1042, "terraco", (.5, .55))
fundo("bg_blog",       "cabecalho-blog-pizza-forno-manjericao.webp",            1920, 1116, "pizza_forno")
fundo("bg_post",       "cabecalho-post-fachada-rustica-cantina-italiana.webp",  1920, 1127, "terraco", (.5, .2))

# ---------------- index: areas do restaurante (template: room1-4) ----------------
foto("area_salao", "ambientes/salao-principal-restaurante-italiano-rustico.webp", 263, 270, "salao",
     "Área comum do restaurante: salão com mesas e cadeiras de madeira e decoração rústica italiana",
     "Área comum - Ristorantti Cucina Italiana")
foto("area_bar", "ambientes/bar-principal-garrafas-banquetas-restaurante-italiano.webp", 262, 270, "bar",
     "Bar principal do restaurante italiano com prateleiras de garrafas e banquetas ao balcão",
     "Bar principal - Ristorantti Cucina Italiana")
foto("area_cerveja", "ambientes/area-da-cerveja-chopeiras-bar-cantina-italiana.webp", 263, 270, "cerveja",
     "Área da cerveja com chopeiras de cervejas importadas sobre o balcão de madeira",
     "Área da cerveja - Ristorantti Cucina Italiana")
foto("area_externa", "ambientes/area-externa-mesas-rua-italiana-bar-pizzaria.webp", 262, 270, "externa",
     "Área externa do restaurante com mesas ao ar livre em uma charmosa rua italiana",
     "Área externa - Ristorantti Cucina Italiana")

# ---------------- index: sobre nos (template: about_bg) ----------------
foto("sobre_pizza", "pizza-margherita-manjericao-massa-artesanal.webp", 555, 450, "pizza",
     "Pizza margherita artesanal com molho de tomate, queijo derretido e folhas de manjericão fresco",
     "Pizza margherita artesanal - Ristorantti Cucina Italiana")

# ---------------- about.html (template: about_bg, 555x450) ----------------
foto("sobre_terraco", "cantina-terraco-rustico-historia-sobre-nos.webp", 555, 450, "terraco",
     "Terraço rústico da cantina com mesas, cadeiras azuis e vasos de flores diante da fachada de pedra",
     "Nossa cantina - Ristorantti Cucina Italiana", (.4, .5), 1.0)

# ---------------- index: ultimas do blog (template: blog-1..3, 360x260) ----------------
foto("blog_ossobuco", "blog/ossobuco-al-ragu-prato-tradicional-italiano.webp", 360, 260, "ossobuco",
     "Ossobuco al Ragù servido em prato branco com molho de tomate, cenoura e salsinha",
     "Ossobuco al Ragù - receita italiana tradicional")
foto("blog_lasanha", "blog/lasagna-alla-bolognese-receita-italiana.webp", 360, 260, "lasanha",
     "Fatia de lasagna alla Bolognese com camadas de massa, ragù e queijo gratinado",
     "Lasagna alla Bolognese - receita italiana")
foto("blog_camarao", "blog/tagliatelle-con-gamberi-camarao-massa-fresca.webp", 360, 260, "camarao",
     "Tagliatelle con Gamberi: massa fresca com camarões grandes e ervas frescas",
     "Tagliatelle con Gamberi - massa fresca com camarões")

# ---------------- index: depoimentos (template: testtimonial-1, 80x80) ----------------
# fotos de perfil FICTICIAS (rostos gerados por IA, dominio publico - ver fotos-originais/CREDITOS.md)
foto("dep1", "depoimentos/cliente-ana-beatriz-costa-ristorantti.webp", 80, 80, "cliente_ana",
     "Foto de perfil de Ana Beatriz Costa, cliente do Ristorantti", "Ana Beatriz Costa", (.5, .48), 1.25)
foto("dep2", "depoimentos/cliente-rafael-mendes-ristorantti.webp", 80, 80, "cliente_rafael",
     "Foto de perfil de Rafael Mendes, cliente do Ristorantti", "Rafael Mendes", (.5, .48), 1.25)
foto("dep3", "depoimentos/cliente-camila-ferreira-ristorantti.webp", 80, 80, "cliente_camila",
     "Foto de perfil de Camila Ferreira, cliente do Ristorantti", "Camila Ferreira", (.5, .48), 1.25)
foto("dep4", "depoimentos/cliente-lucas-oliveira-ristorantti.webp", 80, 80, "cliente_lucas",
     "Foto de perfil de Lucas Oliveira, cliente do Ristorantti", "Lucas Oliveira", (.5, .48), 1.25)

# ---------------- rodape: instagram (template: Image-01..08, 58x58) ----------------
foto("insta1", "instagram/pizza-margherita-manjericao-instagram-ristorantti.webp", 58, 58, "pizza",
     "Instagram do Ristorantti: pizza margherita com manjericão", "Pizza margherita", (.35, .4), 1.6)
foto("insta2", "instagram/ossobuco-molho-de-tomate-instagram-ristorantti.webp", 58, 58, "ossobuco",
     "Instagram do Ristorantti: ossobuco com molho de tomate", "Ossobuco al Ragù", (.5, .5), 1.5)
foto("insta3", "instagram/lasagna-bolognese-instagram-ristorantti.webp", 58, 58, "lasanha",
     "Instagram do Ristorantti: lasagna alla Bolognese", "Lasagna alla Bolognese", (.55, .62), 2.2)
foto("insta4", "instagram/massa-com-camarao-instagram-ristorantti.webp", 58, 58, "camarao",
     "Instagram do Ristorantti: massa com camarão", "Massa com camarão", (.55, .5), 1.8)
foto("insta5", "instagram/terraco-mesas-azuis-instagram-ristorantti.webp", 58, 58, "terraco",
     "Instagram do Ristorantti: mesas e cadeiras azuis no terraço", "Terraço italiano", (.3, .55), 2.5)
foto("insta6", "instagram/bar-principal-instagram-ristorantti.webp", 58, 58, "bar",
     "Instagram do Ristorantti: bar principal", "Bar principal", (.5, .5), 1.0)
foto("insta7", "instagram/pizza-no-forno-instagram-ristorantti.webp", 58, 58, "pizza_forno",
     "Instagram do Ristorantti: pizza artesanal com manjericão e tomates", "Pizza artesanal", (.5, .62), 2.4)
foto("insta8", "instagram/rua-italiana-mesas-instagram-ristorantti.webp", 58, 58, "externa",
     "Instagram do Ristorantti: mesas ao ar livre na rua italiana", "Área externa", (.5, .45), 1.3)

# ---------------- cardapio / accomodation.html (template: room1-4, 263x270 e 262x270) ----------------
foto("prato_ossobuco", "cardapio/ossobuco-al-ragu-prato-principal-cantina.webp", 263, 270, "ossobuco",
     "Ossobuco al Ragù: carne macia cozida lentamente em molho de tomate com cenoura e salsinha",
     "Ossobuco al Ragù - Ristorantti Cucina Italiana", (.5, .5), 1.0)
foto("prato_lasanha", "cardapio/lasagna-alla-bolognese-massa-fresca-gratinada.webp", 262, 270, "lasanha",
     "Lasagna alla Bolognese com massa fresca, ragù de carne e queijo gratinado",
     "Lasagna alla Bolognese - Ristorantti Cucina Italiana", (.55, .6), 1.5)
foto("prato_tagliatelle", "cardapio/tagliatelle-con-gamberi-camarao-azeite-alho.webp", 263, 270, "camarao",
     "Tagliatelle con Gamberi: massa fresca com camarões, azeite, alho e ervas",
     "Tagliatelle con Gamberi - Ristorantti Cucina Italiana", (.55, .5), 1.0)
foto("prato_pizza", "cardapio/pizza-margherita-artesanal-tomate-manjericao.webp", 262, 270, "pizza",
     "Pizza margherita artesanal com tomate, mussarela e manjericão fresco",
     "Pizza margherita - Ristorantti Cucina Italiana", (.5, .5), 1.0)
foto("prato_bruschetta", "cardapio/bruschetta-al-pomodoro-antepasto-italiano.webp", 263, 270, "bruschetta",
     "Bruschetta al pomodoro: pão rústico tostado coberto com tomate picado, cebola e manjericão",
     "Bruschetta al Pomodoro - Ristorantti Cucina Italiana")
foto("prato_caprese", "cardapio/insalata-caprese-mussarela-tomate-manjericao.webp", 262, 270, "caprese",
     "Insalata Caprese com fatias de tomate, mussarela e folhas de manjericão fresco",
     "Insalata Caprese - Ristorantti Cucina Italiana")
foto("prato_carbonara", "cardapio/spaghetti-alla-carbonara-massa-italiana.webp", 263, 270, "carbonara",
     "Spaghetti alla Carbonara com guanciale crocante, queijo ralado e salsinha",
     "Spaghetti alla Carbonara - Ristorantti Cucina Italiana")
foto("prato_nhoque", "cardapio/nhoque-ao-sugo-molho-de-tomate-caseiro.webp", 262, 270, "nhoque",
     "Nhoque de batata ao sugo, com molho de tomate, servido em tigela com borda azul",
     "Nhoque ao Sugo - Ristorantti Cucina Italiana")
foto("prato_risoto", "cardapio/risoto-alla-milanese-acafrao-cremoso.webp", 263, 270, "risoto",
     "Risoto alla Milanese cremoso, perfumado com açafrão, servido em prato azul-turquesa",
     "Risoto alla Milanese - Ristorantti Cucina Italiana")
foto("prato_quatro_queijos", "cardapio/pizza-quattro-formaggi-quatro-queijos.webp", 262, 270, "quatro_queijos",
     "Pizza Quattro Formaggi de massa fina com quatro tipos de queijo e molho de tomate",
     "Pizza Quattro Formaggi - Ristorantti Cucina Italiana")
foto("prato_tiramisu", "cardapio/tiramisu-sobremesa-italiana-classica.webp", 263, 270, "tiramisu",
     "Fatia de tiramisù, sobremesa italiana clássica de café e creme, polvilhada com cacau",
     "Tiramisù - Ristorantti Cucina Italiana", (.5, .6), 1.4)
foto("prato_panna_cotta", "cardapio/panna-cotta-calda-frutas-vermelhas-sobremesa.webp", 262, 270, "panna_cotta",
     "Panna cotta com calda de frutas vermelhas, framboesas e fatia de laranja desidratada",
     "Panna Cotta - Ristorantti Cucina Italiana")

# ---------------- galeria (template: gallery/01..06, 01-1..03-1) ----------------
foto("gal_01", "galeria/mesas-azuis-terraco-restaurante-italiano.webp", 360, 250, "terraco",
     "Mesas e cadeiras azuis e brancas no terraço rústico do restaurante italiano",
     "Terraço do Ristorantti com mesas azuis", (.42, .5), 1.8)
foto("gal_02", "galeria/pizza-margherita-close-manjericao-queijo.webp", 360, 380, "pizza",
     "Close de pizza margherita com manjericão fresco e queijo derretido",
     "Pizza margherita em close", (.5, .5), 1.0)
foto("gal_03", "galeria/lasagna-bolognese-camadas-ragu-queijo.webp", 360, 250, "lasanha",
     "Lasagna alla Bolognese com camadas de massa, molho ragù e queijo gratinado",
     "Lasagna alla Bolognese", (.5, .6), 1.0)
foto("gal_04", "galeria/fachada-rustica-pedra-janelas-azuis-trepadeira.webp", 360, 380, "terraco",
     "Fachada rústica de pedra com janelas azuis e trepadeira ao lado do terraço",
     "Fachada rústica do Ristorantti", (.25, .25), 1.7)
foto("gal_05", "galeria/tagliatelle-camarao-prato-massa-fresca.webp", 360, 250, "camarao",
     "Prato de massa fresca com camarões grandes finalizado com ervas",
     "Massa fresca com camarões", (.5, .5), 1.0)
foto("gal_06", "galeria/ingredientes-frescos-manjericao-tomate-pizza.webp", 360, 380, "pizza_forno",
     "Folhas de manjericão fresco, tomates e temperos ao lado da pizza artesanal",
     "Ingredientes frescos da pizza", (.17, .2), 1.8)
foto("gal_07", "galeria/ossobuco-al-ragu-molho-tomate-prato-branco.webp", 360, 250, "ossobuco",
     "Ossobuco al Ragù com molho de tomate e salsinha em prato branco",
     "Ossobuco al Ragù", (.5, .5), 1.0)
foto("gal_08", "galeria/cadeiras-azuis-vasos-flores-terraco-italiano.webp", 360, 380, "terraco",
     "Cadeiras azuis e vasos de flores coloridos no terraço italiano",
     "Cadeiras azuis e flores no terraço", (.1, .62), 2.0)
foto("gal_09", "galeria/pizza-artesanal-forno-bandeja-ingredientes.webp", 360, 250, "pizza_forno",
     "Pizza artesanal assada sobre bandeja, cercada de manjericão e tomates",
     "Pizza artesanal recém-saída do forno", (.5, .62), 1.3)

# ---------------- blog.html (template: cat-post 360x220, main-blog 555x280, post1-4 100x60, add 300x250, author 120x120) ----------------
foto("cat_massas", "blog/categorias/massas-frescas-lasagna-categoria-blog.webp", 360, 220, "lasanha",
     "Categoria Massas Frescas: lasagna alla Bolognese gratinada", "Massas Frescas", (.5, .6), 1.0)
foto("cat_pizzas", "blog/categorias/pizzas-artesanais-margherita-categoria-blog.webp", 360, 220, "pizza",
     "Categoria Pizzas Artesanais: pizza margherita com manjericão", "Pizzas Artesanais", (.5, .5), 1.0)
foto("cat_classicos", "blog/categorias/pratos-classicos-ossobuco-categoria-blog.webp", 360, 220, "ossobuco",
     "Categoria Pratos Clássicos: ossobuco al ragù", "Pratos Clássicos", (.5, .5), 1.0)

foto("post1", "blog/destaques/ossobuco-al-ragu-destaque-blog-cantina.webp", 555, 280, "ossobuco",
     "Ossobuco al Ragù: carne macia com molho de tomate, cenoura e salsinha em prato branco",
     "Ossobuco al Ragù - destaque do blog")
foto("post2", "blog/destaques/lasagna-alla-bolognese-destaque-blog-cantina.webp", 555, 280, "lasanha",
     "Lasagna alla Bolognese com camadas de massa fresca, ragù e queijo gratinado",
     "Lasagna alla Bolognese - blog Ristorantti", (.5, .62))
foto("post3", "blog/destaques/tagliatelle-con-gamberi-destaque-blog-cantina.webp", 555, 280, "camarao",
     "Tagliatelle con Gamberi: massa fresca com camarões suculentos e ervas",
     "Tagliatelle con Gamberi - blog Ristorantti")
foto("post4", "blog/destaques/pizza-napoletana-massa-fermentacao-destaque-blog.webp", 555, 280, "pizza",
     "Pizza napoletana de massa artesanal com tomate, queijo e manjericão",
     "Pizza napoletana - blog Ristorantti", (.5, .45))
foto("post5", "blog/destaques/aperitivo-ao-ar-livre-terraco-cantina-italiana.webp", 555, 280, "terraco",
     "Terraço da cantina com mesas ao ar livre, ideal para um aperitivo italiano",
     "Aperitivo ao ar livre - blog Ristorantti", (.5, .5))

foto("pop1", "blog/populares/ossobuco-miniatura-post-popular.webp", 100, 60, "ossobuco",
     "Miniatura do post sobre ossobuco", "Ossobuco al Ragù", (.5, .5), 1.2)
foto("pop2", "blog/populares/lasagna-miniatura-post-popular.webp", 100, 60, "lasanha",
     "Miniatura do post sobre lasagna", "Lasagna alla Bolognese", (.55, .62), 1.6)
foto("pop3", "blog/populares/pizza-miniatura-post-popular.webp", 100, 60, "pizza",
     "Miniatura do post sobre pizza napoletana", "Pizza napoletana", (.4, .4), 1.3)
foto("pop4", "blog/populares/terraco-miniatura-post-popular.webp", 100, 60, "terraco",
     "Miniatura do post sobre aperitivo ao ar livre", "Aperitivo ao ar livre", (.3, .55), 2.2)

avatar("autor", "blog/chef-marco-bellini-autor-do-blog.webp", 120, "MB", "#8b2e2e",
       "Avatar do chef Marco Bellini, autor do blog do Ristorantti", "Chef Marco Bellini")
_add("promo", "blog/promo-reserve-sua-mesa-ristorantti.webp", 300, 250, "promo", "pizza_forno", (.5, .62), 1.6,
     "Anúncio: reserve sua mesa no Ristorantti Cucina Italiana", "Reserve sua mesa - Ristorantti")

# ---------------- blog-single.html (template: feature-img1 750x350, post-img1/2 360x350, prev/next 60x60, c1-c5 60x60) ----------------
foto("art_feature", "blog/ossobuco-al-ragu-artigo-prato-principal-cantina.webp", 750, 350, "ossobuco",
     "Ossobuco al Ragù: fatia de jarrete cozida lentamente em molho de tomate, servida com salsinha",
     "Ossobuco al Ragù - receita da cantina")
foto("art_img1", "blog/ossobuco-cozido-lentamente-molho-de-tomate-cenoura.webp", 360, 350, "ossobuco",
     "Detalhe do ossobuco com molho de tomate, cenoura e folhas de salsinha",
     "Detalhe do ossobuco", (.4, .5), 1.0)
foto("art_img2", "blog/mesas-do-terraco-onde-o-ossobuco-e-servido.webp", 360, 350, "terraco",
     "Mesas do terraço do Ristorantti, onde o ossobuco também pode ser saboreado ao ar livre",
     "Terraço do Ristorantti", (.42, .5), 2.2)
foto("nav_prev", "blog/post-anterior-lasagna-miniatura.webp", 60, 60, "lasanha",
     "Miniatura do post anterior: lasagna alla Bolognese", "Post anterior", (.55, .62), 2.2)
foto("nav_next", "blog/proximo-post-pizza-napoletana-miniatura.webp", 60, 60, "pizza",
     "Miniatura do próximo post: pizza napoletana", "Próximo post", (.4, .4), 1.6)

avatar("com1", "blog/comentarios/leitora-juliana-torres-avatar.webp", 60, "JT", "#b5482f",
       "Avatar da leitora Juliana Torres", "Juliana Torres")
avatar("com2", "blog/comentarios/leitor-marcos-vinicius-avatar.webp", 60, "MV", "#5b7c3a",
       "Avatar do leitor Marcos Vinícius", "Marcos Vinícius")
avatar("com3", "blog/comentarios/leitora-patricia-lima-avatar.webp", 60, "PL", "#c98f2b",
       "Avatar da leitora Patrícia Lima", "Patrícia Lima")
avatar("com4", "blog/comentarios/leitor-henrique-alves-avatar.webp", 60, "HA", "#7b3f3f",
       "Avatar do leitor Henrique Alves", "Henrique Alves")
avatar("com5", "blog/comentarios/leitora-sofia-rocha-avatar.webp", 60, "SR", "#4a6c8a",
       "Avatar da leitora Sofia Rocha", "Sofia Rocha")
