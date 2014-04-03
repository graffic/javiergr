"""javier.gr flask application"""
from datetime import datetime
from itertools import groupby
import os.path

from flask import (
    Flask,
    render_template,
    make_response,
    url_for,
    abort,
    g)
from flask.helpers import safe_join, send_from_directory

from javiergr.assets import register_assets
from javiergr.blog import BLOG
from javiergr.blog_pages import register_pages
from javiergr.zodb import FlaskZODB
from javiergr.md_extensions import JavierExtensions

APP = Flask(__name__)

APP.config.update(dict(
    DEBUG=True,
    FLATPAGES_ROOT='blog',
    FLATPAGES_EXTENSION='.md',
    FLATPAGES_MARKDOWN_EXTENSIONS=['codehilite', JavierExtensions()],
    FLATPAGES_AUTO_RELOAD=True))
APP.register_blueprint(BLOG, url_prefix='/blog')
DB = FlaskZODB(APP)
register_assets(APP)
register_pages(APP)


def template_mdate(template):
    """Gets modification datetime of a template file"""
    mtime = os.path.getmtime(
        os.path.join(APP.jinja_loader.searchpath[0], template))
    return datetime.fromtimestamp(mtime)


@APP.context_processor
def template_settings():
    """Extra template globals/context"""
    return dict(
        CONTACT_EMAIL='bolibic@gmail.com',
        BASE_URL='http://javier.gr')


@APP.template_filter()
def l10n_date(date):
    """Jinja filter for human dates from date objects"""
    return date.strftime('%a %d %B %Y')


@APP.route('/sitemap.xml')
def sitemap():
    """Builds a sitemap with all pages and flat-pages"""
    # Gather urls
    urls = [
        ('/', template_mdate('index.html'), 1),
        ('/about/', template_mdate('about.html'), 0.9),
        ('/blog/', g.pages.sorted[0]['date'], 0.7)]
    for year in g.pages.years:
        most_recent = g.pages.by_year(year)[0]['date']
        urls.append((url_for('blog.by_year', year=year), most_recent, 0.5))
    for page in g.pages:
        urls.append((
            url_for('blog.flat_page', path=page.path),
            page['date'],
            0.5))

    # XML response
    sitemap_xml = render_template('sitemap.xml', urls=urls)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response


@APP.route('/')
def index():
    """main index page"""
    return render_template('index.html', pages=g.pages.sorted[:3])


@APP.route('/about/')
def about():
    """about page"""
    return render_template('about.html')
