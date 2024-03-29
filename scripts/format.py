import os

import png

from scripts import assets_dir, examples_dir


def _load_png(
        file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes],
) -> tuple[list[list[tuple[int, int, int, int]]], int, int]:
    width, height, bitmap, _ = png.Reader(filename=file_path).read()
    data = []
    for bitmap_row in bitmap:
        data_row = []
        for x in range(0, width * 4, 4):
            red = bitmap_row[x]
            green = bitmap_row[x + 1]
            blue = bitmap_row[x + 2]
            alpha = bitmap_row[x + 3]
            data_row.append((red, green, blue, alpha))
        data.append(data_row)
    return data, width, height


def _save_png(
        data: list[list[tuple[int, int, int, int]]],
        file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes],
):
    bitmap = []
    for data_row in data:
        bitmap_row = []
        for red, green, blue, alpha in data_row:
            bitmap_row.append(red)
            bitmap_row.append(green)
            bitmap_row.append(blue)
            bitmap_row.append(alpha)
        bitmap.append(bitmap_row)
    png.from_array(bitmap, 'RGBA').save(file_path)


def _scale_bitmap(
        data: list[list[tuple[int, int, int, int]]],
        scale: int,
) -> list[list[tuple[int, int, int, int]]]:
    new_data = []
    for data_row in data:
        for _ in range(scale):
            new_data_row = []
            for pixel in data_row:
                for _ in range(scale):
                    new_data_row.append(pixel)
            new_data.append(new_data_row)
    return new_data


def _format_assets():
    for root_dir in [assets_dir, examples_dir]:
        for file_dir, _, file_names in list(os.walk(root_dir)):
            for file_name in file_names:
                if not file_name.endswith('@1x.png'):
                    continue

                file_path_1x = os.path.join(file_dir, file_name)
                data_1x = _load_png(file_path_1x)[0]
                _save_png(data_1x, file_path_1x)

                data_2x = _scale_bitmap(data_1x, 2)
                file_path_2x = file_path_1x.removesuffix('@1x.png') + '@2x.png'
                _save_png(data_2x, file_path_2x)


def main():
    _format_assets()


if __name__ == '__main__':
    main()
