#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
# Termux Ultimate Toolkit v4.2 - Installer
# ============================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

clear

echo -e "${BLUE}"
cat << "EOF"
╔══════════════════════════════════════════════╗
║     🔥 TERMUX ULTIMATE TOOLKIT v4.2 🔥       ║
║         Installing... Please wait            ║
╚══════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Step 1: Update packages
echo -e "${GREEN}[*] Updating packages...${NC}"
pkg update -y

# Step 2: Install dependencies
echo -e "${GREEN}[*] Installing dependencies...${NC}"
pkg install python termux-api -y

# Step 3: Install Python modules
echo -e "${GREEN}[*] Installing Python modules...${NC}"
pip install requests --quiet

# Step 4: Create local bin
echo -e "${GREEN}[*] Creating shortcut...${NC}"
mkdir -p $PREFIX/bin

# Step 5: Copy main script
echo -e "${GREEN}[*] Installing toolkit...${NC}"
cp toolkit.py $PREFIX/bin/toolkit
chmod +x $PREFIX/bin/toolkit

# Step 6: Clean history
echo -e "${GREEN}[*] Cleaning up...${NC}"
rm -rf ~/.bash_history 2>/dev/null
history -c 2>/dev/null

# Step 7: Done
echo -e "${GREEN}"
cat << "EOF"
╔══════════════════════════════════════════════╗
║  ✅ INSTALLATION COMPLETE!                   ║
║                                              ║
║  🎯 Type 'toolkit' to start                  ║
║  📁 Run 'termux-setup-storage' first         ║
║                                              ║
║  ⚠️  Accept storage permission!              ║
╚══════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Optional: ask to run storage setup
echo -e "${YELLOW}[?] Do you want to run termux-setup-storage now? (y/n)${NC}"
read -r answer
if [[ "$answer" == "y" || "$answer" == "Y" ]]; then
    termux-setup-storage
    echo -e "${GREEN}[✅] Storage permission granted!${NC}"
else
    echo -e "${YELLOW}[⚠️] Remember to run 'termux-setup-storage' manually later!${NC}"
fi

echo -e "\n${GREEN}Installation finished${NC}"
