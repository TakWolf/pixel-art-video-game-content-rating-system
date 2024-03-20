import os

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
assets_dir = os.path.join(project_root_dir, 'assets')
examples_dir = os.path.join(project_root_dir, 'examples')
build_dir = os.path.join(project_root_dir, 'build')
releases_dir = os.path.join(build_dir, 'releases')
