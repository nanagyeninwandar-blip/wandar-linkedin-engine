# Wandar LinkedIn Pipeline — Weekly Auto-Run
# Triggered every Sunday at 08:00 by Windows Task Scheduler.

$projectDir = "f:\WANDAR\GTM Engine\Chief LinkedIn Strategist_Writer"
$claudeExe = "C:\Users\Fii\.local\bin\claude.exe"
$logFile = Join-Path $projectDir "pipeline-run.log"

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content $logFile "[$timestamp] Pipeline started"

Set-Location $projectDir

& $claudeExe -p "run pipeline" --dangerously-skip-permissions 2>&1 | Tee-Object -Append -FilePath $logFile

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content $logFile "[$timestamp] Pipeline finished"
