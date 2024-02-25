# Productivity / Kinda Fun terminal scripts

To use create a new directory and name it something descriptive e.g "scripts", then need to add permissions to use the scripts by doing
chmod +x "file_name", will need to give permissions for all script running files.

## Bash Aliases

export PATH=$PATH:/home/umar.dabhoiwala/scripts
alias fetch="scripts/notes/fetch_notes.py"

alias type-test="/home/umar.dabhoiwala/scripts/type-test/typing_test.sh"
alias note="/home/umar.dabhoiwala/scripts/notes/note.py"


git_diff_commit() {
    local OUTPUT_FILE="diff_output.txt"  # Predefined output file name

    # Ensure we're in a Git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "This directory is not a git repository."
    return 1
    fi
    git diff --cached > "$OUTPUT_FILE
    commit_changes.py "$OUTPUT_FILE
    }

alias talk='talk.py'