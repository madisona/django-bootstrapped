
from django import test
from django import template
from django.conf import settings

class TemplateTagTests(test.TestCase):

    def setUp(self):
        self.original_template_debug = settings.TEMPLATE_DEBUG

    def tearDown(self):
        settings.TEMPLATE_DEBUG = self.original_template_debug

    def test_renders_regular_css_tag_when_template_debug_on(self):
        settings.TEMPLATE_DEBUG = True

        t = template.Template("""
            {% load bootstrap %}
            {% bootstrap_css %}
        """)
        result = t.render(template.Context())
        expected_tag = '<link rel="stylesheet" type="text/css" href="{STATIC_URL}bootstrapped/css/bootstrap.css" media="all" />'.format(
            STATIC_URL=settings.STATIC_URL,
        )

        self.assertEqual(expected_tag, result.strip())

    def test_renders_minified_css_tag_when_template_debug_off(self):
        settings.TEMPLATE_DEBUG = False

        t = template.Template("""
            {% load bootstrap %}
            {% bootstrap_css %}
        """)
        result = t.render(template.Context())
        expected_tag = '<link rel="stylesheet" type="text/css" href="{STATIC_URL}bootstrapped/css/bootstrap.min.css" media="all" />'.format(
            STATIC_URL=settings.STATIC_URL,
        )

        self.assertEqual(expected_tag, result.strip())