from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from core.RS3Reader import RS3Reader
from rst.forms import UploadRstFileForm


def index(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.method == "POST":
        form = UploadRstFileForm(request.POST, request.FILES)
        file = request.FILES["file"]
        reader = RS3Reader(file.read())
        counting = {
            relation.replace('-', ' ').capitalize(): count
            for relation, count in reader.count_relations().items()
        }
        context["counting"] = counting
    else:
        form = UploadRstFileForm()
    context["form"] = form
    return render(request, "rst/index.html", context)
