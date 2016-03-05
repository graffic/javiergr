from setuptools import setup


setup(
    name='javiergr',
    version='1.0',
    description='javier.gr site',
    author='Javier Gonel',
    author_email='bolibic@gmail.com',
    url='http://javier.gr/',
    install_requires = [
        'Flask',
        'Flask-Assets',
        'Flask-FlatPages',
        'Frozen-Flask',
        'Pygments'
    ]
)
