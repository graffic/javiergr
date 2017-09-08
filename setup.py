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
    ],
    dependency_links = [
        'https://github.com/miracle2k/webassets/tarball/master#egg=webassets-0.12.1'
    ]
)
