# AP2 de Design Gráfico e User Experience

Site da **Ristorantti Cucina Italiana**, uma cantina italiana fictícia, criado a partir da **estrutura** do
template *Royal Hotel* (`royal-master`), com **textos, imagens, logo e favicon novos**.

- Disciplina: Design Gráfico e UX (Ciência de Dados e IA, turma 8003) - Prof. Maurice Chalom
- Entrega: **13/11/2026** (presença obrigatória para apresentar o site)

## Estrutura do repositório

| Pasta | O que é |
|---|---|
| `royal-master/` | O **site** (HTML/CSS/JS). Abra `royal-master/index.html`. |
| `fotos-originais/` | Fotos **sem otimização**, no tamanho original (entrega do professor). Veja o `LEIA-ME.txt` dentro. |
| `fotos-otimizadas/` | As mesmas imagens **otimizadas** (WebP/PNG), já com nomes de SEO. Gerada automaticamente. |
| `ferramentas/` | Scripts que recortam/otimizam as imagens + `relatorio-imagens.md` (peso, formato, pendências). |

## Páginas (mesma estrutura do template)

| Arquivo | Conteúdo na cantina |
|---|---|
| `index.html` | Início: banner, reserva de mesa, áreas do restaurante, diferenciais, história, depoimentos, blog |
| `accomodation.html` | **Cardápio** (pratos especiais + cardápio completo) e formulário de reserva (`#reserva`) |
| `gallery.html` | Galeria de fotos com lightbox |
| `blog.html` | Blog: destaque, categorias e 5 posts (o primeiro leva ao `blog-single.html`) |
| `blog-single.html` | Post completo: *Ossobuco al Ragù* |
| `about.html`, `contact.html` | Sobre nós e Contato (também adaptados) |

## Como trocar uma foto

1. Salve a foto **original** em `fotos-originais/` com o nome da chave, por exemplo `tiramisu.jpg`
   (as chaves que faltam estão listadas em `fotos-originais/LEIA-ME.txt`).
2. Na raiz do repositório, rode:

   ```bash
   python ferramentas/imagens.py
   ```

O script recorta **sem distorcer** para a dimensão exata do template, converte para WebP otimizado,
atualiza `royal-master/image/` e `fotos-otimizadas/` e reescreve o `relatorio-imagens.md`.
Precisa de Python 3 e `pip install pillow`. Todas as dimensões, nomes de arquivo, `alt` e `title`
estão em `ferramentas/manifesto.py`.

## Checklist do briefing

- [x] Estrutura do `royal-master` mantida; conteúdo, logo e favicon trocados
- [x] Títulos, textos, botões e imagens trocados em `index`, `accomodation`, `gallery`, `blog` e `blog-single`
- [x] Link funcional de um destaque do `blog.html` para o `blog-single.html`
- [x] Imagens com **as mesmas dimensões** do template (conferido automaticamente pelo script)
- [x] Imagens otimizadas (WebP) com **nomes estratégicos para SEO**, `alt` e `title` em todas
- [x] 8 fotos de pratos do cardápio baixadas do Wikimedia Commons (licença livre; créditos em
      `fotos-originais/CREDITOS.md` e no fim da página *Cardápio*)
- [x] Fotos de perfil dos 4 clientes dos depoimentos: rostos **fictícios gerados por IA** (domínio público,
      Wikimedia Commons; créditos em `fotos-originais/CREDITOS.md`). Os avatares dos comentários e do autor do
      blog ainda são monogramas (iniciais)
- [ ] Colocar em `fotos-originais/` os arquivos **originais** das 10 fotos que o grupo já usava
      (`terraco`, `pizza_forno`, `pizza`, `ossobuco`, `lasanha`, `camarao`, `salao`, `bar`, `cerveja`, `externa`).
      Hoje o site usa a versão WebP delas (em `ferramentas/fontes-provisorias/`); anote também a autoria/fonte
      de cada uma em `fotos-originais/CREDITOS.md`
- [ ] Gerar o `.zip` (site + fotos-originais + fotos-otimizadas) e enviar para
      `maurice.chalom@professores.ibmec.edu.br` com o título **Trabalho AP2 - design gráfico e UX (8003)** e o
      nome completo dos integrantes no corpo do e-mail

## Créditos

Template *Royal Hotel* por [Colorlib](https://colorlib.com), licença CC BY 3.0 (o link de crédito no rodapé
deve ser mantido). Textos e dados do restaurante (endereço, telefone, preços, nomes) são **fictícios**.
