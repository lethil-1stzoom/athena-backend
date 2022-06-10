from django.shortcuts import get_object_or_404, render
from Files.models import FileGroups, ImageFiles, UniqueURL, VideoFiles


def get_from_share(request, token):
    url = get_object_or_404(UniqueURL, token=token)
    if url.is_valid():
        if url.type == "image":
            data = get_object_or_404(ImageFiles, id=url.obj_id)
        if url.type == "video":
            data = get_object_or_404(VideoFiles, id=url.obj_id)
        if url.type == "group":
            data = get_object_or_404(FileGroups, id=url.obj_id)
        url.visited += 1
        url.save()
        context = {
            'data': data,
            'type': data.type()
        }
    return render(request, 'Files/index.html', context)
