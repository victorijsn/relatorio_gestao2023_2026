# Walkthrough — Estruturação do Relatório de Gestão SETADES (2023–2026) em AsciiDoc

## O que foi construído

Toda a estrutura modular do **Relatório de Gestão SETADES (2023–2026)** foi criada e preparada para receber os textos das áreas técnicas, tanto via edição direta em `.adoc` quanto por importação automatizada de arquivos Word (`.docx`).

### 1. Identidade Visual SECOM-ES e Tipografia (`tema/`)
- **[setades-theme.yml](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/tema/setades-theme.yml)**: Tema completo para `Asciidoctor PDF` seguindo o manual [Identidade Visual do Governo do Estado_SECOM_ES.pdf](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/tema/Identidade%20Visual%20do%20Governo%20do%20Estado_SECOM_ES.pdf):
  - **Paleta Oficial**: Azul (`#5081A0`, `#366C88`, `#365A6D`), Marsala (`#B16C73`, `#9C5C6A`, `#7B4A55`), Cinza (`#CFCFCF`, `#7B7B7A`, `#585857`) e cores de alertas (`#28A058`, `#E2DD2D`, `#5081A0`, `#9C5C6A`).
  - **Capa Institucional**: Configurada com o [Brasão Setades.png](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/tema/Bras%C3%A3o%20Setades.png).
  - **Fontes Open Sans (`tema/fonts/`)**: Copiadas a partir da instalação local da máquina (`OpenSans-Light.ttf`, `OpenSans-Regular.ttf`, `OpenSans-Semibold.ttf`, `OpenSans-Bold.ttf`, `OpenSans-ExtraBold.ttf` e variantes) para incorporação direta no PDF.

### 2. Documento Mestre e Capítulos Modulares (`index.adoc` e `capitulos/`)
- **[index.adoc](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/index.adoc)**: Arquivo raiz que concatena a introdução, as **4 Subsecretarias** e as **10 Gerências/Unidades**.
- **[00-introducao.adoc](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/capitulos/00-introducao.adoc)**: Apresentação institucional e tabela-síntese das 58 ações mapeadas.
- **Capítulos por Subsecretaria e Unidade** (pré-populados com todas as 58 ações, responsáveis e estrutura de ficha de 1 página por ação conforme o [Modelo do texto.docx](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/Modelo%20do%20texto.docx)):
  - **SUBAAD**: [_index.adoc](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/capitulos/SUBAAD/_index.adoc), [SUBAAD-GGCONV.adoc](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/capitulos/SUBAAD/SUBAAD-GGCONV.adoc), [SUBAAD-GADM.adoc](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/capitulos/SUBAAD/SUBAAD-GADM.adoc)
  - **SUBAPI**: [_index.adoc](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/capitulos/SUBAPI/_index.adoc), [SUBAPI-GCAM.adoc](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/capitulos/SUBAPI/SUBAPI-GCAM.adoc)
  - **SUBADES**: [_index.adoc](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/capitulos/SUBADES/_index.adoc), [SUBADES-GPSB.adoc](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/capitulos/SUBADES/SUBADES-GPSB.adoc), [SUBADES-GPSE.adoc](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/capitulos/SUBADES/SUBADES-GPSE.adoc), [SUBADES-GBTR.adoc](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/capitulos/SUBADES/SUBADES-GBTR.adoc), [SUBADES-GSUAS.adoc](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/capitulos/SUBADES/SUBADES-GSUAS.adoc), [SUBADES-VIGILANCIA.adoc](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/capitulos/SUBADES/SUBADES-VIGILANCIA.adoc), [SUBADES-GSAN.adoc](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/capitulos/SUBADES/SUBADES-GSAN.adoc)
  - **SUBGEP**: [_index.adoc](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/capitulos/SUBGEP/_index.adoc), [SUBGEP-NAGI.adoc](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/capitulos/SUBGEP/SUBGEP-NAGI.adoc)

### 3. Scripts de Automação e Documentação
- **[gerar_estrutura_inicial.py](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/scripts/gerar_estrutura_inicial.py)**: Gera ou regenera todos os templates `.adoc` das subsecretarias e gerências.
- **[converter_docx_para_adoc.py](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/scripts/converter_docx_para_adoc.py)**: Converte automaticamente arquivos `.docx` colocados na pasta `Textos - áreas/` para os arquivos `.adoc` correspondentes em `capitulos/`.
- **[compilar.ps1](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/compilar.ps1)**: Executa a conversão de novos `.docx` e invoca o `asciidoctor-pdf` para gerar `dist/Relatorio_Gestao_SETADES_2023_2026.pdf`.
- **[LEIAME.adoc](file:///C:/Users/2970805/Documents/RelatorioGestao_2023a2026/LEIAME.adoc)**: Manual completo de operação do projeto.

---

## Verificação e Próximos Passos

1. **Validação da geração de templates**: `python scripts/gerar_estrutura_inicial.py` executou com sucesso, criando os 15 arquivos `.adoc` em `capitulos/` (4 Subsecretarias, 10 Unidades e 58 Ações).
2. **Validação do parser `.docx`**: `converter_docx_para_adoc.py` foi testado sobre `Modelo do texto.docx`, extraindo corretamente a tabela de identificação da unidade e a estrutura da Parte 1.
3. **Como usar a partir de agora**:
   - Deposite os arquivos `.docx` recebidos das gerências na pasta `Textos - áreas/` (ou edite diretamente os arquivos em `capitulos/`).
   - Caso queira instalar o `asciidoctor-pdf` após autenticar na proxy da rede SETADES, execute no seu terminal PowerShell:
     ```powershell
     winget install RubyInstallerTeam.RubyWithDevKit.3.2
     gem install asciidoctor asciidoctor-pdf
     .\compilar.ps1
     ```
