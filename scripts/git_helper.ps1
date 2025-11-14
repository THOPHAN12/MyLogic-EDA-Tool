# Git Helper Script for MyLogic Team Collaboration (PowerShell)
# Usage: .\scripts\git_helper.ps1 <command> [args]

param(
    [Parameter(Position=0)]
    [string]$Command,
    
    [Parameter(Position=1)]
    [string]$Arg1
)

# Colors
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Show help
function Show-Help {
    Write-Host "Git Helper Script for MyLogic Team" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\scripts\git_helper.ps1 <command> [args]"
    Write-Host ""
    Write-Host "Commands:"
    Write-Host "  setup              - Setup branches (develop, feature branches)"
    Write-Host "  new-feature <name> - Create new feature branch (use tho- or minh- prefix)"
    Write-Host "  sync               - Sync current branch with develop"
    Write-Host "  status             - Show branch status"
    Write-Host "  push-feature       - Push current feature branch"
    Write-Host "  merge-feature <branch> - Merge feature branch into develop"
    Write-Host "  list-branches      - List all branches"
    Write-Host ""
}

# Setup branches
function Setup-Branches {
    Write-Info "Setting up branches..."
    
    # Create develop if not exists
    $developExists = git show-ref --verify --quiet refs/heads/develop 2>$null
    if (-not $developExists) {
        git checkout -b develop
        Write-Success "Created develop branch"
    } else {
        git checkout develop
        Write-Info "Switched to develop branch"
    }
    
    # Pull latest
    git pull origin develop 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "develop not on remote yet"
    }
    
    Write-Success "Branches setup complete!"
    $currentBranch = git branch --show-current
    Write-Info "Current branch: $currentBranch"
}

# Create new feature branch
function New-Feature {
    param([string]$FeatureName)
    
    if ([string]::IsNullOrEmpty($FeatureName)) {
        Write-Error "Feature name required!"
        Write-Host "Usage: .\scripts\git_helper.ps1 new-feature <name>"
        Write-Host "Example: .\scripts\git_helper.ps1 new-feature tho-library-loader"
        exit 1
    }
    
    # Check if branch name has prefix
    if ($FeatureName -notmatch "^(tho|minh)-") {
        Write-Warning "Feature name should start with 'tho-' or 'minh-'"
        $response = Read-Host "Continue anyway? (y/n)"
        if ($response -ne "y" -and $response -ne "Y") {
            exit 1
        }
    }
    
    $branchName = "feature/$FeatureName"
    
    # Switch to develop and update
    git checkout develop
    git pull origin develop 2>$null
    
    # Create feature branch
    $branchExists = git show-ref --verify --quiet refs/heads/$branchName 2>$null
    if ($branchExists) {
        Write-Warning "Branch $branchName already exists"
        git checkout $branchName
    } else {
        git checkout -b $branchName
        Write-Success "Created and switched to $branchName"
    }
}

# Sync with develop
function Sync-WithDevelop {
    $currentBranch = git branch --show-current
    
    if ($currentBranch -eq "develop" -or $currentBranch -eq "main") {
        Write-Info "Updating $currentBranch from remote..."
        git pull origin $currentBranch
        Write-Success "Updated $currentBranch"
        return
    }
    
    Write-Info "Syncing $currentBranch with develop..."
    
    # Check for uncommitted changes
    $hasChanges = git diff-index --quiet HEAD -- 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "You have uncommitted changes!"
        $response = Read-Host "Stash changes? (y/n)"
        if ($response -eq "y" -or $response -eq "Y") {
            git stash
            Write-Info "Changes stashed"
        } else {
            Write-Error "Cannot sync with uncommitted changes"
            exit 1
        }
    }
    
    # Update develop
    git checkout develop
    git pull origin develop 2>$null
    
    # Merge develop into feature branch
    git checkout $currentBranch
    git merge develop
    
    # Restore stashed changes
    $stashList = git stash list
    if ($stashList) {
        git stash pop
        Write-Info "Restored stashed changes"
    }
    
    Write-Success "Synced $currentBranch with develop"
}

# Show status
function Show-Status {
    $currentBranch = git branch --show-current
    
    Write-Host ""
    Write-Info "=== Git Status ==="
    Write-Host "Current branch: $currentBranch"
    Write-Host ""
    
    # Show uncommitted changes
    $hasChanges = git diff-index --quiet HEAD -- 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "You have uncommitted changes:"
        git status --short
    } else {
        Write-Success "Working tree clean"
    }
    
    Write-Host ""
    
    # Show commits ahead/behind
    $upstream = git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>$null
    if ($upstream) {
        $ahead = git rev-list --count "$upstream..HEAD" 2>$null
        $behind = git rev-list --count "HEAD..$upstream" 2>$null
        
        if ($ahead -gt 0) {
            Write-Info "Ahead of remote: $ahead commits"
        }
        if ($behind -gt 0) {
            Write-Warning "Behind remote: $behind commits"
        }
        if ($ahead -eq 0 -and $behind -eq 0) {
            Write-Success "Up to date with remote"
        }
    }
    
    Write-Host ""
}

# Push feature branch
function Push-Feature {
    $currentBranch = git branch --show-current
    
    if ($currentBranch -notmatch "^feature/") {
        Write-Error "Not on a feature branch!"
        exit 1
    }
    
    Write-Info "Pushing $currentBranch to remote..."
    git push -u origin $currentBranch
    Write-Success "Pushed $currentBranch"
}

# Merge feature branch
function Merge-Feature {
    param([string]$BranchName)
    
    if ([string]::IsNullOrEmpty($BranchName)) {
        Write-Error "Branch name required!"
        Write-Host "Usage: .\scripts\git_helper.ps1 merge-feature <branch>"
        Write-Host "Example: .\scripts\git_helper.ps1 merge-feature feature/tho-library-loader"
        exit 1
    }
    
    # Check if branch exists
    $branchExists = git show-ref --verify --quiet refs/heads/$BranchName 2>$null
    if (-not $branchExists) {
        Write-Error "Branch $BranchName does not exist!"
        exit 1
    }
    
    Write-Info "Merging $BranchName into develop..."
    
    # Switch to develop
    git checkout develop
    git pull origin develop 2>$null
    
    # Merge
    git merge $BranchName --no-ff -m "Merge $BranchName into develop"
    
    Write-Success "Merged $BranchName into develop"
    Write-Info "You can now push: git push origin develop"
}

# List branches
function List-Branches {
    Write-Host ""
    Write-Info "=== Local Branches ==="
    git branch
    
    Write-Host ""
    Write-Info "=== Remote Branches ==="
    git branch -r
    
    Write-Host ""
    Write-Info "=== Current Branch ==="
    git branch --show-current
    Write-Host ""
}

# Main
switch ($Command) {
    "setup" {
        Setup-Branches
    }
    "new-feature" {
        New-Feature $Arg1
    }
    "sync" {
        Sync-WithDevelop
    }
    "status" {
        Show-Status
    }
    "push-feature" {
        Push-Feature
    }
    "merge-feature" {
        Merge-Feature $Arg1
    }
    "list-branches" {
        List-Branches
    }
    { $_ -in "help", "--help", "-h", "" } {
        Show-Help
    }
    default {
        Write-Error "Unknown command: $Command"
        Show-Help
        exit 1
    }
}

