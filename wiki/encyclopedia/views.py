from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    return render(request, "encyclopedia/wiki.html", {
        "entry": util.get_entry(title)
    })

def search(request):
    entry = request.POST.get('q')
    entries = util.list_entries()
    possibilities = []
    for element in entries:
        for i in element:
            if i in entry:
                possibilities.append(element)
    return render(request, "encyclopedia/search.html", {
        "possibilities": possibilities,
        "entry": util.get_entry(entry)
    })