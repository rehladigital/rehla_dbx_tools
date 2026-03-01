# Windows Wake Watchdog

Use this watchdog to alert when cycle files stop changing for too long.

## Script

- `tools/windows_wakeup_watchdog.ps1`

## Default behavior

- Watches:
  - `docs/CYCLE_LOG.md`
  - `docs/PROCESS_DASHBOARD.md`
  - `docs/LOOP_CONTEXT.md`
- Polls every 30 seconds
- Alerts after 10 minutes of no file changes
- Triggers:
  - console warning
  - beep sequence
  - Windows popup (unless disabled)

## Run

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\windows_wakeup_watchdog.ps1
```

## Custom threshold

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\windows_wakeup_watchdog.ps1 -MaxIdleMinutes 5 -PollSeconds 15
```

## Disable popup (beep + console only)

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\windows_wakeup_watchdog.ps1 -NoPopup
```

## Watch custom files

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\windows_wakeup_watchdog.ps1 -WatchFiles @("docs/CYCLE_LOG.md","pyproject.toml")
```
