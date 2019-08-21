from django import template

import datetime

register = template.Library()

@register.filter()
def formatSeconds(s):
    return datetime.timedelta(seconds=s).__str__();


@register.filter()
def truncatemiddlechars(s, arg):
    s = s.split("/")[-1]
    if arg > len(s):
        arg = len(s)
    return s[:int(arg/2)]+"[...]"+s[-int(arg/2):]
