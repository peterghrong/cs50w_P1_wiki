from django.shortcuts import render, redirect
from django import forms

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, title):
    return render(request, "encyclopedia/content.html", {"content": util.get_entry(title), "title": title})


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


class NewPage(forms.Form):

    # class Meta:
    header = forms.CharField(
        label="New Header")

    body = forms.CharField(label="New Contents",
                           widget=forms.Textarea(attrs={'rows': 3}))


def add(request):
    return render(request, "encyclopedia/create.html", {"form": NewPage()})
