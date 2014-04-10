"""Flask freezer setup and script"""
from functools import partial
import os.path
import os
import shutil

from flask_frozen import Freezer

from javiergr import app_factory


def bootstrap_fonts(app):
    """Bootstrap static files included in the css"""
    fonts_dir = os.path.join('bower_components', 'bootstrap', 'dist', 'fonts')
    fonts = os.path.join(app.static_folder, fonts_dir)
    for name in os.listdir(fonts):
        yield 'static', {'filename': os.path.join(fonts_dir, name)}


def copy_extra(freezer):
    """Copy files from extra folder to the root"""
    extra_path = os.path.join(freezer.app.root_path, 'extra')
    for item in os.listdir(extra_path):
        src = os.path.join(extra_path, item)
        dst = os.path.join(freezer.root, item)
        shutil.copyfile(src, dst)


def freeze():
    """Prepare and run the freezer"""
    app = app_factory({'FREEZER_DESTINATION': '../output'})
    freezer = Freezer(app, with_static_files=False)
    freezer.register_generator(partial(bootstrap_fonts, app))
    freezer.freeze()
    copy_extra(freezer)


if __name__ == '__main__':
    freeze()
