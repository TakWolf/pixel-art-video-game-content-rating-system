from pathlib import Path

from png import PngImage, PngHeader, PngColorType, PngFilterType

from tools import ASSETS_DIR, EXAMPLES_DIR


def _load_png(file_path: Path) -> tuple[list[list[tuple[int, int, int, int]]], int, int]:
    image = PngImage.load(file_path)
    if image.header.color_type != PngColorType.TRUECOLOR_ALPHA or image.header.bit_depth != 8:
        image = image.to_rgba(bit_depth=8)
    bitmap = [
        [
            (row[x], row[x + 1], row[x + 2], row[x + 3])
            for x in range(0, len(row), 4)
        ]
        for row in image.bitmap
    ]
    return bitmap, image.header.width, image.header.height


def _save_png(bitmap: list[list[tuple[int, int, int, int]]], file_path: Path) -> None:
    image = PngImage(
        header=PngHeader((len(bitmap[0]), len(bitmap))),
        bitmap=[
            [
                sample
                for pixel in row
                for sample in pixel
            ]
            for row in bitmap
        ],
    )
    image.save(file_path, filter_type=PngFilterType.NONE)


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
        for file_path_1x in root_dir.rglob('*@1x.png'):
            if not file_path_1x.is_file():
                continue

            bitmap_1x = _load_png(file_path_1x)[0]
            _save_png(bitmap_1x, file_path_1x)

            bitmap_2x = _scale_bitmap(bitmap_1x, 2)
            file_path_2x = file_path_1x.with_stem(file_path_1x.stem.replace('@1x', '@2x'))
            _save_png(bitmap_2x, file_path_2x)


def main() -> None:
    _format_assets()


if __name__ == '__main__':
    main()
