# -*- coding: utf-8 -*-
"""
Conversor automatizado de arquivos Word (.docx) preenchidos segundo o
'Modelo do texto.docx' na pasta 'Textos - áreas/' para os arquivos AsciiDoc (.adoc)
correspondentes em 'capitulos/<SUBSECRETARIA>/'.

Uso:
    python scripts/converter_docx_para_adoc.py
    python scripts/converter_docx_para_adoc.py --arquivo "Textos - áreas/SUBADES - GSUAS.docx"
"""

import argparse
import os
import re
import zipfile
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

# Mapeamento de palavras-chave / siglas do nome do arquivo ou da tabela para o destino .adoc
MAPA_UNIDADES: List[Tuple[List[str], str, str]] = [
    (["GGCONV", "CONVENIO", "CONVÊNIO"], "SUBAAD", "SUBAAD-GGCONV.adoc"),
    (["GADM", "SUBAAD - GA", "GERENCIA ADMINISTRATIVA", "GERÊNCIA ADMINISTRATIVA"], "SUBAAD", "SUBAAD-GADM.adoc"),
    (["GCAM", "SUBAPI", "CAPACITACAO", "CAPACITAÇÃO", "PRIMEIRA INFANCIA", "PRIMEIRA INFÂNCIA"], "SUBAPI", "SUBAPI-GCAM.adoc"),
    (["GPSB", "PROTECAO SOCIAL BASICA", "PROTEÇÃO SOCIAL BÁSICA"], "SUBADES", "SUBADES-GPSB.adoc"),
    (["GPSE", "PROTECAO SOCIAL ESPECIAL", "PROTEÇÃO SOCIAL ESPECIAL"], "SUBADES", "SUBADES-GPSE.adoc"),
    (["GBTR", "BENEFICIOS", "BENEFÍCIOS", "TRANSFERENCIA DE RENDA", "TRANSFERÊNCIA DE RENDA"], "SUBADES", "SUBADES-GBTR.adoc"),
    (["GSUAS", "SISTEMA UNICO", "SISTEMA ÚNICO"], "SUBADES", "SUBADES-GSUAS.adoc"),
    (["VIGILANCIA", "VIGILÂNCIA"], "SUBADES", "SUBADES-VIGILANCIA.adoc"),
    (["GSAN", "SEGURANCA ALIMENTAR", "SEGURANÇA ALIMENTAR"], "SUBADES", "SUBADES-GSAN.adoc"),
    (["NAGI", "SUBGEP", "AVALIACAO E GESTAO", "AVALIAÇÃO E GESTÃO"], "SUBGEP", "SUBGEP-NAGI.adoc"),
]

FRASES_IGNORAR = (
    "Modelo de preenchimento: Relatório de Gestão SETADES",
    "Instruções de uso:",
    "Copie este arquivo para a pasta Textos - áreas",
    "Preencha uma ficha da Parte 1 para cada ação",
    "Para consultar prazos e diretrizes gerais",
    "Identificação da unidade",
    "(Digite o título oficial da iniciativa.",
    "Orientações: Explique o que é a iniciativa",
    "Orientações: Destaque os resultados alcançados",
    "Orientações: Aponte as principais dificuldades",
)


def limpar_prefixo_resposta(texto: str) -> str:
    texto = texto.strip()
    texto = re.sub(r"^Resposta\s*:\s*", "", texto, flags=re.IGNORECASE)
    if texto in ("(Escreva o texto aqui)", ""):
        return ""
    return texto


def extrair_elementos_docx(caminho_docx: str) -> Tuple[List[List[List[str]]], List[str]]:
    """Retorna (lista_de_tabelas, lista_de_paragrafos) do arquivo .docx."""
    with zipfile.ZipFile(caminho_docx) as z:
        xml_content = z.read("word/document.xml")
    tree = ET.fromstring(xml_content)

    tabelas: List[List[List[str]]] = []
    paragrafos: List[str] = []

    body = tree.find("w:body", NS)
    if body is None:
        return tabelas, paragrafos

    for elem in body:
        tag = elem.tag.split("}")[-1]
        if tag == "p":
            textos = [t.text for t in elem.findall(".//w:t", NS) if t.text]
            linha = "".join(textos).strip()
            if linha:
                paragrafos.append(linha)
        elif tag == "tbl":
            linhas_tbl: List[List[str]] = []
            for row in elem.findall(".//w:tr", NS):
                celulas: List[str] = []
                for cell in row.findall(".//w:tc", NS):
                    ctext = "".join(t.text for t in cell.findall(".//w:t", NS) if t.text)
                    celulas.append(ctext.strip())
                if any(celulas):
                    linhas_tbl.append(celulas)
            if linhas_tbl:
                tabelas.append(linhas_tbl)

    return tabelas, paragrafos


def parse_docx_modelo(caminho_docx: str) -> Dict:
    """Extrai os metadados da unidade e a lista de ações relatadas de um .docx."""
    tabelas, paragrafos = extrair_elementos_docx(caminho_docx)

    identificacao = {
        "Subsecretaria": "",
        "Gerência ou setor": "",
        "Responsável": "",
        "Contato": "",
    }

    if tabelas:
        for linha in tabelas[0]:
            if len(linha) >= 2:
                chave, valor = linha[0].strip(), linha[1].strip()
                for k in identificacao:
                    if chave.lower().startswith(k.lower()[:10]):
                        identificacao[k] = valor

    acoes: List[Dict[str, str]] = []
    acao_atual: Optional[Dict[str, str]] = None
    secao_atual: Optional[str] = None
    aguardando_titulo = False

    for p in paragrafos:
        if any(p.startswith(frase) for frase in FRASES_IGNORAR):
            continue

        if re.match(r"^Parte\s+1\s*:", p, flags=re.IGNORECASE):
            if acao_atual and acao_atual.get("titulo"):
                acoes.append(acao_atual)
            acao_atual = {
                "titulo": "",
                "descricao": [],
                "entregas": [],
                "desafios": [],
            }
            secao_atual = None
            aguardando_titulo = True
            continue

        if re.match(r"^Parte\s+2\s*:", p, flags=re.IGNORECASE):
            # Caso o documento tenha Parte 2 (Compêndio de atos), encerra a leitura da Parte 1
            break

        if re.match(r"^1\.\s*Descri[çc][ãa]o\s+resumida", p, flags=re.IGNORECASE):
            secao_atual = "descricao"
            aguardando_titulo = False
            continue

        if re.match(r"^2\.\s*Entregas\s+realizadas", p, flags=re.IGNORECASE):
            secao_atual = "entregas"
            aguardando_titulo = False
            continue

        if re.match(r"^3\.\s*Desafios\s+para\s+a\s+continuidade", p, flags=re.IGNORECASE):
            secao_atual = "desafios"
            aguardando_titulo = False
            continue

        if aguardando_titulo and acao_atual is not None:
            if p.lower() != "nome da ação, projeto ou processo":
                acao_atual["titulo"] = p
                aguardando_titulo = False
            continue

        if acao_atual is not None and secao_atual in ("descricao", "entregas", "desafios"):
            limpo = limpar_prefixo_resposta(p)
            if limpo:
                acao_atual[secao_atual].append(limpo)

    if acao_atual and acao_atual.get("titulo"):
        acoes.append(acao_atual)

    return {
        "identificacao": identificacao,
        "acoes": acoes,
    }


def identificar_destino(nome_arquivo: str, identificacao: Dict[str, str]) -> Optional[Tuple[str, str]]:
    texto_busca = " ".join(
        [
            nome_arquivo.upper(),
            identificacao.get("Subsecretaria", "").upper(),
            identificacao.get("Gerência ou setor", "").upper(),
        ]
    )
    for chaves, sub, arq in MAPA_UNIDADES:
        for ch in chaves:
            if ch.upper() in texto_busca:
                return sub, arq
    return None


def gerar_adoc_unidade(dados: Dict, nome_padrao_unidade: str) -> str:
    ident = dados["identificacao"]
    titulo_unidade = ident.get("Gerência ou setor") or nome_padrao_unidade
    subsecretaria = ident.get("Subsecretaria") or "_Não informada_"
    responsavel = ident.get("Responsável") or "_Não informado_"
    contato = ident.get("Contato") or "_Não informado_"

    linhas = [
        f"= {titulo_unidade}",
        "",
        ".Identificação da Unidade",
        '[cols="1,3", options="header"]',
        "|===",
        "| Campo | Preenchimento",
        f"| *Subsecretaria* | {subsecretaria}",
        f"| *Gerência ou setor* | {titulo_unidade}",
        f"| *Responsável* | {responsavel}",
        f"| *Contato* | {contato}",
        "|===",
        "",
        "'''",
        "",
    ]

    for acao in dados["acoes"]:
        titulo_acao = acao["titulo"]
        desc = "\n\n".join(acao["descricao"]) or "_Texto pendente de envio pela área técnica._"
        entr = "\n\n".join(acao["entregas"]) or "_Texto pendente de envio pela área técnica._"
        desa = "\n\n".join(acao["desafios"]) or "_Texto pendente de envio pela área técnica._"

        linhas.extend(
            [
                f"== {titulo_acao}",
                "",
                f"[.detalhe]#Parte 1: Relato da ação (limite de 1 página por ação) • Responsável: {responsavel}#",
                "",
                "=== 1. Descrição resumida",
                desc,
                "",
                "=== 2. Entregas realizadas no mandato (2023 a 2026)",
                entr,
                "",
                "=== 3. Desafios para a continuidade da ação",
                desa,
                "",
                "<<<",
                "",
            ]
        )

    return "\n".join(linhas)


def processar_pasta(base_dir: str, arquivo_especifico: Optional[str] = None) -> int:
    pasta_entrada = os.path.join(base_dir, "Textos - áreas")
    if arquivo_especifico:
        arquivos = [arquivo_especifico]
    else:
        if not os.path.isdir(pasta_entrada):
            print(f"Pasta '{pasta_entrada}' não encontrada.")
            return 0
        arquivos = [
            os.path.join(pasta_entrada, f)
            for f in sorted(os.listdir(pasta_entrada))
            if f.lower().endswith(".docx") and not f.startswith("~$")
        ]

    if not arquivos:
        print("Nenhum arquivo .docx encontrado em 'Textos - áreas/' para conversão.")
        return 0

    convertidos = 0
    for caminho in arquivos:
        nome_arq = os.path.basename(caminho)
        dados = parse_docx_modelo(caminho)
        destino = identificar_destino(nome_arq, dados["identificacao"])

        if destino:
            sub, arq_adoc = destino
            caminho_saida = os.path.join(base_dir, "capitulos", sub, arq_adoc)
        else:
            slug = re.sub(r"[^A-Za-z0-9_-]+", "-", os.path.splitext(nome_arq)[0]).strip("-")
            os.makedirs(os.path.join(base_dir, "capitulos", "EXTRAS"), exist_ok=True)
            caminho_saida = os.path.join(base_dir, "capitulos", "EXTRAS", f"{slug}.adoc")

        if not dados["acoes"]:
            print(f"[AVISO] '{nome_arq}' não possui fichas preenchidas na Parte 1; mantendo template atual.")
            continue

        conteudo_adoc = gerar_adoc_unidade(dados, os.path.splitext(nome_arq)[0])
        with open(caminho_saida, "w", encoding="utf-8") as f:
            f.write(conteudo_adoc)
        convertidos += 1
        print(f"[OK] '{nome_arq}' ({len(dados['acoes'])} ações) -> '{caminho_saida}'")

    return convertidos


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converte arquivos .docx das áreas para .adoc")
    parser.add_argument("--arquivo", help="Caminho para um arquivo .docx específico", default=None)
    args = parser.parse_args()

    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    processar_pasta(raiz, args.arquivo)
