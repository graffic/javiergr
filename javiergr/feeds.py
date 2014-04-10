from datetime import datetime
import os

from flask import (
    Blueprint,
    current_app,
    g,
    make_response,
    render_template,
    url_for)

feeds = Blueprint('feeds', __name__)


def template_mdate(template):
    """Gets modification datetime of a template file"""
    mtime = os.path.getmtime(
        os.path.join(current_app.jinja_loader.searchpath[0], template))
    return datetime.fromtimestamp(mtime)


@feeds.route('/sitemap.xml')
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
