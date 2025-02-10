from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from core.RS3Reader import RS3Reader
from rst.forms import UploadRstFileForm


def index(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UploadRstFileForm(request.POST, request.FILES)
        file = request.FILES["file"]
        reader = RS3Reader(file.read())
        print(reader.count_relations())
    else:
        form = UploadRstFileForm()
    return render(request, "rst/index.html", {'form': form})
