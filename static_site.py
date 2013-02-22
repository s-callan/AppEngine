import codecs
import os

import jinja2
import webapp2

import markdown2


wrapper = codecs.open(os.path.join(os.path.dirname(__file__), "templates", "default.html"), encoding="UTF-8").read()

loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"))
jinja_environment = jinja2.Environment(loader=loader)


class MarkdownPage(webapp2.RequestHandler):
    def get(self, page=''):
        if page == "" or page[-1] == '/':
            page += "index"
        path = os.path.join(os.path.dirname(__file__), "pages", page + ".md")
        if not os.path.exists(path):
            self.abort(404)

        body = codecs.open(path, encoding="UTF-8").read()
        title = body.split("\n")[0].strip("# \r\n\t")
        body = markdown2.markdown(body, extras=["fenced-code-blocks", "wiki-tables"])
        if page == "index":
            up = ""
        elif not page.endswith("index"):
            up = '<a href="./">Up</a>'
        else:
            up = '<a href="..">Up</a>'

        page = wrapper % {"title": title, "body": body, "up":up}
        self.response.out.write(page.encode("UTF-8"))


app = webapp2.WSGIApplication(
    [('/', MarkdownPage),
     ('/(.*).htm', MarkdownPage),
     ('/(.*/)', MarkdownPage),
    ])
