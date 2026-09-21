from pathlib import Path

PROJECT_ROOT_DIR = Path(__file__).parents[1]
ASSETS_DIR = PROJECT_ROOT_DIR.joinpath('assets')
EXAMPLES_DIR = PROJECT_ROOT_DIR.joinpath('examples')
BUILD_DIR = PROJECT_ROOT_DIR.joinpath('build')
RELEASES_DIR = BUILD_DIR.joinpath('releases')
