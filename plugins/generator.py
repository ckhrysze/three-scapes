from jinja2 import FileSystemLoader, Template, Environment

loader = FileSystemLoader("templates")
env = Environment(loader=loader)
template = env.get_template("StatusBars.xml")

f = open("test.xml", "w")
f.write(template.render(foo="asdf"))

