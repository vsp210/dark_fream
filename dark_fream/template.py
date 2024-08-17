from jinja2 import Environment, FileSystemLoader

def render(request, template_name, context={}, templates='templates'):
    env = Environment(loader=FileSystemLoader(templates))
    template = env.get_template(template_name)
    return template.render(context)
