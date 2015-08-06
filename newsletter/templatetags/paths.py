import re

from django import template

register = template.Library()


@register.filter
def paragraph_markup(text):
    new_text = re.sub(r'<p[^>]*>', '<p style=\"-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; font-family: \'Droid Serif\', Georgia, serif; font-size: 16px; line-height: 120%\">', text, 0)

    return new_text


@register.simple_tag
def base_styles(tag):
    if tag == 'body':
        return '-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; ' \
               'height: 100% !important; margin: 0; padding: 0; ' \
               'width: 100% !important;'
    elif tag == '#bodyTable' or tag == '#bodyCell':
        return 'height: 100% !important; margin: 0; padding: 0; ' \
               'width: 100% !important;'
    elif tag == 'table':
        return '-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;' \
               ' border-collapse: collapse; mso-table-lspace: 0pt; ' \
               'mso-table-rspace: 0pt;'
    elif tag == 'td':
        return '-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; ' \
               'mso-table-lspace: 0pt; mso-table-rspace: 0pt;'
    elif tag == 'a':
        return '-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;'
    elif tag == 'img':
        return 'border: 0; outline: none; text-decoration: none; ' \
               '-ms-interpolation-mode: bicubic;'
    elif tag == 'p':
        return '-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;'
    elif tag == 'li':
        return '-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;'
    elif tag == 'blockquote':
        return '-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;'
    elif tag == 'h1':
        return '-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;'
    return ""
