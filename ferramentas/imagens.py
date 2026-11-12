# -*- coding: utf-8 -*-
"""
PIPELINE DE IMAGENS - Ristorantti Cucina Italiana

Uso (na raiz do repositorio):
    python ferramentas/imagens.py

Para cada imagem do MANIFESTO (ferramentas/manifesto.py):
  1. procura a foto-base em  fotos-originais/<chave>.(jpg|jpeg|png|webp|tif|bmp)
       -> se achar: usa o ORIGINAL (melhor qualidade)
       -> senao: usa a versao provisoria em ferramentas/fontes-provisorias/<chave>.webp
       -> senao: gera um quadro "FOTO PENDENTE" com a dimensao certa
  2. recorta SEM distorcer para a dimensao EXATA do template e converte para WebP otimizado
  3. grava em royal-master/image/...  (nome estrategico para SEO)
  4. copia as otimizadas (menos as pendentes) para fotos-otimizadas/
  5. escreve ferramentas/relatorio-imagens.md (peso, formato, pendencias, ampliacoes)
"""
import os
import time
import shutil
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manifesto import FONTES, SLOTS  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SITE_IMG = os.path.join(RAIZ, "royal-master", "image")
ORIGINAIS = os.path.join(RAIZ, "fotos-originais")
PROVISORIAS = os.path.join(RAIZ, "ferramentas", "fontes-provisorias")
OTIMIZADAS = os.path.join(RAIZ, "fotos-otimizadas")
RELATORIO = os.path.join(RAIZ, "ferramentas", "relatorio-imagens.md")

EXTS = (".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp")
QUALIDADE = 74          # WebP (fotos pequenas/medias): bom equilibrio peso x nitidez
QUALIDADE_FUNDO = 62    # WebP dos fundos grandes (1920 px, sob camada escura): bem mais leve
LIMITE_AMPLIACAO = 1.15  # acima disso o relatorio avisa que a foto-base e pequena

# ---------------------------------------------------------------- fontes tipograficas
def _fonte(nomes, tam):
    pastas = ["C:/Windows/Fonts", "/System/Library/Fonts/Supplemental", "/Library/Fonts",
              "/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/truetype/liberation"]
    for n in nomes:
        for p in pastas:
            f = os.path.join(p, n)
            if os.path.exists(f):
                return ImageFont.truetype(f, tam)
    return ImageFont.load_default()


def serif_bold_italic(t): return _fonte(["georgiaz.ttf", "Georgia Bold Italic.ttf", "DejaVuSerif-BoldItalic.ttf"], t)
def serif_bold(t): return _fonte(["georgiab.ttf", "Georgia Bold.ttf", "DejaVuSerif-Bold.ttf"], t)
def sans_bold(t): return _fonte(["arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf"], t)
def sans(t): return _fonte(["arial.ttf", "Arial.ttf", "DejaVuSans.ttf"], t)


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


VERDE, CREME, VERMELHO, ESCURO = "#008C45", "#e9e4d8", "#CD212A", "#222222"

# ---------------------------------------------------------------- abrir / recortar
def achar_fonte(chave):
    """Devolve (caminho, tipo) com tipo 'original' | 'provisoria' | None."""
    for ext in EXTS:
        p = os.path.join(ORIGINAIS, chave + ext)
        if os.path.exists(p):
            return p, "original"
    p = os.path.join(PROVISORIAS, chave + ".webp")
    if os.path.exists(p):
        return p, "provisoria"
    return None, None


def abrir(path):
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)  # respeita rotacao do celular
    if "icc_profile" in im.info:      # converte perfil de cor para sRGB (web)
        try:
            from PIL import ImageCms
            import io
            src = ImageCms.ImageCmsProfile(io.BytesIO(im.info["icc_profile"]))
            im = ImageCms.profileToProfile(im.convert("RGB"), src, ImageCms.createProfile("sRGB"))
        except Exception:
            pass
    return im.convert("RGB")


def caixa_recorte(sw, sh, w, h, focus, zoom):
    """Maior caixa com a proporcao w:h dentro da foto, aproximada por 'zoom', centrada no foco."""
    alvo = w / h
    bw = min(sw, sh * alvo)
    bh = bw / alvo
    bw, bh = bw / zoom, bh / zoom
    cx, cy = focus[0] * sw, focus[1] * sh
    x0 = max(0.0, min(max(cx - bw / 2, 0), sw - bw))
    y0 = max(0.0, min(max(cy - bh / 2, 0), sh - bh))
    return (x0, y0, x0 + bw, y0 + bh)


def recortar(im, w, h, focus, zoom):
    box = caixa_recorte(im.width, im.height, w, h, focus, zoom)
    ampliacao = w / (box[2] - box[0])
    if im.size == (w, h):
        return im.copy(), 1.0
    return im.resize((w, h), Image.LANCZOS, box=box), ampliacao


# ---------------------------------------------------------------- imagens geradas
def tracejado(d, x0, y0, x1, y1, cor, passo=8):
    x = x0
    while x < x1:
        d.line([(x, y0), (min(x + passo / 2, x1), y0)], fill=cor, width=2)
        d.line([(x, y1), (min(x + passo / 2, x1), y1)], fill=cor, width=2)
        x += passo
    y = y0
    while y < y1:
        d.line([(x0, y), (x0, min(y + passo / 2, y1))], fill=cor, width=2)
        d.line([(x1, y), (x1, min(y + passo / 2, y1))], fill=cor, width=2)
        y += passo


def centralizado(d, texto, cx, cy, fonte, cor, largura_max):
    palavras, linhas, atual = texto.split(), [], ""
    for p in palavras:
        teste = (atual + " " + p).strip()
        if d.textlength(teste, font=fonte) <= largura_max or not atual:
            atual = teste
        else:
            linhas.append(atual)
            atual = p
    linhas.append(atual)
    alt_linha = fonte.size + 4
    y = cy - alt_linha * len(linhas) / 2 + alt_linha / 2
    for l in linhas:
        d.text((cx, y), l, font=fonte, fill=cor, anchor="mm")
        y += alt_linha
    return y


def quadro_pendente(s):
    w, h = s["w"], s["h"]
    im = Image.new("RGB", (w, h), hex2rgb("#f3ead9"))
    d = ImageDraw.Draw(im)
    tracejado(d, 6, 6, w - 7, h - 7, hex2rgb("#b79b6b"))
    nome = FONTES[s["src"]][0]
    esc = max(0.6, min(w, 520) / 263)
    d.text((w / 2, h * 0.30), "FOTO PENDENTE", font=sans_bold(int(15 * esc)), fill=hex2rgb(VERMELHO), anchor="mm")
    centralizado(d, nome, w / 2, h * 0.50, serif_bold(int(19 * esc)), hex2rgb(ESCURO), w - 30)
    d.text((w / 2, h * 0.72), f"{w} x {h} px", font=sans(int(13 * esc)), fill=hex2rgb("#777777"), anchor="mm")
    d.text((w / 2, h * 0.82), f"fotos-originais/{s['src']}.jpg", font=sans(int(11 * esc)), fill=hex2rgb("#999999"), anchor="mm")
    return im


def monograma(s):
    w, h = s["w"], s["h"]
    t = min(w, h)  # circulo e letras seguem o menor lado (funciona tambem para 62x64)
    im = Image.new("RGB", (w, h), hex2rgb(s["cor"]))
    d = ImageDraw.Draw(im)
    cx, cy, r = w / 2, h / 2, t * .44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=hex2rgb("#fff7e8"), width=max(1, t // 40))
    d.text((cx, cy + t * .02), s["ini"], font=serif_bold(int(t * .38)), fill=hex2rgb("#fff7e8"), anchor="mm")
    return im


def barra_tricolor(d, x, y, larg, alt):
    t = larg / 3
    d.rectangle([x, y, x + t, y + alt], fill=hex2rgb(VERDE))
    d.rectangle([x + t, y, x + 2 * t, y + alt], fill=hex2rgb(CREME))
    d.rectangle([x + 2 * t, y, x + larg, y + alt], fill=hex2rgb(VERMELHO))


def logotipo(s):
    """Logotipo (so o nome + faixa tricolor), mesma PROPORCAO do logo do template (163x30).
    Desenhado em 4x e reduzido, para ficar nitido em qualquer tamanho."""
    w, h = s["w"], s["h"]
    k = 4
    W, H = w * k, h * k
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f1 = serif_bold_italic(int(H * 0.60))
    texto = "Ristorantti"
    larg = d.textlength(texto, font=f1)
    x0 = int(H * 0.04)
    d.text((x0, int(H * 0.70)), texto, font=f1, fill=hex2rgb(ESCURO), anchor="ls")
    barra_tricolor(d, x0 + int(H * 0.02), int(H * 0.80), larg - int(H * 0.02), int(H * 0.08))
    conteudo = im.crop(im.getbbox())
    tela = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tela.paste(conteudo, (0, (H - conteudo.height) // 2))
    return tela.resize((w, h), Image.LANCZOS)


def favicon(s):
    t = s["w"]
    im = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, t - 1, t - 1], radius=t * .22, fill=hex2rgb(VERMELHO))
    d.text((t / 2, t * .44), "R", font=serif_bold_italic(int(t * .62)), fill=hex2rgb("#fff7e8"), anchor="mm")
    barra_tricolor(d, t * .20, t * .80, t * .60, max(3, t // 16))
    return im


def promo(s, base):
    im, _ = recortar(base, s["w"], s["h"], s["focus"], s["zoom"])
    im = im.convert("RGBA")
    sombra = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ds = ImageDraw.Draw(sombra)
    for y in range(im.height):
        a = int(70 + 150 * (y / im.height))
        ds.line([(0, y), (im.width, y)], fill=(20, 8, 4, a))
    im = Image.alpha_composite(im, sombra)
    d = ImageDraw.Draw(im)
    w, h = im.size
    d.text((w / 2, h * .50), "Reserve", font=serif_bold_italic(44), fill=(255, 247, 232), anchor="mm")
    d.text((w / 2, h * .66), "sua mesa", font=serif_bold_italic(44), fill=(255, 247, 232), anchor="mm")
    d.text((w / 2, h * .84), "CUCINA ITALIANA  ·  TER A DOM", font=sans_bold(12), fill=(243, 195, 0), anchor="mm")
    barra_tricolor(d, w * .3, h * .92, w * .4, 4)
    return im.convert("RGB")


# ---------------------------------------------------------------- salvar
def salvar(im, caminho, kind):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    for tentativa in range(5):  # o Windows (antivirus/sincronizacao) as vezes bloqueia a gravacao por instantes
        try:
            if caminho.endswith(".png"):
                im.save(caminho, "PNG", optimize=True)
            else:
                q = QUALIDADE_FUNDO if im.width >= 1600 else QUALIDADE
                im.save(caminho, "WEBP", quality=q, method=6)
            return
        except OSError:
            if tentativa == 4:
                raise
            time.sleep(0.5)


def kb(p):
    return os.path.getsize(p) / 1024


def main():
    os.makedirs(ORIGINAIS, exist_ok=True)
    os.makedirs(OTIMIZADAS, exist_ok=True)
    cache = {}
    linhas, pendentes, ampliadas, provis = [], [], [], set()
    usadas_otimizadas = set()

    for s in SLOTS.values():
        saida = os.path.join(SITE_IMG, s["out"])
        estado, fonte_txt, ampl = "ok", "(gerada)", 1.0

        if s["kind"] == "logo":
            im = logotipo(s)
        elif s["kind"] == "favicon":
            im = favicon(s)
        elif s["kind"] == "avatar":
            im = monograma(s)
        else:
            chave = s["src"]
            path, tipo = achar_fonte(chave)
            if path is None:
                im, estado, fonte_txt = quadro_pendente(s), "PENDENTE", f"falta fotos-originais/{chave}.jpg"
                if chave not in pendentes:
                    pendentes.append(chave)
            else:
                if path not in cache:
                    cache[path] = abrir(path)
                base = cache[path]
                fonte_txt = f"{os.path.relpath(path, RAIZ)}"
                if tipo == "provisoria":
                    estado = "provisoria"
                    provis.add(chave)
                if s["kind"] == "promo":
                    im = promo(s, base)
                else:
                    # mesma dimensao da fonte provisoria ja otimizada: copia sem recomprimir
                    if tipo == "provisoria" and base.size == (s["w"], s["h"]) and s["zoom"] == 1.0:
                        os.makedirs(os.path.dirname(saida), exist_ok=True)
                        shutil.copyfile(path, saida)
                        im = None
                    else:
                        im, ampl = recortar(base, s["w"], s["h"], s["focus"], s["zoom"])
                        if ampl > LIMITE_AMPLIACAO:
                            estado = "ampliada"
                            ampliadas.append((s["id"], chave, ampl))

        if im is not None:
            salvar(im, saida, s["kind"])

        # confere dimensao final
        with Image.open(saida) as chk:
            assert chk.size == (s["w"], s["h"]), (s["id"], chk.size, (s["w"], s["h"]))

        if estado != "PENDENTE":
            destino = os.path.join(OTIMIZADAS, os.path.basename(s["out"]))
            shutil.copyfile(saida, destino)
            usadas_otimizadas.add(os.path.basename(destino))
        linhas.append((s["id"], s["out"], f"{s['w']}x{s['h']}", os.path.splitext(s["out"])[1][1:].upper(),
                       kb(saida), fonte_txt, estado, ampl))

    # remove da pasta de otimizadas o que nao e mais usado (nomes antigos)
    for f in os.listdir(OTIMIZADAS):
        if f not in usadas_otimizadas and f.lower().endswith((".webp", ".png", ".jpg", ".avif")):
            os.remove(os.path.join(OTIMIZADAS, f))

    escrever_relatorio(linhas, pendentes, ampliadas, provis)
    escrever_leiame_originais(pendentes, provis)
    total = sum(l[4] for l in linhas)
    print(f"{len(linhas)} imagens geradas | {total:,.0f} KB no total | {len(pendentes)} fotos pendentes | "
          f"{len(provis)} fotos-base provisorias | {len(ampliadas)} ampliadas")


def escrever_relatorio(linhas, pendentes, ampliadas, provis):
    t = ["# Relatório de imagens - Ristorantti Cucina Italiana", "",
         "Gerado por `python ferramentas/imagens.py`. Dimensões = exatamente as do template Royal Hotel.", ""]
    t += [f"- Imagens no site: **{len(linhas)}**  |  peso total: **{sum(l[4] for l in linhas):,.0f} KB**",
          f"- Fotos-base ainda PROVISÓRIAS (trocar pelo original): **{len(provis)}** -> {', '.join(sorted(provis)) or '-'}",
          f"- Fotos PENDENTES (quadro 'FOTO PENDENTE' no site): **{len(pendentes)}** -> {', '.join(pendentes) or '-'}", ""]
    if ampliadas:
        t += ["## Atenção: fotos-base pequenas (ampliadas)", "",
              "| imagem | foto-base | ampliação |", "|---|---|---|"]
        t += [f"| {i} | {c} | {a:.2f}x |" for i, c, a in ampliadas]
        t += ["", "Troque por uma foto maior para ficar nítida.", ""]
    t += ["## Todas as imagens", "", "| id | arquivo (royal-master/image/) | dimensão | formato | KB | foto-base | estado |",
          "|---|---|---|---|---:|---|---|"]
    for i, o, d, f, k, src, est, _ in linhas:
        t.append(f"| {i} | {o} | {d} | {f} | {k:.1f} | {src} | {est} |")
    with open(RELATORIO, "w", encoding="utf-8") as f:
        f.write("\n".join(t) + "\n")


def escrever_leiame_originais(pendentes, provis):
    t = ["FOTOS ORIGINAIS (sem otimização) - Ristorantti Cucina Italiana", "=" * 62, "",
         "Coloque aqui as fotos NO TAMANHO ORIGINAL (como baixadas/produzidas), uma por chave,",
         "com o nome da chave + extensão. Exemplo:  ossobuco.jpg   terraco.jpg   tiramisu.png",
         "Depois rode, na raiz do repositório:   python ferramentas/imagens.py",
         "O script recorta, otimiza (WebP) e atualiza o site e a pasta fotos-otimizadas/ sozinho.", "",
         "Dica: quanto maior a foto original, melhor (mínimo indicado ao lado de cada chave).", "",
         "--- AINDA FALTAM (aparecem como 'FOTO PENDENTE' no site) ---"]
    for k in pendentes:
        t.append(f"  {k + '.jpg':<22} {FONTES[k][1]}")
    t += ["", "--- JÁ USAMOS UMA VERSÃO PROVISÓRIA (coloque o ORIGINAL para trocar) ---"]
    for k in sorted(provis):
        t.append(f"  {k + '.jpg':<22} {FONTES[k][1]}")
    with open(os.path.join(ORIGINAIS, "LEIA-ME.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(t) + "\n")


if __name__ == "__main__":
    main()
