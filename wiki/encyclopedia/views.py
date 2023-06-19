from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect, HttpResponse

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':3, 'cols':5, 'style': 'height: 15em;'}))

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
            if i.lower() in entry.lower():
                if element not in possibilities:
                    possibilities.append(element)
    return render(request, "encyclopedia/search.html", {
        "possibilities": possibilities,
        "entry": util.get_entry(entry)
    })

def create(request):
    if request.method == "POST":
         form = NewEntryForm(request.POST)
         if form.is_valid():
              title = form.cleaned_data["title"]
              content = form.cleaned_data["content"]
              if title not in util.list_entries():
                  util.save_entry(title, content)
                  return HttpResponseRedirect(f'/wiki/{title}')
              else:
                  return render(request, "encyclopedia/error.html")
    return render(request, "encyclopedia/create.html", {
        "form": NewEntryForm()
    })