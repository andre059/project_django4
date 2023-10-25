from django import template
from django.conf import settings
from django.db.models.fields.files import FieldFile
from django.forms import Media

register = template.Library()


@register.simple_tag
def mediapath(image_path):
    return f"{settings.MEDIA_URL}{image_path}"


# @register.simple_tag
# def path_tag(format_string):
    # return settings.MEDIA_URL + str(format_string)


# @register.simple_tag
# @register.filter()
# def mediapath(data: FieldFile) -> str:
    # """
    # Make url path to media

    # Examples:
        # <img src="{{ object.image|mediapath }}" />
        # or
        # <img src="{% mediapath object.image %}" />
    # """
    # return data.url if data else '#'


@register.filter
def path_filter(text):
    return settings.MEDIA_URL + str(text)

