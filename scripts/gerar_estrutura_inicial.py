# -*- coding: utf-8 -*-
"""
Gera a estrutura modular inicial em AsciiDoc (.adoc) para o Relatório de Gestão
SETADES (2023–2026) a partir do Modelo do Texto e da Lista de Ações por
Subsecretaria, Gerência e Responsáveis.
"""

import os

ESTRUTURA = [
    {
        "sigla": "SUBAAD",
        "nome": "Subsecretaria de Estado para Assuntos Administrativos (SUBAAD)",
        "descricao": "Unidade responsável pela coordenação administrativa, orçamentária, financeira, de contratos e de convênios da SETADES.",
        "unidades": [
            {
                "codigo": "SUBAAD-GGCONV",
                "nome": "Gerência de Gestão de Convênios (GGCONV)",
                "responsaveis": [
                    {
                        "nome": "Thiago Mendes dos Santos (Gerente de Gestão de Convênios)",
                        "acoes": [
                            "Gestão de Convênios e Instrumentos de Parceria da SETADES",
                        ],
                    }
                ],
            },
            {
                "codigo": "SUBAAD-GADM",
                "nome": "Gerência Administrativa (GADM)",
                "responsaveis": [
                    {
                        "nome": "Fabiana Cardinott Reis Mignone (Gerente Administrativa)",
                        "acoes": [
                            "Gestão e Execução dos Contratos Administrativos de Natureza Continuada",
                        ],
                    }
                ],
            },
        ],
    },
    {
        "sigla": "SUBAPI",
        "nome": "Subsecretaria de Estado de Articulação de Políticas Intersetoriais (SUBAPI)",
        "descricao": "Unidade responsável pela articulação intersetorial, formação e fortalecimento das políticas voltadas à Primeira Infância e ações integradas.",
        "unidades": [
            {
                "codigo": "SUBAPI-GCAM",
                "nome": "Gerência de Capacitação, Articulação e Mobilização",
                "responsaveis": [
                    {
                        "nome": "Cláudia Pessin Machado Vieira",
                        "acoes": [
                            "FOCO - Programa de Formação dos Gestores e Profissionais da Assistência Social, Saúde e Educação",
                            "BPIC - Boas Práticas pela Primeira Infância",
                            "Observatório Capixaba da Primeira Infância",
                            "Concurso Primeira Infância com Arte - PIARTE",
                        ],
                    },
                    {
                        "nome": "Elaine de Oliveira Leppaus",
                        "acoes": [
                            'Especialização lato sensu "Intersetorialidade para o Desenvolvimento Integral da Primeira Infância"',
                        ],
                    },
                ],
            }
        ],
    },
    {
        "sigla": "SUBADES",
        "nome": "Subsecretaria de Estado de Assistência e Desenvolvimento Social (SUBADES)",
        "descricao": "Unidade responsável pela coordenação estadual do Sistema Único de Assistência Social (SUAS), Proteção Social Básica e Especial, Benefícios, Vigilância Socioassistencial e Segurança Alimentar e Nutricional.",
        "unidades": [
            {
                "codigo": "SUBADES-GPSB",
                "nome": "Gerência de Proteção Social Básica (GPSB)",
                "responsaveis": [
                    {
                        "nome": "Nilzamara Rosa Tesch Oliveira (Gerente)",
                        "acoes": [
                            "Apoio Técnico e Assessoramento aos Municípios na Gestão e Execução dos Serviços da Proteção Social Básica",
                            "Monitoramento dos Serviços Socioassistenciais da Proteção Social Básica nos Municípios do Espírito Santo",
                            "Cofinanciamento Estadual para Construção, Reforma e Ampliação de Equipamentos Socioassistenciais",
                            "Cofinanciamento Estadual para Aquisição de Mobiliário dos Equipamentos Socioassistenciais",
                        ],
                    }
                ],
            },
            {
                "codigo": "SUBADES-GPSE",
                "nome": "Gerência de Proteção Social Especial (GPSE)",
                "responsaveis": [
                    {
                        "nome": "Douglas Mothé Rossetto (Gerente)",
                        "acoes": [
                            "Cobertura dos CREAS e fortalecimento do PAEFI",
                            "Atenção à população em situação de rua e oferta de Centros POP",
                            "Apoio técnico e assessoramento aos municípios",
                            "Produção de orientações técnicas e materiais de apoio",
                            "Monitoramento e validação da rede de Proteção Social Especial",
                            "Incentivo à implantação de Centros Dia e Residências Inclusivas",
                            "Qualificação da infraestrutura das unidades da PSE",
                            "Acompanhamento das Residências Inclusivas e estudos de organização consorciada",
                        ],
                    }
                ],
            },
            {
                "codigo": "SUBADES-GBTR",
                "nome": "Gerência de Benefícios e Transferência de Renda (GBTR)",
                "responsaveis": [
                    {
                        "nome": "Ricardo Azevedo Masruha (Gerente)",
                        "acoes": [
                            "Programa Bolsa Capixaba",
                            "Programa Vale Gás Capixaba",
                            "Cartão Reconstrução",
                            "Gestão e Monitoramento dos Benefícios Estaduais",
                            "Coordenação Estadual do Cadastro Único e Programa Bolsa Família",
                            "Benefícios Eventuais",
                            "Benefício de Prestação Continuada (BPC) e Programa BPC na Escola",
                        ],
                    }
                ],
            },
            {
                "codigo": "SUBADES-GSUAS",
                "nome": "Gerência do Sistema Único de Assistência Social (GSUAS)",
                "responsaveis": [
                    {
                        "nome": "Quécia Cristina De Abreu (Gerente)",
                        "acoes": [
                            "Cofinanciamento Estadual dos Benefícios Eventuais e Serviços Socioassistenciais Continuados",
                            "Aprimoramento da Gestão e apoio técnico aos municípios",
                            "Fortalecimento das instâncias de pactuação e controle social (CIB/ES e CEAS/ES)",
                            "Rede SUAS",
                            "Gestão do Trabalho e Educação Permanente do SUAS",
                            "Revista do SUAS ES",
                        ],
                    }
                ],
            },
            {
                "codigo": "SUBADES-VIGILANCIA",
                "nome": "Vigilância Socioassistencial",
                "responsaveis": [
                    {
                        "nome": "Rafael Duarte Oliveira (Coordenador)",
                        "acoes": [
                            "Diagnóstico Socioterritorial, enquanto projeto",
                            "Vigilância em Rede, enquanto ação",
                            "Monitoramento do RMA, enquanto processo",
                            "Monitoramento dos indicadores socioassistenciais, enquanto processo",
                            "Apoio técnico para acesso aos sistemas, enquanto processo",
                            "Orientação técnica aos municípios, enquanto processo",
                            "Produção de boletins internos, enquanto processo",
                            "Organização e atualização do CADUAS, enquanto processo",
                        ],
                    }
                ],
            },
            {
                "codigo": "SUBADES-GSAN",
                "nome": "Gerência de Segurança Alimentar e Nutricional (GSAN)",
                "responsaveis": [
                    {
                        "nome": "Isadora Chagas Queiroz (Gerente)",
                        "acoes": [
                            "Ação 6863 - Segurança Alimentar e Nutricional (SAN)",
                            "Programa Compra Direta de Alimentos (CDA)",
                            "Programa de Aquisição de Alimentos (PAA)",
                            "Projeto Cozinhas Solidárias",
                            "Formação Continuada em Segurança Alimentar e Nutricional",
                            "Manutenção Corretiva, Preventiva e Evolutiva do Sistema SisCDA (Contrato nº 2025.000022.47101.01 – Form's Informática LTDA)",
                            "Execução Operacional do Pagamento aos Agricultores Beneficiados do Programa CDA (Contrato nº 2024.000004.47101.01 – BANESTES)",
                        ],
                    }
                ],
            },
        ],
    },
    {
        "sigla": "SUBGEP",
        "nome": "Subsecretaria de Estado de Gestão de Programas e Projetos (SUBGEP)",
        "descricao": "Unidade responsável pela gestão da informação, monitoramento e avaliação de políticas públicas, gestão do conhecimento, planejamento estratégico e inovação em processos.",
        "unidades": [
            {
                "codigo": "SUBGEP-NAGI",
                "nome": "Núcleo de Avaliação e Gestão da Informação (NAGI)",
                "responsaveis": [
                    {
                        "nome": "Victor Nunes Toscano (Gerente)",
                        "acoes": [
                            "HUB-SETADES - Projeto de gestão do conhecimento da secretaria",
                            "Sistema de Gestão de Eventos da SETADES - Projeto",
                            "Comissão de aprimoramento do Programa Incluir 2.0",
                            "Rotina de tratamento de Dados e Informações da SETADES",
                            "Relatórios de gestão da SETADES",
                            "Relatório de Gestão para o Tribunal de Contas do Espírito Santo",
                            "Ponto focal do Planejamento de Governo junto à SEP",
                            "Condução do planejamento estratégico da SETADES",
                            "Gestão da parceria com Motriz, SEGER e Fapes para o programa de trainee",
                            "Construção de instrumentos de monitoramento e avaliação das políticas da SETADES",
                            "Coordenação do Escritório Local de Processos e Inovação (ELPI)",
                        ],
                    }
                ],
            }
        ],
    },
]


def gerar_introducao(base_dir: str) -> None:
    intro_path = os.path.join(base_dir, "capitulos", "00-introducao.adoc")
    conteudo = """= Apresentação Institucional

[.introducao]#RELATÓRIO DE GESTÃO QUADRIENAL • 2023 A 2026#

O presente **Relatório de Gestão da Secretaria de Estado de Trabalho, Assistência e Desenvolvimento Social (SETADES)** consolida as principais ações, projetos e processos prioritários executados no ciclo governamental de **2023 a 2026**.

Estruturado por Subsecretaria e Gerência/Unidade Técnica, cada relato segue o modelo institucional padronizado em três eixos:

* **1. Descrição**: caracterização da iniciativa, público atendido e periodicidade;
* **2. Entregas realizadas no mandato (2023 a 2026)**: resultados alcançados, metas cumpridas, volume de atendimentos, cobertura municipal e execução orçamentária;
* **3. Desafios para a continuidade da ação**: pontos de atenção orçamentários, operacionais, tecnológicos e de gestão para o próximo ciclo.

.Síntese da Estrutura Mapeada no Relatório
[cols="2,3,1,1", options="header"]
|===
| Sigla | Subsecretaria | Unidades | Ações Mapeadas

| *SUBAAD*
| Subsecretaria de Estado para Assuntos Administrativos
| 2
| 2

| *SUBAPI*
| Subsecretaria de Estado de Articulação de Políticas Intersetoriais
| 1
| 5

| *SUBADES*
| Subsecretaria de Estado de Assistência e Desenvolvimento Social
| 6
| 40

| *SUBGEP*
| Subsecretaria de Estado de Gestão de Programas e Projetos
| 1
| 11

| *TOTAL*
| *4 Subsecretarias*
| *10*
| *58*
|===

<<<
"""
    with open(intro_path, "w", encoding="utf-8") as f:
        f.write(conteudo)


def gerar_arquivos_subsecretarias(base_dir: str) -> None:
    total_unidades = 0
    total_acoes = 0

    for sub in ESTRUTURA:
        sigla = sub["sigla"]
        sub_dir = os.path.join(base_dir, "capitulos", sigla)
        os.makedirs(sub_dir, exist_ok=True)

        # Arquivo de abertura da Subsecretaria (_index.adoc)
        index_sub_path = os.path.join(sub_dir, "_index.adoc")
        qtd_unidades = len(sub["unidades"])
        qtd_acoes_sub = sum(
            len(r["acoes"]) for u in sub["unidades"] for r in u["responsaveis"]
        )

        linhas_abertura = [
            f"= {sub['nome']}",
            "",
            f"[.introducao]#UNIDADES TÉCNICAS: {qtd_unidades} • AÇÕES E PROCESSOS RELATADOS: {qtd_acoes_sub}#",
            "",
            sub["descricao"],
            "",
            ".Quadro Síntese das Unidades e Responsáveis",
            '[cols="2,2,1", options="header"]',
            "|===",
            "| Gerência / Unidade | Responsável | Nº de Ações",
            "",
        ]
        for u in sub["unidades"]:
            resps = " / ".join(r["nome"] for r in u["responsaveis"])
            n_acoes = sum(len(r["acoes"]) for r in u["responsaveis"])
            linhas_abertura.append(f"| {u['nome']} | {resps} | {n_acoes}")
        linhas_abertura.extend(["|===", "", "'''", ""])

        with open(index_sub_path, "w", encoding="utf-8") as f:
            f.write("\n".join(linhas_abertura))

        # Arquivos por Gerência/Unidade
        for u in sub["unidades"]:
            total_unidades += 1
            arq_path = os.path.join(sub_dir, f"{u['codigo']}.adoc")
            resps_texto = "; ".join(r["nome"] for r in u["responsaveis"])

            blocos = [
                f"= {u['nome']}",
                "",
                ".Identificação da Unidade",
                '[cols="1,3", options="header"]',
                "|===",
                "| Campo | Preenchimento",
                f"| *Subsecretaria* | {sub['nome']}",
                f"| *Gerência ou setor* | {u['nome']}",
                f"| *Responsável* | {resps_texto}",
                "| *Contato* | _A preencher (e-mail institucional e telefone/ramal)_",
                "|===",
                "",
                "'''",
                "",
            ]

            for resp in u["responsaveis"]:
                for acao in resp["acoes"]:
                    total_acoes += 1
                    blocos.extend(
                        [
                            f"== {acao}",
                            "",
                            "=== 1. Descrição",
                            "// Orientações: Explique o que é a iniciativa, quem ela atende (público externo, como famílias e municípios, ou áreas internas da administração) e com qual frequência acontece (contínua, anual, por edital, etc.).",
                            "_Texto pendente de envio pela área técnica._",
                            "",
                            "=== 2. Entregas realizadas no mandato (2023 a 2026)",
                            "// Orientações: Destaque os resultados alcançados, metas cumpridas, volume de atendimentos ou benefícios, municípios contemplados e recursos executados entre 2023 e 2026.",
                            "_Texto pendente de envio pela área técnica._",
                            "",
                            "=== 3. Desafios para a continuidade da ação",
                            "// Orientações: Aponte as principais dificuldades orçamentárias, operacionais, de pessoal ou de tecnologia que os próximos gestores precisarão enfrentar para manter ou aprimorar a ação.",
                            "_Texto pendente de envio pela área técnica._",
                            "",
                            "<<<",
                            "",
                        ]
                    )

            with open(arq_path, "w", encoding="utf-8") as f:
                f.write("\n".join(blocos))

    print(
        f"Estrutura gerada com sucesso: {len(ESTRUTURA)} Subsecretarias, "
        f"{total_unidades} Unidades/Gerências e {total_acoes} Ações."
    )


if __name__ == "__main__":
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gerar_introducao(raiz)
    gerar_arquivos_subsecretarias(raiz)
