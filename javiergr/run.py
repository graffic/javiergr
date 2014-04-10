"""Serves the flask app"""
from javiergr import app_factory


if __name__ == '__main__':
    app_factory().run()
