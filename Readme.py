import main
import markdown

class Readme:
  def GET(self):
    if main.args.readme is None:
      return "This project has no README.md"
    md = open(main.args.readme).read()
    return main.render.readme(markdown.markdown(md))

