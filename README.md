# OmniForge: Autonomous Web Runtime & High-Performance Execution Platform

**OmniForge** is a next-generation sovereign web runtime engineered for autonomous agent execution, high-resilience web automation, and enterprise-grade cloud workloads.

Going far beyond traditional consumer browsers, OmniForge provides an isolated, telemetry-free, and high-fidelity rendering architecture designed from the ground up for modern AI agents, distributed automation pipelines, and mission-critical web infrastructure.

---

## ⚡ Quick 1-Line Installation

### Linux VPS & Cloud Workloads (Ubuntu, Debian, Fedora, Arch)
Run as `root` (or with `sudo`):
```bash
curl -sSL https://raw.githubusercontent.com/howtosecu/OmniForge/main/scripts/install.sh | sudo bash
```

### Windows Workstations & Server (Windows 10/11, Windows Server 2022)
Run inside Administrator PowerShell:
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -useb https://raw.githubusercontent.com/howtosecu/OmniForge/main/scripts/install.ps1 | iex"
```

---

## 🌐 Vision: Beyond the Traditional Web Browser

Traditional browsers are built for human consumer navigation, cluttered with proprietary telemetry, inconsistent background services, and fragile automation interfaces. 

**OmniForge redefines the web platform as an enterprise execution engine:**

- **Autonomous Agentic Infrastructure**: Built natively to interface with modern AI agent frameworks (Playwright, Puppeteer, CDP, custom agents) with maximum execution fidelity and zero friction.
- **Sovereign & Telemetry-Free Architecture**: Operates with zero third-party telemetry, no background tracking pings, and complete network autonomy.
- **Hardware-Consistent Execution**: Delivers reproducible rendering across headless servers, containerized Docker clusters, and bare-metal instances without environment distortion.
- **Ultra-Resilient Cloud Deployment**: Optimized resource footprint for high-density concurrency on cloud instances with minimal memory and CPU overhead.

---

## 📦 Supported Platforms & Release Binaries

OmniForge ships standalone, optimized runtime packages for major enterprise platforms:

| Operating System | Architecture | Package Format | Target Form Factors |
| :--- | :--- | :--- | :--- |
| **Linux** | AMD64 (x86_64) | `.tar.xz` & `.AppImage` | Cloud VPS, Kubernetes, Docker Containers |
| **Windows** | AMD64 (x86_64) | `.zip` (Portable) & `.exe` | Windows 10/11, Windows Server 2019/2022 |
| **macOS** | ARM64 | `.dmg` | Apple Silicon (M1/M2/M3/M4) Workstations |

Every official build is published with cryptographic `SHA256SUMS.txt` on the [Releases](https://github.com/howtosecu/OmniForge/releases) page to guarantee end-to-end payload integrity.

---

## 🚀 Quick Usage

Once installed, OmniForge can be invoked as a standalone runtime or integrated into automation pipelines:

### Standalone CLI Execution
```bash
# Launch OmniForge with clean profile isolation
omniforge --user-data-dir=/tmp/omniforge-session-01

# Headless server execution
omniforge --headless --remote-debugging-port=9222
```

### Automation Integration (Node.js / Python via CDP)
Connect any standard automation framework directly to the OmniForge runtime:
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    page = browser.new_page()
    page.goto("https://example.com")
    print(page.title())
```

---

## 🛡️ Security & Integrity

- **Deterministic Binaries**: Builds are compiled in an isolated, reproducible environment to prevent supply-chain tampering.
- **Offline Autonomy**: Fully operational in air-gapped networks and sovereign cloud VPCs without phone-home requirements.
- **Zero-Data Retention**: Default runtime options prevent persistent session bleeding across independent execution contexts.

---

## 📄 License

OmniForge is distributed under the Apache-2.0 and BSD-3-Clause licenses.
