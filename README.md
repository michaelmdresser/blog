# blog

Building:

``` sh
# Update the list with new posts
python3 build.py
```

Running a test local version of the blog

``` sh
python3 build.py && (cd docs && python3 -m http.server 8000)
```

## Helpful references for the Pandoc + Markdown approach

- https://www.romangeber.com/static_websites_with_pandoc/
- https://github.com/fcanas/bake/blob/master/template.tmp
- https://ordecon.com/2020/07/pandoc-as-a-site-generator.html
- https://github.com/ivanstojic/pandoc-ssg/blob/master/_pandoc/templates/default.html5
- https://github.com/ivanstojic/pandoc-ssg/blob/master/Makefile
- https://pandoc.org/MANUAL.html#templates
- https://github.com/kjhealy/pandoc-templates/blob/master/templates/html.template
- https://gist.github.com/killercup/5917178
