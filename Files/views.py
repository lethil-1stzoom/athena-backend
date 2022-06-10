from django.shortcuts import get_object_or_404, render
from API.seralizers import get_object_by_type
from Files.models import FileGroups, ImageFiles, UniqueURL, VideoFiles


def get_from_share(request, token):
    url = get_object_or_404(UniqueURL, token=token)
    context = {}
    if url.is_valid():
        data = get_object_by_type(url)
        url.visited += 1
        url.save()
        context = {
            'data': data,
            'type': url.type
        }
    return render(request, 'Files/index.html', context)
