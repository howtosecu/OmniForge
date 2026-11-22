#!/usr/bin/env bash
# OmniForge Automated 1-Line Installer for macOS (Apple Silicon ARM64)
# Official repository: https://github.com/howtosecu/OmniForge

set -euo pipefail

echo "=========================================================="
echo "    OmniForge Autonomous Web Runtime Installer (macOS)   "
echo "=========================================================="

OS="$(uname -s)"
if [ "$OS" != "Darwin" ]; then
    echo "[-] Error: This installer is intended for macOS (Darwin)."
    exit 1
fi

ARCH="$(uname -m)"
if [ "$ARCH" != "arm64" ]; then
    echo "[!] Warning: Detected architecture '$ARCH'. OmniForge is optimized for Apple Silicon (arm64)."
    if [ "$ARCH" = "x86_64" ]; then
        echo "[*] If running under Rosetta 2, please run natively using an arm64 terminal."
    fi
fi

EDITION="${EDITION:-phantom}"
INSTALL_DIR="/Applications/OmniForge"
BIN_LINK="/usr/local/bin/omniforge"

# If not running as root and /usr/local/bin isn't writable, use /opt/homebrew/bin
if [ ! -w "/usr/local/bin" ] && [ -d "/opt/homebrew/bin" ] && [ -w "/opt/homebrew/bin" ]; then
    BIN_LINK="/opt/homebrew/bin/omniforge"
fi

echo "[+] Target edition: $EDITION"
echo "[+] Querying latest release metadata from howtosecu/OmniForge..."
LATEST_RELEASE_JSON=$(curl -sSL "https://api.github.com/repos/howtosecu/OmniForge/releases/latest" || true)

DOWNLOAD_URL=$(echo "$LATEST_RELEASE_JSON" | grep -o "https://[^\"]*omniforge-${EDITION}-[^\"]*darwin-arm64\.tar\.xz" | head -n 1 || true)

if [ -z "$DOWNLOAD_URL" ]; then
    DOWNLOAD_URL=$(echo "$LATEST_RELEASE_JSON" | grep -o 'https://[^"]*omniforge-[^"]*darwin-arm64\.tar\.xz' | head -n 1 || true)
fi

if [ -z "$DOWNLOAD_URL" ]; then
    DOWNLOAD_URL=$(echo "$LATEST_RELEASE_JSON" | grep -o 'https://[^"]*darwin-arm64\.tar\.xz' | head -n 1 || true)
fi

if [ -z "$DOWNLOAD_URL" ]; then
    echo "[-] Notice: No official darwin-arm64 release binary found yet on GitHub Releases."
    echo "[!] Please verify release status on https://github.com/howtosecu/OmniForge/releases"
    exit 1
fi

TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

echo "[+] Downloading OmniForge package from $DOWNLOAD_URL..."
curl -fSL "$DOWNLOAD_URL" -o "$TMP_DIR/omniforge.tar.xz"

echo "[+] Installing to $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"
tar -xf "$TMP_DIR/omniforge.tar.xz" --strip-components=1 -C "$INSTALL_DIR"

echo "[+] Removing Gatekeeper quarantine attributes..."
xattr -cr "$INSTALL_DIR" 2>/dev/null || true

echo "[+] Applying ad-hoc codesign signature..."
if [ -d "$INSTALL_DIR/Chromium.app" ]; then
    codesign --force --deep -s - "$INSTALL_DIR/Chromium.app" 2>/dev/null || true
fi
if [ -f "$INSTALL_DIR/omniforge" ]; then
    codesign --force --deep -s - "$INSTALL_DIR/omniforge" 2>/dev/null || true
fi

# Set up CLI wrapper / symlink
TARGET_EXEC=""
if [ -f "$INSTALL_DIR/omniforge" ]; then
    chmod +x "$INSTALL_DIR/omniforge"
    TARGET_EXEC="$INSTALL_DIR/omniforge"
elif [ -d "$INSTALL_DIR/Chromium.app" ]; then
    TARGET_EXEC="$INSTALL_DIR/Chromium.app/Contents/MacOS/Chromium"
fi

if [ -n "$TARGET_EXEC" ]; then
    mkdir -p "$(dirname "$BIN_LINK")" 2>/dev/null || true
    if [ -w "$(dirname "$BIN_LINK")" ]; then
        ln -sf "$TARGET_EXEC" "$BIN_LINK"
        echo "[✔] CLI symlink created at $BIN_LINK"
    else
        echo "[*] To create a global CLI link, run:"
        echo "    sudo ln -sf \"$TARGET_EXEC\" \"$BIN_LINK\""
    fi
fi

echo "[✔] OmniForge successfully installed to $INSTALL_DIR"
echo "[*] Verify installation with: omniforge --version"
