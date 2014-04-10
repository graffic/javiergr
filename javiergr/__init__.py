"""javier.gr flask application"""
from flask import Flask

from javiergr.assets import register_assets
from javiergr.blog import blog
from javiergr.blog_pages import register_pages
from javiergr.feeds import feeds
from javiergr.individual import individual
from javiergr.md_extensions import JavierExtensions


def app_factory(extra_config=None):
    """Builds the flask application"""
    app = Flask(__name__)

    # App defaults
    app.config.update(dict(
        DEBUG=True,
        FLATPAGES_ROOT='blog',
        FLATPAGES_EXTENSION='.md',
        FLATPAGES_MARKDOWN_EXTENSIONS=['codehilite', JavierExtensions()],
        FLATPAGES_AUTO_RELOAD=True))
    # Extra config
    if extra_config:
        app.config.update(extra_config)

    # Blueprints
    app.register_blueprint(blog, url_prefix='/blog')
    app.register_blueprint(individual)
    app.register_blueprint(feeds)

    # Other configuration
    app.context_processor(template_settings)
    app.add_template_filter(l10n_date)
    register_assets(app)
    register_pages(app)
    return app


def template_settings():
    """Extra template globals/context"""
    return dict(
        CONTACT_EMAIL='bolibic@gmail.com',
        BASE_URL='http://javier.gr')


def l10n_date(date):
    """Jinja filter for human dates from date objects"""
    return date.strftime('%a %d %B %Y')
