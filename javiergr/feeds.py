"""
Blueprint for sitemap and atom feeds
"""
from datetime import datetime
import os

from flask import (
    Blueprint,
    current_app,
    g,
    make_response,
    render_template,
    url_for)

FEEDS = Blueprint('feeds', __name__)


def template_mdate(template):
    """Gets modification datetime of a template file"""
    mtime = os.path.getmtime(
        os.path.join(current_app.jinja_loader.searchpath[0], template))
    return datetime.fromtimestamp(mtime)


@FEEDS.route('/sitemap.xml')
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
    return xmlify('sitemap.xml', urls=urls)


@FEEDS.route('/atom.xml')
def atom():
    """Atom XML feed"""
    sorted_pages = g.pages.sorted
    last_update = sorted_pages[0]['date'].isoformat() + 'T00:00:00Z'
    pages = [(
        page['title'],
        url_for('blog.flat_page', path=page.path),
        "tag:javier.gr,%s:%s" % (page['date'].isoformat(), page.path),
        page['date'].isoformat() + 'T00:00:00Z',
        page['summary']) for page in sorted_pages]

    # XML response
    return xmlify('atom.xml', last_update=last_update, pages=pages)


def xmlify(template, **kwargs):
    """Renders an XML template"""
    xml = render_template(template, **kwargs)
    response = make_response(xml)
    response.headers["Content-Type"] = "application/xml"
    return response
