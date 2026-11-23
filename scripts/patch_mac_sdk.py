#!/usr/bin/env python3
"""
Patch missing CoreGraphics/AppKit constants and properties
for macOS 15 SDK compatibility in Chromium (Skia, Blink, ui/display/mac).
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

def patch_kcg_byte_order(root: str) -> int:
    candidate_subdirs = [
        "skia",
        os.path.join("third_party", "blink"),
        "ui",
        "content",
        "base",
        "media",
        "chrome",
        "components",
    ]
    count = 0
    valid_exts = ('.mm', '.m', '.cc', '.cpp', '.h')

    for sub in candidate_subdirs:
        for search_base in [os.path.join(root, sub), os.path.join(root, "engine-src", sub)]:
            if not os.path.exists(search_base):
                continue
            for dirpath, _, filenames in os.walk(search_base):
                for f in filenames:
                    if f.endswith(valid_exts):
                        p = os.path.join(dirpath, f)
                        try:
                            with open(p, "r", encoding="utf-8", errors="ignore") as fp:
                                content = fp.read()
                            if "kCGImageByteOrder32Host" in content and "#define kCGImageByteOrder32Host" not in content:
                                with open(p, "w", encoding="utf-8") as fp:
                                    fp.write(FALLBACK_CODE + content)
                                print(f"[+] Successfully patched {p} with kCGImageByteOrder32Host fallback.")
                                count += 1
                        except Exception as e:
                            print(f"[!] Warning reading/writing {p}: {e}")
    return count

def patch_display(root: str) -> int:
    display_dirs = [
        os.path.join(root, "ui", "display", "mac"),
        os.path.join(root, "engine-src", "ui", "display", "mac"),
    ]

    count = 0
    for display_mac in display_dirs:
        if not os.path.exists(display_mac):
            continue
        files_to_check = glob.glob(os.path.join(display_mac, "*.mm")) + \
                         glob.glob(os.path.join(display_mac, "*.h"))
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
    kcg_patched = patch_kcg_byte_order(root)
    display_patched = patch_display(root)
    print(f"[✔] macOS 15 SDK compatibility patch complete (kCGImageByteOrder32Host: {kcg_patched}, Display: {display_patched}).")

if __name__ == "__main__":
    main()
