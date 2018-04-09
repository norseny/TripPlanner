from django import template
from django.utils.translation import gettext as _


register = template.Library()

@register.filter(name='cust_trunc')
def truncate_chars(value):
    s = str(value)
    s1 = s.replace("object", "")
    s2 = s1.replace(" ", "")
    s3 = ''.join([i for i in s2 if not i.isdigit() if not i == '(' if not i == ')'])
    result = _(s3)
    return result