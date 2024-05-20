from pathlib import Path

project_root_dir = Path(__file__).parent.joinpath('..').resolve()
assets_dir = project_root_dir.joinpath('assets')
examples_dir = project_root_dir.joinpath('examples')
build_dir = project_root_dir.joinpath('build')
releases_dir = build_dir.joinpath('releases')
