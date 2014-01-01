"""Webassets configuration and handling"""
import os.path

from flask.ext.assets import Environment, Bundle
from pygments.formatters import HtmlFormatter


def _create_code_css(app):
    """
    Creates the code.css file for code highlighting

    This will be used to merge all the css in one file
    """
    filename = os.path.join(app.static_folder, 'style', 'code.css')
    with open(filename, 'w') as code_css:
        css = HtmlFormatter(style='default').get_style_defs('.codehilite')
        code_css.write(css)


def register_assets(app):
    """Register Webassets in the app"""
    _create_code_css(app)

    assets = Environment(app)
    bundle = Bundle('style/main.less', 'style/code.css',
                    filters='less,cleancss',
                    output='css/main.%(version)s.css')
    assets.register('css', bundle)
