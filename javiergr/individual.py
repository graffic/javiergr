"""
Individual pages
"""
from flask import (
    Blueprint,
    g,
    render_template)

individual = Blueprint('individual', __name__)


@individual.route('/')
def index():
    """main index page"""
    return render_template('index.html', pages=g.pages.sorted[:3])


@individual.route('/about/')
def about():
    """about page"""
    return render_template('about.html')
