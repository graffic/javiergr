"""Flask freezer setup and script"""
import os.path
import os
import shutil

from flask_frozen import Freezer

from javiergr import APP

APP.config['FREEZER_DESTINATION'] = '../output'

FREEZER = Freezer(APP, with_static_files=False)


@FREEZER.register_generator
def bootstrap_fonts():
    """Bootstrap static files included in the css"""
    fonts_dir = os.path.join('bower_components', 'bootstrap', 'fonts')
    fonts = os.path.join(APP.static_folder, fonts_dir)
    for name in os.listdir(fonts):
        yield 'static', {'filename': os.path.join(fonts_dir, name)}


def copy_extra():
    """Copy files from extra folder to the root"""
    extra_path = os.path.join(APP.root_path, 'extra')
    for item in os.listdir(extra_path):
        src = os.path.join(extra_path, item)
        dst = os.path.join(FREEZER.root, item)
        shutil.copyfile(src, dst)


if __name__ == '__main__':
    FREEZER.freeze()
    copy_extra()
