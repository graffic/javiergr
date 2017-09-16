"""
Individual pages
"""
from flask import (
    Blueprint,
    g,
    render_template)

INDIVIDUAL = Blueprint('individual', __name__)


@INDIVIDUAL.route('/')
def index():
    """main index page"""
    return render_template('index.html', pages=g.pages.sorted[:3])


@INDIVIDUAL.route('/about/')
def about():
    """about page"""
    return render_template('about.html')
