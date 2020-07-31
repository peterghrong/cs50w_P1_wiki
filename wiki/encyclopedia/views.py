from django.shortcuts import render, redirect
from django import forms
from os import path
from wiki.settings import BASE_DIR
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, title):
    return render(request, "encyclopedia/content.html", {"content": util.get_entry(title), "title": title})


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
    header = forms.CharField(label="New Header")

    body = forms.CharField(label="New Content",
                           widget=forms.Textarea(attrs={'rows': 3}))


def create(request):
    return render(request, "encyclopedia/create.html", {"form": NewPage()})


def add(request):
    # boilerplate data validation
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["header"]
            body = form.cleaned_data["body"]

            # this part takes care of the md file generation
            file_path = path.join(
                BASE_DIR, f'entries/{title.capitalize()}.md')
            with open(file_path, "w") as file:
                file.write(body)
            return render(request, "encyclopedia/content.html", {"content": body})

    return render(request, "encyclopedia/content.html", {"content": "Failed"})
