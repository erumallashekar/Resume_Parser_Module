<#
PowerShell helper to stage only the relevant project files for this Django project.
Run from the repository root (where `manage.py` lives):
  .\stage_project.ps1
#>

$paths = @(
    'Resume_Parser_App/',
    'Resume_Parser/',
    'manage.py',
    'sample_resume.txt'
)

Write-Host "Staging selected paths:`n" -ForegroundColor Cyan
foreach ($p in $paths) {
    if (Test-Path $p) {
        Write-Host "Adding $p"
        git add -- "$p"
    } else {
        Write-Host "Skipped (not found): $p" -ForegroundColor Yellow
    }
}

Write-Host "\nStaged files:" -ForegroundColor Cyan
git status --short
