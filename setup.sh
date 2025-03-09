#!/usr/bin/env sh

# Detect the shell
SHELL_NAME=$(basename "$SHELL")

echo "Detected shell: $SHELL_NAME"

# Add PYTHONPATH to shell profile (works for Bash, Zsh, and Fish)
PYTHONPATH_LINE='export PYTHONPATH="/home/kali/Desktop/PenTek/pentek:$PYTHONPATH"'

# Function to add to profile if not already present
add_to_profile() {
    PROFILE_FILE=$1
    if [ -f "$PROFILE_FILE" ]; then
        if ! grep -qxF "$PYTHONPATH_LINE" "$PROFILE_FILE"; then
            echo "$PYTHONPATH_LINE" >> "$PROFILE_FILE"
            echo "Added PYTHONPATH to $PROFILE_FILE"
        else
            echo "PYTHONPATH already set in $PROFILE_FILE"
        fi
    fi
}

# Update environment for current shell
case "$SHELL_NAME" in
    bash)
        add_to_profile "$HOME/.bashrc"
        ;;
    zsh)
        add_to_profile "$HOME/.zshrc"
        ;;
    fish)
        add_to_profile "$HOME/.config/fish/config.fish"
        ;;
    *)
        echo "Unsupported shell: $SHELL_NAME"
        ;;
esac

# Reload the shell profile to apply changes immediately
case "$SHELL_NAME" in
    bash)
        source "$HOME/.bashrc"
        ;;
    zsh)
        source "$HOME/.zshrc"
        ;;
    fish)
        source "$HOME/.config/fish/config.fish"
        ;;
esac

echo "Setup complete! Restart your terminal or run 'exec $SHELL_NAME' to apply changes."
