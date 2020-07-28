from django.shortcuts import render, redirect
from django import forms

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, title):
    return render(request, "encyclopedia/content.html", {"content": util.get_entry(title), "title": title})


class NewSearchForm(forms.Form):
    new_input = forms.CharField(label="New Search")
# to be finished
# if the query matches, the user should be redirected to a page containing results
# if no query matches, then the user should be taken to a search result
# page that displays a list of encyclopedia entries as substring


def search(request):
    search = request.POST['q']
    lst = util.sub_query(str(search))
    if util.get_entry(search) is not None:
        return redirect(f'/{search}')
    elif len(lst) != 0:
        return render(request, "encyclopedia/index.html", {"entries": lst})
    else:
        return render(request, "encyclopedia/content.html", {"title": "Not Found"})
