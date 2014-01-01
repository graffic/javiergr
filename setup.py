from setuptools import setup


setup(
    name='javiergr',
    version='1.0',
    description='javier.gr site',
    author='Javier Gonel',
    author_email='bolibic@gmail.com',
    url='http://javier.gr/',
    install_requires = [
        'Flask==0.10.1',
        'Flask-Assets==0.9.dev',
        'Flask-FlatPages==0.5',
        'Frozen-Flask==0.11']
)
