"""Webassets configuration and handling"""
import os.path

from flask import send_from_directory
from flask_assets import Environment, Bundle
# pylint: disable=no-name-in-module
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
    app.add_url_rule(
        '/static/fonts/bootstrap/<path:filename>',
        'bootstrap_fonts',
        bootstrap_fonts)


def bootstrap_fonts(filename):
    "Sends bootstrap font files"
    # It will do: os.path.join(current_app.root_path, filename)
    return send_from_directory(
        '../node_modules/bootstrap/fonts/', filename)
