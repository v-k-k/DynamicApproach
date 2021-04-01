from jinja2 import Environment, FileSystemLoader


def index(context):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('index.html')
    return template.render(host=context['host'], port=context['port'], greeting=context['greeting'])


def endpoint(context):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('index.html')
    return template.render(result=context['result'],
                           approach=context['approach'],
                           execution_time=context['execution_time'])
