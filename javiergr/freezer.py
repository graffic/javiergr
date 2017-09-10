"""Flask freezer setup and script"""
from functools import partial
from os.path import join
from datetime import datetime
import os
import shutil

from flask_frozen import Freezer

from javiergr import app_factory


def bootstrap_fonts(app):
    """Bootstrap static files included in the css"""
    fonts = join(app.root_path, '..', 'node_modules', 'bootstrap', 'fonts')
    for name in os.listdir(fonts):
        yield 'bootstrap_fonts', {'filename': name}

def copy_extra(freezer):
    """Copy files from extra folder to the root"""
    extra_path = join(freezer.app.root_path, 'extra')
    for item in os.listdir(extra_path):
        src = join(extra_path, item)
        dst = join(freezer.root, item)
        shutil.copyfile(src, dst)

def freezer_template_context():
    return dict(FREEZE_DATE=datetime.utcnow().isoformat())

def freeze():
    """Prepare and run the freezer"""
    app = app_factory({'FREEZER_DESTINATION': join('..', 'output')})
    app.context_processor(freezer_template_context)
    freezer = Freezer(app, with_static_files=False)
    freezer.register_generator(partial(bootstrap_fonts, app))
    freezer.freeze()
    copy_extra(freezer)


if __name__ == '__main__':
    freeze()
