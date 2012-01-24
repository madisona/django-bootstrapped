
from django import template
from django.conf import settings



register = template.Library()

JS_TAG = '<script src="{STATIC_URL}bootstrapped/js/bootstrap-{file_name}{extension}" type="text/javascript"></script>'
CSS_TAG = '<link rel="stylesheet" type="text/css" href="{STATIC_URL}bootstrapped/css/{file_name}{extension}" media="all" />'

LESS_JS_TAG = '<script src="{STATIC_URL}bootstrapped/js/less-1.1.5.min.js" type="text/javascript"></script>'.format(STATIC_URL=settings.STATIC_URL)

BOOTSTRAP_JS = (
    'alerts',
    'buttons',
    'dropdown',
    'modal',
    'twipsy',
    # popover requires twipsy loaded first
    'popover',
    'scrollspy',
    'tabs',
)

def get_script_extension(ext):
    """
    If template debug is false we want to deliver minified versions.
    :param ext:
        file extension. Should include the '.'
    """
    return settings.TEMPLATE_DEBUG and ext or ".min" + ext

def get_formatted_tag(format_string, file_name, extension):
    return format_string.format(
        STATIC_URL=settings.STATIC_URL,
        file_name=file_name,
        extension=get_script_extension(extension),
    )

def get_js_tag(file_name):
    return get_formatted_tag(JS_TAG, file_name, ".js")

def get_css_tag(file_name):
    return get_formatted_tag(CSS_TAG, file_name, ".css")

class BootstrapJSNode(template.Node):

    def __init__(self, *args):
        self.js_files = args

    def render_all_scripts(self, script_list):
        return ''.join([get_js_tag(f) for f in script_list])

    def render(self, context):
        if self.js_files == ('all',):
            return self.render_all_scripts(BOOTSTRAP_JS)

        seen, tags = [], []
        for f in self.js_files:
            if f in seen:
                continue

            if f == 'popover' and 'twipsy' not in seen:
                tags.append(get_js_tag('twipsy'))
                seen.append('twipsy')
            tags.append(get_js_tag(f))
            seen.append(f)

        return ''.join(tags)


@register.simple_tag
def bootstrap_css():
    return get_css_tag("bootstrap")


# todo: django 1.4 gives the ability to send unlimited arguments in a simple_tag. Convert to that once it is available.
@register.tag(name='bootstrap_js')
def do_bootstrap_js(parser, token):
    """
    USAGE:
      {% load bootstrap %}

      {% bootstrap_js dropdown %}

    or, to include everything

      {% bootstrap_js all %}
    """
    js_files = token.split_contents()[1:]
    if js_files != ['all'] and not all([f in BOOTSTRAP_JS for f in js_files]):
        raise template.TemplateSyntaxError("You can only include valid bootstrap js files.")

    return BootstrapJSNode(*js_files)


def get_less_css(file_path):
    return '<link rel="stylesheet/less" type="text/css" href="{STATIC_URL}{file_path}" media="all" />'.format(
        STATIC_URL=settings.STATIC_URL,
        file_path=file_path,
    )

@register.simple_tag
def bootstrap_less():
    return ''.join([get_less_css("lib/bootstrap.less"), LESS_JS_TAG,])

@register.simple_tag
def bootstrap_custom_less(less_path):
    return ''.join([get_less_css(less_path), LESS_JS_TAG,])
