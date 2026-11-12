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
| `ferramentas/` | Scripts que recortam/otimizam as imagens (`imagens.py`) e geram o zip da entrega (`gerar-zip.py`) + `relatorio-imagens.md` (peso, formato, pendências). |

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

## Reserva de mesa (WhatsApp)

O bloco **Reserve sua mesa** (página inicial e *Cardápio*) funciona sem servidor: o botão valida data, adultos e
ambiente, confere o horário de funcionamento (terça a domingo, 12h às 23h; segundas bloqueadas no calendário) e abre
o WhatsApp com a mensagem da reserva pronta. O seletor de data está em português (`DD/MM/AAAA hh:mm`).

Para a mensagem ir direto ao restaurante, coloque o número (DDI+DDD+número, só dígitos, ex.: `5521999999999`) na
constante `WHATSAPP_RESTAURANTE` em `royal-master/js/custom.js`. Vazio, o WhatsApp abre e a pessoa escolhe o contato.

## Gerar o zip da entrega

```bash
python ferramentas/gerar-zip.py --integrantes "Nome Completo 1; Nome Completo 2"
```

Confere o projeto (links quebrados, imagens, `alt`/`title`, fotos originais que faltam) e cria em `entrega/`
(fora do Git) o `AP2-Ristorantti-Cucina-Italiana-8003.zip` com `site/`, `fotos-originais/` e `fotos-otimizadas/`,
mais o `EMAIL-rascunho.txt` com destinatário, assunto e corpo prontos.

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
- [x] Fotos originais (sem otimização) dos ambientes e dos pratos principais também em `fotos-originais/`
      (Wikimedia Commons, licenças livres; autoria e licença em `fotos-originais/CREDITOS.md` e no fim da página *Cardápio*)
- [x] Restos do template removidos (documentação `royal-Doc/`, `elements.html`, README do template, imagens e CSS sem uso)
- [x] Logo com a mesma proporção do template (163×30; arquivo em 2×, 326×60)
- [x] Reserva de mesa funcional (mensagem pronta no WhatsApp) e script que gera o zip
- [ ] Rodar `python ferramentas/gerar-zip.py` (depois de colocar os originais) e enviar o `.zip` para
      `maurice.chalom@professores.ibmec.edu.br` com o título **Trabalho AP2 - design gráfico e UX (8003)** e o
      nome completo dos integrantes no corpo do e-mail

## Créditos

Template *Royal Hotel* por [Colorlib](https://colorlib.com), licença CC BY 3.0 (o link de crédito no rodapé
deve ser mantido). Textos e dados do restaurante (endereço, telefone, preços, nomes) são **fictícios**.
