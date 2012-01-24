
from django import test
from django import template
from django.conf import settings

from bootstrapped.templatetags.bootstrap import get_js_tag, BOOTSTRAP_JS

class TemplateTagTests(test.TestCase):

    def setUp(self):
        self.original_template_debug = settings.TEMPLATE_DEBUG

    def tearDown(self):
        settings.TEMPLATE_DEBUG = self.original_template_debug

    def test_get_js_tag_returns_js_script_tag(self):
        settings.TEMPLATE_DEBUG = True
        tag = get_js_tag("modal")
        expected = '<script src="{0}bootstrapped/js/bootstrap-modal.js" type="text/javascript"></script>'.format(settings.STATIC_URL)
        self.assertEqual(expected, tag)

    def test_get_js_tag_returns_minified_js_script_tag_when_not_debug(self):
        settings.TEMPLATE_DEBUG = False
        tag = get_js_tag("modal")
        expected = '<script src="{0}bootstrapped/js/bootstrap-modal.min.js" type="text/javascript"></script>'.format(settings.STATIC_URL)
        self.assertEqual(expected, tag)

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

    def test_bootstrap_js_adds_script_tag_for_given_file(self):
        t = template.Template("""
            {% load bootstrap %}
            {% bootstrap_js modal %}
        """)
        result = t.render(template.Context())
        expected_tag = get_js_tag("modal")
        self.assertEqual(expected_tag, result.strip())

    def test_bootstrap_js_adds_script_tag_for_multiple_files(self):
        t = template.Template("""
            {% load bootstrap %}
            {% bootstrap_js modal dropdown %}
        """)
        result = t.render(template.Context())
        expected_tags = [get_js_tag("modal"), get_js_tag("dropdown")]
        self.assertEqual("".join(expected_tags), result.strip())

    def test_bootstrap_js_raises_exception_when_requesting_js_that_doesnt_exist(self):

        with self.assertRaises(template.TemplateSyntaxError):
            template.Template("""
                {% load bootstrap %}
                {% bootstrap_js doesnt_exist %}
            """)

    def test_bootstrap_js_raises_exception_when_requesting_valid_file_and_invalid(self):

        with self.assertRaises(template.TemplateSyntaxError):
            template.Template("""
                {% load bootstrap %}
                {% bootstrap_js modal dropdown doesnt_exist %}
            """)

    def test_requesting_all_js_adds_all_files(self):
        expected_tags = [get_js_tag(f) for f in BOOTSTRAP_JS]

        t = template.Template("""
            {% load bootstrap %}
            {% bootstrap_js all %}
        """)
        result = t.render(template.Context())
        self.assertEqual("".join(expected_tags), result.strip())

    def test_adding_popover_also_adds_twipsy_before_popover_when_twipsy_not_present(self):
        expected_tags = [get_js_tag(f) for f in ["twipsy", "popover"]]

        t = template.Template("""
            {% load bootstrap %}
            {% bootstrap_js popover %}
        """)
        result = t.render(template.Context())
        self.assertEqual("".join(expected_tags), result.strip())

    def test_adding_popover_doesnt_add_twipsy_when_already_present(self):
        expected_tags = [get_js_tag(f) for f in ["twipsy", "popover"]]

        t = template.Template("""
            {% load bootstrap %}
            {% bootstrap_js twipsy popover %}
        """)
        result = t.render(template.Context())
        self.assertEqual("".join(expected_tags), result.strip())

    def test_fixes_twipsy_order_when_declared_in_wrong_order(self):
        expected_tags = [get_js_tag(f) for f in ["twipsy", "popover"]]

        t = template.Template("""
            {% load bootstrap %}
            {% bootstrap_js popover twipsy %}
        """)
        result = t.render(template.Context())
        self.assertEqual("".join(expected_tags), result.strip())

    def test_only_adds_same_file_once(self):
        expected_tags = [get_js_tag(f) for f in ["modal"]]

        t = template.Template("""
            {% load bootstrap %}
            {% bootstrap_js modal modal %}
        """)
        result = t.render(template.Context())
        self.assertEqual("".join(expected_tags), result.strip())