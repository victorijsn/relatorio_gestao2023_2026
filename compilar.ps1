<#
.SYNOPSIS
    Script de automação para conversão dos arquivos Word (.docx) das áreas e
    compilação do Relatório de Gestão SETADES (2023–2026) em PDF via Asciidoctor PDF.

.EXAMPLE
    .\compilar.ps1
    .\compilar.ps1 -RegenerarTemplates
#>

param (
    [switch]$RegenerarTemplates = $false,
    [switch]$PularConversaoDocx = $false
)

$ErrorActionPreference = "Stop"
$Raiz = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Raiz

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host " Relatório de Gestão SETADES (2023-2026) - Pipeline Editorial" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

# 1. Regenerar templates base caso solicitado
if ($RegenerarTemplates) {
    Write-Host "`n[1/3] Regenerando estrutura modular base a partir da Lista de Ações..." -ForegroundColor Yellow
    python "scripts\gerar_estrutura_inicial.py"
}

# 2. Importar arquivos .docx depositados em "Textos - áreas/"
if (-not $PularConversaoDocx) {
    Write-Host "`n[2/3] Verificando arquivos .docx na pasta 'Textos - áreas/'..." -ForegroundColor Yellow
    python "scripts\converter_docx_para_adoc.py"
}

# 3. Compilar PDF com Asciidoctor PDF e tema oficial SECOM-ES
Write-Host "`n[3/3] Compilando PDF consolidado (dist\Relatorio_Gestao_SETADES_2023_2026.pdf)..." -ForegroundColor Yellow

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
            $ArquivoSaida = "dist/Relatorio_Gestao_SETADES_2023_2026_atualizado.pdf"
            Write-Host "`n[AVISO] O PDF principal está aberto em outro programa (ex.: Adobe Reader)." -ForegroundColor Yellow
            Write-Host "Gerando versão atualizada em: $ArquivoSaida" -ForegroundColor Yellow
        }
    }

    & $AsciidoctorPdf "index.adoc" `
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
