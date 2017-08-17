# ===
# PowerShell Profile Prompt Settings
# Sam Whang | WGB
# ---
# https://stackoverflow.com/questions/1287718/how-can-i-display-my-current-git-\
# branch-name-in-my-powershell-prompt
# ---
# https://superuser.com/questions/446827/configure-the-windows-powershell-to-\
# display-only-the-current-folder-name-in-the
# ===

function Write-BranchName() {
    try {
        $branch=git rev-parse --abbrev-ref HEAD
        if ($branch -eq "HEAD") {
            # we're probably in detached HEAD state, so print the SHA
            $branch = git rev-parse --short HEAD
            Write-Host " ($branch)" -ForegroundColor "magenta"
        }
        else {
            # we're on an actual branch, so print it
            Write-Host " ($branch)" -ForegroundColor "darkblue"
        }
    } catch {
        # we'll end up here if we're in a newly initiated git repo
        Write-Host " (no branches yet)" -ForegroundColor "yellow"
    }
}

function prompt {
    #$base = "PS "
    $path = "$($executionContext.SessionState.Path.CurrentLocation)"
    #$path = Split-Path -leaf -path (Get-Location)
    $userPrompt = "$('> $' * ($nestedPromptLevel + 1)) "

    #Write-Host "`n$base" -NoNewline

    if (Test-Path .git) {
        Write-Host $path -NoNewline -ForegroundColor "darkcyan"
        Write-BranchName
    }
    else {
        # we're not in a repo so don't bother displaying branch name/sha
        Write-Host $path -ForegroundColor "darkcyan"
    }

    return $userPrompt
} 
