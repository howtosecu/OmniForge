#!/usr/bin/env python3
"""
Patch missing CoreGraphics/AppKit constants and properties
for macOS 15 SDK compatibility in Chromium (Skia and ui/display/mac).
"""
import os
import sys
import glob

SKIA_FALLBACK_CODE = """#ifndef kCGImageByteOrder32Host
#if defined(__BIG_ENDIAN__) && __BIG_ENDIAN__
#define kCGImageByteOrder32Host kCGImageByteOrder32Big
#else
#define kCGImageByteOrder32Host kCGImageByteOrder32Little
#endif
#endif
"""

NSSCREEN_CATEGORY = """
#if defined(__OBJC__)
@interface NSScreen (OmniForgeDisplayID)
@property(readonly) CGDirectDisplayID CGDirectDisplayID;
@end
@implementation NSScreen (OmniForgeDisplayID)
- (CGDirectDisplayID)CGDirectDisplayID {
  NSNumber* num = [[self deviceDescription] objectForKey:@"NSScreenNumber"];
  return num ? (CGDirectDisplayID)[num unsignedIntValue] : 0;
}
@end
#endif
"""

REPLACEMENT_TARGET = '(((NSNumber*)[[screen deviceDescription] objectForKey:@"NSScreenNumber"]).unsignedIntValue)'

def patch_skia(root: str) -> int:
    skia_ext = os.path.join(root, "skia", "ext")
    if not os.path.exists(skia_ext) and os.path.exists(os.path.join(root, "engine-src", "skia", "ext")):
        skia_ext = os.path.join(root, "engine-src", "skia", "ext")

    files_to_check = [os.path.join(skia_ext, "skia_utils_mac.mm")] + \
                     glob.glob(os.path.join(skia_ext, "*.mm")) + \
                     glob.glob(os.path.join(skia_ext, "*.h"))

    count = 0
    for p in files_to_check:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if "kCGImageByteOrder32Host" in content and "#define kCGImageByteOrder32Host" not in content:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(SKIA_FALLBACK_CODE + content)
                print(f"[+] Successfully patched {p} with kCGImageByteOrder32Host fallback.")
                count += 1
    return count

def patch_display(root: str) -> int:
    display_mac = os.path.join(root, "ui", "display", "mac")
    if not os.path.exists(display_mac) and os.path.exists(os.path.join(root, "engine-src", "ui", "display", "mac")):
        display_mac = os.path.join(root, "engine-src", "ui", "display", "mac")

    files_to_check = glob.glob(os.path.join(display_mac, "*.mm")) + \
                     glob.glob(os.path.join(display_mac, "*.h"))

    count = 0
    for p in files_to_check:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            modified = False
            if "screen.CGDirectDisplayID" in content:
                content = content.replace("screen.CGDirectDisplayID", REPLACEMENT_TARGET)
                modified = True
            if "[screen CGDirectDisplayID]" in content:
                content = content.replace("[screen CGDirectDisplayID]", REPLACEMENT_TARGET)
                modified = True
            if "CGDirectDisplayID" in content and "OmniForgeDisplayID" not in content:
                content = content + "\n" + NSSCREEN_CATEGORY
                modified = True
            if modified:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"[+] Successfully patched {p} with NSScreen CGDirectDisplayID compatibility.")
                count += 1
    return count

def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    skia_patched = patch_skia(root)
    display_patched = patch_display(root)
    print(f"[✔] macOS 15 SDK compatibility patch complete (Skia: {skia_patched}, Display: {display_patched}).")

if __name__ == "__main__":
    main()
