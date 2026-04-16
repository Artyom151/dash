#!/bin/bash

# Dash Installer
# Material Design 3 App Launcher for Hyprland

set -e

echo "🚀 Installing Dash..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Check dependencies
echo -e "${BLUE}Checking dependencies...${NC}"

check_dep() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}✗ $1 not found${NC}"
        return 1
    else
        echo -e "${GREEN}✓ $1${NC}"
        return 0
    fi
}

MISSING_DEPS=0

check_dep python3 || MISSING_DEPS=1
check_dep hyprctl || MISSING_DEPS=1

# Check Python GTK
if python3 -c "import gi; gi.require_version('Gtk', '3.0')" 2>/dev/null; then
    echo -e "${GREEN}✓ GTK3${NC}"
else
    echo -e "${RED}✗ GTK3 (python-gobject)${NC}"
    MISSING_DEPS=1
fi

# Check gtk-layer-shell
if python3 -c "import gi; gi.require_version('GtkLayerShell', '0.1')" 2>/dev/null; then
    echo -e "${GREEN}✓ gtk-layer-shell${NC}"
else
    echo -e "${RED}✗ gtk-layer-shell${NC}"
    MISSING_DEPS=1
fi

if [ $MISSING_DEPS -eq 1 ]; then
    echo -e "\n${RED}Missing dependencies. Install with:${NC}"
    echo "sudo pacman -S python-gobject gtk3 gtk-layer-shell"
    exit 1
fi

# Create directories
echo -e "\n${BLUE}Creating directories...${NC}"
mkdir -p ~/.config/hypr/scripts
mkdir -p ~/.config/hypr/custom

# Copy main script
echo -e "${BLUE}Installing Dash...${NC}"
cp main.py ~/.config/hypr/scripts/dash.py
chmod +x ~/.config/hypr/scripts/dash.py
echo -e "${GREEN}✓ Installed to ~/.config/hypr/scripts/dash.py${NC}"

# Add keybind
KEYBIND_FILE="$HOME/.config/hypr/custom/keybinds.conf"
KEYBIND_LINE="bind = SUPER, D, exec, python ~/.config/hypr/scripts/dash.py"

if [ -f "$KEYBIND_FILE" ]; then
    if grep -q "dash.py" "$KEYBIND_FILE"; then
        echo -e "${BLUE}Keybind already exists${NC}"
    else
        echo "" >> "$KEYBIND_FILE"
        echo "# Dash - App Launcher" >> "$KEYBIND_FILE"
        echo "$KEYBIND_LINE" >> "$KEYBIND_FILE"
        echo -e "${GREEN}✓ Added keybind to $KEYBIND_FILE${NC}"
    fi
else
    echo "# Dash - App Launcher" > "$KEYBIND_FILE"
    echo "$KEYBIND_LINE" >> "$KEYBIND_FILE"
    echo -e "${GREEN}✓ Created $KEYBIND_FILE${NC}"
fi

# Reload Hyprland
echo -e "\n${BLUE}Reloading Hyprland...${NC}"
hyprctl reload
echo -e "${GREEN}✓ Hyprland reloaded${NC}"

echo -e "\n${GREEN}✨ Dash installed successfully!${NC}"
echo -e "\nPress ${BLUE}Super+D${NC} to launch Dash"
echo -e "Run ${BLUE}python ~/.config/hypr/scripts/dash.py${NC} to test manually"
