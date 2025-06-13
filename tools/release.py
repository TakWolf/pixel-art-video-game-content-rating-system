import shutil
import zipfile

import markdown

from tools import project_root_dir, assets_dir, examples_dir, releases_dir

_VERSION = '0.0.0'


def _make_release_zip():
    file_path = releases_dir.joinpath(f'pixel-art-video-game-content-rating-system-{_VERSION}.zip')
    with zipfile.ZipFile(file_path, 'w') as file:
        for root_dir in [assets_dir, examples_dir]:
            for file_dir, _, file_names in root_dir.walk():
                for file_name in file_names:
                    if not file_name.endswith('.png'):
                        continue
                    file_path = file_dir.joinpath(file_name)
                    arc_path = file_path.relative_to(project_root_dir)
                    file.write(file_path, arc_path)
        file.write(project_root_dir.joinpath('LICENSE'), 'LICENSE')
        file.write(project_root_dir.joinpath('README.md'), 'README.md')


def _make_itchio_readme():
    md_file_path = project_root_dir.joinpath('README.md')
    md_text = md_file_path.read_text('utf-8')
    md_text = md_text.replace('](LICENSE)', '](https://github.com/TakWolf/pixel-art-video-game-content-rating-system/blob/master/LICENSE)')
    md_text = md_text.replace('![](assets/', '![](https://raw.githubusercontent.com/TakWolf/pixel-art-video-game-content-rating-system/master/assets/')
    md_text = md_text.replace('![](examples/', '![](https://raw.githubusercontent.com/TakWolf/pixel-art-video-game-content-rating-system/master/examples/')
    html = markdown.markdown(md_text)
    html_file_path = releases_dir.joinpath('itchio-readme.html')
    html_file_path.write_text(f'{html}\n', 'utf-8')


def main():
    if releases_dir.exists():
        shutil.rmtree(releases_dir)
    releases_dir.mkdir(parents=True)

    _make_release_zip()
    _make_itchio_readme()


if __name__ == '__main__':
    main()
