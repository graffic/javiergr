"""
Markdown extensions for flatpages
"""
from flask import g, url_for

from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension


class LocalImages(Treeprocessor):
    """
    Use url_for for images local to the flat_page

    This is useful for better urls and for freezing.
    """
    def __init__(self, page):
        super().__init__()
        self.__page = page

    def run(self, root):
        images = (e for e in root.getiterator() if e.tag == 'img')
        for image in images:
            src = image.get('src')
            if '/' in src:
                continue
            new_src = url_for('blog.flat_page_content', path=self.__page.path,
                              filename=src)
            image.set('src', new_src)
        return root


class JavierExtensions(Extension):
    """
    Extend markdown parsing with:
    - url_for for images local to the flat page markdown article
    """
    def extendMarkdown(self, md, md_globals):
        page = g.get('flat_page')
        md.treeprocessors.add('ReviewLinks', LocalImages(page), '_end')
