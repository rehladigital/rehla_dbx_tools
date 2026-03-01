param(
    [int]$MaxIdleMinutes = 10,
    [int]$PollSeconds = 30,
    [string[]]$WatchFiles = @("docs/CYCLE_LOG.md", "docs/PROCESS_DASHBOARD.md", "docs/LOOP_CONTEXT.md"),
    [switch]$NoPopup
)

function Start-RehlaWakeWatchdog {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RepoRoot,
        [Parameter(Mandatory = $true)]
        [string[]]$Files,
        [Parameter(Mandatory = $true)]
        [int]$IdleMinutes,
        [Parameter(Mandatory = $true)]
        [int]$IntervalSeconds,
        [Parameter(Mandatory = $true)]
        [bool]$DisablePopup
    )

    $resolvedFiles = @()
    foreach ($file in $Files) {
        $fullPath = Join-Path $RepoRoot $file
        if (Test-Path $fullPath) {
            $resolvedFiles += $fullPath
        } else {
            Write-Warning "Watch file not found and will be skipped: $file"
        }
    }

    if ($resolvedFiles.Count -eq 0) {
        throw "No valid watch files were found. Update -WatchFiles to existing paths."
    }

    $lastChange = (Get-Date)
    $lastFingerprint = ""
    $alerted = $false

    Write-Host "Wake watchdog started. Monitoring files:" -ForegroundColor Cyan
    $resolvedFiles | ForEach-Object { Write-Host " - $_" }
    Write-Host "Idle threshold: $IdleMinutes minutes | Poll interval: $IntervalSeconds seconds"
    Write-Host "Press Ctrl+C to stop."

    while ($true) {
        $state = foreach ($file in $resolvedFiles) {
            $item = Get-Item $file
            "$($item.FullName)|$($item.LastWriteTimeUtc.Ticks)"
        }
        $fingerprint = ($state -join ";")

        if ($fingerprint -ne $lastFingerprint) {
            $lastFingerprint = $fingerprint
            $lastChange = Get-Date
            $alerted = $false
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Activity detected, watchdog reset." -ForegroundColor DarkGreen
        }

        $idleFor = (Get-Date) - $lastChange
        if (-not $alerted -and $idleFor.TotalMinutes -ge $IdleMinutes) {
            $alerted = $true
            $message = "No cycle activity for $([int]$idleFor.TotalMinutes) minutes. Check agent progress."
            Write-Warning $message
            [console]::Beep(1000, 350)
            [console]::Beep(1000, 350)
            [console]::Beep(900, 500)

            if (-not $DisablePopup) {
                try {
                    Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop
                    [System.Windows.Forms.MessageBox]::Show(
                        $message,
                        "Rehla Cycle Watchdog",
                        [System.Windows.Forms.MessageBoxButtons]::OK,
                        [System.Windows.Forms.MessageBoxIcon]::Warning
                    ) | Out-Null
                } catch {
                    Write-Warning "Popup notification unavailable on this host. Audio + console alert only."
                }
            }
        }

        Start-Sleep -Seconds $IntervalSeconds
    }
}

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptRoot

Start-RehlaWakeWatchdog `
    -RepoRoot $repoRoot `
    -Files $WatchFiles `
    -IdleMinutes $MaxIdleMinutes `
    -IntervalSeconds $PollSeconds `
    -DisablePopup ([bool]$NoPopup)
