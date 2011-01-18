import markdown
import codecs

HTML_START = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Hoisting and Deep Linking</title>
</head>
<body>
""".lstrip()

HTML_END = """
</body>
</html>
"""

class IndexPage(object):
    md_filename = 'readme.markdown'
    html_filename = 'index.html'

    def read_md(self):
        with codecs.open(self.md_filename, mode="r", encoding="utf8") as f:
            self.md = f.read()

    def render(self):
        self.read_md()
        md = markdown.Markdown(extensions=['toc'])
        return HTML_START + md.convert(self.md) + HTML_END

    def write_html(self):
        with codecs.open(self.html_filename, mode="w", encoding="utf8") as f:
            f.write(self.render())

if __name__ == '__main__':
    IndexPage().write_html()
