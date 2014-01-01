"""javier.gr flask application"""
from datetime import datetime
import os.path

from flask import (
    Flask,
    render_template,
    make_response,
    url_for,
    abort)
from flask_flatpages import FlatPages

from javiergr.assets import register_assets
from javiergr.zodb import FlaskZODB

APP = Flask(__name__)

APP.config.update(dict(
    DEBUG=True,
    FLATPAGES_ROOT='blog',
    FLATPAGES_EXTENSION='.md',
    FLATPAGES_AUTO_RELOAD=True))

DB = FlaskZODB(APP)
PAGES = FlatPages(APP)
register_assets(APP)


def years_pages(pages):
    """Gets a list of integers with the years we have pages in"""
    return sorted(set(page['date'].year for page in pages), reverse=True)


def sort_pages(pages):
    """Sort pages by date"""
    return sorted(pages, key=lambda p: p['date'], reverse=True)


def pages_year(pages, year):
    """Get pages for a specific year"""
    return sort_pages((p for p in pages if p['date'].year == year))


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
        ('/blog/', sort_pages(PAGES)[0]['date'], 0.7)]
    for year in years_pages(PAGES):
        most_recent = pages_year(PAGES, year)[0]['date']
        urls.append((url_for('blog_year', year=year), most_recent, 0.5))
    for page in PAGES:
        urls.append((url_for('flat_page', path=page.path), page['date'], 0.5))

    # XML response
    sitemap_xml = render_template('sitemap.xml', urls=urls)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response


@APP.route('/')
def index():
    """main index page"""
    return render_template('index.html', pages=sort_pages(PAGES)[:5])


@APP.route('/about/')
def about():
    """about page"""
    return render_template('about.html')


@APP.route('/blog/')
def blog():
    """blog index page"""
    items = sort_pages(PAGES)
    return render_template(
        'blog.html', pages=items[:15], years=years_pages(PAGES))


@APP.route('/blog/<int:year>/')
def blog_year(year):
    """blog archive per year"""
    items = pages_year(PAGES, year)
    if not items:
        abort(404)
    return render_template(
        'archives.html', pages=items, years=years_pages(PAGES),
        current_year=year)


@APP.route('/blog/<path:path>/')
def flat_page(path):
    """flat pages rendering"""
    page = PAGES.get_or_404(path)
    return render_template('article.html', page=page)
