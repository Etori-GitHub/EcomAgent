#!/usr/bin/env powershell
# Gateway Start Script - Stable Version
# Separate Gateway and Monitor Service

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

$logDir = "$scriptDir\logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

$logFile = "$logDir\gateway.log"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  OpenClaw Gateway + Monitor Starter" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Log: $logFile" -ForegroundColor Gray
Write-Host ""

# Clear old log (optional)
if (Test-Path $logFile) {
    Clear-Content $logFile
    Write-Host "Cleared old log" -ForegroundColor Gray
}

# Set UTF-8 encoding
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Monitor service is now started manually
# To start monitor: python src/monitor.py
Write-Host "Note: Monitor service should be started manually" -ForegroundColor Yellow
Write-Host "  Run: python src/monitor.py" -ForegroundColor Gray
Write-Host ""

Write-Host "Starting Gateway..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop both services" -ForegroundColor Yellow
Write-Host ""

# Use cmd to start Gateway, avoid PowerShell pipeline issues
# 方案：使用 .NET StreamWriter 以共享模式写入日志，避免与 Python 冲突

# 创建共享写模式的 StreamWriter
$fs = [System.IO.FileStream]::new($logFile, [System.IO.FileMode]::Append, [System.IO.FileAccess]::Write, [System.IO.FileShare]::ReadWrite)
$writer = [System.IO.StreamWriter]::new($fs, [System.Text.Encoding]::UTF8)

try {
    cmd /c "openclaw gateway --verbose --ws-log full 2>&1" | ForEach-Object {
        $line = $_
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        $logLine = "[$timestamp] $line"
        
        # Output to console
        Write-Host $line
        
        # Write to log file (共享模式)
        $writer.WriteLine($logLine)
        $writer.Flush()
    }
} finally {
    $writer.Close()
    $fs.Close()
}

Write-Host ""
Write-Host "Gateway stopped" -ForegroundColor Cyan
Write-Host "Note: Monitor service is running separately" -ForegroundColor Yellow
