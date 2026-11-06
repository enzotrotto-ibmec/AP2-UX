# -*- coding: utf-8 -*-
"""
GERA O ZIP DA ENTREGA - AP2 Design Grafico e UX (turma 8003)

Uso (na raiz do repositorio):
    python ferramentas/gerar-zip.py
    python ferramentas/gerar-zip.py --integrantes "Fulano de Tal; Ciclano da Silva"

O que faz:
  1. confere o projeto (arquivos/links quebrados, imagens do manifesto, alt/title, fotos originais)
  2. monta  entrega/AP2-Ristorantti-Cucina-Italiana-8003.zip  com
         site/               o site (conteudo de royal-master/)
         fotos-originais/    fotos novas no tamanho original (sem otimizacao)
         fotos-otimizadas/   as mesmas fotos otimizadas, com nomes de SEO
         LEIA-ME.txt         resumo para o professor
  3. escreve  entrega/EMAIL-rascunho.txt  (destinatario, assunto e corpo prontos)

A pasta entrega/ esta no .gitignore (o zip nao vai para o GitHub).
"""
import argparse
import datetime
import os
import re
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manifesto import MARCA, SLOTS  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SITE = os.path.join(RAIZ, "royal-master")
ORIGINAIS = os.path.join(RAIZ, "fotos-originais")
OTIMIZADAS = os.path.join(RAIZ, "fotos-otimizadas")
SAIDA = os.path.join(RAIZ, "entrega")
NOME_ZIP = "AP2-Ristorantti-Cucina-Italiana-8003.zip"

PROFESSOR = "maurice.chalom@professores.ibmec.edu.br"
ASSUNTO = "Trabalho AP2 - design gráfico e UX (8003)"
PRAZO = "13/11/2026"
PAGINAS = ["index.html", "accomodation.html", "gallery.html", "blog.html", "blog-single.html", "about.html", "contact.html"]
EXTS_FOTO = (".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp")
IGNORAR = {".DS_Store", "Thumbs.db", "__pycache__", ".git"}
LIMITE_EMAIL_MB = 20  # Gmail aceita anexos de ate 25 MB


# ---------------------------------------------------------------- conferencias
def conferir():
    """Devolve (erros, avisos). Erros impedem gerar o zip."""
    erros, avisos = [], []

    # 1. paginas existem e nao tem link/arquivo quebrado
    for pg in PAGINAS:
        caminho = os.path.join(SITE, pg)
        if not os.path.exists(caminho):
            erros.append(f"pagina ausente: royal-master/{pg}")
            continue
        html = open(caminho, encoding="utf-8").read()
        for m in re.finditer(r'(?:src|href)="([^"#?]+)', html):
            u = m.group(1)
            if u.startswith(("http", "mailto", "tel", "javascript", "//")):
                continue
            if not os.path.exists(os.path.join(SITE, u)):
                erros.append(f"link/arquivo quebrado em {pg}: {u}")
        for tag in re.findall(r"<img\b[^>]*>", html):
            if 'alt="' not in tag or 'title="' not in tag:
                src = re.search(r'src="([^"]+)"', tag)
                erros.append(f"imagem sem alt/title em {pg}: {src.group(1) if src else tag[:60]}")

    # 2. toda imagem do manifesto existe no site e em fotos-otimizadas
    for s in SLOTS.values():
        if not os.path.exists(os.path.join(SITE, "image", s["out"])):
            erros.append(f"imagem do site ausente: image/{s['out']}  (rode python ferramentas/imagens.py)")
        if not os.path.exists(os.path.join(OTIMIZADAS, os.path.basename(s["out"]))):
            avisos.append(f"falta em fotos-otimizadas/: {os.path.basename(s['out'])}  (rode python ferramentas/imagens.py)")

    # 3. fotos originais: quais fontes ainda sao so a versao provisoria?
    chaves = sorted({s["src"] for s in SLOTS.values() if s["src"]})
    sem_original = [c for c in chaves
                    if not any(os.path.exists(os.path.join(ORIGINAIS, c + e)) for e in EXTS_FOTO)]
    if sem_original:
        avisos.append("AINDA FALTAM os arquivos ORIGINAIS (sem otimizar) de: " + ", ".join(sem_original)
                      + "\n      -> coloque em fotos-originais/<chave>.jpg e rode python ferramentas/imagens.py")
    return erros, avisos


# ---------------------------------------------------------------- zip
def arquivos_de(pasta, ignorar_extra=()):
    for raiz, dirs, nomes in os.walk(pasta):
        dirs[:] = sorted(d for d in dirs if d not in IGNORAR)
        for n in sorted(nomes):
            if n in IGNORAR or n in ignorar_extra:
                continue
            yield os.path.join(raiz, n)


def leiame(integrantes):
    nomes = "\n".join(f"  - {n}" for n in integrantes) if integrantes else "  (nomes no corpo do e-mail)"
    return f"""AP2 - DESIGN GRAFICO E USER EXPERIENCE - turma 8003 - Prof. Maurice Chalom
{MARCA}
Gerado em {datetime.date.today().strftime('%d/%m/%Y')}

INTEGRANTES
{nomes}

COMO ABRIR
  Abra  site/index.html  no navegador (nao precisa de servidor).

CONTEUDO DESTE ZIP
  site/              site completo, feito sobre a ESTRUTURA do template Royal Hotel (Colorlib):
                     index, accomodation (cardapio), gallery, blog, blog-single, about e contact.
                     Textos, titulos, botoes, imagens, logo e favicon foram trocados pelo tema
                     "cantina italiana". O link do blog.html para o blog-single.html funciona.
  fotos-originais/   fotos novas no tamanho original, sem otimizacao (+ CREDITOS.md com autoria/licencas).
  fotos-otimizadas/  as mesmas imagens do site, otimizadas (WebP/PNG) e com nomes de arquivo
                     pensados para SEO. Todas tem EXATAMENTE a dimensao da imagem equivalente do template
                     e levam os atributos alt e title no HTML.

OBSERVACOES
  - Textos, enderecos, telefones, precos e depoimentos sao ficticios.
  - Fotos dos pratos: Wikimedia Commons (licencas livres; creditos na pagina Cardapio e em CREDITOS.md).
  - Fotos de perfil dos depoimentos: rostos gerados por IA (dominio publico), nao sao pessoas reais.
  - Template Royal Hotel por Colorlib, licenca CC BY 3.0 (link de credito mantido no rodape).
"""


def email(integrantes, tamanho_mb):
    nomes = "\n".join(f"- {n}" for n in integrantes) if integrantes else "- [NOME COMPLETO DO INTEGRANTE 1]\n- [NOME COMPLETO DO INTEGRANTE 2]"
    return f"""Para:    {PROFESSOR}
Assunto: {ASSUNTO}
Anexo:   entrega/{NOME_ZIP}  ({tamanho_mb:.1f} MB)

Prezado professor Maurice,

Segue em anexo o zip do trabalho AP2 de Design Gráfico e UX (turma 8003): o site da
"{MARCA}", refeito sobre a estrutura do template Royal Hotel, com a pasta das fotos
novas no tamanho original e a pasta das fotos otimizadas com nomes pensados para SEO.

Integrantes do grupo:
{nomes}

Atenciosamente,
[NOME]
"""


def main():
    ap = argparse.ArgumentParser(description="Gera o zip da entrega da AP2.")
    ap.add_argument("--integrantes", default="", help='nomes completos separados por ";"')
    args = ap.parse_args()
    integrantes = [n.strip() for n in args.integrantes.split(";") if n.strip()]

    erros, avisos = conferir()
    for e in erros:
        print("ERRO   :", e)
    if erros:
        print(f"\n{len(erros)} erro(s). Corrija e rode de novo; o zip NAO foi gerado.")
        sys.exit(1)

    os.makedirs(SAIDA, exist_ok=True)
    destino = os.path.join(SAIDA, NOME_ZIP)
    lista = []
    for caminho in arquivos_de(SITE):
        lista.append((caminho, "site/" + os.path.relpath(caminho, SITE).replace(os.sep, "/")))
    for caminho in arquivos_de(ORIGINAIS, ignorar_extra={"LEIA-ME.txt"}):
        lista.append((caminho, "fotos-originais/" + os.path.relpath(caminho, ORIGINAIS).replace(os.sep, "/")))
    for caminho in arquivos_de(OTIMIZADAS):
        lista.append((caminho, "fotos-otimizadas/" + os.path.relpath(caminho, OTIMIZADAS).replace(os.sep, "/")))

    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr("LEIA-ME.txt", leiame(integrantes))
        for caminho, nome in lista:
            z.write(caminho, nome)

    mb = os.path.getsize(destino) / 1024 / 1024
    with open(os.path.join(SAIDA, "EMAIL-rascunho.txt"), "w", encoding="utf-8") as f:
        f.write(email(integrantes, mb))

    contagem = {p: sum(1 for _, n in lista if n.startswith(p + "/")) for p in ("site", "fotos-originais", "fotos-otimizadas")}
    print(f"Zip gerado: entrega/{NOME_ZIP}  ({mb:.1f} MB)")
    print("  " + " | ".join(f"{p}: {n} arquivos" for p, n in contagem.items()))
    print("Rascunho do e-mail: entrega/EMAIL-rascunho.txt")
    if mb > LIMITE_EMAIL_MB:
        avisos.append(f"o zip tem {mb:.1f} MB; anexos grandes podem ser recusados (Gmail: 25 MB). Use um link do Drive se precisar.")
    if not integrantes:
        avisos.append('nomes dos integrantes nao informados: rode de novo com --integrantes "Nome 1; Nome 2" '
                      "ou edite entrega/EMAIL-rascunho.txt")
    for a in avisos:
        print("ATENCAO:", a)
    print(f"\nPrazo de entrega: {PRAZO} (presenca obrigatoria).")


if __name__ == "__main__":
    main()
