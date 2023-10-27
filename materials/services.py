from django.conf import settings
from django.core.cache import cache

from materials.models import Materials


def get_cached_for_materials(pk):
    if settings.CACHES_ENABLED:
        key = f'object_list{pk}'
        object_list = cache.get(key)
        if object_list is None:
            object_list = Materials.objects.filter(pk=pk).first()
            if object_list:
                object_list.views_count += 1
                object_list.save()
            cache.set(key, object_list)
    else:
        object_list = Materials.objects.filetr(pk=pk)

    return object_list
