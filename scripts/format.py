import os

import png

from scripts import assets_dir, examples_dir


def _load_png(
        file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes],
) -> tuple[list[list[tuple[int, int, int, int]]], int, int]:
    width, height, pixels, _ = png.Reader(filename=file_path).read()
    bitmap = []
    for pixels_row in pixels:
        bitmap_row = []
        for x in range(0, width * 4, 4):
            red = pixels_row[x]
            green = pixels_row[x + 1]
            blue = pixels_row[x + 2]
            alpha = pixels_row[x + 3]
            bitmap_row.append((red, green, blue, alpha))
        bitmap.append(bitmap_row)
    return bitmap, width, height


def _save_png(
        bitmap: list[list[tuple[int, int, int, int]]],
        file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes],
):
    pixels = []
    for bitmap_row in bitmap:
        pixels_row = []
        for red, green, blue, alpha in bitmap_row:
            pixels_row.append(red)
            pixels_row.append(green)
            pixels_row.append(blue)
            pixels_row.append(alpha)
        pixels.append(pixels_row)
    png.from_array(pixels, 'RGBA').save(file_path)


def _scale_bitmap(
        bitmap: list[list[tuple[int, int, int, int]]],
        scale: int,
) -> list[list[tuple[int, int, int, int]]]:
    new_bitmap = []
    for bitmap_row in bitmap:
        for _ in range(scale):
            new_bitmap_row = []
            for pixel in bitmap_row:
                for _ in range(scale):
                    new_bitmap_row.append(pixel)
            new_bitmap.append(new_bitmap_row)
    return new_bitmap


def _format_assets():
    for root_dir in [assets_dir, examples_dir]:
        for file_dir, _, file_names in list(os.walk(root_dir)):
            for file_name in file_names:
                if not file_name.endswith('@1x.png'):
                    continue

                file_path_1x = os.path.join(file_dir, file_name)
                bitmap_1x = _load_png(file_path_1x)[0]
                _save_png(bitmap_1x, file_path_1x)

                bitmap_2x = _scale_bitmap(bitmap_1x, 2)
                file_path_2x = file_path_1x.removesuffix('@1x.png') + '@2x.png'
                _save_png(bitmap_2x, file_path_2x)


def main():
    _format_assets()


if __name__ == '__main__':
    main()
