import os
import shutil
import zipfile

import markdown

from scripts import project_root_dir, assets_dir, examples_dir, build_dir

_VERSION = '0.0.0'


def _make_release_zip():
    file_path = os.path.join(build_dir, f'pixel-art-video-game-content-rating-system-{_VERSION}.zip')
    with zipfile.ZipFile(file_path, 'w') as file:
        for root_dir in [assets_dir, examples_dir]:
            for file_dir, _, file_names in list(os.walk(root_dir)):
                for file_name in file_names:
                    if not file_name.endswith('.png'):
                        continue
                    file_path = os.path.join(file_dir, file_name)
                    arc_path = file_path.removeprefix(project_root_dir)
                    file.write(file_path, arc_path)
        file.write(os.path.join(project_root_dir, 'LICENSE'), 'LICENSE')
        file.write(os.path.join(project_root_dir, 'README.md'), 'README.md')


def _make_itchio_readme():
    md_file_path = os.path.join(project_root_dir, 'README.md')
    with open(md_file_path, 'r', encoding='utf-8') as file:
        md_text = file.read()
    md_text = md_text.replace('![](assets/', '![](https://raw.githubusercontent.com/TakWolf/pixel-art-video-game-content-rating-system/master/assets/')
    md_text = md_text.replace('![](examples/', '![](https://raw.githubusercontent.com/TakWolf/pixel-art-video-game-content-rating-system/master/examples/')
    html = markdown.markdown(md_text)
    html_file_path = os.path.join(build_dir, 'itchio-readme.html')
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(html)
        file.write('\n')


def main():
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.makedirs(build_dir)

    _make_release_zip()
    _make_itchio_readme()


if __name__ == '__main__':
    main()
