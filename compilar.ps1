<#
.SYNOPSIS
    Script de automação para validação estrutural dos capítulos em AsciiDoc,
    importação opcional de arquivos Word (.docx) e compilação do Relatório de
    Gestão SETADES (2023–2026) em PDF via Asciidoctor PDF.

.EXAMPLE
    .\compilar.ps1
    .\compilar.ps1 -PadronizarCapitulos
    .\compilar.ps1 -ImportarDocx
    .\compilar.ps1 -ImportarDocx -SobrescreverDocx
    .\compilar.ps1 -RegenerarTemplates
#>

param (
    [switch]$RegenerarTemplates = $false,
    [switch]$ImportarDocx = $false,
    [switch]$SobrescreverDocx = $false,
    [switch]$PadronizarCapitulos = $false,
    [switch]$Forcar = $false
)

$ErrorActionPreference = "Stop"
$Raiz = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Raiz

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host " Relatório de Gestão SETADES (2023-2026) - Pipeline Editorial" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

$Utf8SemBom = New-Object System.Text.UTF8Encoding($false)

function Obter-CapitulosUnidades {
    Get-ChildItem -Path "capitulos\*\*.adoc" -File |
        Where-Object { $_.Name -ne "_index.adoc" } |
        Sort-Object FullName
}

# 1. Regenerar templates base caso solicitado explicitamente
if ($RegenerarTemplates) {
    Write-Host "`n[OPCIONAL] Regeneração de templates base solicitada." -ForegroundColor Yellow
    Write-Host "  ATENÇÃO: Esta ação sobrescreve os arquivos .adoc em 'capitulos/' com o template inicial." -ForegroundColor Red
    if (-not $Forcar) {
        $Resp = Read-Host "  Digite 'SIM' para confirmar a sobrescrita"
        if ($Resp -ne "SIM") {
            Write-Host "  Operação cancelada pelo usuário." -ForegroundColor Yellow
            exit 0
        }
    }
    python "scripts\gerar_estrutura_inicial.py"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`n[ERRO] Falha ao regenerar templates (código $LASTEXITCODE)." -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

# 2. Importar arquivos .docx depositados em "Textos - áreas/" (somente sob demanda)
if ($ImportarDocx) {
    Write-Host "`n[OPCIONAL] Importando arquivos .docx da pasta 'Textos - áreas/'..." -ForegroundColor Yellow
    if ($SobrescreverDocx) {
        python "scripts\converter_docx_para_adoc.py" --sobrescrever
    } else {
        python "scripts\converter_docx_para_adoc.py"
    }
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`n[ERRO] Falha na conversão de arquivos .docx (código $LASTEXITCODE)." -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

# 3. Padronizar capítulos para a estrutura revisada (ex.: SUBADES-GBTR), se solicitado
if ($PadronizarCapitulos) {
    Write-Host "`n[OPCIONAL] Padronizando capítulos para a estrutura revisada (padrão SUBADES-GBTR)..." -ForegroundColor Yellow
    $Atualizados = 0
    foreach ($Arq in (Obter-CapitulosUnidades)) {
        $Conteudo = [System.IO.File]::ReadAllText($Arq.FullName, [System.Text.Encoding]::UTF8)
        $NovoConteudo = $Conteudo
        # Remove linha antiga [.detalhe]#Parte 1: ...# (e a linha em branco imediata seguinte, se houver)
        $NovoConteudo = [regex]::Replace($NovoConteudo, '(?m)^\[\.detalhe\]#Parte\s+1:.*#\r?\n(\r?\n)?', '')
        # Padroniza "=== 1. Descrição resumida" para "=== 1. Descrição"
        $NovoConteudo = [regex]::Replace($NovoConteudo, '(?m)^=== 1\. Descrição resumida(?=\r?$)', '=== 1. Descrição')

        if ($NovoConteudo -ne $Conteudo) {
            [System.IO.File]::WriteAllText($Arq.FullName, $NovoConteudo, $Utf8SemBom)
            $Rel = $Arq.FullName.Substring($Raiz.Length + 1)
            Write-Host "  [PADRONIZADO] $Rel" -ForegroundColor Green
            $Atualizados++
        }
    }
    if ($Atualizados -eq 0) {
        Write-Host "  Todos os capítulos já estão no formato revisado." -ForegroundColor Green
    } else {
        Write-Host "  Total de capítulos padronizados: $Atualizados" -ForegroundColor Green
    }
}

# 4. Validar estrutura revisada dos capítulos antes da compilação
Write-Host "`n[1/2] Validando estrutura revisada dos capítulos em 'capitulos/'..." -ForegroundColor Yellow
$Capitulos = Obter-CapitulosUnidades
$QtdComLegado = 0
$TotalPendencias = 0

foreach ($Arq in $Capitulos) {
    $Rel = $Arq.FullName.Substring($Raiz.Length + 1)
    $Texto = [System.IO.File]::ReadAllText($Arq.FullName, [System.Text.Encoding]::UTF8)

    $TemIdentificacao = [regex]::IsMatch($Texto, '(?m)^\.Identificação da Unidade\r?$')
    $QtdParte1 = ([regex]::Matches($Texto, '(?m)^\[\.detalhe\]#Parte\s+1:')).Count
    $QtdDescResumida = ([regex]::Matches($Texto, '(?m)^=== 1\. Descrição resumida(?=\r?$)')).Count
    $QtdPendentes = ([regex]::Matches($Texto, '_Texto pendente de envio pela área técnica\._')).Count
    $TotalPendencias += $QtdPendentes

    $Alertas = @()
    if (-not $TemIdentificacao) { $Alertas += "sem tabela '.Identificação da Unidade'" }
    if ($QtdParte1 -gt 0) { $Alertas += "$QtdParte1 linha(s) antiga(s) '[.detalhe]#Parte 1:...#'" }
    if ($QtdDescResumida -gt 0) { $Alertas += "$QtdDescResumida título(s) '=== 1. Descrição resumida'" }

    if ($Alertas.Count -gt 0) {
        $QtdComLegado++
        Write-Host ("  [AVISO] {0}: {1}" -f $Rel, ($Alertas -join "; ")) -ForegroundColor Yellow
    }
}

$QtdConformes = $Capitulos.Count - $QtdComLegado
Write-Host ("  Resumo: {0}/{1} capítulos na estrutura revisada | {2} seção(ões) ainda pendente(s) de texto." -f $QtdConformes, $Capitulos.Count, $TotalPendencias) -ForegroundColor Cyan
if ($QtdComLegado -gt 0) {
    Write-Host "  Dica: execute '.\compilar.ps1 -PadronizarCapitulos' para atualizar automaticamente os capítulos com formato antigo." -ForegroundColor DarkYellow
}

# 5. Compilar PDF com Asciidoctor PDF e tema oficial SECOM-ES
Write-Host "`n[2/2] Compilando PDF consolidado (dist\Relatorio_Gestao_SETADES_2023_2026.pdf)..." -ForegroundColor Yellow

$AsciidoctorPdf = Get-Command "asciidoctor-pdf" -ErrorAction SilentlyContinue

if ($null -eq $AsciidoctorPdf) {
    # Procurar em instalações comuns do Ruby no Windows
    $PossiveisCaminhos = Get-ChildItem -Path "C:\Ruby*\bin\asciidoctor-pdf.bat", "$env:LOCALAPPDATA\Programs\Ruby*\bin\asciidoctor-pdf.bat" -ErrorAction SilentlyContinue
    if ($PossiveisCaminhos) {
        $AsciidoctorPdf = $PossiveisCaminhos[0].FullName
    }
}

if ($null -eq $AsciidoctorPdf) {
    $GemCmd = "C:\Ruby32-x64\bin\gem.cmd"
    if (Test-Path $GemCmd) {
        Write-Host "`n[INSTALAÇÃO] O Ruby 3.2 já está instalado em C:\Ruby32-x64, mas falta a gem 'asciidoctor-pdf'." -ForegroundColor Yellow
        Write-Host "Abrindo janela de credenciais do Windows para autenticar no proxy (setades.proxy.dcpr.es.gov.br:1860)..." -ForegroundColor Cyan
        $cred = Get-Credential -Message "Digite seu usuário e senha de rede da SETADES para instalar o asciidoctor-pdf"
        $user = [uri]::EscapeDataString($cred.UserName)
        $pass = [uri]::EscapeDataString($cred.GetNetworkCredential().Password)
        $proxyUrl = "http://${user}:${pass}@setades.proxy.dcpr.es.gov.br:1860"
        $env:HTTP_PROXY = $proxyUrl
        $env:HTTPS_PROXY = $proxyUrl
        & $GemCmd install asciidoctor asciidoctor-pdf --no-document --http-proxy $proxyUrl
        if (Test-Path "C:\Ruby32-x64\bin\asciidoctor-pdf.bat") {
            $AsciidoctorPdf = "C:\Ruby32-x64\bin\asciidoctor-pdf.bat"
        }
    }
}

if ($null -ne $AsciidoctorPdf) {
    New-Item -ItemType Directory -Force -Path "dist" | Out-Null
    $ArquivoSaida = "dist/Relatorio_Gestao_SETADES_2023_2026.pdf"

    # Verificar se o arquivo PDF está aberto/bloqueado por outro leitor (ex.: Adobe Reader)
    if (Test-Path $ArquivoSaida) {
        try {
            $stream = [System.IO.File]::Open($ArquivoSaida, 'Open', 'Write', 'None')
            $stream.Close()
        } catch {
            $Timestamp = Get-Date -Format "HHmmss"
            $ArquivoSaida = "dist/Relatorio_Gestao_SETADES_2023_2026_$Timestamp.pdf"
            Write-Host "`n[AVISO] O PDF principal está aberto em outro programa (ex.: Adobe Reader)." -ForegroundColor Yellow
            Write-Host "Gerando versão atualizada em: $ArquivoSaida" -ForegroundColor Yellow
        }
    }

    & $AsciidoctorPdf "index.adoc" `
        -r "./scripts/rodape_por_pagina.rb" `
        -a pdf-theme="tema/setades-theme.yml" `
        -a pdf-fontsdir="tema/fonts" `
        -o $ArquivoSaida

    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n[SUCESSO] PDF gerado em: $ArquivoSaida" -ForegroundColor Green
    } else {
        Write-Host "`n[ERRO] A compilação do Asciidoctor PDF retornou código $LASTEXITCODE." -ForegroundColor Red
        exit $LASTEXITCODE
    }
} else {
    Write-Host "`n[ATENÇÃO] Não foi possível localizar ou instalar o 'asciidoctor-pdf'." -ForegroundColor Yellow
}
