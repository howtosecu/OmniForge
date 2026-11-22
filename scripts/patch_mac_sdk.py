#!/usr/bin/env python3
"""
Patch missing CoreGraphics constants (such as kCGImageByteOrder32Host)
for macOS 15 SDK compatibility in Chromium Skia.
"""
import os
import sys
import glob

FALLBACK_CODE = """#ifndef kCGImageByteOrder32Host
#if defined(__BIG_ENDIAN__) && __BIG_ENDIAN__
#define kCGImageByteOrder32Host kCGImageByteOrder32Big
#else
#define kCGImageByteOrder32Host kCGImageByteOrder32Little
#endif
#endif
"""

def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    skia_ext = os.path.join(root, "skia", "ext")
    if not os.path.exists(skia_ext):
        # Maybe we are in engine-src or repo root
        if os.path.exists(os.path.join(root, "engine-src", "skia", "ext")):
            skia_ext = os.path.join(root, "engine-src", "skia", "ext")

    files_to_check = [os.path.join(skia_ext, "skia_utils_mac.mm")] + \
                     glob.glob(os.path.join(skia_ext, "*.mm")) + \
                     glob.glob(os.path.join(skia_ext, "*.h"))

    patched_count = 0
    for p in files_to_check:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if "kCGImageByteOrder32Host" in content and "#define kCGImageByteOrder32Host" not in content:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(FALLBACK_CODE + content)
                print(f"[+] Successfully patched {p} with kCGImageByteOrder32Host fallback.")
                patched_count += 1

    print(f"[✔] Skia macOS 15 SDK patch check completed ({patched_count} files patched).")

if __name__ == "__main__":
    main()
