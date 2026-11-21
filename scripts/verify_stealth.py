#!/usr/bin/env python3
"""
OmniForge Stealth & Anti-Bot Invariant Gate Verifier
Validates that the compiled binary does not leak headless/automation signatures.
"""
import subprocess
import json
import sys
import re
import os

HTML_PROBE = """<!DOCTYPE html><html><body><script>
document.write(JSON.stringify({
  webdriver: navigator.webdriver,
  hardwareConcurrency: navigator.hardwareConcurrency,
  has_headless_in_ua: /HeadlessChrome/i.test(navigator.userAgent),
  plugins_count: navigator.plugins.length,
  has_chrome: typeof window.chrome !== 'undefined'
}));
</script></body></html>"""

def main():
    binary = sys.argv[1] if len(sys.argv) > 1 else "./chrome"
    if not os.path.isfile(binary) and not os.path.islink(binary):
        print(f"[-] Error: Target binary '{binary}' does not exist.")
        sys.exit(1)

    probe_file = "/tmp/stealth_ci_probe.html"
    with open(probe_file, "w") as f:
        f.write(HTML_PROBE)

    cmd = [
        binary,
        "--no-sandbox",
        "--headless=new",
        "--disable-gpu",
        "--fingerprint-platform=win",
        "--fingerprint-hardware-concurrency=16",
        "--dump-dom",
        f"file://{probe_file}"
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    match = re.search(r'(\{.*\})', res.stdout)
    if not match:
        print("[-] Failed to find probe JSON in DOM output!")
        print(res.stdout[:500])
        sys.exit(1)

    data = json.loads(match.group(1))
    print("[+] Stealth Invariant Probe Results:")
    print(json.dumps(data, indent=2))

    # Hard Invariant Assertions
    assert data["webdriver"] is False, f"LEAK: navigator.webdriver is {data['webdriver']}!"
    assert data["hardwareConcurrency"] == 16, f"LEAK: hardwareConcurrency is {data['hardwareConcurrency']} (expected 16)!"
    assert data["has_headless_in_ua"] is False, "LEAK: HeadlessChrome leaked in User-Agent string!"
    assert data["plugins_count"] >= 3, f"LEAK: plugins.length is {data['plugins_count']} (expected >= 3)!"
    assert data["has_chrome"] is True, "LEAK: window.chrome object is missing!"

    print("[✔] All 5 Stealth Invariant Assertions PASSED with 0 Leaks!")

if __name__ == "__main__":
    main()
