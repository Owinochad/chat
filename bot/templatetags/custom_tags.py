from django import template

register = template.Library()

@register.simple_tag
def first_message_tag(messages):
    if messages:
        return messages[0].tags
    return ''
