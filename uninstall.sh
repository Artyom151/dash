#!/bin/bash

# Dash Uninstaller

set -e

echo "🗑️  Uninstalling Dash..."

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Remove script
if [ -f ~/.config/hypr/scripts/dash.py ]; then
    rm ~/.config/hypr/scripts/dash.py
    echo -e "${GREEN}✓ Removed dash.py${NC}"
fi

# Remove keybind
KEYBIND_FILE="$HOME/.config/hypr/custom/keybinds.conf"
if [ -f "$KEYBIND_FILE" ]; then
    sed -i '/# Dash - App Launcher/d' "$KEYBIND_FILE"
    sed -i '/dash.py/d' "$KEYBIND_FILE"
    echo -e "${GREEN}✓ Removed keybind${NC}"
fi

# Reload Hyprland
if command -v hyprctl &> /dev/null; then
    hyprctl reload
    echo -e "${GREEN}✓ Hyprland reloaded${NC}"
fi

echo -e "\n${GREEN}Dash uninstalled successfully!${NC}"
