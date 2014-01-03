title: This blog is powered by
date: 2014-01-03
category: technical
slug: this-blog-is-powered-by
published: true
summary: I restarted my homepage, but this time using flask and flask freezer.

After some years using [Wordpress][wordpress], and some attempts at static blog generators
I've switched to [Flask][flask]. If you want to know why, keep reading. If you
just want to see the code, [click here][blogsource].

First Version
-------------

The first versions were based on [Wordpress][wordpress], but it had some things I
didn't like much:

- Keeping an eye on wordpress vulnerabilities and wordpress plugin
  vulnerabilities.
- Wordpress way of editing posts. Even for simple things I had to “fight”
  a bit with the WYSIWYG editor to make things look like I wanted.
- Wordpress templates are easy, but are based on what Wordpress thinks a template should be.
  You might want to organize things in another way: different problems, different solutions.

I could have:

- Used the hosted wordpress to forget about version updates.
- Bought a personalized wordpress template.

It was clear for me that I wanted more control about my homepage.


Static blog/page generators
---------------------------

Static blog generators give you more control. After watching many personal
pages moving to [Octopress][octopress]/[Jekyll][jekyll]. There are many other
good tools like [Middleman][middleman] for full static sites and not only
blogs.

I looked for something more... python. Again, there are a lot of static site
generators in python. I ended up trying two:

- [Nikola][nikola]
- [Pelican][pelican]

At the time I checked [Nikola][nikola] it needed some extra plugins to do what
I wanted but the code was clean. [Pelican][pelican] was ready to use, but code
is a bit messy. The future of Nikola seems to have as many plugins as pelican,
and the future of pelican to have as good code base as Nikola. Good projects to
keep an eye on.

In both cases you should follow the tools and structure defined by the engines.
If you want to do something more, you should use a plugin (Pelican had all I
needed). If you want to do something different, you need to read the code.

Every tool enforces some patterns. It's something good to start with if you
don't know where to start.  But web frameworks don't impose so many things
(only some).  General purpose web frameworks leave you enough space to build
almost any web site/application you want.

Also my old friend [@jcea][jcea] said: If you build your site well enough
you can always `wget` it and make it static.

Flask
-----

Another friend, [@oscarmlage][oscarmlage], told me about his blog engine running with
flask: [flask-htmlblog][flask-htmlblog] and other very interesting flask plugins.

Flask had all the plugins I needed, and also has a “wget” plugin called freezer.
It is simple to use and uses jinja2 (like pelican). I had the site running with
pelican, it took me a couple hours to move it to flask.  

What are my dependencies?

- [Flask][flask]: All the web mumbo-jumbo.
- [Flask Flat Pages][flask-flatpages]: Use markdown files as sources
- [Frozen Flask][frozen-flask]: Dump the site as static HTML pages.
- [Webassets][webassets] and its [flask adapter][flask-assets]: Minify/clean less, css, and javascript
  assets.

The rest is some code for the views and the project structure. Check the [source][blogsource]!.

Problems found
--------------

### Python 3.

Some libraries needed 2to3. I hope to have time to commit back the python 3 compatibility.

### Special static files

There are some static files like robots.txt, humans.txt and even an .htaccess needed
for apache. For these files I added an extra step after freezing the site.

    :::python
    def copy_extra():
        """Copy files from extra folder to the root"""
        extra_path = os.path.join(APP.root_path, 'extra')
        for item in os.listdir(extra_path):
	        src = os.path.join(extra_path, item)
            dst = os.path.join(FREEZER.root, item)
	        shutil.copyfile(src, dst)

Also in the freezing process (generating the HTML files), I need to copy some
files from one bower component: bootstrap fonts.

    :::python
	FREEZER = Freezer(APP, with_static_files=False)

	@FREEZER.register_generator
	def bootstrap_fonts():
	    """Bootstrap static files included in the css"""
		fonts_dir = os.path.join('bower_components', 'bootstrap', 'fonts')
		fonts = os.path.join(APP.static_folder, fonts_dir)
        for name in os.listdir(fonts):
            yield 'static', {'filename': os.path.join(fonts_dir, name)}


Next steps
----------

### Disqus.

I wanted to make the comments available as static content for search engine
crawlers. At the time of writing I have a pending [pull request][disqusreq] in the disqus
API bindings for python in order to add python 3.3 support (and tests). 

### ZODB. 

The flask-ZODB plugin didn't want to work with python 3. So I created 
[something similar][zodb-plugin]. I must say that Flask can be extended really easily, Kudos!


[flask]: http://flask.pocoo.org
[blogsource]: https://github.com/graffic/javiergr
[wordpress]: http://wordpress.org
[octopress]: http://octopress.org
[jekyll]: http://jekyllrb.com
[middleman]: http://middlemanapp.com
[nikola]: http://getnikola.com
[pelican]: http://blog.getpelican.com
[jcea]: http://www.jcea.es
[oscarmlage]: http://www.oscarmlage.com
[flask-htmlblog]: https://bitbucket.org/r0sk/flask-htmlblog
[flask-flatpages]: http://pythonhosted.org/Flask-FlatPages/
[frozen-flask]: http://pythonhosted.org/Frozen-Flask/
[webassets]: http://webassets.readthedocs.org/en/latest/
[flask-assets]: http://elsdoerfer.name/docs/flask-assets/
[disqusreq]: https://github.com/disqus/disqus-python/pull/6
[zodb-plugin]: https://github.com/graffic/javiergr/blob/master/javiergr/zodb.py
