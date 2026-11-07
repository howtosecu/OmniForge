#!/usr/bin/env bash
# OmniForge Automated 1-Line Installer for Linux
# Official repository: https://github.com/howtosecu/OmniForge

set -euo pipefail

echo "=========================================================="
echo "      OmniForge Autonomous Web Runtime Installer          "
echo "=========================================================="

ARCH=$(uname -m)
if [ "$ARCH" != "x86_64" ]; then
    echo "[-] Error: Currently only x86_64 architecture is supported."
    exit 1
fi

INSTALL_DIR="/opt/omniforge"
BIN_LINK="/usr/local/bin/omniforge"

echo "[+] Querying latest release metadata from howtosecu/OmniForge..."
LATEST_RELEASE_JSON=$(curl -sSL "https://api.github.com/repos/howtosecu/OmniForge/releases/latest" || true)

DOWNLOAD_URL=$(echo "$LATEST_RELEASE_JSON" | grep -o 'https://[^"]*omniforge-[^"]*linux-x86_64\.tar\.xz' | head -n 1 || true)

if [ -z "$DOWNLOAD_URL" ]; then
    # Fallback to any linux tar.xz asset
    DOWNLOAD_URL=$(echo "$LATEST_RELEASE_JSON" | grep -o 'https://[^"]*linux-x86_64\.tar\.xz' | head -n 1 || true)
fi

if [ -z "$DOWNLOAD_URL" ]; then
    echo "[-] Notice: No official binary release found yet on GitHub Releases."
    echo "[!] Please trigger an automated build release first on GitHub Actions."
    exit 1
fi

TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

echo "[+] Downloading OmniForge package from $DOWNLOAD_URL..."
curl -fSL "$DOWNLOAD_URL" -o "$TMP_DIR/omniforge.tar.xz"

echo "[+] Installing to $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"
tar -xf "$TMP_DIR/omniforge.tar.xz" --strip-components=1 -C "$INSTALL_DIR"

if [ -f "$INSTALL_DIR/omniforge" ]; then
    chmod +x "$INSTALL_DIR/omniforge"
    ln -sf "$INSTALL_DIR/omniforge" "$BIN_LINK"
elif [ -f "$INSTALL_DIR/chrome" ]; then
    mv "$INSTALL_DIR/chrome" "$INSTALL_DIR/omniforge"
    chmod +x "$INSTALL_DIR/omniforge"
    ln -sf "$INSTALL_DIR/omniforge" "$BIN_LINK"
fi

echo "[✔] OmniForge successfully installed to $INSTALL_DIR"
echo "[*] Verify installation with: omniforge --version"
