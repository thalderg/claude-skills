# Removes only the repo-guard hook and skill link (Windows).
# Run:  powershell -ExecutionPolicy Bypass -File .\uninstall.ps1
$H = $PSScriptRoot
$S = Join-Path $HOME '.claude\settings.json'
$Link = Join-Path $HOME '.claude\skills\repo-guard-sandbox'
if (Test-Path $Link) { (Get-Item $Link).Delete() }   # removes the junction only, not the skill files
$Py = (Get-Command python, py -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1).Source
if ((Test-Path $S) -and $Py) { & $Py (Join-Path $H 'settings_merge.py') remove $S }
Write-Host "repo-guard hook and skill removed (backup: $S.bak-repo-guard)."
