#!/bin/bash
# Git Helper Script for MyLogic Team Collaboration
# Usage: ./scripts/git_helper.sh <command> [args]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored message
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Show help
show_help() {
    echo "Git Helper Script for MyLogic Team"
    echo ""
    echo "Usage: ./scripts/git_helper.sh <command> [args]"
    echo ""
    echo "Commands:"
    echo "  setup              - Setup branches (develop, feature branches)"
    echo "  new-feature <name> - Create new feature branch (use tho- or minh- prefix)"
    echo "  sync               - Sync current branch with develop"
    echo "  status             - Show branch status"
    echo "  push-feature       - Push current feature branch"
    echo "  merge-feature <branch> - Merge feature branch into develop"
    echo "  list-branches      - List all branches"
    echo ""
}

# Setup branches
setup_branches() {
    print_info "Setting up branches..."
    
    # Create develop if not exists
    if ! git show-ref --verify --quiet refs/heads/develop; then
        git checkout -b develop
        print_success "Created develop branch"
    else
        git checkout develop
        print_info "Switched to develop branch"
    fi
    
    # Pull latest
    git pull origin develop 2>/dev/null || print_warning "develop not on remote yet"
    
    print_success "Branches setup complete!"
    print_info "Current branch: $(git branch --show-current)"
}

# Create new feature branch
new_feature() {
    local feature_name=$1
    
    if [ -z "$feature_name" ]; then
        print_error "Feature name required!"
        echo "Usage: ./scripts/git_helper.sh new-feature <name>"
        echo "Example: ./scripts/git_helper.sh new-feature tho-library-loader"
        exit 1
    fi
    
    # Check if branch name has prefix
    if [[ ! "$feature_name" =~ ^(tho|minh)- ]]; then
        print_warning "Feature name should start with 'tho-' or 'minh-'"
        read -p "Continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    local branch_name="feature/$feature_name"
    
    # Switch to develop and update
    git checkout develop
    git pull origin develop 2>/dev/null || true
    
    # Create feature branch
    if git show-ref --verify --quiet refs/heads/$branch_name; then
        print_warning "Branch $branch_name already exists"
        git checkout $branch_name
    else
        git checkout -b $branch_name
        print_success "Created and switched to $branch_name"
    fi
}

# Sync with develop
sync_with_develop() {
    local current_branch=$(git branch --show-current)
    
    if [ "$current_branch" = "develop" ] || [ "$current_branch" = "main" ]; then
        print_info "Updating $current_branch from remote..."
        git pull origin $current_branch
        print_success "Updated $current_branch"
        return
    fi
    
    print_info "Syncing $current_branch with develop..."
    
    # Save current changes
    if ! git diff-index --quiet HEAD --; then
        print_warning "You have uncommitted changes!"
        read -p "Stash changes? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git stash
            print_info "Changes stashed"
        else
            print_error "Cannot sync with uncommitted changes"
            exit 1
        fi
    fi
    
    # Update develop
    git checkout develop
    git pull origin develop 2>/dev/null || true
    
    # Merge develop into feature branch
    git checkout $current_branch
    git merge develop
    
    # Restore stashed changes
    if git stash list | grep -q .; then
        git stash pop
        print_info "Restored stashed changes"
    fi
    
    print_success "Synced $current_branch with develop"
}

# Show status
show_status() {
    local current_branch=$(git branch --show-current)
    
    echo ""
    print_info "=== Git Status ==="
    echo "Current branch: $current_branch"
    echo ""
    
    # Show uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        print_warning "You have uncommitted changes:"
        git status --short
    else
        print_success "Working tree clean"
    fi
    
    echo ""
    
    # Show commits ahead/behind
    if git rev-parse --abbrev-ref --symbolic-full-name @{u} &>/dev/null; then
        local ahead=$(git rev-list --count @{u}..HEAD 2>/dev/null || echo "0")
        local behind=$(git rev-list --count HEAD..@{u} 2>/dev/null || echo "0")
        
        if [ "$ahead" -gt 0 ]; then
            print_info "Ahead of remote: $ahead commits"
        fi
        if [ "$behind" -gt 0 ]; then
            print_warning "Behind remote: $behind commits"
        fi
        if [ "$ahead" -eq 0 ] && [ "$behind" -eq 0 ]; then
            print_success "Up to date with remote"
        fi
    fi
    
    echo ""
}

# Push feature branch
push_feature() {
    local current_branch=$(git branch --show-current)
    
    if [[ ! "$current_branch" =~ ^feature/ ]]; then
        print_error "Not on a feature branch!"
        exit 1
    fi
    
    print_info "Pushing $current_branch to remote..."
    git push -u origin $current_branch
    print_success "Pushed $current_branch"
}

# Merge feature branch
merge_feature() {
    local branch_name=$1
    
    if [ -z "$branch_name" ]; then
        print_error "Branch name required!"
        echo "Usage: ./scripts/git_helper.sh merge-feature <branch>"
        echo "Example: ./scripts/git_helper.sh merge-feature feature/tho-library-loader"
        exit 1
    fi
    
    # Check if branch exists
    if ! git show-ref --verify --quiet refs/heads/$branch_name; then
        print_error "Branch $branch_name does not exist!"
        exit 1
    fi
    
    print_info "Merging $branch_name into develop..."
    
    # Switch to develop
    git checkout develop
    git pull origin develop 2>/dev/null || true
    
    # Merge
    git merge $branch_name --no-ff -m "Merge $branch_name into develop"
    
    print_success "Merged $branch_name into develop"
    print_info "You can now push: git push origin develop"
}

# List branches
list_branches() {
    echo ""
    print_info "=== Local Branches ==="
    git branch
    
    echo ""
    print_info "=== Remote Branches ==="
    git branch -r
    
    echo ""
    print_info "=== Current Branch ==="
    echo "$(git branch --show-current)"
    echo ""
}

# Main
case "$1" in
    setup)
        setup_branches
        ;;
    new-feature)
        new_feature "$2"
        ;;
    sync)
        sync_with_develop
        ;;
    status)
        show_status
        ;;
    push-feature)
        push_feature
        ;;
    merge-feature)
        merge_feature "$2"
        ;;
    list-branches)
        list_branches
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac

