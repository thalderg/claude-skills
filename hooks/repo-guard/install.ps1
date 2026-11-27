# Installs the repo-guard hook and skill for Claude Code (user level) on Windows. No administrator rights needed.
# Needs repo-guard first (install.ps1 in the repo-guard folder).
# Run:  powershell -ExecutionPolicy Bypass -File .\install.ps1
$ErrorActionPreference = 'Stop'
$H = $PSScriptRoot
$S = Join-Path $HOME '.claude\settings.json'
if (-not (Get-Command repo-guard.cmd -ErrorAction SilentlyContinue) -and -not (Test-Path (Join-Path $HOME 'bin\repo-guard.cmd'))) {
    throw 'Install repo-guard first (install.ps1 in the repo-guard folder).'
}
$Py = $null
foreach ($c in 'python', 'py', 'python3') {
    $cmd = Get-Command $c -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $cmd) { continue }
    try { $p = & $cmd.Source -c "import sys; print(sys.executable)" 2>$null; if ($LASTEXITCODE -eq 0 -and $p) { $Py = $p.Trim(); break } } catch { }
}
if (-not $Py) { throw 'Python 3 is needed (see the repo-guard install).' }

# skill: a directory junction (works without administrator rights, unlike a symbolic link)
$Skills = Join-Path $HOME '.claude\skills'
New-Item -ItemType Directory -Force -Path $Skills | Out-Null
$Link = Join-Path $Skills 'repo-guard-sandbox'
if (Test-Path $Link) { (Get-Item $Link).Delete() }
New-Item -ItemType Junction -Path $Link -Target (Join-Path $H 'skill\repo-guard-sandbox') | Out-Null

# hook: python plus the script, both with forward slashes (works in cmd and in the Git Bash that Claude Code uses)
$Cmd = '"' + ($Py -replace '\\', '/') + '" "' + ((Join-Path $H 'claude-code\pretooluse.py') -replace '\\', '/') + '"'
& $Py (Join-Path $H 'settings_merge.py') add $S $Cmd
if ($LASTEXITCODE -ne 0) { throw "Could not update $S (it is unchanged; a backup is in $S.bak-repo-guard)." }
Write-Host "Hook added to $S (backup: $S.bak-repo-guard). Skill linked: $Link. Start a new Claude Code session."
