"""
Blog view functions
"""
from calendar import month_name
from itertools import groupby
import os

from flask import Blueprint, render_template, g, send_from_directory, abort

blog = Blueprint('blog', __name__)


@blog.route('/')
def index():
    """blog index page"""
    pages = g.pages
    items = pages.sorted
    return render_template(
        'blog.html', pages=items[:15], years=pages.years)


@blog.route('/<int:year>/')
def by_year(year):
    """blog archive per year"""

    items = g.pages.by_year(year)
    if not items:
        abort(404)
    # Group per month
    months = groupby(items, lambda p: month_name[p['date'].month])
    return render_template(
        'blog_year.html', months=months, years=g.pages.years,
        current_year=year)


@blog.route('/<path:path>/<string:filename>')
def flat_page_content(path, filename):
    """flat pages content (static) rendering"""
    g.pages.flatpages.get_or_404(path)
    path = os.path.join(blog.root_path, 'blog', os.path.dirname(path))
    return send_from_directory(path, filename)


@blog.route('/<path:path>/')
def flat_page(path):
    """flat pages rendering"""
    page = g.pages.flatpages.get_or_404(path)
    # Configure the img link plugin
    g.flat_page = page
    return render_template('article.html', page=page)
