# Script to check branch structure and permissions
# Usage: .\scripts\check_branches.ps1

Write-Host "=== BRANCH STRUCTURE CHECK ===" -ForegroundColor Cyan
Write-Host ""

# Check current branch
$currentBranch = git branch --show-current
Write-Host "Current branch: $currentBranch" -ForegroundColor Yellow
Write-Host ""

# List all local branches
Write-Host "=== LOCAL BRANCHES ===" -ForegroundColor Green
git branch

Write-Host ""
Write-Host "=== REMOTE BRANCHES ===" -ForegroundColor Green
git branch -r

Write-Host ""
Write-Host "=== ALL BRANCHES ===" -ForegroundColor Green
git branch -a

Write-Host ""
Write-Host "=== BRANCH STATUS ===" -ForegroundColor Cyan

# Check if develop exists
$developExists = git show-ref --verify --quiet refs/heads/develop 2>$null
if ($developExists) {
    Write-Host "[OK] develop branch exists locally" -ForegroundColor Green
} else {
    Write-Host "[MISSING] develop branch not found locally" -ForegroundColor Red
}

# Check if main exists
$mainExists = git show-ref --verify --quiet refs/heads/main 2>$null
if ($mainExists) {
    Write-Host "[OK] main branch exists locally" -ForegroundColor Green
} else {
    Write-Host "[MISSING] main branch not found locally" -ForegroundColor Red
}

# Check remote branches
Write-Host ""
Write-Host "=== REMOTE BRANCH STATUS ===" -ForegroundColor Cyan

$remoteBranches = git branch -r
$expectedBranches = @(
    "origin/main",
    "origin/develop",
    "origin/feature/tho-library-loader",
    "origin/feature/tho-technology-mapping",
    "origin/feature/tho-synthesis-algorithms",
    "origin/feature/minh-cli-improvements",
    "origin/feature/minh-testing",
    "origin/feature/minh-documentation"
)

foreach ($expected in $expectedBranches) {
    if ($remoteBranches -match $expected) {
        Write-Host "[OK] $expected exists on remote" -ForegroundColor Green
    } else {
        Write-Host "[MISSING] $expected not found on remote" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "=== BRANCH TRACKING ===" -ForegroundColor Cyan

# Check tracking for current branch
$tracking = git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>$null
if ($tracking) {
    Write-Host "Current branch tracks: $tracking" -ForegroundColor Green
} else {
    Write-Host "Current branch has no upstream tracking" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== RECOMMENDED BRANCHES ===" -ForegroundColor Cyan
Write-Host "Main branches:"
Write-Host "  - main (production)"
Write-Host "  - develop (development)"
Write-Host ""
Write-Host "Thọ's branches:"
Write-Host "  - feature/tho-library-loader"
Write-Host "  - feature/tho-technology-mapping"
Write-Host "  - feature/tho-synthesis-algorithms"
Write-Host ""
Write-Host "Minh's branches:"
Write-Host "  - feature/minh-cli-improvements"
Write-Host "  - feature/minh-testing"
Write-Host "  - feature/minh-documentation"

Write-Host ""
Write-Host "=== CHECK COMPLETE ===" -ForegroundColor Cyan

