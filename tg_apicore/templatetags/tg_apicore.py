from django import template
from django.utils.safestring import mark_safe

import markdown
from rest_framework.templatetags.rest_framework import highlight_code


register = template.Library()

register.tag('code', highlight_code)


def get_markdown_renderer():
    return markdown.Markdown(
        extensions=[
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ],
        extension_configs={
            'markdown.extensions.codehilite': {
                'css_class': 'highlight',
            },
            'markdown.extensions.toc': {
                'anchorlink': True,
            },
        },
    )


@register.simple_tag
def render_markdown(markdown_text):
    html = get_markdown_renderer().convert(markdown_text)
    return mark_safe(html)


@register.simple_tag
def render_markdown_toc(markdown_text):
    md = get_markdown_renderer()
    md.convert(markdown_text)
    return mark_safe(md.toc)
