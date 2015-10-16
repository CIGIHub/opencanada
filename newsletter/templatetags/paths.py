from bs4 import BeautifulSoup, Comment
from django import template

register = template.Library()


@register.filter
def paragraph_markup(text):
    # new_text = re.sub(r'<p[^>]*>', '<p style=\"-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; margin: 5px 0; font-family: \'Libre Baskerville\',Georgia,serif; font-size: 16px; line-height: 120%;\">', text, 0)
    new_text = text.replace('<p>', '').replace('</p>', '')

    return new_text


@register.filter
def html_cleanup(text):
    doc = BeautifulSoup(text, "html.parser")
    comments = doc.findAll(text=lambda text: isinstance(text, Comment))
    [comment.extract() for comment in comments]
    new_text = doc
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
        return '-webkit-text-size-adjust: 100%;' \
               '-ms-text-size-adjust: 100%; ' \
               'mso-table-lspace: 0pt; mso-table-rspace: 0pt; '\
               'text-align:left;' \
               'font-family: \'Libre Baskerville\',Georgia,serif; ' \
               'font-size: 14px; '\
               'line-height: 165%; '\
               'padding: 10px 0;'
    elif tag == 'a':
        return '-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;'\
               'color: #bf1e2e;'\
               'text-decoration:none;'
    elif tag == 'img':
        return 'border: 0; outline: none; text-decoration: none; ' \
               '-ms-interpolation-mode: bicubic;'
    elif tag == 'p':
        return 'font-family: \'Libre Baskerville\',Georgia,serif; ' \
               '-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;'
    elif tag == 'li':
        return '-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;'
    elif tag == 'blockquote':
        return '-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;'
    elif tag == 'h1':
        return '-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;'
    elif tag == 'h2':
        return "font-family: proxima-nova,Helvetica,sans-serif; " \
               "font-size: 21px;" \
               "font-weight: 900;" \
               "line-height: 25px;" \
               "color: #000000;" \
               "padding: 0px;" \
               "margin: 0px;"
    elif tag == 'wordmark':
        return 'font-family:proxima-nova,Helvetica,sans-serif;' \
               'text-transform:uppercase;' \
               'color: white;' \
               'text-decoration: none;' \
               'font-weight:400;' \
               'font-size:18px;' \
               'line-height:18px;'
    return ""
