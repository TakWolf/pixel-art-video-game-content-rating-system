from pathlib import Path

import png

from tools import ASSETS_DIR, EXAMPLES_DIR


def _load_png(file_path: Path) -> tuple[list[list[tuple[int, int, int, int]]], int, int]:
    width, height, pixels, _ = png.Reader(filename=file_path).read()
    bitmap = []
    for row in pixels:
        bitmap_row = []
        for x in range(0, width * 4, 4):
            red = row[x]
            green = row[x + 1]
            blue = row[x + 2]
            alpha = row[x + 3]
            bitmap_row.append((red, green, blue, alpha))
        bitmap.append(bitmap_row)
    return bitmap, width, height


def _save_png(bitmap: list[list[tuple[int, int, int, int]]], file_path: Path) -> None:
    pixels = []
    for bitmap_row in bitmap:
        row = []
        for red, green, blue, alpha in bitmap_row:
            row.append(red)
            row.append(green)
            row.append(blue)
            row.append(alpha)
        pixels.append(row)
    png.from_array(pixels, 'RGBA').save(file_path)


def _scale_bitmap(bitmap: list[list[tuple[int, int, int, int]]], scale: int) -> list[list[tuple[int, int, int, int]]]:
    new_bitmap = []
    for bitmap_row in bitmap:
        for _ in range(scale):
            new_bitmap_row = []
            for pixel in bitmap_row:
                for _ in range(scale):
                    new_bitmap_row.append(pixel)
            new_bitmap.append(new_bitmap_row)
    return new_bitmap


def _format_assets() -> None:
    for root_dir in [ASSETS_DIR, EXAMPLES_DIR]:
        for file_dir, _, file_names in root_dir.walk():
            for file_name in file_names:
                if not file_name.endswith('@1x.png'):
                    continue

                file_path_1x = file_dir.joinpath(file_name)
                bitmap_1x = _load_png(file_path_1x)[0]
                _save_png(bitmap_1x, file_path_1x)

                bitmap_2x = _scale_bitmap(bitmap_1x, 2)
                file_path_2x = file_path_1x.with_stem(file_path_1x.stem.replace('@1x', '@2x'))
                _save_png(bitmap_2x, file_path_2x)


def main() -> None:
    _format_assets()


if __name__ == '__main__':
    main()
