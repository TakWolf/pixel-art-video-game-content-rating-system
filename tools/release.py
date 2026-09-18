import shutil
from zipfile import ZipFile

import markdown

from tools import PROJECT_ROOT_DIR, ASSETS_DIR, EXAMPLES_DIR, RELEASES_DIR

_VERSION = '0.0.0'


def _make_release_zip() -> None:
    file_path = RELEASES_DIR.joinpath(f'pixel-art-video-game-content-rating-system-{_VERSION}.zip')
    with ZipFile(file_path, 'w') as file:
        for root_dir in [ASSETS_DIR, EXAMPLES_DIR]:
            for file_dir, _, file_names in root_dir.walk():
                for file_name in file_names:
                    if not file_name.endswith('.png'):
                        continue

                    file_path = file_dir.joinpath(file_name)
                    arc_path = file_path.relative_to(PROJECT_ROOT_DIR)
                    file.write(file_path, arc_path)

        file.write(PROJECT_ROOT_DIR.joinpath('LICENSE'), 'LICENSE')
        file.write(PROJECT_ROOT_DIR.joinpath('README.md'), 'README.md')


def _make_itchio_readme() -> None:
    md_file_path = PROJECT_ROOT_DIR.joinpath('README.md')
    md_text = md_file_path.read_text('utf-8')
    md_text = md_text.replace('](LICENSE)', '](https://github.com/TakWolf/pixel-art-video-game-content-rating-system/blob/master/LICENSE)')
    md_text = md_text.replace('![](assets/', '![](https://raw.githubusercontent.com/TakWolf/pixel-art-video-game-content-rating-system/master/assets/')
    md_text = md_text.replace('![](examples/', '![](https://raw.githubusercontent.com/TakWolf/pixel-art-video-game-content-rating-system/master/examples/')
    html = markdown.markdown(md_text)
    html_file_path = RELEASES_DIR.joinpath('itchio-readme.html')
    html_file_path.write_text(f'{html}\n', 'utf-8')


def main() -> None:
    if RELEASES_DIR.exists():
        shutil.rmtree(RELEASES_DIR)
    RELEASES_DIR.mkdir(parents=True)

    _make_release_zip()
    _make_itchio_readme()


if __name__ == '__main__':
    main()
