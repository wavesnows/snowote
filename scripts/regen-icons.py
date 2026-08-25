#!/usr/bin/env python3
"""Regenerate snowote icons with proper macOS Big Sur padding.

Takes the existing 512x512 icon content, places it centered at 80% of a 1024
canvas (macOS squircle spec: ~824 content + 100px transparent padding on each
side), and regenerates PNG / ICNS / ICO / favicon.

This preserves the original visual design — only adds the missing padding so
the icon no longer appears oversized in the macOS Dock.
"""
import os
import shutil
from PIL import Image

SIZE = 1024
# macOS Big Sur: content occupies ~80% of the canvas
CONTENT_RATIO = 0.824  # 824/1024
SOURCE_PNG = 'build/icon-backup/icon.png'
OUT_PNG = 'build/icon.png'
OUT_ICNS = 'build/icon.icns'
OUT_ICO = 'build/icon.ico'
OUT_FAVICON = 'public/favicon.ico'


def make_base(size: int, source: Image.Image) -> Image.Image:
    """Place source icon centered at CONTENT_RATIO of the canvas."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    content_size = int(size * CONTENT_RATIO)
    offset = (size - content_size) // 2
    # Resize source to content_size x content_size (preserving aspect ratio)
    src = source.convert('RGBA')
    # Use LANCZOS for downscaling quality
    src_resized = src.resize((content_size, content_size), Image.LANCZOS)
    img.paste(src_resized, (offset, offset), src_resized)
    return img


def main():
    os.makedirs('build', exist_ok=True)
    os.makedirs('public', exist_ok=True)

    source = Image.open(SOURCE_PNG)
    print(f'Source: {source.size} mode={source.mode}')

    # 1024 PNG
    base = make_base(SIZE, source)
    base.save(OUT_PNG)
    print(f'Wrote {OUT_PNG} ({SIZE}x{SIZE})')

    # macOS .icns via iconutil
    iconset = 'build/icon.iconset'
    if os.path.exists(iconset):
        shutil.rmtree(iconset)
    os.makedirs(iconset)
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    for s in sizes:
        im = make_base(s, source)
        im.save(f'{iconset}/icon_{s}x{s}.png')
        if s <= 512:
            im2 = make_base(s * 2, source)
            im2.save(f'{iconset}/icon_{s}x{s}@2x.png')
    ret = os.system(f'iconutil -c icns "{iconset}" -o "{OUT_ICNS}"')
    if ret == 0:
        print(f'Wrote {OUT_ICNS}')
    else:
        print(f'iconutil failed (ret={ret})')

    # Windows .ico
    ico_sizes = [16, 32, 48, 64, 128, 256]
    base.save(OUT_ICO, sizes=[(s, s) for s in ico_sizes])
    print(f'Wrote {OUT_ICO}')

    # Favicon
    base.save(OUT_FAVICON, sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print(f'Wrote {OUT_FAVICON}')


if __name__ == '__main__':
    main()
